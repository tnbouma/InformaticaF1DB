--------- IMPORTANT --------------

It is highly recommended to run "main.py" in the terminal in full screen! (On a machine running Windows)

----- SUPPORTED PLATFORMS ------

Available on:
- Windows (Developed and Tested on Windows 11) -->	All Features
- MacOS (Tested on MacOS Monterey v12.5) -->		Basic Features

-------- ERRORS -----------

if you get the error "Couldn't open database", it should be easily fixable by running "main.py" in the terminal.

if you get the error "cannot find f1db.db in tnbouma_db", make sure f1db.db is inside the same folder as "main.py". You could also rebuild the f1db.db by making a new file in DB Browser (SQLite) and choose File -> Import -> database from SQL file, you can use the f1db.sql in the tnbouma_db folder. Make sure you save the file as "f1db.db" in the tnbouma_db folder.

You could run into a menu not printing. This a problem that occurs when you don't have enough space in your terminal. You can fix this by either:
- Making your terminal bigger (especially width)
OR
- Enabling ForcePrint (More information under the tab settings)

------- CODE LAYOUT -------

- Import modules (OS specific)
- Define color-codes
- Define settings
- Define basic functions (like errors, warnings, clearterminal, closeprogram, etc.)
- Define terminal size related functions
- Define StartUp functions (Check if database is in directory, Open database, Check terminal size, Check OS, etc.)
- Define Menu scripts
- Define Visual script
- Define Every Menu Option (Used for getting data and translating it into data the Visual script understands)
- Define Main body

- Call for startup()
- Call for main()

This code layout is very useful when you want to add more menus. You can add a new menu without having to recode the visuals at all.
Every menu has the same visualizer with VERY minor changes, like color-coding or similar features.


------- ERRORMESSAGES -----

A custom errormessage system for possible errors like:

Errors: <-- "Prints error in red and terminates program"

- Database isn't in the directory it should be
- Database doesn't open
- There is a value in the menu which shouldn't be there
- Invalid path given from menu
- etc.

Warnings: <-- "Prints warning in yellow (And waits for user input in some cases)"

- Terminal height is too low
- Terminal width is too low
- Data cannot comfortably print (due to the size of the terminal), (ONLY WITH FORCEPRINT DISABLED)
- etc.

--- TERMINAL RESIZING ------

The script checks (on StartUp()) if the terminal is big enough to comfortably print everything. If not it will ask the user if they want to resize or not.

If the user entered "y" or "yes"
--> Terminal will output real-time size of terminal to enable the user to resize the terminal. The resizing program will automatically quit when the desired size has been reached.

If the user entered "n" or "no"
--> User gets redirected to main program. (THIS IS ASKING FOR UNEXPECTED BEHAVIOR and should ONLY be used when absolutely necessary)

------- SETTINGS -----------

You can access the settings from selecting menu 0 from the main menu.

Type the number of the bool-value you want to switch. And type 0 to return to main menu.

Settings:
- ForcePrint, forces the terminal to print if enabled, even if there is no space. I have this disabled at default to avoid unexpected errors with printing.  

-------- MENUS -------------

Menu 1:
- Shows the important stats of a circuit
- List of circuits to choose from at the beginning
- Previous names of a circuit only show up if they exist
- Multiple previous names get automatically split into multiple rows

Menu 2:
- Shows the important stats of a driver
- Shows the position from the stat in relation to the other drivers
- List of drivers to choose from at the beginning
- Unimportant stats like NULL or 0 are automatically greyed out.

Menu 3:
- Shows the important stats of a team
- Shows the position from the stat in relation to the other teams
- List of teams to choose from at the beginning
- Unimportant stats like NULL or 0 are automatically greyed out.

Menu 4.1:
- Shows driver + constructor standings of that year
- Colorcoded 1st, 2nd and 3rd places
- NULL values regarding the position will result in DSQ's

Menu 4.2:
- Shows winner, runner-up and third person in the driver standings of that year
- Colorcoded 1st, 2nd and 3rd places
- NULL values regarding the position will result in DSQ's

** if you want to request the standings of more years at the same time, try to make your terminal bigger. The maximum amount of years is dependent on the available lines in your terminal.

--------- DATABASE MANIPULATION -----------------

I've downloaded the .SQL file from the F1DB releases tab and imported it into an empty database file.
I've deleted all unnecessary columns and tables (data which my script will not use) reducing the size (of the Data Base File) from over 100 MB to only 228 KB

- I've replaced the repeating strings from column type (from circuit) with integers and added a conversion table.
- Made Driver visuals dependent on name instead of id.
- Replaced driver_id (in season_driver_standings) strings (nino-farina) with integers (655).
- Did the same for country_id
- Did the same for constructor_id (You can find the script used to generate the commands in the folder "DatabaseManipulation")

-------------- FILES ----------------------------

- DatabaseManipulation (Folder)
---> DatabaseManipulation\SHORT SCRIPT.py 	->	Writes commands for database manipulation purposes to COMMANDS.txt (Saves time, otherwise you'd have to do 300 lines by hand)
---> DatabaseManipulation\COMMANDS.txt     	->	text file for commands (I copied the commands from here)

- f1db.sqbpro	-> Shortcut to open f1db.db in DB Browser SQLite
- f1db.db	-> Gets used by main.py and is the "native" database file
- f1db.sql	-> Acts as a back-up database which you can use to restore the database
- main.py	-> Has all the menu's. Run this to browse the database.
- README.txt	-> Has the explanations of the project.

--------------- SOURCES -------------------------

- F1DB Main Page (https://github.com/f1db/f1db)
- F1DB Downloads (https://github.com/f1db/f1db/releases) v2024.6.0 --> f1db-sql-sqlite.zip