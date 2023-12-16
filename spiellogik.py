class Spielfeld():

    # Die Klasse Spielfeld füllt automatisch die aktuelle Spalte, in die geworfen wird
    # Es wird geprüft, ob die Zeile, Spalte oder Diagonale die Bedingung 4 in einer Reihe erfüllt
    #
    #  Die Codierung des Spielfelds erfolgt über eine Integer. 
    # Leer = 0,
    # Spieler1 = 1,
    # Spieler2 = 2
    #
    # Für den Sieg wird in den Funktionen nur geprüft, ob irgendwer gewonnen hat. Wer gewonnen hat, wird in der Funktion drop() anhand der übergebenen Spielernummer ermittelt


    def __init__(self):
        self.spielfeld = np.zeros((6,7,), dtype = int)

    def _winning_rule(self, arr) -> bool:
        siegSpieler1 = np.array([1,1,1,1])
        siegSpieler2 = np.array([2,2,2,2])

        sub_arrays = [arr[i:i+4] for i in range(len(arr) -3)]

        siegSpieler1 = any([np.array_equal(win1rule,sub) for sub in sub_arrays])
        siegSpieler2 = any([np.array_equal(win2rule,sub) for sub in sub_arrays])

        if siegSpieler1 or siegSpieler2:
            return True
        else:
            return False
        


        
    def _get_diagonals(self, _table, zeile, spalte) -> list:     # gibt die Diagonalen zurück, welche den angegebenen Pixel enthalten
        diags = []
        diags.append(np.diagonal(_table, offset=(spalte - zeile)))
        diags.append(np.diagonal(np.rot90(_table), offset=-_table.shape[1] + (spalte+zeile)+1))
        return diags
    


    def _get_axes(self, _table, zeile, spalte) -> list:         # gibt die Zeilen und Spalten zurück, in den der aktuelle Pixel enthalten ist
        axes = []
        axes.append(_table[zeile,:])                            # gibt die ganze Zeile zurück
        axes.append(_table[:,spalte])                           # gibt die ganze Spalte zurück
        return axes


    def _winning_check(self, zeile, spalte) -> bool:

        # bekommt alle Zeilen, Spalten und Diagonalen als Vektoren und überprüft dann, ob in einem dieser Vektoren 4 mal die Gleiche Zahl (Spielerzahl) hinternander steckt

        all_arr = []
        all_arr.extend(self._get_diagonals(self.spielfeld, zeile, spalte))
        all_arr.extend(self._get_axes(self.spielfeld, zeile, spalte))

        for arr in all_arr:
            winner = self._winning_rule(arr)
            if winner:
                return True
            else:
                pass
    


    def drop(self, spieler, spalte):

        spalten_vec = self.spielfeld[:,spalte]      # kopiere die aktuelle Spalte in einen Vektor, um damit zu arbeiten
        non_zero = np.where(spalten_vec != 0)[0]    # zählt, wo nicht null ist. Damit muss an der Stelle dann gefüllt werden

        if non_zero.size == 0:                      # 
            zeile = self.spielfeld.shape[0]-1
            self.spielfeld[zeile,spalte] = spieler

        else:                                       # 
            zeile = non_zero[0]-1
            self.spielfeld[zeile,spalte] = spieler


        if self._winning_check(zeile, spalte):
            return 1
        else:
            return self.spielfeld
        

    def reset(self):                                # setzt das Spielfeld zurück
        return self.table.fill(0)
