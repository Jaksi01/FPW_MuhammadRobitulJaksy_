from Testing.main_menu import run_main_menu
from Testing.main_testing import run_game

if __name__ == "__main__":
    while True:
        action = run_main_menu()

        if action == "start_game":
            result = run_game()

            if result == "back_to_menu":
                continue
            elif result == "quit":
                break

        elif action == "quit":
            break
