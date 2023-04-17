from machine import Pin, TouchPad
from neopixel import NeoPixel
from ulab import numpy as np

#### allgemeine Definitionen

anzahlReihen = 6
anzahlPixel = anzahlReihen*7

#### Touch Sensoren
# Pin 0, 2, 4, 12, 13 14, 15, 27, 32, 33
# Eingang gegen 0 --> gedrückt. Eingang über 1000 --> nicht gedrückt

touch_schwelle = 600


eingang_touch_0 = TouchPad(Pin(15)) 
eingang_touch_1 = TouchPad(Pin(2))
eingang_touch_2 = TouchPad(Pin(4))
eingang_touch_3 = TouchPad(Pin(12))
eingang_touch_4 = TouchPad(Pin(13))
eingang_touch_5 = TouchPad(Pin(14)) 

#### Ende Touch Sensoren

#### Neo Pixel

pixel_pin = Pin(0, Pin.OUT)   # GPIO0 als Ausgang für NeoPixel
pixel = NeoPixel(pixel_pin, anzahlPixel, "GRB") # Farbmodell anpassen   


#### Ende Neo Pixel




farbe_spieler_1 = pixel.colorHSV(0, 255, 255) # rot
farbe_spieler_2 = pixel.colorHSV(43691, 255, 255) # blau


spielfeld = np.zeros(6, 7, dtype=int)


def update_neopixel():
    # array zerlegen
    ausgabe = spielfeld.flatten() # macht reihenweise, also erst oberste reihe, dann zweite hintendran usw.

    # Wenn Wert gleich 1 --> Farbe spieler 1
    x = np.where(ausgabe == 1)
    for index in x:
        pixel[index] = farbe_spieler_1
    

    # Wenn Wert gleich 2 --> Farbe spieler 2
    x = np.where(ausgabe == 2)
    for index in x:
        pixel[index] = farbe_spieler_2

    
    # pixel senden
    pixel.write()

    return

def reset_matrix():

    # TODO Spielfeld darf nicht schwarz sein, da man das durch das Plexiglas nicht sieht. Vorschlag: Grau oder Weiß

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


def init_game():

    # alles zurücksetzten

    reset_matrix()
    spielfeld = np.zeros(6, 7, dtype=int)

    # farben einlesen
    
    farbe_spieler_1 = get_player_color()
    farbe_spieler_2 = get_player_color()

    # start Game


    # end game



    return