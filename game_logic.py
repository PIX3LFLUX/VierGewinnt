import numpy as np
from spielfeld import Spielfeld  # Stelle sicher, dass die Spielfeld-Klasse in spielfeld.py liegt

class GameLogic:
    def __init__(self):
        """Initialisiert das Spiel und das Spielfeld."""
        self.spielfeld = Spielfeld()
        self.current_player = 1  # 1 für Spieler 1, 2 für Spieler 2
        self.winner = None

    def reset(self):
        """Setzt das Spiel zurück."""
        self.spielfeld.reset()
        self.current_player = 1
        self.winner = None
        print("Spiel wurde zurückgesetzt.")

    def set_player(self, player_num, player_type):
        """Setzt den aktuellen Spieler fest."""
        print(f"Spieler {player_num} ist {player_type}")
        self.current_player = player_num

    def play_turn(self, spalte):
        """Simuliert einen Spielzug für den aktuellen Spieler."""
        if self.winner:
            print("Das Spiel ist bereits beendet.")
            return None

        # Führe den Wurf des aktuellen Spielers aus
        spielfeld, status = self.spielfeld.wurf(self.current_player, spalte)

        if status == -1:
            print("Diese Spalte ist voll. Wähle eine andere Spalte.")
            return None  # Ungültiger Zug

        # Zeige das Spielfeld nach jedem Zug an
        self.spielfeld.zeige_spielfeld()

        if status == 1:  # Gewinner gefunden
            print(f"Spieler {self.current_player} hat gewonnen!")
            self.winner = self.current_player
            return self.current_player

        elif status == -2:  # Unentschieden
            print("Das Spiel endet unentschieden!")
            self.winner = 0
            return 0

        # Wechsel zum nächsten Spieler
        self.current_player = 2 if self.current_player == 1 else 1
        return None

    def get_winner_positions(self):
        """Gibt die Positionen der Gewinnsteine zurück (falls vorhanden)."""
        if self.winner:
            return np.where(self.spielfeld.spielfeld != 0)
        return []

    def gib_spielfeld(self):
        """Gibt das aktuelle Spielfeld zurück."""
        return self.spielfeld.gib_spielfeld()