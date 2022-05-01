# Magic: the Gathering pick order
For M:tG players who need a quick primer to draft formats they're new to.

This python application allows M:tG players who are new to a format, need a leg up in drafting, or just need a second opinion on comparing two potential first picks, to get a leg up on the competition. Type in names of cards that you want analyzed, and get the card's ranking returned back, with more preferred picks up top.

Controls  
Enter - Input new card (preserves old search results)  
Backspace - Undo previous keystroke, or on empty line, clears the line  
Ctrl + D - Clear line  
Ctrl + C - Exit  

Thanks to Frank Karsten for the initial seed data for Magic: Origins drafts, and Modern Horizon drafts. You can find his analysis [here.](http://www.channelfireball.com/articles/a-pick-order-list-for-magic-origins/)

Thanks to LSV for the updated seed data for Magic: Origins drafts and the DTK set. You can find his articles [here.](http://www.channelfireball.com/author/luis-scott-vargas/)

Thanks to TCGPlayer for the pick orders for 3xZEN. You can find the original data [here.](http://magic.tcgplayer.com/strategy/draft-091006.asp) Do note that this data is missing lands and artifacts in the analysis.

Thanks to reddit user _Concepcion for their compiled Strixhaven draft data. [Original reddit post here](https://redd.it/mr6jhh), and [original data compilation here.](https://docs.google.com/spreadsheets/d/1SBLdCAugGsRrAcrZiGBhL5_mQoPgYopBuUj-4GOPfQk/) In addition, thanks to _Concepcion for their compiled Streets of New Capenna draft data! [Original reddit post](https://www.reddit.com/r/MagicArena/comments/uctrpp/streets_of_new_capenna_limited_grades_compilation/) and [original compilation.](https://docs.google.com/spreadsheets/d/1vmP9OcbCE6Vj1ZNOVjgpjHMZWjmOMQ6M7opIaWtpy1Q/edit?usp=sharing)

# Example
Here's a sample P1P1 of a pack of Magic: Origins, provided by ChannelFireball [here.](http://www.channelfireball.com/articles/whats-the-pick-magic-origins-pack-1-pick-1-with-huey-2/)

![mtg pick order in action](readme/example.png)

# Pick Number

There are two types of data provided so far. One scale goes from 0.0 (low) to 5.0 (high), and is an absolute rating of the card. The other scale goes from 1.0 (high) to 15.0 (low) and indicates the average pick the card is taken in. There's currently no obvious distinguishing factor between the two, but the program will always put the preferred picks at the top of the list, to make things easy for you!
