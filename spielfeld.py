import numpy as np

class Spielfeld:
    def __init__(self):
        self.spielfeld = np.zeros((6, 7), dtype=np.int8)  # 6 Reihen, 7 Spalten, Standardgröße

    def _korrelation(self, filter):
        # bekomme nach und nach verschiedene Filter übergeben, die dann auf das Spielfeld angewendet werden

        padded_spielfeld = np.zeros((self.spielfeld.shape[0] + filter.shape[0] - 1, self.spielfeld.shape[1] + filter.shape[1] - 1), dtype=np.int8)
        padded_spielfeld[filter.shape[0] - 1:, filter.shape[1] - 1:] = self.spielfeld

        #np.pad(self.spielfeld, [(filter.shape[0] - 1, 0), (filter.shape[1] - 1, 0)], mode='constant')

        ergebnis = np.zeros((self.spielfeld.shape[0], self.spielfeld.shape[1]), dtype=np.int8)

        for i in range(ergebnis.shape[0]):
            for j in range(ergebnis.shape[1]):
                sub_matrix = padded_spielfeld[i:i + filter.shape[0], j:j + filter.shape[1]]
                ergebnis[i, j] = np.sum(sub_matrix * filter)


        return ergebnis

    def _finde_pos(self, array, value):
        """Sucht Positionen, an denen der Wert `value` im Array vorkommt."""
        pos = []
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                if array[i, j] == value:
                    pos.append((i, j))
        return pos

    def _pruefe_gewonnen(self, spieler):
        # Erstelle Filter für horizontale, vertikale und diagonale Gewinnmuster
        
        pruef_wert = spieler*4

        x = 0

        while(1):
            if x == 0:
                filter = np.eye(4, dtype=np.int8)  # diagonal absteigend

            elif x == 1:
                filter = np.flip(filter, axis=0) # diagonal aufsteigend

            elif x == 2:
                filter = np.array([[1,1,1,1]], dtype=np.int8) # horizontal

            elif x == 3:
                filter = np.array([[1],[1],[1],[1]], dtype=np.int8) # vertikal

            # korrelieren
            ergebnis = self._korrelation(filter)

            # print("Ergebnis nach Korr: \n" , ergebnis)

            # prüfe ob irgendwo pruef_wert in den Ergebnissen enthalten ist (4 oder -4)
            # gib dann die Koordinaten zurück
            pos = self._finde_pos(ergebnis, pruef_wert)

            # print("Filter", filter)

            if len(pos) > 0:
                return pos[0], filter
        
            else:
                x = x + 1
                if x == 4:
                    return False, []

    def wurf(self, spieler, spalte):
        """Führt einen Zug für den aktuellen Spieler in der angegebenen Spalte aus.
        Spieler 1 wird durch +1 und Spieler 2 durch -1 repräsentiert.
        """
        spalten_vec = self.spielfeld[:, spalte]  # Spalte extrahieren
        non_zero = np.nonzero(spalten_vec)[0]  # Finde gefüllte Positionen

        # Platzieren des Steins in der nächstfreien Zeile
        wert = 1 if spieler == 1 else -1  # Spieler 1 -> 1, Spieler 2 -> -1

        if non_zero.size == 0:
            zeile = self.spielfeld.shape[0] - 1
            self.spielfeld[zeile, spalte] = wert
        elif non_zero.size == 6:
            return self.spielfeld, -1  # Spalte voll, ungültiger Zug
        else:
            zeile = non_zero[0] - 1
            self.spielfeld[zeile, spalte] = wert

        # Überprüfen, ob der aktuelle Spieler gewonnen hat
        pos, filter = self._pruefe_gewonnen(wert)

        if pos:  # Es gibt einen Gewinner
            # Gewinnsteine maskieren
            maskiertes_spiel = np.zeros_like(self.spielfeld)
            for i in range(filter.shape[0]):
                for j in range(filter.shape[1]):
                    if filter[i, j] == 1:
                        try:
                            maskiertes_spiel[pos[0] - filter.shape[0] + 1 + i, pos[1] - filter.shape[1] + 1 + j] = wert
                        except IndexError:
                            continue  # Schutz vor Randbedingungen des Spielfelds
            return maskiertes_spiel, 1  # Gewinner gefunden

        # Überprüfen, ob das Spielfeld voll ist (Unentschieden)
        if not np.any(self.spielfeld == 0):  # Spielfeld komplett gefüllt
            return self.spielfeld, -2  # Unentschieden

        return self.spielfeld, 0  # Kein Gewinn, Spiel geht weiter

    def reset(self):
        """Setzt das Spielfeld zurück."""
        self.spielfeld = np.zeros((6, 7), dtype=np.int8)
        return self.spielfeld

    def zeige_spielfeld(self):
        """Zeigt das Spielfeld auf der Konsole an."""
        for zeile in self.spielfeld:
            print(' '.join(['⚪' if feld == 0 else ('🔴' if feld == 1 else '🟡') for feld in zeile]))
        print("1  2  3  4  5  6  7\n")

    def gib_spielfeld(self):
        """Gibt das aktuelle Spielfeld zurück."""
        return self.spielfeld