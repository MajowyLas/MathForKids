#!/usr/bin/env python3
"""
Scraper mieszkań z tarnowiak.pl
Szuka mieszkań 4-pokojowych powyżej 80m²

Kategorie:
  - sprzedam  : mieszkania na sprzedaż
  - wynajme   : mieszkania do wynajęcia

Użycie:
  python scraper_tarnowiak.py
  python scraper_tarnowiak.py --kategoria sprzedam
  python scraper_tarnowiak.py --kategoria wynajme
  python scraper_tarnowiak.py --kategoria oba
  python scraper_tarnowiak.py --pokoje 4 --min-m2 80
  python scraper_tarnowiak.py --opóźnienie 2.0 --wyniki wyniki.csv
"""

import re
import time
import csv
import argparse
import logging
from dataclasses import dataclass, fields
from typing import Optional

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

BASE_URL = "https://www.tarnowiak.pl"

KATEGORIE = {
    "sprzedam": "/ogloszenia/nieruchomosci/mieszkania/sprzedam/",
    "wynajme":  "/ogloszenia/nieruchomosci/mieszkania/wynajme/",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.tarnowiak.pl/",
}


@dataclass
class Ogloszenie:
    tytul:    str
    cena:     str
    pokoje:   Optional[int]
    metry:    Optional[float]
    adres:    str
    url:      str
    kategoria: str


# ---------------------------------------------------------------------------
# Parsowanie liczby pokoi z tekstu
# ---------------------------------------------------------------------------

WZORCE_POKOI = [
    re.compile(r"(\d+)\s*(?:-\s*)?poko(?:j|i|ó)(?:owe|owy|u|)", re.I),
    re.compile(r"(\d+)\s+pok\.?", re.I),
    re.compile(r"poko(?:j|i|ó)\w*\s*:\s*(\d+)", re.I),
    re.compile(r"liczba\s+poko(?:j|i|ó)\w*\s*:\s*(\d+)", re.I),
    re.compile(r"(\d+)\s*rooms?", re.I),
]

WZORCE_METROW = [
    re.compile(r"(\d+[.,]?\d*)\s*m(?:2|²|&sup2;)", re.I),
    re.compile(r"(\d+[.,]?\d*)\s*mkw", re.I),
    re.compile(r"powierzchni[ae]\s*:?\s*(\d+[.,]?\d*)", re.I),
]


def wyodrebnij_pokoje(tekst: str) -> Optional[int]:
    for wzorzec in WZORCE_POKOI:
        m = wzorzec.search(tekst)
        if m:
            return int(m.group(1))
    return None


def wyodrebnij_metry(tekst: str) -> Optional[float]:
    for wzorzec in WZORCE_METROW:
        m = wzorzec.search(tekst)
        if m:
            return float(m.group(1).replace(",", "."))
    return None


# ---------------------------------------------------------------------------
# Pobieranie stron
# ---------------------------------------------------------------------------

def pobierz_strone(url: str, sesja: requests.Session, proba: int = 3) -> Optional[BeautifulSoup]:
    for i in range(proba):
        try:
            r = sesja.get(url, headers=HEADERS, timeout=15)
            r.raise_for_status()
            return BeautifulSoup(r.text, "html.parser")
        except requests.RequestException as e:
            log.warning("Błąd pobierania %s (próba %d/%d): %s", url, i + 1, proba, e)
            if i < proba - 1:
                time.sleep(2 ** i)
    return None


def url_strony(bazowy_path: str, numer: int) -> str:
    """Buduje URL dla danej strony wyników."""
    sciezka = bazowy_path.rstrip("/")
    if numer == 1:
        return BASE_URL + sciezka + "/"
    # Format paginacji: /sprzedam:strona-2/
    base = sciezka.split(":")[0]
    return BASE_URL + base + f":strona-{numer}/"


# ---------------------------------------------------------------------------
# Parsowanie listy ogłoszeń
# ---------------------------------------------------------------------------

