# Wiarygodne źródła medyczne

Kiedy temat wymaga sprawdzenia aktualnej wiedzy medycznej (nie tylko
ogólnej wiedzy z treningu), użyj `WebSearch`/`WebFetch` i preferuj
poniższe domeny. Zawsze podawaj w odpowiedzi, z jakiego źródła pochodzi
dana informacja.

## Organizacje międzynarodowe / agencje rządowe
- who.int — World Health Organization
- cdc.gov — Centers for Disease Control and Prevention
- nih.gov, medlineplus.gov — National Institutes of Health / MedlinePlus
  (dobre dla prostych, przystępnych opisów objawów i chorób)
- nhs.uk — National Health Service (UK) — bardzo dobre, przystępne opisy
  objawów, "when to see a doctor", "when to call 999/111"
- ncbi.nlm.nih.gov/pubmed, pubmed.ncbi.nlm.nih.gov — bazy badań naukowych
- cochranelibrary.com — przeglądy systematyczne (Cochrane Reviews)

## Podręczniki / encyklopedie medyczne uznawane przez lekarzy
- merckmanuals.com (MSD Manuals) — uznawany podręcznik kliniczny,
  dostępny też w wersji dla pacjentów (consumer version)
- mayoclinic.org — Mayo Clinic, przystępne i rzetelne opisy objawów i
  chorób, sekcje "When to see a doctor"
- uptodate.com — złoty standard kliniczny (częściowo płatny/ograniczony
  dostęp, ale warto sprawdzić darmowe streszczenia "patient information")

## Źródła polskie
- mp.pl (Medycyna Praktyczna) — polskie wytyczne kliniczne i artykuły dla
  pacjentów, często tłumaczenia wytycznych europejskich/amerykańskich
- gov.pl/web/zdrowie — komunikaty Ministerstwa Zdrowia
- nfz.gov.pl — informacje o organizacji opieki zdrowotnej w PL (np. gdzie
  szukać nocnej/świątecznej pomocy)

## Wytyczne specjalistyczne (gdy temat tego wymaga)
- American Heart Association (heart.org) — kardiologia, resuscytacja
- American Academy of Pediatrics (aap.org) — pediatria
- ACOG (acog.org) — ginekologia/położnictwo
- IDSA (idsociety.org) — choroby zakaźne

## Zasady korzystania ze źródeł
1. Preferuj źródła zaktualizowane w ostatnich latach; jeśli strona ma
   widoczną datę publikacji/aktualizacji, zwróć na to uwagę.
2. W razie sprzeczności między źródłami zaznacz to wprost, nie wybieraj
   arbitralnie jednej wersji bez komentarza (przykład: godziny działania
   linii kryzysowej 116 123 są podawane różnie w różnych źródłach — patrz
   `red_flags.md`).
3. Nie cytuj forów, blogów, mediów społecznościowych ani stron sprzedażowych
   suplementów/leków jako źródła wiedzy klinicznej.
4. Jeśli nie udało się zweryfikować informacji w wiarygodnym źródle, powiedz
   to wprost, zamiast zgadywać.

## Uwaga techniczna: WebFetch vs WebSearch

Wiele domen medycznych (np. nhs.uk, cdc.gov, heart.org, mayoclinic.org)
blokuje bezpośrednie żądania `WebFetch` (HTTP 403) dla ruchu automatycznego.
W praktyce lepiej działa `WebSearch` — zwraca fragmenty treści wraz z
linkami źródłowymi i nie jest blokowany. Traktuj `WebFetch` jako uzupełnienie
(np. dla stron, które go nie blokują), a `WebSearch` jako domyślne narzędzie
do weryfikacji wytycznych medycznych. Zawsze podawaj link do źródła w
odpowiedzi, nawet jeśli pochodzi z fragmentu wyszukiwania, a nie z pełnej
treści strony.
