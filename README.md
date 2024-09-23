<div align="center">
  <h1 align="center">Vier Gewinnt</h1>
</div>

  ![Bilder](/bilder/_DSF4458.jpg?raw=true "Titelbild")

# Connect Four Game with Raspberry Pi and NeoPixel Display

This is a custom **Connect Four (Vier Gewinnt)** game implemented using a **Raspberry Pi** and a **NeoPixel LED display**. The game allows two human players, or AI opponents, to compete in a dynamic game of Connect Four.

## Features
- **NeoPixel Display**: Visualizes the Connect Four game board with LEDs.
- **Player Types**: You can play against another human or the AI.
- **AI Players**: Both players can be controlled by AI, with varying decision-making strategies.
- **Animations**: Eye-catching animations such as rainbow cycles and blinking for the winning player.
- **Automatic Restarts**: If both players are AI, a new game automatically starts after 5 seconds of game completion.

## Hardware Requirements
- Raspberry Pi 4 (or similar)
- NeoPixel LED display with at least 42 LEDs (7x6 grid)
- Buttons connected to the GPIO pins for player input
- Python 3.x environment with the following libraries:
  - `RPi.GPIO`
  - `neopixel`
  - `numpy`

## Software Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/viergewinnt
   cd viergewinnt

2. **Set up Python virtual environment:**
   ```bash
   sudo apt-get install python3-venv
   python3 -m venv venv
   source venv/bin/activate

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

## Game Instructions

- Game Ready: When the rainbow animation is running, press any button to start the game.
- Player Selection: Choose for each player:
- Press 1 to select Human.
- Press 2 to select AI.
- Gameplay: Each player can drop their discs into one of the 7 columns:
- Press buttons 1 to 7 to select the column.
- Game End: The winning discs will blink for 5 seconds.
- If both players are AI, a new game will start automatically.

