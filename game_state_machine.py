import time
from display import Display
from game_logic import GameLogic

STATE_RESET = 0
STATE_PLAYER_SELECTION1 = 1
STATE_PLAYER_SELECTION2 = 2
STATE_GAME = 3
STATE_GAME_END = 4

class GameStateMachine:
    def __init__(self):
        self.state = None  # Kein Zustand am Anfang
        self.previous_state = None
        self.display = Display()  # Initialisiere das Display
        self.game_logic = GameLogic()  # Initialisiere die Spiellogik

        # Setze initial den RESET Zustand und starte die Regenbogenanimation
        self.set_state(STATE_RESET)

    def set_state(self, new_state):
        """Wechselt den Zustand und behandelt die Display-Aktionen."""
        if self.state != new_state:
            # Stoppe die Regenbogenanimation und lösche das Display, wenn der RESET-Zustand verlassen wird
            if self.state == STATE_RESET:
                self.display.rainbow_stop()
                self.display.clear()
                print("Regenbogenanimation gestoppt und Display gelöscht.")

            self.previous_state = self.state
            self.state = new_state
            print(f"Zustand gewechselt zu: {self.get_state_name()}")

            # Starte die Regenbogenanimation, wenn der RESET-Zustand betreten wird
            if self.state == STATE_RESET:
                self.display.rainbow_start(wait=0.01)
                print("Regenbogenanimation gestartet.")

    def get_state_name(self):
        """Gibt den Namen des aktuellen Zustands zurück."""
        if self.state == STATE_RESET:
            return "RESET"
        elif self.state == STATE_PLAYER_SELECTION1:
            return "PLAYER_SELECTION1"
        elif self.state == STATE_PLAYER_SELECTION2:
            return "PLAYER_SELECTION2"
        elif self.state == STATE_GAME:
            return "GAME"
        elif self.state == STATE_GAME_END:
            return "GAME_END"
        else:
            return "UNKNOWN"

    def go_back(self):
        """Gehe einen Zustand zurück, falls möglich."""
        if self.previous_state is not None:
            print(f"Zurück zum Zustand: {self.get_state_name()}")
            self.set_state(self.previous_state)

    def handle_input(self, short_presses, long_presses):
        """Verarbeitet die Tastendrücke und wechselt entsprechend den Zustand."""
        if self.state == STATE_RESET and short_presses:
            print("Short Press erkannt im Zustand RESET.")
            self.set_state(STATE_PLAYER_SELECTION1)
            self.game_logic.reset()  # Setze das Spiel zurück

        elif self.state == STATE_PLAYER_SELECTION1 and short_presses:
            if 1 in short_presses or 2 in short_presses:
                print(f"Taste {short_presses[0]} gedrückt für Spieler 1 Auswahl.")
                self.set_state(STATE_PLAYER_SELECTION2)
                self.game_logic.set_player(1, "Mensch" if 1 in short_presses else "KI")
                # Update Display für Spielerwahl
                self.display.update_player_selection_display(1, "Mensch" if 1 in short_presses else "KI")

        elif self.state == STATE_PLAYER_SELECTION2 and short_presses:
            if 1 in short_presses or 2 in short_presses:
                print(f"Taste {short_presses[0]} gedrückt für Spieler 2 Auswahl.")
                self.set_state(STATE_GAME)
                self.game_logic.set_player(2, "Mensch" if 1 in short_presses else "KI")
                # Update Display für Spielerwahl
                self.display.update_player_selection_display(2, "Mensch" if 1 in short_presses else "KI")

        elif self.state == STATE_GAME and short_presses:
            spalte = short_presses[0] - 1  # Verarbeite die Spaltenwahl
            print(f"Spielzug in Spalte {spalte + 1}.")
            ergebnis = self.game_logic.play_turn(spalte)  # Ergebnis des Spielzugs
            # Spielfeld nach dem Zug aktualisieren
            self.display.update_board(self.game_logic.spielfeld.gib_spielfeld())
            # Überprüfen, ob das Ergebnis nicht leer ist (entweder Sieg oder Unentschieden)
            if ergebnis is not None:
                self.set_state(STATE_GAME_END)  # Gehe in den Spiel-End-Zustand

        elif self.state == STATE_GAME_END:
            print("Spielende, Spiel kann zurückgesetzt werden.")
            time.sleep(5)  # Warten für 5s, dann Neustart
            self.set_state(STATE_RESET)

        # Handling für Long Press
        if 7 in long_presses:
            if 1 in long_presses:
                print("Long Press auf Taste 1 + 7 erkannt: Zurücksetzen.")
                self.set_state(STATE_RESET)
            else:
                print("Long Press auf Taste 7 erkannt: Gehe zum vorherigen Zustand.")
                self.go_back()