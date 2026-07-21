# Instagram Claude — dokument referencyjny biznesu

> Roboczy dokument strategiczny. Budujemy na nim niszę, ofertę i produkty.
> Ostatnia aktualizacja: 2026-07-21

---

## 🎯 Jednozdaniowe pozycjonowanie

**AI tam, gdzie pomaga — Twój głos zostaje Twój.**

---

## Część 1 — Przepracowanie niszy, klientki, bio

### CO — o czym i w czym jestem mocna

1. **O czym mogę mówić godzinami (i to nie jest praca):**
   Tworzenie i rozwijanie produktów (szczególnie z Claude Code), które faktycznie rozwiązują czyjś problem. Lubię też metryki, dane, analizę.

2. **Z czym ludzie przychodzą do mnie po pomoc:**
   Eskalacja i przepychanie ważnych tematów, rozwiązywanie konfliktów, konsultacje wokół metryk i procesu.

3. **W czym czuję się pewnie nawet bez przygotowania:**
   Metody zwinne, praca i prowadzenie zespołu, metryki wszelakie, prowadzenie warsztatów i facylitacja.

4. **Czego klientki potrzebują ode mnie najbardziej:**
   Wsparcia w technologii (AI), której nie znają, a która ma potencjał uprościć i wzbogacić ich pracę.

5. **Co ma największy potencjał na zarobek:**
   Praca z AI — konkretnie z **Claude**, nie ChatGPT.

---

### KTO — moja klientka

1. **Z kim chcę pracować:**
   Z kobietami. Z doświadczenia bycia jedną z niewielu kobiet w IT (15 lat, głównie z mężczyznami) — chcę wspierać właśnie kobiety.

2. **Kim jest ta osoba:**
   Kobieta 30–40 lat, prowadzi już działający, zarabiający biznes na Instagramie — stać ją na narzędzie i na współpracę. Działa dużo, ale content zabiera masę czasu, efekty niezadowalające, nie nadąża za trendami i konkurencją. Patrzy na statystyki, ale nie wie, co z nich wynika. Nietechniczna — próbowała ChatGPT, ale brak jej pewności, żeby iść dalej. Nie ma czasu ani energii uczyć się kolejnego skomplikowanego narzędzia. Tutoriale o AI, które widziała, są nudne i niedopasowane.

3. **Z jakimi problemami się zmaga:**
   - Brak czasu i energii
   - Brak pomysłów na content
   - Nie nadąża za trendami / konkurencją
   - Nie umie czytać własnych danych
   - Działa chaotycznie
   - Zmęczona contentem „sztucznym, AI-owym"
   - Brak pewności technicznej

---

### 🧭 Moje DLA KOGO

> Kobiety **30–40 lat**, prowadzące już **działający, zarabiający biznes na Instagramie**, które chcą przejść na kolejny poziom rozwoju — **nierozumiejące własnych danych, nietechniczne, ale z budżetem** na rozwiązanie problemu.

---

## Część 2 — Wymarzony rezultat

1. **Jaka zmiana zachodzi u klientek po współpracy:**
   Mają działający, stabilny system, który wspiera je na wybranych etapach cyklu tworzenia i sprzedawania produktu.

2. **Za co są mi najbardziej wdzięczne:**
   Za odzyskany czas oraz większe poczucie sprawczości i wiary w siebie.

3. **Co potrafię zrobić, czego inne nie potrafią:**
   Potrafię cierpliwie wysłuchać i zrozumieć problem, a potem rozwiązać go **dwutorowo** — od razu, za pomocą narzędzi AI, oraz na przyszłość, ucząc klientkę samodzielnego korzystania z narzędzia.

---

### 🌟 Mój WYMARZONY REZULTAT

> Klientki mają działający, stabilny system wspierający wybrane etapy cyklu produktowego — **odzyskują czas** i zyskują **większe poczucie sprawczości i wiary w siebie**.

---

## 🔑 Formuła: Pomagam ... osiągnąć ... dzięki ...

**AI tam, gdzie pomaga — Twój głos zostaje Twój.**

---

## 🛠️ Pomysł produktowy: Raporty AI dla Instagrama

