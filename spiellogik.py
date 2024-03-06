from ulab import numpy as np



# Gewinnmatrixen
#spieler1Vec = np.array([1,1,1,1], dtype=np.int8)
#spieler2Vec = np.array([2,2,2,2], dtype=np.int8)

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

        spalten_vec = self.spielfeld[:,spalte]      # kopiere die aktuelle Spalte in einen Vektor, um damit zu arbeiten
        non_zero = np.nonzero(spalten_vec)[0]       # zählt, wo nicht null ist. Damit muss an der Stelle dann gefüllt werden

        
        #print("Non_Zero: ", non_zero)
        #print("Non_Zero Size: ", non_zero.size)

        if non_zero.size == 0:                      
            zeile = self.spielfeld.shape[0]-1
            self.spielfeld[zeile,spalte] = spieler

        elif non_zero.size == 6:
            # spalte voll, nochmal spielen
            # TODO: Blinken lassen oder so
            return self.spielfeld, -1

        else:                                       
            zeile = non_zero[0]-1
            self.spielfeld[zeile,spalte] = spieler


        #if self._pruefe_gewonnen(zeile, spalte):
        pos, filter = self._pruefe_gewonnen(spieler)

        if pos: # es gibt einen Gewinner, pos ist nicht leer
            #print("Indizes: " , pos)
            # spielfeld mit filter an der position pos maskieren
            maskiertes_spiel = np.zeros((6,7), dtype=np.int8)

            maskiertes_spiel[pos[0]-filter.shape[0]+1:pos[0]+1, pos[1]-filter.shape[1]+1:pos[1]+1] = filter*spieler
            #print(maskiertes_spiel)

            return maskiertes_spiel, 1
        
        
        else: # kein Gewinner, weiter spielen
            check_spielfeld = self.spielfeld.copy()
            check_spielfeld.sort(axis=None)

            # prüfe ob spielfeld voll:
            if check_spielfeld[0] != 0:
                return self.spielfeld, -2
            
            # wenn nicht, weiter spielen
            return self.spielfeld, 0
      

    def reset(self):                                # setzt das Spielfeld zurück
        self.spielfeld = np.zeros((6,7), dtype=np.int8)
        return self.spielfeld
    
    def gib_spielfeld(self):
        return self.spielfeld
