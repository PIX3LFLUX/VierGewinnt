import time
import RPi.GPIO as GPIO
from controller import Controller
from config import TASTER_PINS
from game_state_machine import GameStateMachine, STATE_GAME
from ki import KI  # Importiere die KI

def main():
    controller = Controller(TASTER_PINS)
    game_state_machine = GameStateMachine()
    ki_engine = KI()  # Initialisiere die KI-Engine

    try:
        while True:
            short_presses = controller.get_short_press()
            long_presses = controller.get_long_press()

            # Überprüfe, ob der aktuelle Spieler eine KI ist
            current_player = game_state_machine.game_logic.current_player
            current_player_type = game_state_machine.game_logic.player_types[current_player]

            if game_state_machine.state == STATE_GAME and current_player_type == "KI":
                print(f"KI (Spieler {current_player}) ist am Zug...")
                board = game_state_machine.game_logic.spielfeld.gib_spielfeld()
                ki_spalte = ki_engine.get_spalte(board)  # KI wählt eine Spalte
                print(f"KI wählt Spalte {ki_spalte + 1}")
                short_presses = [ki_spalte + 1]  # Simuliere den Zug der KI als Short Press

            # Übergibt die erkannten oder simulierten Tasten an die Zustandsmaschine
            game_state_machine.handle_input(short_presses, long_presses)

            time.sleep(0.1)  # Warte 100ms, um die CPU-Last zu minimieren

    except KeyboardInterrupt:
        print("Programm beendet.")
    finally:
        GPIO.cleanup()  # GPIO-Pins sauber zurücksetzen

if __name__ == "__main__":
    main()