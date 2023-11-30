# VierGewinnt

## Projektbeschreibung

Dies ist das Spiel '4-Gewinnt' auf einer LED Matrix mit Touchbedienung als Projektarbeit an der Hochschule Karlsruhe.

#Todo: Was tut das Programm

## Wie man das projekt nuzt

ESP32 mit Micropython

Visual Studio Code mit pymakr

Zunächst muss die Hardware Gebaut werden. Mehr dazu folgt...

## Todo

Idee: jeder spieler wählt seine Farbe, HSV und Hue durch die äußeren Touch sensoren verändern

## Einkaufsliste

| Beschreibung         | Link                                                                                                                                                                                                                                                                                                                                                                                                             | Bild                                                                                                                         | Preis | Anzhal      |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ----- | ----------- |
| LED Streifen WS2812b | https://www.amazon.de/BTF-LIGHTING-WS2812B-adressierbare-Streifen-Wasserdicht/dp/B01CDTEBKA/ref=sr_1_7?crid=244G4JRW9ZBJ7&keywords=ws2812b+30+led%2Fm&qid=1680710500&sprefix=ws2812b+%2Caps%2C112&sr=8-7https://www.amazon.de/BTF-LIGHTING-WS2812B-adressierbare-Streifen-Wasserdicht/dp/B01CDTEBKA/ref=sr_1_7?crid=244G4JRW9ZBJ7&keywords=ws2812b+30+led%2Fm&qid=1680710500&sprefix=ws2812b+%2Caps%2C112&sr=8-7 | <img title="" src="file:///C:/Users/lucas/AppData/Roaming/marktext/images/2023-04-05-18-27-04-image.png" alt="" width="111"> | 28    | 1 (42 Leds) |
| ESP 32               | https://www.amazon.de/AZDelivery-NodeMCU-Development-Nachfolgermodell-ESP8266/dp/B071P98VTG/ref=sr_1_1_sspa?__mk_de_DE=ÅMÅŽÕÑ&crid=UIGUY09EZS7N&keywords=esp32&qid=1680710547&sprefix=esp32%2Caps%2C118&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1                                                                                                                                                         | ![](C:\Users\lucas\AppData\Roaming\marktext\images\2023-04-05-18-28-05-image.png)                                            | 11,29 | 1           |
| Acryglas             | https://www.amazon.de/AtHaus®-Acrylglas-Materialstärke-Milchglas-Plexiglas/dp/B09J3RZKYG/ref=sr_1_11?keywords=plexiglas%2Bmilchig%2B3mm&qid=1680710575&sprefix=plexiglas%2Bmil%2Caps%2C130&sr=8-11&th=1                                                                                                                                                                                                          | ![](C:\Users\lucas\AppData\Roaming\marktext\images\2023-04-05-18-29-53-image.png)                                            | 10    | 1           |
| Rahmenholz           | https://www.bauhaus.info/latten-rahmen/rahmenholz/p/20756143                                                                                                                                                                                                                                                                                                                                                     | ![](C:\Users\lucas\AppData\Roaming\marktext\images\2023-04-05-18-31-22-image.png)                                            | 15    | 1 (1,8 lfm) |
| Sperrholzplatte      | https://www.bauhaus.info/sperrholzplatten/sperrholzplatte-fixmass/p/14454573                                                                                                                                                                                                                                                                                                                                     | ![](C:\Users\lucas\AppData\Roaming\marktext\images\2023-04-05-18-32-34-image.png)                                            | 11    | 1           |

Ein alltes Handynetzteil für die Stromversorgung wird als vorhanden angebommen. 

Gesamtkosten ca. 75-80 Euro ohne versand.

## Weitere Ressourcen

- [Touch Sensor - ESP32 - &mdash; ESP-IDF Programming Guide latest documentation](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/touch_pad.html)

- [Micropython ESP Handbuch](https://docs.micropython.org/en/latest/esp32/quickref.html#neopixel-and-apa106-driver)

- [ESP32 einrichten in VSCODE](https://draeger-it.blog/visual-studio-code-fuer-micropython-einrichten/)

- [GitHub - v923z/micropython-ulab: a numpy-like fast vector module for micropython, circuitpython, and their derivatives](https://github.com/v923z/micropython-ulab)

## Mircopython aufsetzten

Micropython mit ulab ist wie Numpy nur für Mircocontroller. Einen fertig compilierten Build gibt es im Ordner ``firmware``.

Zum selber erstellen wird wie folgt vorgegangen: 

Zunächst wird ein Ordner angelegt, welcher kein Leerzeichen enthaten darf:

```bash
mkdir micropython-ulab && cd micropython-ulab
```

Folgender Code funktioniert unter Unix Systemen, es muss jedoch ``CMake > 3.12`` installiert sein:

```bash
export BUILD_DIR=$(pwd)

git clone https://github.com/v923z/micropython-ulab.git ulab
git clone https://github.com/micropython/micropython.git

cd $BUILD_DIR/micropython/

git clone -b v4.2.1 --recursive https://github.com/espressif/esp-idf.git


cd esp-idf
./install.sh
. ./export.sh
```

Damit werden die benötigten Abhängigkeiten heruntergeladen und die ESP-IDF installiert. 

Anschließend wird der micropython cross-compiler und die ESP Submodule erstellt:

```bash
cd $BUILD_DIR/micropython/mpy-cross
make
cd $BUILD_DIR/micropython/ports/esp32
make submodules
```

Im Verzeichnis ``$BUILD_DIR/micropython/ports/esp32`` wird das alte ``Makefile `` gespeichert: 

```bash
mv Makefile MakefileOld
```

 Ein neues Makefile mit folgendem Inhalt wird erstellt und mit ``make`` ausgeführt:

```bash
BOARD = GENERIC
USER_C_MODULES = $(BUILD_DIR)/ulab/code/micropython.cmake

include MakefileOld
```

```bash
make
```

Es wird ein neues Verzeichnis ``build`` erstellt, aus dem die Dateien ``bootloader.bin``, ``partition-table.bin`` und ``micropython.bin`` kopiert werden.

Anschließend wird mit ``esptool `` der ESP Flash bereinigt und die neue Firmware auf den ESP geflashed:

```bash
esptool.py -p (PORT) erase_flash

esptool.py -p (PORT) -b 460800 --before default_reset --after hard_reset --chip esp32  write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x1000 bootloader.bin 0x8000 partition-table.bin 0x10000 micropython.bin

```





## Bilder

![_DSF9845.JPG](C:\Users\cedri\Uni\FH\Projektarbeit\kleineBilder\_DSF9845.JPG)

![_DSF9847.JPG](C:\Users\cedri\Uni\FH\Projektarbeit\kleineBilder\_DSF9847.JPG)

![_DSF9844.JPG](C:\Users\cedri\Uni\FH\Projektarbeit\kleineBilder\_DSF9844.JPG)

![_DSF9843.JPG](C:\Users\cedri\Uni\FH\Projektarbeit\kleineBilder\_DSF9843.JPG)

![_DSF9842.JPG](C:\Users\cedri\Uni\FH\Projektarbeit\kleineBilder\_DSF9842.JPG)

![_DSF9840.JPG](C:\Users\cedri\Uni\FH\Projektarbeit\kleineBilder\_DSF9840.JPG)

![_DSF9839.JPG](C:\Users\cedri\Uni\FH\Projektarbeit\kleineBilder\_DSF9839.JPG)

![_DSF9838.JPG](C:\Users\cedri\Uni\FH\Projektarbeit\kleineBilder\_DSF9838.JPG)