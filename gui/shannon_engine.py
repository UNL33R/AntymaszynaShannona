from random import randint

class ShannonGame:
    """Logika z MaszynaShannona.py - maszyna ucząca się przewidywać ruchy gracza"""
    
    def __init__(self):
        self.wyboryCzlowieka = []
        self.wyboryMaszyny = []
        self.zapisaneWzorce = {
            "WSW": ["Nieznany", 0], "WSL": ["Nieznany", 0],
            "WDW": ["Nieznany", 0], "WDL": ["Nieznany", 0],
            "LSW": ["Nieznany", 0], "LSL": ["Nieznany", 0],
            "LDW": ["Nieznany", 0], "LDL": ["Nieznany", 0]
        }
        self.ostatni_wzorzec = None
        self.przewidywany_ruch_maszyny = randint(0, 1)
    
    def make_move(self, wybor_czlowieka):
        """Przetwórz ruch gracza i zwróć odpowiedź maszyny"""
        self.wyboryCzlowieka.append(wybor_czlowieka)
        self.wyboryMaszyny.append(self.przewidywany_ruch_maszyny)
        
        # Sprawdź wynik
        if wybor_czlowieka == self.przewidywany_ruch_maszyny:
            result = "loss"  # Maszyna zgadła
        else:
            result = "win"   # Gracz wygrał
        
        # Uczenie i predykcja
        self._learn_and_predict()
        
        return {
            "result": result,
            "machine_choice": self.przewidywany_ruch_maszyny,
            "human_choice": wybor_czlowieka,
            "patterns": self.zapisaneWzorce,
            "prediction": self.przewidywany_ruch_maszyny,
            "has_pattern": self.ostatni_wzorzec is not None
        }
    
    def _learn_and_predict(self):
        """Uczenie się wzorców i przewidywanie następnego ruchu"""
        wynikiCzlowieka = []
        zmianaCzlowieka = []
        
        # Przelicz W/L i S/D
        for i in range(len(self.wyboryCzlowieka)):
            if self.wyboryCzlowieka[i] == self.wyboryMaszyny[i]:
                wynikiCzlowieka.append("L")
            else:
                wynikiCzlowieka.append("W")
            
            if i < len(self.wyboryCzlowieka) - 1:
                if self.wyboryCzlowieka[i] == self.wyboryCzlowieka[i + 1]:
                    zmianaCzlowieka.append("S")
                else:
                    zmianaCzlowieka.append("D")
        
        # Uczenie (jeśli mamy >= 3 rundy)
        if len(self.wyboryCzlowieka) >= 3:
            przedostatnie2wyniki = wynikiCzlowieka[-3:-1]
            przedostniaZmiana = zmianaCzlowieka[-2:-1]
            zmianaPoWzorcu = zmianaCzlowieka[-1]
            
            wzorzec_uczenia = (
                przedostatnie2wyniki[0] +
                przedostniaZmiana[0] +
                przedostatnie2wyniki[1]
            )
            
            # Aktualizuj tabelę wzorców
            if self.zapisaneWzorce[wzorzec_uczenia][0] == "Nieznany":
                self.zapisaneWzorce[wzorzec_uczenia][0] = zmianaPoWzorcu
                self.zapisaneWzorce[wzorzec_uczenia][1] = 1
            elif self.zapisaneWzorce[wzorzec_uczenia][0] == zmianaPoWzorcu:
                self.zapisaneWzorce[wzorzec_uczenia][1] += 1
            else:
                self.zapisaneWzorce[wzorzec_uczenia][0] = "Nieznany"
                self.zapisaneWzorce[wzorzec_uczenia][1] = 0
            
            # Wzorzec do predykcji
            poprzedni_wynik = wynikiCzlowieka[-2]
            ostatni_wynik = wynikiCzlowieka[-1]
            ostatnia_zmiana = zmianaCzlowieka[-1]
            
            self.ostatni_wzorzec = (
                poprzedni_wynik +
                ostatnia_zmiana +
                ostatni_wynik
            )
        else:
            self.ostatni_wzorzec = None
        
        # Predykcja następnego ruchu
        if (
            self.ostatni_wzorzec is not None and
            self.zapisaneWzorce[self.ostatni_wzorzec][0] != "Nieznany" and
            self.zapisaneWzorce[self.ostatni_wzorzec][1] >= 2
        ):
            przewidywana_zmiana = self.zapisaneWzorce[self.ostatni_wzorzec][0]
            ostatni_ruch_czlowieka = self.wyboryCzlowieka[-1]
            
            if przewidywana_zmiana == "S":
                self.przewidywany_ruch_maszyny = ostatni_ruch_czlowieka
            else:
                self.przewidywany_ruch_maszyny = 1 - ostatni_ruch_czlowieka
        else:
            self.przewidywany_ruch_maszyny = randint(0, 1)
    
    def reset(self):
        """Resetuj grę"""
        self.__init__()


