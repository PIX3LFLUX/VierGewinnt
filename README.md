# VierGewinnt

## Projektbeschreibung

Dies ist eine Implementierung des Spiels '4-Gewinnt' auf einer LED Matrix im Rahmen einer Projektarbeit an der Hochschule Karlsruhe. Die einzelnen Spalten werden über Taster ausgewählt. Die Außenmaße der dargestellten Lösung betragen circa 1 m x 1 m.

## Was wird benötigt

Beschreibung | Menge | Kosten
-------- | -------- | --------
ESP32S3 Dev Board   | 1   | ca. 10 €
LEDs (WS2812b / Neopixel)   | 42 LEDs   | ca. 15 €
opakes Acrylglas (2 mm) | 1 m x 1 m | ca. 20 €
Rahmenholz 12 cm x 1.8 cm | ca. 4 lfd m | ca x €
KG Wasserrohr 125 mm | ca. 3 m | 12 €
Rückplatte aus Sperrholz / Spahnplatte | 1 m x 1 m | ca. 25 €
Schrauben, Kleber, Winkel | - | - 
5V Netzteil (min. 3 A) | - | -
Kabel | | 

Werkzeuge wie Säge, Akkuschrauber und Lötkolben sollten natürlich ebenfalls vorhanden sein.

Das Rohr wirkt als Begrenzung des Lichts, damit der Spielstein später als rund gesehen wird. Anhand des Durchmessers lässt sich die Gesamtgröße des Spiels definieren.
Als Rückplatte haben wir zwei Möbelbauplatten (100 cm x 60 cm) verwendet, diese verwinden sich nicht und reflektieren dank ihrer weißen Beschichtung das Licht sehr gut.
Als LED Streifen haben wir einen Adafruit Neopixel RGBW Streifen verwendet. Durch beimischen der weißen LED lässt sich ein helleres Licht erzeugen.
Die Taster wurden auf Unterlegscheiben festgeschraubt, welche mit Silikon in einem passenden Loch verklebt wurden.

## Bau der Hardware
Wir sind wie folgt vorgegangen:
1. einzelne LED vom Strip abschneiden und mit 3 Kabeln verbinden. Wir haben jeweils 7 LEDs in einen String verbunden. Auf Aus- / Eingang der LEDs achten! Der Ausgang der letzten LED wird in den Eingang der nächsten Reihe angelötet. Wichtig ist dabei, dass alle Eingänge auf der linken Seite beginnen! _TODO Bild_
2. KG-Rohr in 3 - 4 cm starke Abschnitte teilen (42 Stück)
3. Rohrstücken mit Heißkleber zu einer 6x7 Matrix verbinden
4. Rückplatte auf Maße der Matrix zusenden ![Bilder](/bilder/_DSF9839.JPG?raw=true "Bild1")
5. LEDs auf Rückplatte aufkleben (wir haben extra starkes Doppelseitiges Klebeband verwendet) 
6. Alle Strings verbinden. 5V und Masse an einem Ende jedes Strings anlöten. Damit sind nun die Stromversorgungen jedes Strings parallel, die Daten jedoch alle in Reihe geschalten ![Bilder](/bilder/_DSF9842.JPG?raw=true "Bild1")
7. Rahmen um die Rückplatte herum bauen. Wir haben zum einschieben der Plexiglasplatte mit einem 3 mm Sägeblatt und der Kreissäge eine ca. 8 mm tiefe Nut in die Rahmenhölzer eingelassen. In die obere Rahmenseite die 7 Taster einlassen.
8. Plexiglasplatte auf Maß bringen, sie muss rundum ca. 5 mm größer als die Rückplatte sein
9. Plexiglasplatte in die Nut einlassen, Rahmen verkleben ![Bilder](/bilder/_DSF9845.JPG?raw=true "Bild1")
10. Rohrmatrix von hinten einlassen
11. Rückwand mit LEDS von hinten einlassen und mit Winkeln gegen ein Rausfallen sichern.




| Beschreibung         | Link                                                                                                                                                                                                                                                                                                                                                                                                             | Bild                                                                                                                         | Preis | Anzhal      |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ----- | ----------- |
| LED Streifen WS2812b | https://www.amazon.de/BTF-LIGHTING-WS2812B-adressierbare-Streifen-Wasserdicht/dp/B01CDTEBKA/ref=sr_1_7?crid=244G4JRW9ZBJ7&keywords=ws2812b+30+led%2Fm&qid=1680710500&sprefix=ws2812b+%2Caps%2C112&sr=8-7https://www.amazon.de/BTF-LIGHTING-WS2812B-adressierbare-Streifen-Wasserdicht/dp/B01CDTEBKA/ref=sr_1_7?crid=244G4JRW9ZBJ7&keywords=ws2812b+30+led%2Fm&qid=1680710500&sprefix=ws2812b+%2Caps%2C112&sr=8-7 | <img title="" src="file:///C:/Users/lucas/AppData/Roaming/marktext/images/2023-04-05-18-27-04-image.png" alt="" width="111"> | 28    | 1 (42 Leds) |
| ESP 32               | https://www.amazon.de/AZDelivery-NodeMCU-Development-Nachfolgermodell-ESP8266/dp/B071P98VTG/ref=sr_1_1_sspa?__mk_de_DE=ÅMÅŽÕÑ&crid=UIGUY09EZS7N&keywords=esp32&qid=1680710547&sprefix=esp32%2Caps%2C118&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1                                                                                                                                                         | ![](C:\Users\lucas\AppData\Roaming\marktext\images\2023-04-05-18-28-05-image.png)                                            | 11,29 | 1           |
| Acryglas             | https://www.amazon.de/AtHaus®-Acrylglas-Materialstärke-Milchglas-Plexiglas/dp/B09J3RZKYG/ref=sr_1_11?keywords=plexiglas%2Bmilchig%2B3mm&qid=1680710575&sprefix=plexiglas%2Bmil%2Caps%2C130&sr=8-11&th=1                                                                                                                                                                                                          | ![](C:\Users\lucas\AppData\Roaming\marktext\images\2023-04-05-18-29-53-image.png)                                            | 10    | 1           |
| Rahmenholz           | https://www.bauhaus.info/latten-rahmen/rahmenholz/p/20756143                                                                                                                                                                                                                                                                                                                                                     | ![](C:\Users\lucas\AppData\Roaming\marktext\images\2023-04-05-18-31-22-image.png)                                            | 15    | 1 (1,8 lfm) |
| Sperrholzplatte      | https://www.bauhaus.info/sperrholzplatten/sperrholzplatte-fixmass/p/14454573                                                                                                                                                                                                                                                                                                                                     | ![](C:\Users\lucas\AppData\Roaming\marktext\images\2023-04-05-18-32-34-image.png)                                            | 11    | 1           |

Ein alltes Handynetzteil für die Stromversorgung wird als vorhanden angebommen. 

## Wie man das projekt nuzt



ESP32 mit Micropython

Visual Studio Code mit pymakr

Zunächst muss die Hardware Gebaut werden. Mehr dazu folgt...


## Einkaufsliste



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

![Bilder](/bilder/_DSF9838.JPG?raw=true "Bild1")



![Bilder](/bilder/_DSF9840.JPG?raw=true "Bild1")



![Bilder](/bilder/_DSF9843.JPG?raw=true "Bild1")
![Bilder](/bilder/_DSF9844.JPG?raw=true "Bild1")


![Bilder](/bilder/_DSF9847.JPG?raw=true "Bild1")