def parsuj_liste(soup: BeautifulSoup, url_kategorii: str, kategoria: str) -> list[Ogloszenie]:
    """Wyodrębnia ogłoszenia z jednej strony wyników."""
    wyniki = []

    # Próbujemy kilku możliwych selektorów dla kontenera ogłoszeń
    kontenery = (
        soup.select("article.listing-item")
        or soup.select("div.listing-item")
        or soup.select("li.item")
        or soup.select(".ogloszenie")
        or soup.select("div[class*='offer']")
        or soup.select("div[class*='listing']")
        or soup.select("td.lista_item")
    )

    if not kontenery:
        # Fallback: każdy link prowadzący do ogłoszenia
        kontenery = soup.find_all("a", href=re.compile(r"/ogloszenia/nieruchomosci/mieszkania/\w+/\d+"))
        log.debug("Fallback: znaleziono %d linków ogłoszeń", len(kontenery))
        for a in kontenery:
            href = a.get("href", "")
            full_url = BASE_URL + href if href.startswith("/") else href
            tytul = a.get_text(strip=True) or "—"
            tekst = a.get_text(" ", strip=True)
            wyniki.append(Ogloszenie(
                tytul=tytul,
                cena="—",
                pokoje=wyodrebnij_pokoje(tekst),
                metry=wyodrebnij_metry(tekst),
                adres="—",
                url=full_url,
                kategoria=kategoria,
            ))
        return wyniki

    for kontener in kontenery:
        tekst = kontener.get_text(" ", strip=True)

        # Tytuł
        tag_tytul = (
            kontener.select_one("h2 a, h3 a, .title a, .tytul a, a.title")
            or kontener.select_one("a[href*='/ogloszenia/']")
        )
        if tag_tytul:
            tytul = tag_tytul.get_text(strip=True)
            href = tag_tytul.get("href", "")
            url_ogl = BASE_URL + href if href.startswith("/") else href
        else:
            tytul = tekst[:80]
            url_ogl = url_kategorii

        # Cena
        tag_cena = kontener.select_one(".price, .cena, [class*='price'], [class*='cena']")
        cena = tag_cena.get_text(strip=True) if tag_cena else "—"

        # Adres/lokalizacja
        tag_adres = kontener.select_one(".location, .adres, [class*='location'], [class*='adres']")
        adres = tag_adres.get_text(strip=True) if tag_adres else "—"

        wyniki.append(Ogloszenie(
            tytul=tytul,
            cena=cena,
            pokoje=wyodrebnij_pokoje(tekst),
            metry=wyodrebnij_metry(tekst),
            adres=adres,
            url=url_ogl,
            kategoria=kategoria,
        ))

    return wyniki


# ---------------------------------------------------------------------------
# Pobieranie szczegółów ogłoszenia (opcjonalne wzbogacanie danych)
# ---------------------------------------------------------------------------

def wzbogac_ze_szczegolów(ogl: Ogloszenie, sesja: requests.Session, opoznienie: float) -> Ogloszenie:
    """Jeśli nie udało się wyodrębnić pokoi/m² z listy, pobiera stronę szczegółów."""
    if ogl.pokoje is not None and ogl.metry is not None:
        return ogl
    if ogl.url == BASE_URL:
        return ogl

    time.sleep(opoznienie)
    soup = pobierz_strone(ogl.url, sesja)
    if not soup:
        return ogl

    tekst = soup.get_text(" ", strip=True)

    if ogl.pokoje is None:
        ogl.pokoje = wyodrebnij_pokoje(tekst)
    if ogl.metry is None:
        ogl.metry = wyodrebnij_metry(tekst)

    return ogl


# ---------------------------------------------------------------------------
# Sprawdzanie liczby stron
# ---------------------------------------------------------------------------

def ile_stron(soup: BeautifulSoup) -> int:
    """Odczytuje liczbę stron z paginacji."""
    # Format "strona X z Y"
    m = re.search(r"strona\s+\d+\s+z\s+(\d+)", soup.get_text(" ", strip=True), re.I)
    if m:
        return int(m.group(1))

    # Ostatni link paginacji
    linki = soup.select("a[href*=':strona-']")
    numery = []
    for a in linki:
        n = re.search(r":strona-(\d+)", a.get("href", ""))
        if n:
            numery.append(int(n.group(1)))
    if numery:
        return max(numery)

    return 1


# ---------------------------------------------------------------------------
# Główna pętla scrapowania
# ---------------------------------------------------------------------------

