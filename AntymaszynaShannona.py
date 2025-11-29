from random import randint

wyboryCzlowieka = []
wyboryMaszyny = []

zapisaneWzorce = {
    "WSW": ["Nieznany", 0], "WSL": ["Nieznany", 0],
    "WDW": ["Nieznany", 0], "WDL": ["Nieznany", 0],
    "LSW": ["Nieznany", 0], "LSL": ["Nieznany", 0],
    "LDW": ["Nieznany", 0], "LDL": ["Nieznany", 0]
}

# wzorzec, na podstawie którego MASZYNA będzie przewidywać w KOLEJNEJ rundzie
ostatni_wzorzec = None

# --- 3 RUNDY STARTOWE (maszyna losuje, nie uczy się) ---

powtórzenie = 3
while powtórzenie > 0:
    wyboryCzlowieka.append(input("Runda startowa\nTwój wybór (1 lub 0): "))
    wyboryMaszyny.append(int(input("Wybór maszyny (1 lub 0): ")))
    print(f"Maszyna wybrała: {wyboryMaszyny[-1]}")

    if int(wyboryCzlowieka[-1]) == wyboryMaszyny[-1]:
        print("❌ PRZEGRAŁEŚ (maszyna zgadła twój wybór)")
    else:
        print("✅ WYGRAŁEŚ (maszyna się pomyliła)")

    powtórzenie -= 1

# --- GŁÓWNA PĘTLA: po każdej rundzie aktualizujemy pamięć i przewidujemy NASTĘPNĄ ---

while True:
    # wprowadzasz ostatnio ROZEGRANĄ rundę (tak jak w maszynie)
    wyboryCzlowieka.append(input("\nNowa runda\nTwój ostatni wybór (1 lub 0): "))
    wyboryMaszyny.append(int(input("Ostatni wybór maszyny (1 lub 0): ")))
    print(f"Maszyna wybrała: {wyboryMaszyny[-1]}")

    if int(wyboryCzlowieka[-1]) == wyboryMaszyny[-1]:
        print("❌ PRZEGRAŁEŚ (maszyna zgadła twój wybór)")
    else:
        print("✅ WYGRAŁEŚ (maszyna się pomyliła)")

    # --- PRZELICZ W/L i S/D DLA CAŁEJ HISTORII ---

    wynikiCzlowieka = []   # W / L
    zmianaCzlowieka = []   # S / D

    for i in range(len(wyboryCzlowieka)):
        if int(wyboryCzlowieka[i]) == wyboryMaszyny[i]:
            wynikiCzlowieka.append("L")
        else:
            wynikiCzlowieka.append("W")

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
        zapisaneWzorce[ostatni_wzorzec][0] != "Nieznany"
    ):
        przewidywana_zmiana = zapisaneWzorce[ostatni_wzorzec][0]
        ostatni_ruch_czlowieka = int(wyboryCzlowieka[-1])

        if przewidywana_zmiana == "S":
            przewidywany_ruch_maszyny = ostatni_ruch_czlowieka
        else:  # "D"
            przewidywany_ruch_maszyny = 1 - ostatni_ruch_czlowieka

        print(f"👾 Maszyna PRAWDPODOBNIE wybierze: {przewidywany_ruch_maszyny}")
        print(f"✅ ŻEBY WYGRAĆ, wybierz: {1 - przewidywany_ruch_maszyny}")
    else:
        print("🎲 Maszyna Shannona NIE MA jeszcze wzorca dla tej sytuacji.")
        print("🎲 W następnej rundzie będzie LOSOWAĆ (0 lub 1).")
        print("✅ Tego nie da się przewidzieć – możesz zagrać cokolwiek.")

    print("-" * 50)
