import time
import neopixel
import threading
from config import LED_PIN, NUM_LEDS

class Display:
    def __init__(self):
        # LED_PIN und NUM_LEDS werden aus config.py importiert
        self.num_leds = NUM_LEDS
        self.pixels = neopixel.NeoPixel(LED_PIN, NUM_LEDS, brightness=1, auto_write=False, pixel_order=neopixel.RGBW)
        self.rainbow_active = False  # Flag, das den Status der Regenbogenanimation speichert
        self.rainbow_thread = None
        self.clear()

    def clear(self):
        """Alle LEDs ausschalten."""
        self.pixels.fill((0, 0, 0, 0))  # RGBW auf 0 setzen
        self.pixels.show()

    def set_led(self, row, col, color):
        """Setzt eine bestimmte LED basierend auf Zeile und Spalte auf eine bestimmte Farbe."""
        index = row * 7 + col  # Berechne den Index basierend auf Zeile und Spalte
        if 0 <= index < self.num_leds:
            self.pixels[index] = color

    def update_player_selection_display(self, player, player_type):
        """Aktualisiert das Display für die Spielerwahl."""
        if player == 1:
            # Spieler 1 in Zeile 3, Spalte 3 (rot für Spieler 1)
            self.set_led(2, 2, (0, 255, 0, 0))  # Rot
            # Grün oder Blau abhängig von der Auswahl
            self.set_led(3, 2, (255, 0, 0, 0) if player_type == "Mensch" else (0, 0, 255, 0))  # Grün für Mensch, Blau für KI
        elif player == 2:
            # Spieler 2 in Zeile 3, Spalte 5 (gelb für Spieler 2)
            self.set_led(2, 4, (255, 255, 0, 0))  # Gelb
            # Grün oder Blau abhängig von der Auswahl
            self.set_led(3, 4, (0, 0, 255, 0) if player_type == "Mensch" else (0, 0, 255, 0))  # Grün für Mensch, Blau für KI
        self.pixels.show()  # Aktualisiere das Display

    def update_board(self, board_state):
        """Aktualisiert das LED Display nach jedem Spielzug."""
        # Übersetze die Werte des Spielfelds in die Farben für die NeoPixel
        pixel_data = []
        
        # Richtig zugewiesene Farben für die Spieler (RGBW)
        farbe_spieler = {
            1: (0, 255, 0, 0),   # Spieler 1: Rot (RGB, kein Weißanteil)
            -1: (255, 255, 0, 0)  # Spieler 2: Gelb (RGB, kein Weißanteil)
        }
        
        for row in board_state:
            for cell in row:
                if cell == 1:
                    pixel_data.append(farbe_spieler[1])  # Farbe für Spieler 1
                elif cell == -1:
                    pixel_data.append(farbe_spieler[-1])  # Farbe für Spieler 2
                else:
                    pixel_data.append((0, 0, 0, 0))  # Leere Felder (ausgeschaltet)

        # Übergebe die Farbe-Daten an das Display
        self.update_board_with_colors(pixel_data)

    def update_board_with_colors(self, pixel_data):
        """Übergebe die Farben an die NeoPixel und zeige sie an."""
        for i, color in enumerate(pixel_data):
            self.pixels[i] = color  # Setze jede LED auf die entsprechende Farbe
        self.pixels.show()

    def rainbow_cycle(self, wait):
        """Interne Methode, die die Regenbogenanimation durchführt."""
        while self.rainbow_active:  # Animation läuft nur, solange rainbow_active True ist
            for j in range(255):
                if not self.rainbow_active:  # Prüfen, ob die Animation gestoppt wurde
                    break
                for i in range(self.num_leds):
                    pixel_index = (i * 256 // self.num_leds) + j
                    self.pixels[i] = self.wheel(pixel_index & 255)
                self.pixels.show()
                time.sleep(wait)

    def rainbow_start(self, wait=0.01):
        """Startet die Regenbogenanimation."""
        if not self.rainbow_active:
            self.rainbow_active = True
            self.rainbow_thread = threading.Thread(target=self.rainbow_cycle, args=(wait,))
            self.rainbow_thread.start()

    def rainbow_stop(self):
        """Stoppt die Regenbogenanimation."""
        if self.rainbow_active:
            self.rainbow_active = False
            if self.rainbow_thread is not None:
                self.rainbow_thread.join()  # Warten, bis der Thread beendet ist
            self.clear()  # LEDs nach dem Stop der Animation ausschalten

    def wheel(self, pos):
        """Erzeugt Farben über einen Farbrad-Wert (0-255) mit RGBW-Format."""
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0, 0)  # RGB und Weißkanal ist 0
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3, 0)  # RGB und Weißkanal ist 0
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3, 0)  # RGB und Weißkanal ist 0