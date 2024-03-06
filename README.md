<div align="center">
  <h1 align="center">Vier Gewinnt</h1>
  <h3>Kinderspiel auf einer LED Matrix mit KI Gegner</h3>
</div>

  ![Bilder](/bilder/_DSF4458.jpg?raw=true "Titelbild")

Das ist eine Implementierung des Spiels '4-Gewinnt' mit einem KI Gegner auf einer LED Matrix im Rahmen einer Projektarbeit an der Hochschule Karlsruhe. Die einzelnen Spalten werden über Taster ausgewählt. Die Außenmaße der dargestellten Lösung betragen circa 1 m x 1 m.
Es gibt einen Modus PvP, PvE und EvE. Als KI Gegner wird ein Alpha-Beta Algorithmus verwendet.

## Features

- Spieler können Ihre Farbe auswählen

- Spieler können Player oder KI auswählen

- Diagonal, waagerecht und horizontal werden "4 in einer Reihe" erkannt.

- Wenn das Spielfeld voll ist, ohne das jemand gewonnen hat, wird das ebenfalls erkannt.

## Quick Start

Du benötigst folgendes, um das Spiel nachbauen zu können:

- ESP32 Microcontroller mit [https://micropython.org/](micropython)

- LED Matrix mit 42 Neopixel LEDs in RGBW (RGB geht auch, dann musst du aber die Funktionen umschreiben)

- Ausreichend großes Netzteil (5V / 4A)

Weiterhin sollte folgende Software vorhanden sein:

- Python 3

- esptool

- ggf. Putty o.Ä. zum Debuggen

### 1. Repository klonen

```shell
git clone https://github.com/SachsenBahner/VierGewinnt.git
cd VierGewinnt
```

### 2. Micropython auf das ESP 32 Board aufspielen

Zunächst muss die Notwendige Firmware (micropython mit ulab) auf den ESP Microcontroller geflasht werden. Sie kann aus dem Ordner `firmware` für einen ESP32S3 mit 32 MBit Speicher gedownloadet werden oder unter [Micropython aufsetzten](https://github.com/SachsenBahner/VierGewinnt?tab=readme-ov-file#mircopython-aufsetzten) selbst erstellt werden.

```shell
esptool.py -p (PORT) erase_flash

esptool.py -p /dev/ttyUSB0 -b 460800 --before default_reset --after no_reset --chip esp32s3 write_flash --flash_mode dio --flash_size 32MB --flash_freq 80m 0x0 firmware/bootloader.bin 0x8000 firmware/partition-table.bin 0x10000 firmware/micropython.bin
```

### 3. Pyboard & Pyserial installieren

```shell
wget https://github.com/micropython/micropython/blob/master/tools/pyboard.py
pip install pyserial
```

### 4. ESP 32 mit USB verbinden

### 5. Dateien übertragen

Öffne ein Terminal im Ordner `VierGewinnt`. Zum Übertragen der am PC erstellten Python Dateien empfiehlt sich das Pyboard Tool. Es werden die Dateien main.py, ki.py sowie spiellogik.py übetragen.

```shell
python pyboard.py --device (PORT) -f cp VierGewinnt/main.py :
python pyboard.py --device /dev/ttyUSB0 -f cp VierGewinnt/spiellogik.py :
python pyboard.py --device /dev/ttyUSB0 -f cp VierGewinnt/ki.py :

python pyboard.py --device /dev/ttyUSB0 -f ls

ls :
         139 boot.py
        6319 main.py
        4131 spiellogik.py
```

Mit einem `python pyboard.py --device /dev/ttyUSB0 main.py` kann das Programm ausgeführt werden. 

Nach einem neuen Boot des Boards führt sich das Programm ebenfalls automatisch aus. Es sollte vollständig rot leuchten, dann kann mit den zweiten Taster die Farbe gewechselt werden.

## Bedienung

- Farbe kann mit dem 2. Taster von links oder rechts jeweils im Farbspektrum verschoben werden
- Durch gleichzeitiges Drücken der Taster ganz außen lässt sich die Farbauswahl bestätigen oder nach einem Sieg / Unentschieden ein neues Spiel starten.
- Mit der gleichen Bedienung kann zwischen Player und KI gewählt werden

---

## Detailiertere Beschreibung

## Was wird benötigt

| Beschreibung                           | Menge       | Kosten   |
| -------------------------------------- | ----------- | -------- |
| ESP32S3 Dev Board                      | 1           | ca. 10 € |
| LEDs (WS2812b / Neopixel)              | 42 LEDs     | ca. 15 € |
| opakes Acrylglas (2 mm)                | 1 m x 1 m   | ca. 20 € |
| Rahmenholz 12 cm x 1.8 cm              | ca. 4 lfd m | ca x €   |
| KG Wasserrohr 125 mm                   | ca. 3 m     | 12 €     |
| Rückplatte aus Sperrholz / Spahnplatte | 1 m x 1 m   | ca. 25 € |
| Schrauben, Kleber, Winkel              | -           | -        |
| 5V Netzteil (min. 3 A)                 | -           | -        |
| Kabel                                  |             |          |

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

git clone -b v5.1.2 --recursive https://github.com/espressif/esp-idf.git


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

Wir haben das ESP32-S3-Devkit1 Board verwendet. Für dieses gibt es kein fertiges Board. Daher wurde die sdkconfig.board Datei im Ordner ``$BUILD_DIR/micropython/ports/esp32/ESP32_Generic_S3`` wie folgt angepasst:

```
CONFIG_ESPTOOLPY_FLASHMODE_QIO=y
CONFIG_ESPTOOLPY_FLASHFREQ_80M=y
CONFIG_ESPTOOLPY_AFTER_NORESET=y
CONFIG_ESPTOOLPY_OCT_FLASH=y

CONFIG_ESPTOOLPY_FLASHSIZE_4MB=
CONFIG_ESPTOOLPY_FLASHSIZE_8MB=
CONFIG_ESPTOOLPY_FLASHSIZE_16MB=
CONFIG_ESPTOOLPY_FLASHSIZE_32MB=y
CONFIG_PARTITION_TABLE_CUSTOM=y
CONFIG_PARTITION_TABLE_CUSTOM_FILENAME="partitions-32MiB.csv"
```

Im Verzeichnis ``$BUILD_DIR/micropython/ports/esp32`` wird ein neues ``makefile`` erstellt: 

```bash
nano makefile 
```

 Ein neues Makefile mit folgendem Inhalt wird erstellt und mit ``make`` ausgeführt:

```bash
BOARD = ESP32_GENERIC_S3
USER_C_MODULES = $(BUILD_DIR)/ulab/code/micropython.cmake

include Makefile
```

```bash
make
```

Es wird ein neues Verzeichnis ``build`` erstellt, mit den Dateien ``bootloader.bin``, ``partition-table.bin`` und ``micropython.bin``.

Anschließend wird mit ``esptool `` der ESP Flash bereinigt und die neue Firmware auf den ESP geflashed:

```bash
esptool.py -p (PORT) erase_flash

esptool.py -p /dev/ttyUSB0 -b 460800 --before default_reset --after no_reset --chip esp32s3  write_flash --flash_mode dio --flash_size 32MB --flash_freq 80m 0x0 build-ESP32_GENERIC_S3/bootloader/bootloader.bin 0x8000 build-ESP32_GENERIC_S3/partition_table/partition-table.bin 0x10000 build-ESP32_GENERIC_S3/micropython.bin
```

Leider funktioniert der Octal PSRAM mit dieser Konfiguration nicht.

## Contributing

Ursprünglich sollte die Eingabe mit Touchsensoren erfolgen. Dafür empfiehlt es sich aber, runde Platinenstücke gemäß dem [Datenblatt](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/touch_pad.html) von Espressif anzufertigen und dann mit der Dicke des Isolators zu experimentieren (es wird ein Plattenkondensator realisiert). Gern kann dieses Feature implementiert werden. Auch sind andere Algorithem für eine KI denkbar. 

## Weitere Ressourcen

- [Quelle wheel-Funktion für die Farbauswahl](https://randomnerdtutorials.com/micropython-ws2812b-addressable-rgb-leds-neopixel-esp32-esp8266/)

- [Micropython ESP Handbuch](https://docs.micropython.org/en/latest/esp32/quickref.html#neopixel-and-apa106-driver)

- [ESP32 einrichten in VSCODE](https://draeger-it.blog/visual-studio-code-fuer-micropython-einrichten/)

- [GitHub - v923z/micropython-ulab: a numpy-like fast vector module for micropython, circuitpython, and their derivatives](https://github.com/v923z/micropython-ulab)
