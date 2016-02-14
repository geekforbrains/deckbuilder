Deckbuilder
===========

This is a simple CLI tool for creating quick prototype decks for use with
Tabletop Simulator. It takes a specific JSON formatted file and converts it
into the correct sized sprite sheets.

*Unstable and very much in development at the moment.*

JSON Format Example
-------------------

```json
[
  {
    "rgb": [255, 255, 255],
    "name": "EXAMPLE",
    "cards": [
      [10, {"title": "First Card", "info": ["Info Line #1", "Info Line #2"]}],
      [5, {"title": "Second Card", "info": ["Some Info About It"]}],
    ]
  }
]
```

The above would generate a deck with the name "EXAMPLE" on the back of the cards.
The deck would be made up of 10 "First Card"s and 5 "Second Cards". 

The JSON file can include as many deck definitions as you want.
