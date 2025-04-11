# Maps

This document discusses the origin, design choices, and implementation of the map in APXO.

The terms “map sheet” or just “sheet” are used to refer to the individual map sheets and “map” to refer to the whole space defined by the particular selection and arrangement of map sheets.

## Original Map Sheets

The original map sheets come in two generations. The first-generation sheets are those from *Air Superiority*, *Air Strike*, and *Eagles of the Gulf*. The second-generation sheets are from *The Speed of Heat*. The two generations differ in size, labeling, terrain features along their edges, and the graphical representation of terrain features.

### *Air Superiority*

*Air Superiority* came with four identical map sheets, referred to as sheets A to D. Barbie Pratt designed the sheets for GDW. They are uniformly blue with no terrain, only a hex and mega-hex grid. They are 25 hexes high and 20 hexes wide (8.3 by 5.8 miles).

### *Air Strike*

*Air Strike* came with six map sheets, labeled E to J. Again, Barbie Pratt designed the sheets for GDW.
They are the same size and have the same hex labeling as the Air Superiority map sheets.

The style is typical of GDW games of the epoch. The terrain is light green, with hills shown in two shades of brown, with the darker shade indicating higher elevation. The contrast is high. Villages are shown as block buildings on the terrain, and towns are shown as a continuous texture against a gray background. The maps include airfields, rail yards, docks, bridges, and a tunnel.

Sheets F to J are all land. Sheet E has a shoreline on two sides. The color of the water matches the blue used in the Air Superiority maps, so these can be used to extend the map offshore. Apart from this, as long as the sheets are arranged so that long edges abut other long edges and short edges abut other short edges, the terrain features flow from one sheet to the other.

### *Desert Falcons*

Desert Falcons did not provide any new map sheets but used the existing ones from Air Superiority and Air Strike.

### *Eagles of the Gulf*

*Eagles of the Gulf* appeared in issue 9 of *Battleplan* magazine and volumes 11 and 12 of *Air Power Journal*. It introduced four new sheets, labeled K, L, M, and N. Sheets K and L were published in *Battleplan*. Sheet N was published in volume 11 of *Air Power Journal*. Sheet M seems to have never been published and is only referenced in scenario EOG-23. It is not clear who designed these sheets, but the credits in *Battleplan* give “special thanks to Tony Valle for help on the maps”.

These sheets are printed in black and white. Sheets K and L represent desert terrain. Sheet N represents a stretch of the Suez Canal. 

These sheets are largely compatible with the Air Strike map sheets. One minor exception is that the roads leaving the top and bottom of sheet N do not match those in sheets E to L.

### *The Speed of Heat*

*The Speed of Heat* came with six map sheets, labeled A1, A2, B1, B2, C1, and C2. Rick Barber designed the sheets for Clash of Arms.

These second-generation sheets are smaller than the first-generation map sheets, being 15 hexes high and 20 hexes wide (5.0 by 5.8 miles). 

The design is recognizable as a development of the GDW style. The lowest terrain is shown in light green and the first level of hills in brown, but a second level of hills is added in a medium green. These maps have a lot more texture, for example, in the farmland, rivers, forests, and buildings. Villages, towns, and cities no longer seem to have distinct representations.

All the sheets show terrain. As befitting its subject, the urban area and river in map sheet A2 represent Hanoi and the Red River.

Again, as long as the sheets are arranged so that long edges abut other long edges and short edges abut other short edges, the terrain features flow from one sheet to the other. However, they do not match the first-generation sheets.

## APXO Maps

### Generations

Putting aside the question of the graphical representation of terrain features, first- and second-generation map sheets differ in their size, the geographic features along their edges, and in hex labeling. For these reasons, APXO allows games to be played on maps using sheets either from the first or the second generation, but not a mixture of generations.

### Sheets

APXO implements twenty-six first-generation sheets labeled A to Z:

- A to D: These are adaptations of the original four sheets from *Air Superiority*.

- E to J: These are adaptations of the original six sheets from *Air Strike*. 

- K to N: These are adaptations of the original four sheets from *Eagles of the Gulf*, but sheet M currently does not have terrain features. Also, some of the roads in sheet N have been adjusted to match the other sheets. 

- O to Z: These are twelve new sheets, currently all land at level 0 with no other terrain features. They are for future expansion.

Any number of first-generation sheets can be used at once. When arranged in an approximately square grid, twelve are 80 hexes wide by 75 hexes high (about 27 miles by 25 miles).

APXO implements twelve second-generation sheets labeled *XY*, in which *X* is one of the letters from A to D and *Y* is one of the numbers from 1 to 6:

- A1, A2, B1, B2, C1, and C2: These are adaptations of the original sheets from *The Speed of Heat*. 

- A3, B3, and C3: These are duplicates of A1, B1, and C1. Scenario V-25 in *The Speed of Heat* requires two copies of sheet C1; use sheets C1 and C3 instead.

- A4 to A6, B4 to B6, and C4 to C6, D1 to D6: These are twelve new sheets, currently all land at level 0 with no other terrain features. They are for future expansion.

Any number of the second-generation sheets can be used at once. When arranged in an approximately square grid, the twenty-four are 80 hexes wide by 90 hexes high (about 27 by 30 miles). 

Adding additional first-generation sheets to the implementation would be quite easy. Adding additional second-generation maps would be more difficult, as there is a mapping from hex codes *XXYY* to map sheet.

### Map Sheet Arrangement

The arrangement of map sheets into a map is specifiediven as by a two-dimensional Python array containing strings specifying the sheets. The elements of the array form the rows and columns of a grid. For example, the map for scenario K-5 in *The Speed of Heat* has B1 in the upper left, C1 in the upper right, A1 in the lower left, and B2 in the lower right, and is specified as:

    [
      [ "B1", "C1" ],
      [ "A1", "B2" ],
    ]

The rows of the grid must have the same number of sheets. Missing or blank sheets can be specified as `""`, `"-"`, or `"--"`. For example, the map for scenario V-13 in *The Speed of Heat* is specified as:

    [
      [ "C1", "--" ],
      [ "B1", "C2" ],
      [ "A2", "B2" ],
      [ "A1", "--" ],
    ]

### Inverted Map Sheets

APXO allow any map sheet to be inverted by simply appending `"/i"` to the map sheet name. For example, the map for scenario V-11 of *The Speed of Heat* is specified as:

    [["A1"],["B2/i"],["B1"]]

Inverted map sheets are used in these scenarios:

- *Air Superiority*
  - None
- *Air Strike*
  - No information
- *Desert Falcons*
  - No information
- *Eagles of the Gulf*
  - EOG-11
  - EOG-16
  - EOG-18
  - EOG-19
  - EOG-21
  - EOG-23
- *The Speed of Heat*
  - V-11: B2
  - V-22: C1 and C2

Note that the inversion process inverts the terrain but *does not invert the hex grid*. One consequence of this is that care needs to be taken when an aircraft or ground units that are set up on an inverted sheet; the original hex code cannot be used directly.

### Oblique Map Sheets

APXO does not allow map sheets to be used at an oblique angle; they must be either in the normal orientation or inverted.

Oblique map sheets are used in these scenarios:

- *Air Superiority*
  - H-13
  - H-14
- *Air Strike*
  - No information
- *Desert Falcons*
  - No information
- *Eagles of the Gulf*
  - EOG-4
  - EOG-7
  - EOG-8
  - EOG-20
- *The Speed of Heat*
  - None