class AntiShannonGame:
    """Logika z AntymaszynaShannona.py - pomaga graczowi ograć maszynę Shannona"""
    
    def __init__(self):
        self.wyboryCzlowieka = []
        self.wyboryMaszyny = []
        self.zapisaneWzorce = {
            "WSW": ["Nieznany", 0], "WSL": ["Nieznany", 0],
            "WDW": ["Nieznany", 0], "WDL": ["Nieznany", 0],
            "LSW": ["Nieznany", 0], "LSL": ["Nieznany", 0],
            "LDW": ["Nieznany", 0], "LDL": ["Nieznany", 0]
        }
        self.ostatni_wzorzec = None
    
    def make_move(self, wybor_czlowieka, wybor_maszyny):
        """Przetwórz rundę i zwróć rekomendację"""
        self.wyboryCzlowieka.append(wybor_czlowieka)
        self.wyboryMaszyny.append(wybor_maszyny)
        
        # Sprawdź wynik
        if wybor_czlowieka == wybor_maszyny:
            result = "loss"
        else:
            result = "win"
        
        # Uczenie i rekomendacja
        recommendation = self._learn_and_recommend()
        
        return {
            "result": result,
            "recommendation": recommendation
        }
    
    def _learn_and_recommend(self):
        """Ucz się wzorców i generuj rekomendację"""
        wynikiCzlowieka = []
        zmianaCzlowieka = []
        
        for i in range(len(self.wyboryCzlowieka)):
            if self.wyboryCzlowieka[i] == self.wyboryMaszyny[i]:
                wynikiCzlowieka.append("L")
            else:
                wynikiCzlowieka.append("W")
            
            if i < len(self.wyboryCzlowieka) - 1:
                if self.wyboryCzlowieka[i] == self.wyboryCzlowieka[i + 1]:
                    zmianaCzlowieka.append("S")
                else:
                    zmianaCzlowieka.append("D")
        
        if len(self.wyboryCzlowieka) >= 3:
            przedostatnie2wyniki = wynikiCzlowieka[-3:-1]
            przedostniaZmiana = zmianaCzlowieka[-2:-1]
            zmianaPoWzorcu = zmianaCzlowieka[-1]
            
            wzorzec_uczenia = (
                przedostatnie2wyniki[0] +
                przedostniaZmiana[0] +
                przedostatnie2wyniki[1]
            )
            
            if self.zapisaneWzorce[wzorzec_uczenia][0] == "Nieznany":
                self.zapisaneWzorce[wzorzec_uczenia][0] = zmianaPoWzorcu
                self.zapisaneWzorce[wzorzec_uczenia][1] = 1
            elif self.zapisaneWzorce[wzorzec_uczenia][0] == zmianaPoWzorcu:
                self.zapisaneWzorce[wzorzec_uczenia][1] += 1
            else:
                self.zapisaneWzorce[wzorzec_uczenia][0] = "Nieznany"
                self.zapisaneWzorce[wzorzec_uczenia][1] = 0
            
            poprzedni_wynik = wynikiCzlowieka[-2]
            ostatni_wynik = wynikiCzlowieka[-1]
            ostatnia_zmiana = zmianaCzlowieka[-1]
            
            self.ostatni_wzorzec = (
                poprzedni_wynik +
                ostatnia_zmiana +
                ostatni_wynik
            )
        else:
            self.ostatni_wzorzec = None
        
        # Generuj rekomendację
        if (
            self.ostatni_wzorzec is not None and
            self.zapisaneWzorce[self.ostatni_wzorzec][0] != "Nieznany" and
            self.zapisaneWzorce[self.ostatni_wzorzec][1] >= 2
        ):
            przewidywana_zmiana = self.zapisaneWzorce[self.ostatni_wzorzec][0]
            ostatni_ruch_czlowieka = self.wyboryCzlowieka[-1]
            
            if przewidywana_zmiana == "S":
                przewidywany_ruch_maszyny = ostatni_ruch_czlowieka
            else:
                przewidywany_ruch_maszyny = 1 - ostatni_ruch_czlowieka
            
            zalecany_ruch = 1 - przewidywany_ruch_maszyny
            
            return f"👾 Maszyna prawdopodobnie wybierze: {przewidywany_ruch_maszyny}\n✅ Żeby wygrać, wybierz: {zalecany_ruch}"
        else:
            return "🎲 Maszyna nie ma jeszcze potwierdzonego wzorca. W następnej rundzie będzie losować."
    
    def reset(self):
        """Resetuj grę"""
        self.__init__()


