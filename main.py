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


naechsterSpieler = {1 : -1, -1 : 1}   # {"spieler1" : "spieler2", "spieler2" : "spieler1"}
status = {"spieler" : 1}

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

eingang_0 = Pin(2, Pin.IN, Pin.PULL_UP) 
eingang_1 = Pin(4, Pin.IN, Pin.PULL_UP)
eingang_2 = Pin(12, Pin.IN, Pin.PULL_UP)
eingang_3 = Pin(13, Pin.IN, Pin.PULL_UP)
eingang_4 = Pin(14, Pin.IN, Pin.PULL_UP)
eingang_5 = Pin(15, Pin.IN, Pin.PULL_UP)
eingang_6 = Pin(16, Pin.IN, Pin.PULL_UP)

### Zeitvariablen für Taster zum entprellen

vergangene_zeit = 0
button_delay = 0.03 # 30 ms

### Ende Taster



#### Neo Pixel
#pixel_pin = Pin(0, Pin.OUT)   # GPIO0 als Ausgang für NeoPixel
pixel = NeoPixel(Pin(0), anzahlPixel, bpp=4) # 4 Bytes pro Pixel (RGBW) 

#### Ende Neo Pixel


def wheel(pos):
  #Input a value 0 to 255 to get a color value.
  #The colours are a transition r - g - b - back to r.
  if pos < 0 or pos > 255:
    return (0, 0, 0, 0)
  if pos < 85:
    return (255 - pos * 3, pos * 3, 0, 30)
  if pos < 170:
    pos -= 85
    return (0, 255 - pos * 3, pos * 3, 30)
  pos -= 170
  return (pos * 3, 0, 255 - pos * 3, 30)



#farbe_spieler = [(0, 0, 255, 20), (255, 0, 0, 80)] # Farben für Spieler 1 und 2, nicht mehr benötigt, da Spieler Farbe selbst wählt


spielfeld = spiellogik.Spielfeld()

def update_neopixel(ergebnis):
    # array zerlegen
    ausgabe = ergebnis.flatten() # macht reihenweise, also erst oberste reihe, dann zweite hintendran usw.

    #print("Ergebnis flattend: ", ausgabe)

    # Wenn Wert gleich 1 --> Farbe spieler 1

    # TODO: Schöner
    i = 0
    for index in ausgabe:
        if index == 1:
            pixel[i] = farbe_spieler[0]
        elif index == -1:
            pixel[i] = farbe_spieler[1]
        i = i+1
    
    # pixel senden
    pixel.write()

    return

def reset_matrix():
    global anzahlPixel

    spielfeld.reset()

    for i in range(anzahlPixel):
        pixel[i] = (0, 0, 0, 0) # alle Pixel aus

    pixel.write()

    return


def get_player_color(): # lässt Spieler die eigene Farbe definieren
    global button_delay, anzahlPixel

    #hue = 0
    #farbe = pixel.colorHSV(hue, 255, 255) 
    #pixel.fill(farbe)
    #pixel.write()

    hue = 0


    # beide ganz außen gleichzeitig drücken zum starten
    while (eingang_0.value() != 0) or (eingang_6.value() != 0):
        time.sleep(button_delay)



    

        if eingang_1.value() == 0: # zweites von links geklick
            hue = hue-5


            # fake "Overflow", Python kennt keine maximallänge bei Int
            if hue < 0:
                hue = 255

    #        farbe = pixel.colorHSV(hue, 255, 255) 
    #        pixel.fill(farbe)
    #        pixel.write()

        elif eingang_5.value() == 0: # zweites von rechts geklick, hue +
            hue = hue+5
            
            # fake "Overflow", Python kennt keine maximallänge bei Int
            if hue > 255:
                hue = 0

    #        farbe = pixel.colorHSV(hue, 255, 255) 
    #        pixel.fill(farbe)
    #        pixel.write()
            
        farbe = wheel(hue)

        for i in range(anzahlPixel):
            pixel[i] = farbe

        pixel.write()
        
    while (eingang_0.value() == 0) or (eingang_6.value() == 0): # warte bis beide Taster wieder gelöst sind
        time.sleep(button_delay)

    reset_matrix()

    #return farbe
    return farbe


