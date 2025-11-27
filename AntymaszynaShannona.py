from random import randint

wyboryCzlowieka = []
wyboryMaszyny = []

zapisaneWzorce = {
    "WSW": ["Nieznany", 0], "WSL": ["Nieznany", 0], 
    "WDW": ["Nieznany", 0], "WDL": ["Nieznany", 0], 
    "LSW": ["Nieznany", 0], "LSL": ["Nieznany", 0], 
    "LDW": ["Nieznany", 0], "LDL": ["Nieznany", 0]
}

# ostatni wzorzec użyty do przewidywania
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
    if ostatni_wzorzec is not None and zapisaneWzorce[ostatni_wzorzec][0] != "Nieznany":
        # wiemy, czy po tym wzorcu człowiek zwykle ZMIENIA (D) czy POWTARZA (S)
        przewidywana_zmiana = zapisaneWzorce[ostatni_wzorzec][0]
        ostatni_ruch_czlowieka = int(wyboryCzlowieka[-1])
        
        if przewidywana_zmiana == "S":
            przewidywany_ruch_czlowieka = ostatni_ruch_czlowieka
        else:  # "D"
            przewidywany_ruch_czlowieka = 1 - ostatni_ruch_czlowieka
        
        ruchMaszyny = przewidywany_ruch_czlowieka   # maszyna próbuje ZGADNĄĆ ruch człowieka
    else:
        # jeszcze nie mamy wiedzy – strzał losowy
        ruchMaszyny = randint(0, 1)
    # ---------------------------------------------------------------

    # Dodaj wybór człowieka
    wyboryCzlowieka.append(input("Wpisz 1 lub 0\n"))
    
    # Wypisz wybór maszyny (już nie losowy, tylko przewidywany)
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
    
    # Część wzorca - wygrana czy przegrana?
    przedostatnie2wyniki = wynikiCzlowieka[-3:-1] 
    
    # Część wzorca - zmiana czy nie?
    przedostniaZmiana = zmianaCzlowieka[-2:-1] 
    
    # Reakcja człowieka - zmiana czy nie?
    zmianaPoWzorcu = zmianaCzlowieka[-1] 
    
    # Połączenie w 1 wzorzec
    wzorzec = przedostatnie2wyniki[0] + przedostniaZmiana[0] + przedostatnie2wyniki[1]
    
    # Sprawdź czy wzorzec jest "Nieznany" lub czy odpowiedź się zgadza
    if zapisaneWzorce[wzorzec][0] == "Nieznany":
        # Pierwszy raz widzimy ten wzorzec - zapisz odpowiedź
        zapisaneWzorce[wzorzec][0] = zmianaPoWzorcu
        zapisaneWzorce[wzorzec][1] = 1
    elif zapisaneWzorce[wzorzec][0] == zmianaPoWzorcu:
        # Odpowiedź się zgadza - zwiększ licznik
        zapisaneWzorce[wzorzec][1] = zapisaneWzorce[wzorzec][1] + 1
    else:
        # Odpowiedź się nie zgadza - resetuj wzorzec
        zapisaneWzorce[wzorzec][0] = "Nieznany"
        zapisaneWzorce[wzorzec][1] = 0

    # zapamiętaj ostatni wzorzec do użycia przy KOLEJNEJ predykcji
    ostatni_wzorzec = wzorzec
    
    print(f"Wzorzec: {wzorzec}, Odpowiedź Człowieka: {zapisaneWzorce[wzorzec][0]}, Wystąpień: {zapisaneWzorce[wzorzec][1]}")
    print("-" * 50)
