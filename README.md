# Bingo Generator

This repository works as a simple implementation of a bingo card generator in Python. Just for fun.

## Installation

Just clone the repository

```bash
git clone https://github.com/danifei/bingo-generator.git
```

The only library requirements is the Pillow library. Just install the latest version:

```bash
pip install pillow
```

## Custom Pipeline

The main file is [generator.py](/generator.py). At top of the file you are able to configure all the relevant variables of the generator (those in capital letters). 

In the [/background](/background/) folder, you may place the background images that will be randomly used in the cards. Then, the file [events.txt](/events.txt) is where you need to place the different box values used in the cards. You just need to put one event per row.

When everything is selected just run:

```bash
python generator.py
```