def scrapuj_kategorie(
    kategoria: str,
    path: str,
    pokoje: int,
    min_m2: float,
    opoznienie: float,
    sesja: requests.Session,
    szczegoly: bool,
) -> list[Ogloszenie]:
    log.info("=== Kategoria: %s ===", kategoria)
    url_kat = BASE_URL + path

    soup = pobierz_strone(url_strony(path, 1), sesja)
    if not soup:
        log.error("Nie udało się pobrać pierwszej strony kategorii %s", kategoria)
        return []

    n_stron = ile_stron(soup)
    log.info("Znaleziono %d stron wyników", n_stron)

    wszystkie: list[Ogloszenie] = []

    for nr in range(1, n_stron + 1):
        url_s = url_strony(path, nr)
        log.info("Pobieranie strony %d/%d: %s", nr, n_stron, url_s)

        if nr > 1:
            time.sleep(opoznienie)
            soup = pobierz_strone(url_s, sesja)
            if not soup:
                log.warning("Pominięto stronę %d", nr)
                continue

        ogloszenia = parsuj_liste(soup, url_kat, kategoria)
        log.info("  Znaleziono %d ogłoszeń na stronie", len(ogloszenia))

        for ogl in ogloszenia:
            if szczegoly:
                ogl = wzbogac_ze_szczegolów(ogl, sesja, opoznienie)

            pasuje_pokoje = ogl.pokoje is not None and ogl.pokoje == pokoje
            pasuje_metry  = ogl.metry  is not None and ogl.metry  >= min_m2

            if pasuje_pokoje and pasuje_metry:
                wszystkie.append(ogl)
                log.info("  ✓ %s | %d pok. | %.1f m² | %s", ogl.tytul[:50], ogl.pokoje, ogl.metry, ogl.cena)

    return wszystkie


# ---------------------------------------------------------------------------
# Eksport do CSV
# ---------------------------------------------------------------------------

def zapisz_csv(wyniki: list[Ogloszenie], plik: str) -> None:
    if not wyniki:
        log.info("Brak wyników do zapisania.")
        return
    kolumny = [f.name for f in fields(Ogloszenie)]
    with open(plik, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=kolumny)
        writer.writeheader()
        for ogl in wyniki:
            writer.writerow({f.name: getattr(ogl, f.name) for f in fields(Ogloszenie)})
    log.info("Zapisano %d wyników do %s", len(wyniki), plik)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Scraper mieszkań z tarnowiak.pl")
    p.add_argument("--kategoria", choices=["sprzedam", "wynajme", "oba"], default="oba",
                   help="Kategoria ogłoszeń (domyślnie: oba)")
    p.add_argument("--pokoje", type=int, default=4,
                   help="Liczba pokoi (domyślnie: 4)")
    p.add_argument("--min-m2", type=float, default=80.0,
                   help="Minimalna powierzchnia w m² (domyślnie: 80)")
    p.add_argument("--opoznienie", type=float, default=1.5,
                   help="Opóźnienie między żądaniami w sekundach (domyślnie: 1.5)")
    p.add_argument("--wyniki", default="wyniki.csv",
                   help="Plik CSV z wynikami (domyślnie: wyniki.csv)")
    p.add_argument("--bez-szczegolów", action="store_true",
                   help="Nie odwiedzaj stron szczegółów (szybsze, ale mniej danych)")
    p.add_argument("--verbose", "-v", action="store_true",
                   help="Szczegółowe logi")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    if args.verbose:
        log.setLevel(logging.DEBUG)

    if args.kategoria == "oba":
        wybrane = list(KATEGORIE.items())
    else:
        wybrane = [(args.kategoria, KATEGORIE[args.kategoria])]

    sesja = requests.Session()
    sesja.headers.update(HEADERS)

    wszystkie: list[Ogloszenie] = []

    for nazwa_kat, path in wybrane:
        wyniki = scrapuj_kategorie(
            kategoria=nazwa_kat,
            path=path,
            pokoje=args.pokoje,
            min_m2=args.min_m2,
            opoznienie=args.opoznienie,
            sesja=sesja,
            szczegoly=not args.bez_szczegolów,
        )
        wszystkie.extend(wyniki)

    print("\n" + "=" * 60)
    print(f"WYNIKI: {len(wszystkie)} ogłoszeń ({args.pokoje} pok., min {args.min_m2} m²)")
    print("=" * 60)

    for i, ogl in enumerate(wszystkie, 1):
        pokoje_str = f"{ogl.pokoje} pok." if ogl.pokoje else "? pok."
        metry_str  = f"{ogl.metry:.1f} m²" if ogl.metry else "? m²"
        print(f"\n{i}. {ogl.tytul}")
        print(f"   Kategoria : {ogl.kategoria}")
        print(f"   Powierzchnia: {metry_str}  |  Pokoje: {pokoje_str}")
        print(f"   Cena      : {ogl.cena}")
        print(f"   Adres     : {ogl.adres}")
        print(f"   URL       : {ogl.url}")

    if args.wyniki:
        zapisz_csv(wszystkie, args.wyniki)


if __name__ == "__main__":
    main()
