from machine import Pin
from neopixel import NeoPixel
from ulab import numpy as np
import time
import spiellogik

anzahlPixel = 6*7


# Zustände
ZUSTAND_INIT = "init"
ZUSTAND_SPIELER_WAHELEN = "spieler_waehlen"
ZUSTAND_SPIELEN = "spielen"
ZUSTAND_GEWONNEN = "gewonnen"

aktueller_zustand = ZUSTAND_INIT


naechsterSpieler = {"spieler1" : "spieler2", "spieler2" : "spieler1"}
status = {"spieler" : "spieler1"}

farbe_spieler = {"spieler1" : 0, "spieler2" : 0}



#### Touch Sensoren
# Pin 0, 2, 4, 12, 13 14, 15, 27, 32, 33
# Eingang gegen 0 --> gedrückt. Eingang über 1000 --> nicht gedrückt

#touch_schwelle = 600


#eingang_touch_0 = TouchPad(Pin(15)) 
#eingang_touch_1 = TouchPad(Pin(2))
#eingang_touch_2 = TouchPad(Pin(4))
#eingang_touch_3 = TouchPad(Pin(12))
#eingang_touch_4 = TouchPad(Pin(13))
#eingang_touch_5 = TouchPad(Pin(14)) 
#eingang_touch_6 = TouchPad(Pin(15)) 

#### Ende Touch Sensoren

### Taster

# TODO: Pin Zuordnung prüfen

eingang_0 = Pin(15, Pin.IN, Pin.PULL_UP) 
eingang_1 = Pin(2, Pin.IN, Pin.PULL_UP)
eingang_2 = Pin(4, Pin.IN, Pin.PULL_UP)
eingang_3 = Pin(12, Pin.IN, Pin.PULL_UP)
eingang_4 = Pin(13, Pin.IN, Pin.PULL_UP)
eingang_5 = Pin(14, Pin.IN, Pin.PULL_UP)
eingang_6 = Pin(16, Pin.IN, Pin.PULL_UP)

### Zeitvariablen für Taster zum entprellen

vergangene_zeit = 0
button_delay = 30 # ms

### Ende Taster



#### Neo Pixel
pixel_pin = Pin(0, Pin.OUT)   # GPIO0 als Ausgang für NeoPixel
pixel = NeoPixel(pixel_pin, anzahlPixel, bpp=4) # Farbmodell anpassen   

#### Ende Neo Pixel


### Funktion zum Entprellen
#def button_handler(pin):
#    global vergangene_zeit, button_delay
    
#    if time.ticks_ms() < vergangene_zeit:
#        return
   
#    vergangene_zeit = time.ticks_ms() + button_delay




farbe_spieler["spieler2"] = pixel.colorHSV(0, 255, 255) # rot
farbe_spieler["spieler1"] = pixel.colorHSV(43691, 255, 255) # blau

spielfeld = spiellogik.Spielffeld()

def update_neopixel():
    # array zerlegen
    ausgabe = spielfeld.spielfeld.flatten() # macht reihenweise, also erst oberste reihe, dann zweite hintendran usw.

    # Wenn Wert gleich 1 --> Farbe spieler 1
    x = np.where(ausgabe == 1)
    for index in x:
        pixel[index] = farbe_spieler["spieler1"]
    

    # Wenn Wert gleich 2 --> Farbe spieler 2
    x = np.where(ausgabe == 2)
    for index in x:
        pixel[index] = farbe_spieler["spieler2"]

    
    # pixel senden
    pixel.write()

    return

def reset_matrix():

    spielfeld.reset()

    pixel.fill(0)
    pixel.write()

    return


def get_player_color(): # lässt Spieler die eigene Farbe definieren

    hue = 0
    farbe = pixel.colorHSV(hue, 255, 255) 
    pixel.fill(farbe)
    pixel.write()

    while(eingang_touch_0 > touch_schwelle and eingang_touch_5 > touch_schwelle):  # beide ganz außen gleichzeitig drücken zum starten
        if eingang_touch_1 < touch_schwelle: # zweites von links geklick, hue -
            hue -= 500

            # fake "Overflow", Python kennt keine maximallänge bei Int
            if hue < 0:
                hue = 65535

            farbe = pixel.colorHSV(hue, 255, 255) 
            pixel.fill(farbe)
            pixel.write()

        elif eingang_touch_4 < touch_schwelle: # zweites von rechts geklick, hue +
            hue += 500
            
            # fake "Overflow", Python kennt keine maximallänge bei Int
            if hue > 65535:
                hue = 0

            farbe = pixel.colorHSV(hue, 255, 255) 
            pixel.fill(farbe)
            pixel.write()

    reset_matrix()

    return farbe


def get_spalte():

    global button_delay

    spalte = -1

    while spalte == -1:
        if eingang_0.value() == 0:
            spalte = 0
        elif eingang_1.value() == 0:
            spalte = 1
        elif eingang_2.value() == 0:
            spalte = 2
        elif eingang_3.value() == 0:
            spalte = 3
        elif eingang_4.value() == 0:
            spalte = 4
        elif eingang_5.value() == 0:
            spalte = 5
        elif eingang_6.value() == 0:
            spalte = 6

    time.sleep(button_delay)  # warte die Zeit, um zu entprellen
    # TODO: Bessere Entrpellung als per delay

    return spalte


def spielzug() -> bool:
    spieler = status["spieler"]     # wer ist dran?

    # warte auf Eingabe einer Spalte
    gespielte_spalte = get_spalte()

    # übergib Spalte an Spiellogik

    ergebnis = spielfeld.wurf(spieler, gespielte_spalte)

    update_neopixel()

    # prüfe ob gewonnen

    if (ergebnis == 1):
        # aktueller Spieler hat gewonnen
        time.sleep(1000)

        pixel.fill(farbe_spieler[spieler])
        pixel.write()

        return True


    else:
        # nicht gewonnen -> nächster spieler
        status["spieler"] = naechsterSpieler[spieler]

    return False



def naechstesSpiel():
    global button_delay
    # warte auf Eingabe und starte erneut

    while eingang_0.value() != 0 and eingang_6.value() != 0:

        time.sleep(button_delay)

    while eingang_0.value() == 0 and eingang_6.value() == 0: # warte bis beide Taster wieder gelöst sind
        time.sleep(button_delay)

    return


def main():
    global aktueller_zustand
    global farbe_spieler

    while 1:
        if aktueller_zustand == ZUSTAND_INIT:
            reset_matrix()
            aktueller_zustand = ZUSTAND_SPIELER_WAHELEN

        elif aktueller_zustand == ZUSTAND_SPIELER_WAHELEN:
            # spieler wählen Farbe

            # TODO: farben einlesen

            #farbe_spieler["spieler1"] = get_player_color()
            #farbe_spieler["spieler2"] = get_player_color()

            # spieler wählen PvP oder PvE
            # TODO:

            aktueller_zustand = ZUSTAND_SPIELEN
        
        elif aktueller_zustand == ZUSTAND_SPIELEN:
            
            if spielzug():  # True wenn gewonnen, sonst false
                aktueller_zustand = ZUSTAND_GEWONNEN

        elif aktueller_zustand == ZUSTAND_GEWONNEN:
            naechstesSpiel()
            aktueller_zustand = ZUSTAND_INIT

if __name__ == "__main__":
    main()