def get_spalte():

    global button_delay

    spalte = -1

    while spalte == -1:
        if eingang_0.value() == 0:
            spalte = 0
            time.sleep(button_delay)
            while eingang_0.value() == 0:
                time.sleep(button_delay)

        elif eingang_1.value() == 0:
            spalte = 1
            time.sleep(button_delay)
            while eingang_1.value() == 0:
                time.sleep(button_delay)

        elif eingang_2.value() == 0:
            spalte = 2
            time.sleep(button_delay)
            while eingang_2.value() == 0:
                time.sleep(button_delay)

        elif eingang_3.value() == 0:
            spalte = 3
            time.sleep(button_delay)
            while eingang_3.value() == 0:
                time.sleep(button_delay)

        elif eingang_4.value() == 0:
            spalte = 4
            time.sleep(button_delay)
            while eingang_4.value() == 0:
                time.sleep(button_delay)

        elif eingang_5.value() == 0:
            spalte = 5
            time.sleep(button_delay)
            while eingang_5.value() == 0:
                time.sleep(button_delay)

        elif eingang_6.value() == 0:
            spalte = 6
            time.sleep(button_delay)
            while eingang_6.value() == 0:
                time.sleep(button_delay)
            
        time.sleep(0.01) #10 ms

    time.sleep(button_delay)  # warte die Zeit, um zu entprellen

        
    # TODO: Bessere Entprellung als per delay

    return spalte


def spielzug() -> bool:
    global anzahlPixel, farbe_spieler

    spieler = status["spieler"]     # wer ist dran?

    # warte auf Eingabe einer Spalte
    gespielte_spalte = get_spalte()

    print("Gespielte Spalte: ", gespielte_spalte)

    # übergib Spalte an Spiellogik

    ergebnis = spielfeld.wurf(spieler, gespielte_spalte)

    print("Ergebnis: ", ergebnis)

    

    # prüfe ob gewonnen

    if ergebnis[1] == 1:
        # aktueller Spieler hat gewonnen

        # mache alles aus
        for i in range(anzahlPixel):
            pixel[i] = (0, 0, 0, 0) # alle Pixel aus
        pixel.write()

        # jetzt nur noch die Gewinnerzellen anmachen
        update_neopixel(ergebnis[0])

        #warte kurz
        time.sleep(2)

        # und setzte alles auf die Gewinnerfarbe
        for i in range(anzahlPixel):
            pixel[i] = farbe_spieler[spieler-1]
            pixel.write()
            time.sleep(0.03)
        return True

    elif ergebnis[1] == -1:
        # spalte schon voll, nochmal neu

        # lasse die spalte nun 3 mal blinken
        for z in range(3):
            for i in range(6):
                pixel[gespielte_spalte+7*i] = (0, 0, 0, 0) # alle Pixel aus
                print(i*gespielte_spalte)	
            pixel.write()
            time.sleep(0.3)
            update_neopixel(ergebnis[0])
            time.sleep(0.3)

        return False
    
    elif ergebnis[1] == -2:
        # unentschieden

        # lasse von oben nach unten alle Pixel verscwinden
        for i in range(6):
            for j in range(7):
                pixel[j+7*i] = (0, 0, 0, 0) # alle Pixel aus

        return True

    else:
        # nicht gewonnen -> nächster spieler
        update_neopixel(ergebnis[0])
        status["spieler"] = naechsterSpieler[spieler]

    return False



def naechstesSpiel():
    global button_delay
    # warte auf Eingabe und starte erneut

    while (eingang_0.value() != 0) or (eingang_6.value() != 0):
        time.sleep(button_delay)

    while (eingang_0.value() == 0) or (eingang_6.value() == 0): # warte bis beide Taster wieder gelöst sind
        time.sleep(button_delay)

    return


def main():
    global aktueller_zustand
    global farbe_spieler

    while True:
        print(aktueller_zustand)
        if aktueller_zustand == ZUSTAND_INIT:
            reset_matrix()
            aktueller_zustand = ZUSTAND_SPIELER_WAHELEN

        elif aktueller_zustand == ZUSTAND_SPIELER_WAHELEN:
            # spieler wählen Farbe

            # TODO: farben einlesen

            farbe_spieler[0] = get_player_color()
            farbe_spieler[1] = get_player_color()

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