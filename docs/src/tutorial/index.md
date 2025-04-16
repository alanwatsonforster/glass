# Manual

This manual is written to help players use the glass package to automate the flight part of JD Webster's "Air Power" rules, published in the game "The Speed of Heat". Most of the other parts of the game, including combat, still need to handled manually.

The package is designed to run in a Google Colab notebook. You basically have to type commands that specify the flight type, power setting, and action for each aircraft. You do not have to understand programming to use it.

## Introduction

### Using Colab Notebooks

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

### Loading the Package

Copy these commands into the first code cell in the Colab notebook:

    !test -d glass || git clone --depth=1 https://github.com/alanwatsonforster/glass.git -q
    !cd glass; git pull -q
    import sys
    sys.path.append('glass')
    from glass import *

Then run the cell by typing Ctrl-Enter. After a short delay while the notebook connects to the cloud, the commands will download the code and make it available for use in the notebook.

### Setting Up the Game

Before you can play, you need to set up the game: the map sheets, the direction of north, and the initial positions of aircraft.

Create a second code cell, below the one used to load the package. (Use the “Insert” menu or the buttons that appear when you hover over the midpoints of the bottom of the previous cell.)

Copy these commands into the second code cell:


    startgamesetup("TSOH:T-3")
    endgamesetup()
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