> Roboczy spec. Jedno narzędzie (pipeline), trzy–cztery poziomy sprzedaży.

### Zasada nadrzędna
**Ja operuję narzędziem — klientka dostaje gotowy deliverable.** Klientka niczego nie
instaluje ani nie uczy się obsługi (poza najwyższą, technyczną półką). To wprost
odpowiada jej bólowi: „nie ma czasu ani energii uczyć się kolejnego narzędzia".

### Architektura (jedno źródło, wiele wyjść)
Jeden pipeline:
`pobierz dane z IG → (a) czysty plik danych .xlsx/.csv + (b) zredagowany raport .pdf/.html z interpretacją`

Interpretację („co z tych liczb wynika") drafuje Claude, ja zatwierdzam i nadaję ton
→ *AI tam, gdzie pomaga, głos zostaje mój.*

### Drabinka oferty

| Poziom | Co dostaje klientka | Kto operuje | Rola |
|---|---|---|---|
| **1. Raport** (wejście) | PDF z wnioskami + plik danych | Ja produkuję | walidacja, niski próg |
| **2. Subskrypcja raportu** | To samo, co miesiąc | Ja produkuję | powracający przychód |
| **3. Sesja „rozmowa z danymi"** (premium) | Wspólna sesja, gdzie AI odpowiada na pytania do jej danych — nic nie instaluje | Ja prowadzę MCP | najwyższa wartość, mój czas |
| **4. Własny MCP** (nisza, „konsultacja + setup + tool") | Spakowany MCP dla klientek, które *chcą* same grzebać | Klientka (mniejszość) | dla technicznie ogarniętych; bariera instalacji = powód, by zapłacić za setup |

### MCP — dwa różne warianty (ważne rozróżnienie)
- **MCP-A: rozmowa z gotowym plikiem danych (snapshot).** Łatwe i bezpieczne — brak
  żywego dostępu do API, tokenów, weryfikacji Meta. To wersja na start (poziom 3 i 4).
- **MCP-B: rozmowa z żywymi danymi z API.** Potężniejsze, ale cięższe (tokeny, zgody,
  utrzymanie). Przyszłość, nie MVP.

### MVP (pierwszy krok)
Skrypt/tool: po podaniu jednego konta IG pobiera dane z ostatnich 30/90 dni i generuje
**plik xlsx + raport PDF** z 5–7 wnioskami po ludzku (najlepsze/najgorsze posty,
najlepsze godziny, trend obserwujących, rekomendacje na następny miesiąc).
Demo najpierw na **własnym koncie**, zanim dotknę konta klientki.

### ⚠️ Do zweryfikowania na starcie (blokery techniczne)
- [ ] **Ścieżka dostępu do danych** — którą wybieramy:
  - Instagram Graph API (klasyczna) — wymaga podpięcia konta pod **stronę na Facebooku**, pełna analityka.
  - Instagram API with Instagram Login (nowsza) — **bez FB**, wystarczy konto Business/Creator, zakres bywa węższy.
  - *Konto Business/Creator mają wszystkie klientki (100%). FB-page = do sprawdzenia.*
- [ ] Konto deweloperskie Meta + aplikacja (mam / zakładam od zera?)
- [ ] Mechanizm jednorazowej zgody klientki (OAuth) + przechowywanie tokenu

### Decyzje do podjęcia
- [ ] Forma operowania: Claude Code / prosty skrypt / mini-UI
- [ ] Deliverable na start: sam PDF / sam plik danych / oba
- [ ] Doprecyzowanie poziomu 4 (pakiet „konsultacja + setup") — po pierwszych klientkach
- [ ] Model cenowy dla każdego poziomu

---

## 📌 Do dalszej pracy (backlog)

- [ ] Dopracować bio na Instagram (wersja krótka + długa)
- [ ] Strategia — kanały, format contentu, rytm publikacji
- [ ] Lista produktów do sprzedaży (mapowanie na etapy cyklu produktowego klientki)
- [ ] Definicja oferty wejściowej (low-ticket) i głównej
- [ ] Ustalenie, które etapy cyklu produktowego wspieramy AI
