from random import randint

PATTERNS = ["WSW", "WSL", "WDW", "WDL",
            "LSW", "LSL", "LDW", "LDL"]


def init_memory():
    return {
        p: {"previous_behavior": None, "is_repeated": False, "count": 0}
        for p in PATTERNS
    }


def update_memory(game_history, memory):
    if len(game_history) < 3:
        return None

    playN = game_history[-1]
    playN1 = game_history[-2]
    playN2 = game_history[-3]

    outcomeN2 = 'W' if playN2["playerWon"] else 'L'
    outcomeN1 = 'W' if playN1["playerWon"] else 'L'
    changeN1 = 'S' if playN1["playerMove"] == playN2["playerMove"] else 'D'

    pattern_key = outcomeN2 + changeN1 + outcomeN1

    actual_behavior = 'same' if playN["playerMove"] == playN1["playerMove"] else 'different'

    cell = memory[pattern_key]

    if cell["previous_behavior"] is None:
        cell["previous_behavior"] = actual_behavior
        cell["count"] = 1
        cell["is_repeated"] = False
    else:
        if cell["previous_behavior"] == actual_behavior:
            cell["count"] += 1
            if cell["count"] >= 2:
                cell["is_repeated"] = True
        else:
            cell["previous_behavior"] = actual_behavior
            cell["count"] = 1
            cell["is_repeated"] = False

    return pattern_key, actual_behavior, cell


def get_prediction(game_history, memory):
    if len(game_history) < 2:
        return None, None

    playN1 = game_history[-1]
    playN2 = game_history[-2]

    outcomeN2 = 'W' if playN2["playerWon"] else 'L'
    outcomeN1 = 'W' if playN1["playerWon"] else 'L'
    changeN1 = 'S' if playN1["playerMove"] == playN2["playerMove"] else 'D'

    pattern_key = outcomeN2 + changeN1 + outcomeN1
    cell = memory[pattern_key]

    if cell["is_repeated"] and cell["previous_behavior"] is not None:
        return cell["previous_behavior"], pattern_key
    else:
        return None, pattern_key


def main():
    print("=== ANTYMASZYNA SHANNONA ===\n")
    print("Instrukcja:")
    print(" 1. Graj z maszyną Shannona w GUI.")
    print(" 2. Po KAŻDEJ rundzie przepisz tutaj:")
    print("    - swój ruch (0/1),")
    print("    - ruch maszyny (0/1).")
    print(" 3. Antymaszy na powie Ci, co maszyna PRAWDPODOBNIE zrobi w kolejnej rundzie.\n")

    memory = init_memory()
    game_history = []  # jak w maszynie: {"playerMove": ..., "playerWon": ...}
    round_no = 0

    while True:
        round_no += 1
        print(f"\n## Nowa runda (wpisywanie wyniku rundy {round_no})")

        # 1. Wpisujesz REALNE wyniki z gry
        while True:
            h = input("Twój ostatni wybór (0/1, q = wyjście): ").strip()
            if h.lower() == 'q':
                print("\nKoniec pracy antymaszyny.")
                return
            if h in ("0", "1"):
                player_move = int(h)
                break
            print("Podaj 0 lub 1 (q = wyjście).")

        while True:
            m = input("Ostatni wybór maszyny (0/1): ").strip()
            if m in ("0", "1"):
                machine_move = int(m)
                break
            print("Podaj 0 lub 1.")

        print(f"Maszyna wybrała: {machine_move}")

        player_won = (player_move != machine_move)
        if player_won:
            print("✅ WYGRAŁEŚ (maszyna się pomyliła)")
        else:
            print("❌ PRZEGRAŁEŚ (maszyna trafiła twój ruch)")

        # 2. Zapisujemy runde do historii i uczymy pamięć (tak jak maszyna)
        game_history.append({"playerMove": player_move, "playerWon": player_won})
        learn_info = update_memory(game_history, memory)

        if learn_info is not None:
            pattern_key_learn, actual_behavior, cell = learn_info
            beh_short = 'S' if actual_behavior == 'same' else 'D'
            status = "ZNANY" if cell["is_repeated"] else "NIEPEWNY"
            print(
                f"Wzorzec (uczenie): {pattern_key_learn}, "
                f"Reakcja gracza: {beh_short}, "
                f"licznik: {cell['count']}, status: {status}"
            )
        else:
            print("Za mało danych, żeby cokolwiek się nauczyć (mniej niż 3 rundy).")

        # 3. Przewidujemy KOLEJNY ruch maszyny (runda round_no+1)
        predicted_behavior, pattern_key_pred = get_prediction(game_history, memory)

        if predicted_behavior is None or len(game_history) < 1:
            print("\n🎲 Maszyna NIE MA jeszcze potwierdzonego wzorca dla aktualnej sytuacji.")
            if pattern_key_pred is not None:
                print(f"   Aktualny wzorzec: {pattern_key_pred} – status: NIEPEWNY.")
            print("🎲 W następnej rundzie będzie LOSOWAĆ (0 lub 1).")
            print("✅ Nie da się tego przewidzieć lepiej niż rzut monetą.")
        else:
            last_player_move = game_history[-1]["playerMove"]
            if predicted_behavior == 'same':
                predicted_machine_move = last_player_move
            else:
                predicted_machine_move = 1 - last_player_move

            print(f"\n👾 Aktualny wzorzec: {pattern_key_pred} – status: ZNANY.")
            print(f"   Po takim wzorcu gracz zwykle: "
                  f"{'POWTARZA ruch (S)' if predicted_behavior == 'same' else 'ZMIENIA ruch (D)'}")
            print(f"👾 Maszyna PRAWDPODOBNIE wybierze: {predicted_machine_move}")
            print(f"✅ ŻEBY WYGRAĆ, wybierz: {1 - predicted_machine_move}")

        print("-" * 50)


if __name__ == "__main__":
    main()
