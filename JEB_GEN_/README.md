# Settlement Generator in GDMC 

This is a settlement generator for Minecraft. This project is based on the [GDPC](https://github.com/avdstaaij/gdpc) project and is specifically designed for the [GDMC](https://gendesignmc.engineering.nyu.edu/) competition.

## Author
* Tai-Wei Kuo (LoveSnowEx)
* Tsu-Chuan Su (SubaRya)
* Wei-Cheng Chen (Lapor)
* Wen-Yuan Wu (jw910731)

## Requirements

- Python 3.10

## Installation

1. Clone this [repository](https://github.com/NTNU-GDMC/GDMC)
2. Install the required packages
  ```
  pip install -r requirements.txt
  ```

## Usage

1. Run Minecraft 1.19.2 with [GDMC-HTTP](https://github.com/Niels-NTG/gdmc_http_interface) mod installed
2. Use `/setbuildarea xFrom yFrom zFrom xTo yTo zTo` in Minecraft to set the place where to build the settlement.
3. Run `python main.py` to generate a settlement
4. The settlement will be created in Minecraft
