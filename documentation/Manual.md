# Manual

This manual is written to help players use the apengine package to automate the flight part of JD Webster's "Air Power" rules, published in the game "The Speed of Heat".

The package is designed to run in a Google Colab notebook. You do not have to understand programming to use it.

## Using Colab Notebooks

A Colab notebook allows you to use your browser to edit and run commands in the cloud and to see the results. You can also share Colab notebooks with other players. You do not have to install any software on your computer to use colab (other than a browser) and it is free of charge.

To use Colab, you will need a Google account. If you use Gmail, then you already have an account. If you don't have an account, you will need to [create one](https://support.google.com/accounts/answer/27441?hl=en#zippy=%2Ccheck-if-you-already-have-a-google-account).

Go to the [home page for Colab](https://colab.research.google.com). Click on the button to create a new notebook. You may have to sign-in to your Google account. Your new notebook should appear in a new tab or windows.

Colab notebooks contain “cells”. Each cell can be either text or code. Here, we will mainly be using code cells, although you can use text cells to keep notes or to maintain a commentary on the game. Your new Colab notebook will have been created with an empty code cell.

Each cell has an input area, where you can type and modify commands, and an output area, where you can see the results of typing commands. To edit a command, just click in the field and start typing or deleting. To run a command, type Ctrl-Enter.

Let’s try that. In the code cell, type:

	print("Hello, world!")

Next, run the cell using Ctrl-Enter. It should print “Hello, world!” in the output area just below the input area.

You can create additional cells by hovering your cursor over the midpoint of the top and bottom of a cell or by using the “Insert” menu.

For further information on Colab notebooks, see Google’s “[Welcome to Colab](https://colab.research.google.com/#scrollTo=-gE-Ez1qtyIA)” page and in particular the tutorial video.

## Loading the Package

Copy these commands into the first code cell in the Colab notebook:

!test -d apengine || git clone https://github.com/alanwatsonforster/apengine.git
import sys
sys.path.append('apengine')
from apengine import *
Then run the cell by typing Ctrl-Enter. After a short delay while the notebook connects to the cloud, the commands will download the code and make it available for use in the notebook.

## Setting Up the Game

Before you can play, you need to set up the game: the map sheets, the direction of north, and the initial positions of aircraft.

Create a second code cell, below the one used to load the package. (Use the “Insert” menu or the buttons that appear when you hover over the midpoints of the bottom of the previous cell.)

Copy these commands into the second code cell:


    startsetup("TSOH:K-10")
    endsetup()
    drawmap()
    
These commands set up the map for scenario K-10 in The Speed of Heat. Maps are available for all of the scenarios in The Speed of Heat, except V-11 and V-22 (which use inverted map sheets) and V-25 (which uses sheet C1 twice). They are labeled:

- Training Scenarios: TSOH:T-1 to TSOH-T-6
- General Scenarios: TSOH:G-1 to TSOH:G-3
- Korean War Scenarios: TSOH:K-1 to TSOH:K-10
- Cold War Scenarios: TSOH:CW-1 to TSOH:CW-5
- Vietnam War Scenarios: TSOH:V-1 to TSOH:V-24
- Vietnam War Epilog Scenario: TSOH:V-E

You can also set up your own arrangement of maps, but we’ll get to that later.

The commands end by drawing the map. It will probably appear quite small in your browser, but if you click on it it will be displayed at full size.

