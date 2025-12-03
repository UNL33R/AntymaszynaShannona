# GUI dla Maszyny Shannona

Nowoczesna aplikacja webowa umożliwiająca interaktywne korzystanie z trzech trybów gry opartych na algorytmie uczenia maszynowego Claude'a Shannona.

## 🎮 Tryby gry

### 1. Maszyna Shannona
Zagraj przeciwko maszynie uczącej się! Maszyna analizuje Twoje wzorce zachowań i próbuje przewidzieć Twoje kolejne ruchy.

### 2. Anty-Maszyna Shannona
Otrzymuj rekomendacje jak ograć Maszynę Shannona. Wprowadzaj ruchy z rozgrywki i dostań podpowiedzi.

### 3. Symulacja Automatyczna
Obserwuj pojedynek: Maszyna vs Anty-Maszyna! Uruchom symulację i zobacz, która strona wygra po zadanej liczbie rund.

## 🚀 Uruchomienie

### Krok 1: Instalacja zależności

```bash
cd gui
pip install -r requirements.txt
```

### Krok 2: Uruchomienie serwera

```bash
python server.py
```

### Krok 3: Otwórz przeglądarkę

Przejdź do: **http://localhost:5000**

## 📁 Struktura projektu

```
gui/
├── index.html          # Interfejs użytkownika
├── style.css           # Stylizacja (dark mode, glassmorphism)
├── script.js           # Logika frontendowa i komunikacja z API
├── server.py           # Serwer Flask z endpointami API
├── shannon_engine.py   # Logika gier z oryginalnych skryptów
├── requirements.txt    # Zależności Python
└── README.md          # Ten plik
```

## 🎨 Cechy interfejsu

- 🌙 **Dark mode** z gradientami i efektami glassmorphism
- ✨ **Płynne animacje** i efekty hover
- 📊 **Statystyki w czasie rzeczywistym**
- 📱 **Responsywny design**
- 🎯 **Intuicyjna nawigacja** między trybami

## 🔧 Technologie

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python, Flask
- **Design**: Glassmorphism, gradients, dark mode
- **Fonts**: Google Fonts (Inter)

## 📝 Oryginalne skrypty

Logika gier oparta na:
- `MaszynaShannona.py` - Maszyna ucząca się
- `AntymaszynaShannona.py` - Strategia przeciwko maszynie
- `MaszynaVSAntymaszyna.py` - Automatyczna symulacja

---

Stworzył: Antigravity AI
