import board

# GPIO-Pins für die Taster
TASTER_PINS = [17, 27, 22, 23, 24, 5, 25] # letzter Taster ist vertauscht angelötet.

# LED-Konfiguration (z.B. für NeoPixel)
LED_PIN = board.D18  # GPIO18 (Pin 12) für NeoPixel
NUM_LEDS = 42  # Anzahl der LEDs

# Long-Press Dauer (in Sekunden)
LONG_PRESS_TIME = 3