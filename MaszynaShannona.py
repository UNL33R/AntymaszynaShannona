from random import randint

wyboryCzlowieka = []
wyboryMaszyny = []

zapisaneWzorce = {
    "WSW": ["Nieznany", 0], "WSL": ["Nieznany", 0], 
    "WDW": ["Nieznany", 0], "WDL": ["Nieznany", 0], 
    "LSW": ["Nieznany", 0], "LSL": ["Nieznany", 0], 
    "LDW": ["Nieznany", 0], "LDL": ["Nieznany", 0]
}

# wzorzec używany DO PREDYKCJI w następnej rundzie
ostatni_wzorzec = None

# Początkowe 3 wybory – czysto losowe, bez „inteligencji”
powtórzenie = 3
while powtórzenie > 0:
    wyboryCzlowieka.append(input("Wpisz 1 lub 0\n"))
    wyboryMaszyny.append(randint(0, 1))
    print(f"Maszyna wybrała: {wyboryMaszyny[-1]}")
    
    # Sprawdź wynik
    if int(wyboryCzlowieka[-1]) == wyboryMaszyny[-1]:
        print("❌ PRZEGRAŁEŚ (maszyna zgadła twój wybór)")
    else:
        print("✅ WYGRAŁEŚ (maszyna się pomyliła)")
    
    powtórzenie = powtórzenie - 1

while True:
    # --- WYBÓR MASZYNY NA PODSTAWIE PAMIĘCI (MASZYNA SHANNONA) ---
    if (
        ostatni_wzorzec is not None 
        and zapisaneWzorce[ostatni_wzorzec][0] != "Nieznany"
    ):
        # znamy zachowanie gracza po takim wzorcu: S (ten sam) albo D (inny)
        przewidywana_zmiana = zapisaneWzorce[ostatni_wzorzec][0]
        ostatni_ruch_czlowieka = int(wyboryCzlowieka[-1])
        
        if przewidywana_zmiana == "S":
            przewidywany_ruch_czlowieka = ostatni_ruch_czlowieka
        else:  # "D"
            przewidywany_ruch_czlowieka = 1 - ostatni_ruch_czlowieka
        
        ruchMaszyny = przewidywany_ruch_czlowieka   # maszyna próbuje ZGADNĄĆ ruch człowieka
    else:
        # brak wiedzy dla aktualnego wzorca – strzał losowy
        ruchMaszyny = randint(0, 1)
    # ---------------------------------------------------------------

    # Dodaj wybór człowieka
    wyboryCzlowieka.append(input("Wpisz 1 lub 0\n"))
    
    # Wypisz wybór maszyny
    wyboryMaszyny.append(ruchMaszyny)
    print(f"Maszyna wybrała: {wyboryMaszyny[-1]}")
    
    # Sprawdź wynik
    if int(wyboryCzlowieka[-1]) == wyboryMaszyny[-1]:
        print("❌ PRZEGRAŁEŚ (maszyna zgadła twój wybór)")
    else:
        print("✅ WYGRAŁEŚ (maszyna się pomyliła)")
    
    # WYCZYŚĆ listy wyników przed przeliczeniem
    wynikiCzlowieka = []
    zmianaCzlowieka = []
    
    # Przypisanie W i L do wyborów Człowieka
    for wybor in range(len(wyboryCzlowieka)):
        if int(wyboryCzlowieka[wybor]) == wyboryMaszyny[wybor]:
            wynikiCzlowieka.append("L")
        else:
            wynikiCzlowieka.append("W")
    
    # Przypisanie S i D do wyborów człowieka
    for i in range(len(wyboryCzlowieka) - 1):
        if wyboryCzlowieka[i] == wyboryCzlowieka[i + 1]:
            zmianaCzlowieka.append("S")
        else:
            zmianaCzlowieka.append("D")
    
    # --- UCZENIE: wzorzec dla (N-2, N-1) i zachowanie w N ---
    # Część wzorca - wygrana czy przegrana?
    przedostatnie2wyniki = wynikiCzlowieka[-3:-1]   # wyniki rund N-2 i N-1
    
    # Część wzorca - zmiana czy nie między N-2 a N-1?
    przedostniaZmiana = zmianaCzlowieka[-2:-1]      # zmiana między N-2 i N-1
    
    # Reakcja człowieka po tym wzorcu: zmiana czy nie między N-1 a N
    zmianaPoWzorcu = zmianaCzlowieka[-1]
    
    # Połączenie w 1 wzorzec (N-2, zmiana N-2→N-1, N-1)
    wzorzec_uczenia = (
        przedostatnie2wyniki[0] 
        + przedostniaZmiana[0] 
        + przedostatnie2wyniki[1]
    )
    
    # Aktualizacja pamięci dla wzorca_uczenia
    if zapisaneWzorce[wzorzec_uczenia][0] == "Nieznany":
        zapisaneWzorce[wzorzec_uczenia][0] = zmianaPoWzorcu
        zapisaneWzorce[wzorzec_uczenia][1] = 1
    elif zapisaneWzorce[wzorzec_uczenia][0] == zmianaPoWzorcu:
        zapisaneWzorce[wzorzec_uczenia][1] = zapisaneWzorce[wzorzec_uczenia][1] + 1
    else:
        zapisaneWzorce[wzorzec_uczenia][0] = "Nieznany"
        zapisaneWzorce[wzorzec_uczenia][1] = 0

    # --- NOWE: wzorzec do PREDYKCJI dla następnej rundy (N+1) ---
    # tu patrzymy na OSTATNIE dwie rundy: (N-1, N)
    if len(wynikiCzlowieka) >= 2 and len(zmianaCzlowieka) >= 1:
        poprzedni_wynik = wynikiCzlowieka[-2]   # wynik rundy N-1
        ostatni_wynik   = wynikiCzlowieka[-1]   # wynik rundy N
        ostatnia_zmiana = zmianaCzlowieka[-1]   # zmiana między N-1 i N
        
        ostatni_wzorzec = poprzedni_wynik + ostatnia_zmiana + ostatni_wynik
    else:
        ostatni_wzorzec = None
    
    print(f"Wzorzec (uczenie): {wzorzec_uczenia}, "
          f"Odpowiedź Człowieka: {zapisaneWzorce[wzorzec_uczenia][0]}, "
          f"Wystąpień: {zapisaneWzorce[wzorzec_uczenia][1]}")
    print(f"Wzorzec do predykcji na kolejną rundę: {ostatni_wzorzec}")
    print("-" * 50)
