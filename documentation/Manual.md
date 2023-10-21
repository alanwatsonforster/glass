# Manual

This manual is written to help players use the apengine package to automate the flight part of JD Webster's "Air Power" rules, published in the game "The Speed of Heat". Most of the other parts of the game, including combat, still need to handled manually.

The package is designed to run in a Google Colab notebook. You do not have to understand programming to use it.

## Using Colab Notebooks

A Colab notebook allows you to use your browser to edit and run commands in the cloud and to see the results. You can also share Colab notebooks with other players. You do not have to install any software on your computer to use colab (other than a browser) and it is free of charge.

To use Colab, you will need a Google account. If you use Gmail, then you already have an account. If you don't have an account, you will need to [create one](https://support.google.com/accounts/answer/27441?hl=en#zippy=%2Ccheck-if-you-already-have-a-google-account).

Go to the [home page for Colab](https://colab.research.google.com). Click on the button to create a new notebook. You may have to sign-in to your Google account. Your new notebook should appear in a new tab or window.

Colab notebooks contain “cells”. Each cell can be either text or code. Here, we will mainly be using code cells, although you can use text cells to keep notes or to maintain a commentary on the game. Your new Colab notebook will have been created with an empty code cell.

Each cell has an input area, where you can type and modify commands, and an output area, where you can see the results of typing commands. To edit a command, just click in the field and start typing or deleting. To run a command, type Ctrl-Enter.

Let’s try that. In the code cell, type:

	print("Hello, world!")

Next, run the cell using Ctrl-Enter. It should print “Hello, world!” in the output area just below the input area.

You can create additional cells by hovering your cursor over the midpoint of the top and bottom of a cell or by using the “Insert” menu.

For further information on Colab notebooks, see Google’s “[Welcome to Colab](https://colab.research.google.com/#scrollTo=-gE-Ez1qtyIA)” page and in particular the tutorial video.

## Loading the Package

Copy these commands into the first code cell in the Colab notebook:

    !test -d apengine || git clone --depth=1 https://github.com/alanwatsonforster/apengine.git -q
    !cd apengine; git pull -q
    import sys
    sys.path.append('apengine')
    from apengine import *

Then run the cell by typing Ctrl-Enter. After a short delay while the notebook connects to the cloud, the commands will download the code and make it available for use in the notebook.

## Setting Up the Game

Before you can play, you need to set up the game: the map sheets, the direction of north, and the initial positions of aircraft.

Create a second code cell, below the one used to load the package. (Use the “Insert” menu or the buttons that appear when you hover over the midpoints of the bottom of the previous cell.)

Copy these commands into the second code cell:


    startsetup("TSOH:T-3")
    endsetup()
    drawmap()
    
These commands set up the map for Training Scenario T-3 in The Speed of Heat. Maps are available for all of the scenarios in The Speed of Heat, except V-11 and V-22 (which use inverted map sheets) and V-25 (which uses sheet C1 twice). They are labeled:

- Training Scenarios: TSOH:T-1 to TSOH-T-6
- General Scenarios: TSOH:G-1 to TSOH:G-3
- Korean War Scenarios: TSOH:K-1 to TSOH:K-10
- Cold War Scenarios: TSOH:CW-1 to TSOH:CW-5
- Vietnam War Scenarios: TSOH:V-1 to TSOH:V-24
- Vietnam War Epilog Scenario: TSOH:V-E

You can also set up your own arrangement of maps, but we’ll get to that later.

The commands end by drawing the map. It will probably appear quite small in your browser, but if you click on it it will be displayed at full size.

Now you need to add aircraft. Between "startsetup" and "endsetup" add lines like these:

    A1 = aircraft("A1", "F-80C", "3211"", "N", 30, 4.5, "CL")
    
This creates an F-80C in hex 3211, flying north, at altitude level 30, with speed 4.5, and clean configuration. We use A1 both for the name of the aircraft (the first argument to the call) and the name of the variable (before the equals sign). I recommend using a letter and a number, with the letter being the first letter of the call-sign. So, for example, "Ford 3" would be "F3".

By default, aircraft are unpainted, but you can specify a color like this:

    A1 = aircraft("A1", "F-80C", "3211"", "N", 30, 4.5, "CL", color="natoblue")
    
Commonly used colors are: unpainted, silver, aluminum (or aluminium), green, tan, sand, white, darkblue, lightgray (or lightgrey), darkgray (or darkgrey), natoblue, and natored.

For example, here is how I would set up Training Scenario 3 from The Speed of Heat:

    startsetup("TSOH:T-3")
    C1 = aircraft("C1", "MiG-15bis", "5127", "N" , 18, 5.0, "CL", color="natored")
    C2 = aircraft("C2", "MiG-15bis", "5228", "N" , 18, 5.0, "CL", color="natored")
    U1 = aircraft("U1", "F-86E"    , "6914", "NE", 20, 6.0, "CL", color="natoblue")
    endsetup()
    drawmap()

Rather than leaving all of the aircraft unpainted, I'm using NATO blue for the F-86 and NATO red for the MiG-15s.

When the map is drawn, it is sized to fit the width of the window. You can zoom in by clicking on the map and see it full-screen by selecting "view output fullscreen" in the ... menu in the upper right of the cell. 

On the map, each  aircraft is shown as a dart, with its name to the left and altitude level to the right. Here is the map at the start of Training Scenario 3, and a zoom to show the aircraft. The F-86 is blue and is at altitude level 20. The MiG-15s are red and are at altitude level 18.

![The map at the start of Training Scenario 3](<./Manual/T-3-start.png>)

![The aircraft at the start of Training Scenario 3](<./Manual/T-3-start-zoom.png>)

The representation of the map was designed with the aim of making aircraft and other markers stand out clearly. With a physical map, this is less of an issue as the counters stand out from the map in relief and texture. Therefore, the terrain and hex grid deliberately has low contrast and saturation and the aircraft typically have higher contrast and saturation and are outlined in black.