Now you need to add aircraft. Between "startgamesetup" and "endgamesetup" add lines like these:

    A1 = aircraft("A1", "AF", "F-80C", "3211"", "N", 30, 4.5, "CL")
    
This creates an F-80C in hex 3211, flying north, at altitude level 30, with speed 4.5, and clean configuration. We use A1 both for the name of the aircraft (the first argument to the call) and the name of the variable (before the equals sign). I recommend using a letter and a number, with the letter being the first letter of the call-sign. So, for example, "Ford 3" would be "F3".

By default, aircraft are unpainted, but you can specify a color like this:

    A1 = aircraft("A1", "AF", "F-80C", "3211"", "N", 30, 4.5, "CL", color="natoblue")
    
Commonly used colors are: unpainted, silver, aluminum (or aluminium), green, tan, sand, white, darkblue, lightgray (or lightgrey), darkgray (or darkgrey), natoblue, and natored.

For example, here is how I would set up Training Scenario 3 from The Speed of Heat:

    startgamesetup("TSOH:T-3")
    C1 = aircraft("C1", "AF", "MiG-15bis", "5127", "N" , 18, 5.0, "CL", color="natored")
    C2 = aircraft("C2", "AF", "MiG-15bis", "5228", "N" , 18, 5.0, "CL", color="natored")
    U1 = aircraft("U1", "AF", "F-86E"    , "6914", "NE", 20, 6.0, "CL", color="natoblue")
    endgamesetup()
    drawmap()

Rather than leaving all of the aircraft unpainted, I'm using NATO blue for the F-86 and NATO red for the MiG-15s.

When the map is drawn, it is sized to fit the width of the window. You can zoom in by clicking on the map and see it full-screen by selecting "view output fullscreen" in the ... menu in the upper right of the cell. 

On the map, each  aircraft is shown as a dart, with its name to the left and altitude level to the right. Here is the map at the start of Training Scenario 3, and a zoom to show the aircraft. The F-86 is blue and is at altitude level 20. The MiG-15s are red and are at altitude level 18.

![The map at the start of Training Scenario 3](<../../../tutorial/T-3-start.png>)

![The aircraft at the start of Training Scenario 3](<../../../tutorial/T-3-start-zoom.png>)

The representation of the map was designed with the aim of making aircraft and other markers stand out clearly. With a physical map, this is less of an issue as the counters stand out from the map in relief and texture. Therefore, the terrain and hex grid deliberately has low contrast and saturation and the aircraft typically have higher contrast and saturation and are outlined in black.

### Turns

Create another code cell. Copy this into the cell:

    startgameturn()
    drawmap()
    
(For the time being, don't add a endgameturn command.)
If we run these, we see the aircraft at the start of the turn.

Now, add calls to more the aircraft. In this scenario, 
the MiGs follow random movement. Edit the cell to add these last three commands:

    startgameturn()
    drawmap()
    C1.move("SP", 0, "H,HL,CL,H,H")
    C2.move("SP", 0, "H,HL,DD,DR,H")
    drawmap()

The C1.move and C2.move command move the MiGs C1 and C2 according to special flight moves with actions "H,HL,CL,H,H" and "H,HL,DD,DR,H". I'll explain special flight moves more completely below. After that, these is another drawmap command.

If we run the cell (Ctrl-Enter), two maps are produced: one before any aircraft move and one after the MiGs move. Here is a zoom on the second map. Notice that the flight paths of the two MiGs is shown by a dotted line. Also, MiG C2 is now at altitude level 15. The F-86 has yet to move.

![Turn 1 after the MiGs have moved](<../../../tutorial//T-3-1a.png>)

Above the maps, we get a log of what happened:

    C1: turn 1  : --- start of move --
    C1: turn 1  : flight type   is SP.
    C1: turn 1  : altitude band is MH.
    C1: turn 1  : ---
    C1: turn 1  : start :                  : 5127       N    18
    C1: turn 1  : end   : H,HL,CL,H,H      : 6909       WNW  19
    C1: turn 1  : ---
    C1: turn 1  : altitude band is unchanged at MH.
    C1: turn 1  : --- end of move -- 

    C2: turn 1  : --- start of move --
    C2: turn 1  : flight type   is SP.
    C2: turn 1  : altitude band is MH.
    C2: turn 1  : ---
    C2: turn 1  : start :                  : 5228       N    18
    C2: turn 1  : end   : H,HL,DD,DR,H     : 5225       N    15
    C2: turn 1  :       : - altitude band changed from MH to ML.
    C2: turn 1  : ---
    C2: turn 1  : altitude band changed from MH to ML.
    C2: turn 1  : --- end of move -- 

Now let's move the F-86. This flies according to standard flight rules, so is more representative of a typical aircraft. Let's assume we want to dive down towards MiG C2 while doing a BT to the left to come in on its tail. Let's add two commands to the cell to reflect this. One specifies the flight of the F-86 and the other draws the map again.

    startgameturn()
    drawmap()
    C1.move("SP", 0, "H,HL,CL,H,H")
    C2.move("SP", 0, "H,HL,DD,DR,H")
    drawmap()
    U1.move("SD","M","BTL/H,H/L,H,H/L,DD/WL,DD")
    drawmap()

The first argument to the U1.move command is the type of flight, in this case SD for a steep dive. The second is the power setting, in this case M for full military power. The last argument gives the actions, separated by commas:

- BTL/H: declare a BT to the left and move forward one hex
- H/L: move forward one hex and change facing 30 degrees to the left
- H: move forward one hex
- H/L:  move forward one hex and change facing 30 degrees to the left
- DD/WL: dive two levels and come to wings-level
- DD: dive two more levels

The slashes simply serve to visually separate the elements of each action. They can be omitted.

We can run the cell again (Ctrl-Enter). The startgameturn command restores the positions of the aircraft to where they were at the start of the turn, so we can run this cell multiple times if we want (and often do so as we develop the flight path for each aircraft). After doing so, the third map looks like this:

![Turn 1 after the F-86 has moved](<../../../tutorial/T-3-1b.png>)

Again, above the maps we have a log of what happened, this time giving details of the flight of the F-86, and in particular its final speed:

    U1: turn 1  : --- start of move --
    U1: turn 1  : flight type   is SD.
    U1: turn 1  : power setting is M.
    U1: turn 1  : speed         is 6.0 (LT).
    U1: turn 1  : - transonic drag.
    U1: turn 1  : configuration is CL.
    U1: turn 1  : altitude band is MH.
    U1: turn 1  : - is carrying +0.00 APs.
    U1: turn 1  : - has wings level.
    U1: turn 1  : - has 6.0 FPs (including 0.0 carry).
    U1: turn 1  : - the first FP must be an HFP.
    U1: turn 1  : - at least 2 FPs must be HFPs.
    U1: turn 1  : - at least 1 FP must be a VFP.
    U1: turn 1  : ---
    U1: turn 1  : start :                  : 6914       ENE  20
    U1: turn 1  : FP 1  : BTL/H            : 7014       ENE  20
    U1: turn 1  : FP 2  : H/L              : 5128       NNE  20
    U1: turn 1  : FP 3  : H                : 5127/5228  NNE  20
    U1: turn 1  : FP 4  : H/L              : 5227       N    20
    U1: turn 1  : FP 5  : DD/WL            : 5227       N    18
    U1: turn 1  : FP 6  : DD               : 5227       N    16
    U1: turn 1  :       : - altitude band changed from MH to ML.
    U1: turn 1  : ---
    U1: turn 1  : - used 4 HFPs and 2 VFPs.
    U1: turn 1  : - is carrying 0.0 FPs.
    U1: turn 1  : - turned at BT rate.
    U1: turn 1  : - has wings level.
    U1: turn 1  : -- power           APs = +1.00.
    U1: turn 1  : -- speed           APs = -1.00.
    U1: turn 1  : -- altitude        APs = +2.00.
    U1: turn 1  : -- turns           APs = -2.00.
    U1: turn 1  : -- other maneuvers APs = +0.00.
    U1: turn 1  : -- speedbrakes     APs = +0.00.
    U1: turn 1  : -- carry           APs = +0.00.
    U1: turn 1  : -- total           APs = +0.00.
    U1: turn 1  : - is carrying +0.00 APs.
    U1: turn 1  : speed         is unchanged at 6.0.
    U1: turn 1  : configuration is unchanged at CL.
    U1: turn 1  : altitude band changed from MH to ML.
    U1: turn 1  : --- end of move -- 

The APEngine code interprets the flight type, power setting, and actions and correctly moves the aircraft and determines its finally speed. Note that APEngine treats DPs as negative APs. For clarity, it also separates the power APs (thrust from the power setting) from the speed APs (drag due to the speed).

APEngine also checks for invalid moves, such as entering VC straight from LVL flight (in an aircraft that is not HPR), using too few or too many FPs, using the incorrect combination of HFPs and VFPs, attempting to change facing before accumulating sufficient preparatory FPs, and many other incorrect situations. For example, if we try to dive three levels on a single VFP in order to get down to altitude level 15:

    U1.move("SD","M","BTL/H,H/L,H,H/L,DDD/WL,DD")

then it complains:

    === ERROR: attempt to dive 3 levels per VFP while the flight type is SC. ===

Once all of the aircraft have moved, we finish the turn by adding an endgameturn command at the end:

    endgameturn()
    
The complete cell now looks like this:

    startgameturn()
    drawmap()
    C1.move("SP", 0, "H,HL,CL,H,H")
    C2.move("SP", 0, "H,HL,DD,DR,H")
    drawmap()
    U1.move("SD","M","BTL/H,H/L,H,H/L,DD/WL,DD")
    drawmap()
    endgameturn()

Once we run this cell, with the endgameturn command, the turn is finished. 

Having added the endgameturn command, if we run the cell more than once, instead of repeating turn 1, it will be run turn 2 but with identical commands to turn 1. This is almost certainly not what we want to do. Fortunately, we can easily recover from this by selecting "Run all" from the "Runtime" menu to run everything again from scratch.