def run_simulation(liczba_rund):
    """Symulacja z MaszynaVSAntymaszyna.py"""
    wyboryCzlowieka = []
    wyboryMaszyny = []
    
    zapisaneWzorce = {
        "WSW": ["Nieznany", 0], "WSL": ["Nieznany", 0],
        "WDW": ["Nieznany", 0], "WDL": ["Nieznany", 0],
        "LSW": ["Nieznany", 0], "LSL": ["Nieznany", 0],
        "LDW": ["Nieznany", 0], "LDL": ["Nieznany", 0]
    }
    
    ostatni_wzorzec = None
    nast_ruch_czlowieka = None
    nast_ruch_maszyny = None
    
    wynik_czlowiek = 0
    wynik_maszyna = 0
    
    for runda in range(liczba_rund):
        # Wybór ruchów
        if nast_ruch_czlowieka is None:
            ruch_czlowieka = randint(0, 1)
            ruch_maszyny = randint(0, 1)
        else:
            ruch_czlowieka = nast_ruch_czlowieka
            ruch_maszyny = nast_ruch_maszyny
        
        wyboryCzlowieka.append(ruch_czlowieka)
        wyboryMaszyny.append(ruch_maszyny)
        
        # Sprawdź wynik
        if wyboryCzlowieka[-1] == wyboryMaszyny[-1]:
            wynik_maszyna += 1
        else:
            wynik_czlowiek += 1
        
        # Uczenie
        wynikiCzlowieka = []
        zmianaCzlowieka = []
        
        for i in range(len(wyboryCzlowieka)):
            if wyboryCzlowieka[i] == wyboryMaszyny[i]:
                wynikiCzlowieka.append("L")
            else:
                wynikiCzlowieka.append("W")
            
            if i < len(wyboryCzlowieka) - 1:
                if wyboryCzlowieka[i] == wyboryCzlowieka[i + 1]:
                    zmianaCzlowieka.append("S")
                else:
                    zmianaCzlowieka.append("D")
        
        if len(wyboryCzlowieka) >= 3:
            przedostatnie2wyniki = wynikiCzlowieka[-3:-1]
            przedostniaZmiana = zmianaCzlowieka[-2:-1]
            zmianaPoWzorcu = zmianaCzlowieka[-1]
            
            wzorzec_uczenia = (
                przedostatnie2wyniki[0] +
                przedostniaZmiana[0] +
                przedostatnie2wyniki[1]
            )
            
            if zapisaneWzorce[wzorzec_uczenia][0] == "Nieznany":
                zapisaneWzorce[wzorzec_uczenia][0] = zmianaPoWzorcu
                zapisaneWzorce[wzorzec_uczenia][1] = 1
            elif zapisaneWzorce[wzorzec_uczenia][0] == zmianaPoWzorcu:
                zapisaneWzorce[wzorzec_uczenia][1] += 1
            else:
                zapisaneWzorce[wzorzec_uczenia][0] = "Nieznany"
                zapisaneWzorce[wzorzec_uczenia][1] = 0
            
            poprzedni_wynik = wynikiCzlowieka[-2]
            ostatni_wynik = wynikiCzlowieka[-1]
            ostatnia_zmiana = zmianaCzlowieka[-1]
            
            ostatni_wzorzec = (
                poprzedni_wynik +
                ostatnia_zmiana +
                ostatni_wynik
            )
        else:
            ostatni_wzorzec = None
        
        # Predykcja
        if (
            ostatni_wzorzec is not None and
            zapisaneWzorce[ostatni_wzorzec][0] != "Nieznany" and
            zapisaneWzorce[ostatni_wzorzec][1] >= 2
        ):
            przewidywana_zmiana = zapisaneWzorce[ostatni_wzorzec][0]
            ostatni_ruch_czlowieka = wyboryCzlowieka[-1]
            
            if przewidywana_zmiana == "S":
                przewidywany_ruch_maszyny = ostatni_ruch_czlowieka
            else:
                przewidywany_ruch_maszyny = 1 - ostatni_ruch_czlowieka
            
            nast_ruch_maszyny = przewidywany_ruch_maszyny
            nast_ruch_czlowieka = 1 - przewidywany_ruch_maszyny
        else:
            nast_ruch_maszyny = randint(0, 1)
            nast_ruch_czlowieka = randint(0, 1)
    
    return {
        "total_rounds": liczba_rund,
        "anti_wins": wynik_czlowiek,
        "machine_wins": wynik_maszyna,
        "anti_percentage": (wynik_czlowiek / liczba_rund * 100) if liczba_rund > 0 else 0,
        "machine_percentage": (wynik_maszyna / liczba_rund * 100) if liczba_rund > 0 else 0
    }
