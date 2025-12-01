from random import randint

# Historia ruchów
wyboryCzlowieka = []
wyboryMaszyny = []

# Wzorce jak w poprawionej maszynie Shannona
zapisaneWzorce = {
    "WSW": ["Nieznany", 0], "WSL": ["Nieznany", 0],
    "WDW": ["Nieznany", 0], "WDL": ["Nieznany", 0],
    "LSW": ["Nieznany", 0], "LSL": ["Nieznany", 0],
    "LDW": ["Nieznany", 0], "LDL": ["Nieznany", 0]
}

# wzorzec, na podstawie którego MASZYNA będzie przewidywać w KOLEJNEJ rundzie
ostatni_wzorzec = None

# ile rund ma zagrać maszyna z anty-maszyną
LICZBA_RUND = 500

# tu będziemy trzymać ruchy NA NASTĘPNĄ rundę
nast_ruch_czlowieka = None
nast_ruch_maszyny = None

# LICZNIKI WYNIKU
wynik_czlowiek = 0   # ile razy anty-maszyna (człowiek) wygrał
wynik_maszyna = 0    # ile razy maszyna Shannona trafiła

for runda in range(LICZBA_RUND):
    print(f"\n=== RUNDA {runda + 1} ===")

    # 1. WYBÓR RUCHÓW W TEJ RUNDZIE
    if nast_ruch_czlowieka is None:
        # pierwsza runda – brak predykcji, losujemy niezależnie
        ruch_czlowieka = randint(0, 1)
        ruch_maszyny = randint(0, 1)
    else:
        # kolejne rundy – gramy tym, co zostało wyliczone poprzednio
        ruch_czlowieka = nast_ruch_czlowieka
        ruch_maszyny = nast_ruch_maszyny

    wyboryCzlowieka.append(ruch_czlowieka)
    wyboryMaszyny.append(ruch_maszyny)

    print(f"Ruch anty-maszyny (człowiek): {ruch_czlowieka}")
    print(f"Ruch maszyny Shannona:        {ruch_maszyny}")

    # 2. SPRAWDZENIE, KTO „WYGRAŁ” + AKTUALIZACJA WYNIKU
    if wyboryCzlowieka[-1] == wyboryMaszyny[-1]:
        # maszyna poprawnie przewidziała człowieka
        wynik_maszyna += 1
        print("❌ PRZEGRANA anty-maszyny (maszyna zgadła wybór człowieka)")
    else:
        # anty-maszyna ograła maszynę
        wynik_czlowiek += 1
        print("✅ WYGRANA anty-maszyny (maszyna się pomyliła)")

    print(f"Stan meczu: anty-maszyna {wynik_czlowiek} : {wynik_maszyna} maszyna Shannona")

    # --- PRZELICZ W/L i S/D DLA CAŁEJ HISTORII ---

    wynikiCzlowieka = []   # W / L
    zmianaCzlowieka = []   # S / D

    for i in range(len(wyboryCzlowieka)):
        # wynik W/L
        if wyboryCzlowieka[i] == wyboryMaszyny[i]:
            wynikiCzlowieka.append("L")
        else:
            wynikiCzlowieka.append("W")

        # zmiana S/D (tylko jeśli jest kolejny ruch)
        if i < len(wyboryCzlowieka) - 1:
            if wyboryCzlowieka[i] == wyboryCzlowieka[i + 1]:
                zmianaCzlowieka.append("S")
            else:
                zmianaCzlowieka.append("D")

    # --- UCZENIE: jak w poprawionej maszynie ---

    if len(wyboryCzlowieka) >= 3:
        # N = len(wyboryCzlowieka)
        # wzorzec uczenia oparty na rundach (N-2, N-1), reakcja w N

        przedostatnie2wyniki = wynikiCzlowieka[-3:-1]   # wyniki N-2 i N-1
        przedostniaZmiana = zmianaCzlowieka[-2:-1]      # zmiana N-2 -> N-1
        zmianaPoWzorcu = zmianaCzlowieka[-1]            # zmiana N-1 -> N

        wzorzec_uczenia = (
            przedostatnie2wyniki[0] +
            przedostniaZmiana[0] +
            przedostatnie2wyniki[1]
        )

        # aktualizacja tabeli wzorców
        if zapisaneWzorce[wzorzec_uczenia][0] == "Nieznany":
            zapisaneWzorce[wzorzec_uczenia][0] = zmianaPoWzorcu
            zapisaneWzorce[wzorzec_uczenia][1] = 1
        elif zapisaneWzorce[wzorzec_uczenia][0] == zmianaPoWzorcu:
            zapisaneWzorce[wzorzec_uczenia][1] += 1
        else:
            zapisaneWzorce[wzorzec_uczenia][0] = "Nieznany"
            zapisaneWzorce[wzorzec_uczenia][1] = 0

        print(
            f"Wzorzec (uczenie): {wzorzec_uczenia}, "
            f"Odpowiedź Człowieka: {zapisaneWzorce[wzorzec_uczenia][0]}, "
            f"Wystąpień: {zapisaneWzorce[wzorzec_uczenia][1]}"
        )

        # --- WZORZEC DO PREDYKCJI NA NASTĘPNĄ RUNDĘ (N+1) ---
        # oparty na OSTATNICH dwóch rundach: (N-1, N)
        poprzedni_wynik = wynikiCzlowieka[-2]   # wynik N-1
        ostatni_wynik = wynikiCzlowieka[-1]     # wynik N
        ostatnia_zmiana = zmianaCzlowieka[-1]   # zmiana N-1 -> N

        ostatni_wzorzec = (
            poprzedni_wynik +
            ostatnia_zmiana +
            ostatni_wynik
        )
        print(f"Wzorzec do predykcji kolejnej rundy: {ostatni_wzorzec}")
    else:
        # jeszcze za mało rund, żeby maszyna w ogóle się nauczyła czegokolwiek
        ostatni_wzorzec = None
        print("Za mało danych, brak uczenia (mniej niż 3 rundy).")

    # --- TERAZ PRZEWIDUJEMY KOLEJNY RUCH MASZYNY (ANTI-SHANNON) ---

    if (
        ostatni_wzorzec is not None and
        zapisaneWzorce[ostatni_wzorzec][0] != "Nieznany" and
        zapisaneWzorce[ostatni_wzorzec][1] >= 2   # wzorzec musi być potwierdzony min. 2 razy
    ):
        przewidywana_zmiana = zapisaneWzorce[ostatni_wzorzec][0]
        ostatni_ruch_czlowieka = wyboryCzlowieka[-1]

        if przewidywana_zmiana == "S":
            przewidywany_ruch_maszyny = ostatni_ruch_czlowieka
        else:  # "D"
            przewidywany_ruch_maszyny = 1 - ostatni_ruch_czlowieka

        # Ustawiamy ruchy na NASTĘPNĄ rundę:
        nast_ruch_maszyny = przewidywany_ruch_maszyny
        nast_ruch_czlowieka = 1 - przewidywany_ruch_maszyny

        print(f"👾 [ZNANY WZORZEC] maszyna zagra: {nast_ruch_maszyny}, "
              f"anty-maszyna (człowiek) zagra: {nast_ruch_czlowieka}")
    else:
        # BRAK POTWIERDZONEGO WZORCA → LOSUJEMY NIEZALEŻNIE DLA OBU W NASTĘPNEJ RUNDZIE
        nast_ruch_maszyny = randint(0, 1)
        nast_ruch_czlowieka = randint(0, 1)

        print("🎲 Maszyna Shannona NIE MA jeszcze POTWIERDZONEGO wzorca dla tej sytuacji.")
        print("🎲 W następnej rundzie obie strony będą losować.")
        print(f"   Następny ruch maszyny: {nast_ruch_maszyny}, "
              f"następny ruch anty-maszyny: {nast_ruch_czlowieka}")

    print("-" * 50)

# --- PODSUMOWANIE PO ZAKOŃCZENIU MECZU ---

print("\n=== PODSUMOWANIE MECZU ===")
print(f"Liczba rund: {LICZBA_RUND}")
print(f"Wygrane anty-maszyny (człowiek): {wynik_czlowiek}")
print(f"Trafienia maszyny Shannona:      {wynik_maszyna}")

if LICZBA_RUND > 0:
    proc_czlowiek = wynik_czlowiek / LICZBA_RUND * 100
    proc_maszyna = wynik_maszyna / LICZBA_RUND * 100
    print(f"Procent wygranych anty-maszyny: {proc_czlowiek:.2f}%")
    print(f"Procent trafień maszyny:        {proc_maszyna:.2f}%")
