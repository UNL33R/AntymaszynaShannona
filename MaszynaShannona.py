# MaszynaShannona.py
# Prosta wersja konsolowa maszyny Shannona (zgodna z logiką z GUI).

from random import randint

# Wszystkie możliwe wzorce: W/L, S/D, W/L
PATTERNS = ["WSW", "WSL", "WDW", "WDL",
            "LSW", "LSL", "LDW", "LDL"]


def init_memory():
    """
    Pamięć maszyny: dla każdego wzorca trzymamy:
    - previous_behavior: 'same' / 'different' / None
    - is_repeated: czy zachowanie zostało już POTWIERDZONE (>=2 razy takie samo)
    - count: ile razy z rzędu widzieliśmy to samo zachowanie po tym wzorcu
    """
    return {
        p: {"previous_behavior": None, "is_repeated": False, "count": 0}
        for p in PATTERNS
    }


def update_memory(game_history, memory):
    """
    Aktualizacja pamięci po zakończeniu rundy.
    game_history: lista rund (dict):
        {"playerMove": 0/1, "playerWon": True/False}
    Używamy trójek rund (N-2, N-1) -> zachowanie w N.
    """
    if len(game_history) < 3:
        return None  # za mało danych

    playN = game_history[-1]   # runda N
    playN1 = game_history[-2]  # runda N-1
    playN2 = game_history[-3]  # runda N-2

    # Wyniki W/L z perspektywy gracza
    outcomeN2 = 'W' if playN2["playerWon"] else 'L'
    outcomeN1 = 'W' if playN1["playerWon"] else 'L'

    # Zmiana S/D między N-2 a N-1
    changeN1 = 'S' if playN1["playerMove"] == playN2["playerMove"] else 'D'

    pattern_key = outcomeN2 + changeN1 + outcomeN1

    # Zachowanie gracza po tej sytuacji (w rundzie N): czy powtórzył ruch z N-1?
    actual_behavior = 'same' if playN["playerMove"] == playN1["playerMove"] else 'different'

    cell = memory[pattern_key]

    if cell["previous_behavior"] is None:
        # pierwszy raz widzimy ten wzorzec
        cell["previous_behavior"] = actual_behavior
        cell["count"] = 1
        cell["is_repeated"] = False
    else:
        if cell["previous_behavior"] == actual_behavior:
            # to samo zachowanie co poprzednio -> wzorzec się wzmacnia
            cell["count"] += 1
            if cell["count"] >= 2:
                # co najmniej dwa razy pod rząd to samo zachowanie → uznajemy wzorzec
                cell["is_repeated"] = True
        else:
            # zachowanie inne niż poprzednio → resetujemy licznik
            cell["previous_behavior"] = actual_behavior
            cell["count"] = 1
            cell["is_repeated"] = False

    return pattern_key, actual_behavior, cell


def get_prediction(game_history, memory):
    """
    Przewidywanie zachowania gracza w KOLEJNEJ rundzie na podstawie
    dwóch ostatnich rund (N-2, N-1).
    Zwraca:
    - 'same' / 'different' lub None
    - klucz wzorca (np. 'WSW') lub None
    """
    if len(game_history) < 2:
        return None, None

    playN1 = game_history[-1]  # runda N-1
    playN2 = game_history[-2]  # runda N-2

    outcomeN2 = 'W' if playN2["playerWon"] else 'L'
    outcomeN1 = 'W' if playN1["playerWon"] else 'L'
    changeN1 = 'S' if playN1["playerMove"] == playN2["playerMove"] else 'D'

    pattern_key = outcomeN2 + changeN1 + outcomeN1
    cell = memory[pattern_key]

    if cell["is_repeated"] and cell["previous_behavior"] is not None:
        # wzorzec został już potwierdzony (>=2 razy)
        return cell["previous_behavior"], pattern_key
    else:
        # wzorzec niepewny → maszyna powinna losować
        return None, pattern_key


def main():
    print("=== MASZYNA SHANNONA (wersja tekstowa) ===\n")
    print("W każdej rundzie wpisz 0 lub 1. Maszyna spróbuje przewidzieć Twój ruch.\n")

    memory = init_memory()
    game_history = []  # lista dictów: {"playerMove": ..., "playerWon": ...}
    round_no = 0

    while True:
        round_no += 1
        print(f"\n--- RUNDA {round_no} ---")

        # 1. Maszyna przygotowuje prognozę (na podstawie historii)
        predicted_behavior, pattern_key = get_prediction(game_history, memory)

        if predicted_behavior is None or len(game_history) < 1:
            # brak pewnego wzorca → losujemy