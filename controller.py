import RPi.GPIO as GPIO
import time
from config import LONG_PRESS_TIME

class Controller:
    def __init__(self, taster_pins):
        self.taster_pins = taster_pins
        self.pressed_time = {pin: None for pin in self.taster_pins}  # Startzeit für Long-Press
        self.currently_pressed = {pin: False for pin in self.taster_pins}
        self.short_press_detected = {pin: False for pin in self.taster_pins}
        self.long_press_detected = {pin: False for pin in self.taster_pins}
        GPIO.setmode(GPIO.BCM)

        # Initialisiere Taster-Pins mit erhöhter Bouncetime
        for pin in self.taster_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.BOTH, callback=self.gpio_callback, bouncetime=100)  # Bouncetime

    def gpio_callback(self, channel):
        """Callback-Funktion für GPIO-Interrupt."""
        if GPIO.input(channel) == GPIO.LOW:
            # Taste wurde gedrückt (FALLING-Edge)
            # print(f"Taste {self.get_button_number(channel)} wurde gedrückt (FALLING).")
            self.pressed_time[channel] = time.time()
            self.currently_pressed[channel] = True
        else:
            # Taste wurde losgelassen (RISING-Edge)
            # print(f"Taste {self.get_button_number(channel)} wurde losgelassen (RISING).")
            if self.pressed_time[channel] is not None:
                elapsed_time = time.time() - self.pressed_time[channel]
                if elapsed_time >= LONG_PRESS_TIME:
                    # print(f"Long Press erkannt: Taste {self.get_button_number(channel)} (gehalten für {elapsed_time:.2f}s)")
                    self.long_press_detected[channel] = True
                else:
                    # print(f"Short Press erkannt: Taste {self.get_button_number(channel)} (gehalten für {elapsed_time:.2f}s)")
                    self.short_press_detected[channel] = True
                self.currently_pressed[channel] = False
                self.pressed_time[channel] = None  # Setze Zeit nach Loslassen zurück

    def get_button_number(self, pin):
        """Gibt die Tasternummer (1-7) basierend auf der Position in TASTER_PINS zurück."""
        return self.taster_pins.index(pin) + 1

    def get_short_press(self):
        """Gibt eine Liste von Tasten (1-7) zurück, die kurz gedrückt wurden."""
        short_press = []
        for pin, detected in self.short_press_detected.items():
            if detected:
                short_press.append(self.get_button_number(pin))
                self.short_press_detected[pin] = False  # Zurücksetzen nach Verarbeitung
        return short_press

    def get_long_press(self):
        """Gibt eine Liste von Tasten (1-7) zurück, die lange gedrückt wurden."""
        long_press = []
        for pin, detected in self.long_press_detected.items():
            if detected:
                long_press.append(self.get_button_number(pin))
                self.long_press_detected[pin] = False  # Zurücksetzen nach Verarbeitung
        return long_press