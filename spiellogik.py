from ulab import numpy as np

# Gewinnmatrixen
spieler1Vec = np.array([1,1,1,1], dtype=np.int8)
spieler2Vec = np.array([2,2,2,2], dtype=np.int8)

class Spielfeld():

    # Die Klasse Spielfeld füllt automatisch die aktuelle Spalte, in die geworfen wird
    # Es wird geprüft, ob die Zeile, Spalte oder Diagonale die Bedingung 4 in einer Reihe erfüllt
    #
    #  Die Codierung des Spielfelds erfolgt über eine Integer. 
    # Leer = 0,
    # Spieler1 = 1,
    # Spieler2 = 2
    #
    # Für den Sieg wird in den Funktionen nur geprüft, ob irgendwer gewonnen hat. Wer gewonnen hat, wird in der Funktion wurf() anhand der übergebenen Spielernummer ermittelt


    


    def __init__(self):
        self.spielfeld = np.zeros((6,7), dtype=np.int8)

    def _winning_rule(self, arr) -> bool:
        spieler1Vec = np.array([1,1,1,1])
        spieler2Vec = np.array([2,2,2,2])

        sub_arrays = [arr[i:i+4] for i in range(len(arr) -3)]

        siegSpieler1 = any([np.array_equal(spieler1Vec,sub) for sub in sub_arrays])
        siegSpieler2 = any([np.array_equal(spieler2Vec,sub) for sub in sub_arrays])

        if siegSpieler1 or siegSpieler2:
            return True
        else:
            return False
        


        
    def _gib_diagonal(self, _table, zeile, spalte) -> list:     # gibt die Diagonalen zurück, welche den angegebenen Pixel enthalten
        diagonalen = []
        diagonalen.append(np.diag(_table, k=(spalte - zeile)))  # k = Offset, k=0 wäre ganze Diagonale
        diagonalen.append(np.diag(np.flip(_table, axis=1), k=-_table.shape[1] + (spalte+zeile)+1))  #np.flip(_table, axis=1) = numpy.rot(90)
        return diagonalen
    


    def _gib_gerade(self, _table, zeile, spalte) -> list:         # gibt die Zeilen und Spalten zurück, in den der aktuelle Pixel enthalten ist
        schraegen = []
        schraegen.append(_table[zeile,:])                            # gibt die ganze Zeile zurück
        schraegen.append(_table[:,spalte])                           # gibt die ganze Spalte zurück
        return schraegen


    def _pruefe_gewonnen(self, zeile, spalte) -> bool:

        # bekommt alle Zeilen, Spalten und Diagonalen als Vektoren und überprüft dann, ob in einem dieser Vektoren 4 mal die Gleiche Zahl (Spielerzahl) hinternander steckt

        global spieler1Vec
        global spieler2Vec

        alle_reihen = [] # Array an Arrays mit unterschiedlicher Länge
        alle_reihen.extend(self._gib_diagonal(self.spielfeld, zeile, spalte))
        alle_reihen.extend(self._gib_gerade(self.spielfeld, zeile, spalte))

        
        # zerlege das Array in die einzelnen unterschiedlich langen Arrays

        for reihen in alle_reihen:

            # zerlege nun das eine Array in einzelne Arrays, welche je 4 Pixel lang sind
            vierer_reihen = [reihen[i:i+4] for i in range(len(reihen) -3)]

            siegSpieler1 = any([all(spieler1Vec == eine_vierer_reihe) for eine_vierer_reihe in vierer_reihen])
            siegSpieler2 = any([all(spieler2Vec == eine_vierer_reihe) for eine_vierer_reihe in vierer_reihen])

            if siegSpieler1 or siegSpieler2:
                return True
            else:
                pass

        return False
    


    def wurf(self, spieler, spalte):

        spalten_vec = self.spielfeld[:,spalte]      # kopiere die aktuelle Spalte in einen Vektor, um damit zu arbeiten
        non_zero = np.nonzero(spalten_vec)[0]    # zählt, wo nicht null ist. Damit muss an der Stelle dann gefüllt werden

        if non_zero.size == 0:                      
            zeile = self.spielfeld.shape[0]-1
            self.spielfeld[zeile,spalte] = spieler

        else:                                       
            zeile = non_zero[0]-1
            self.spielfeld[zeile,spalte] = spieler


        if self._pruefe_gewonnen(zeile, spalte):
            return 1
        else:
            return self.spielfeld
        

    def reset(self):                                # setzt das Spielfeld zurück
        self.spielfeld = np.zeros((6,7), dtype=np.int8)
        return self.spielfeld
