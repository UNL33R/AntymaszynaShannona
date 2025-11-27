from random import randint

wyboryCzlowieka = [1, 0, 1, 1, 0]
wyboryMaszyny = [0, 0, 0, 0, 0]
wynikiCzlowieka = []
#wyboryMaszyny.append(randint(0, 1))
zmianaCzlowieka = []

#przypisanie W i L do wyborow Czlowieka
for wybor in range(len(wyboryCzlowieka)):
    if wyboryCzlowieka[wybor] == wyboryMaszyny[wybor]:
        wynikiCzlowieka.append("L")
    else:
        wynikiCzlowieka.append("W")
    


for i in range(len(wyboryCzlowieka) - 1):
    if wyboryCzlowieka[i] == wyboryCzlowieka[i + 1]:
        zmianaCzlowieka.append("S")
    else:
        zmianaCzlowieka.append("D")




'''
ostatnie2wyniki = wynikiCzlowieka[-2:]
ostatniaZmiana = zmianaCzlowieka[-1:]


print(ostatnie2wyniki)
print(ostatniaZmiana)
'''

przedostatnie2wyniki = wynikiCzlowieka[-3:-1]

# Zmiana między nimi (indeks -2 w zmianaCzlowieka)
przedostniaZmiana = zmianaCzlowieka[-2:-1]


print("2 przedostatnie wyniki:", przedostatnie2wyniki)
print("Zmiana między nimi:", przedostniaZmiana)
print("Zmiana po tej sekwencji:", zmianaPoWzorcu)

wzorzec = [przedostatnie2wyniki[0], przedostniaZmiana[0], przedostatnie2wyniki[1]]

zapisaneWzorce = {
    "WSW": "Nieznany", "WSL": "Nieznany", 
    "WDW": "Nieznany", "WDL": "Nieznany", 
    "LSW": "Nieznany", "LSL": "Nieznany", 
    "LDW": "Nieznany", "LDL": "Nieznany"
}

#if wzorzec == [W, S, W]:
