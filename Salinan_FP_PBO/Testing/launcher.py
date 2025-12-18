from Testing.main_menu import run_main_menu
from Testing.main_testing import run_game

if __name__ == "__main__":
    action = run_main_menu()
    if action == "start_game":
        run_game()
