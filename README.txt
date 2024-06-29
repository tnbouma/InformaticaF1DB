--------- IMPORTANT --------------

It is highly recommended to run "main.py" in the terminal in full screen!

----- CROSS PLATFORM ------

Available on:
- Windows (Developed and Tested on Windows 11)

-------- ERRORS -----------

if you get the error "Couldn't open database", it should be easily fixable by running "main.py" in the terminal. If the problem persists try running as an admin.

if you get the error "cannot find f1db.db in tnbouma_db", make sure f1db.db is inside the same folder as "main.py". You could also rebuild the f1db.db by opening the database in DB BROWSER (SQLite) and click on "File -> Export -> Database to SQL File -> Select All -> Save" And make sure you save the file in the tnbouma_db folder.

IF DATA DOESN'T PRINT IT IS MOST LIKELY BECAUSE YOUR TERMINAL IS TOO SMALL!, THIS IS ESPECIALLY LIKELY TO HAPPEN IN MENU 4.2

------- CODE LAYOUT -------

- Import modules (OS specific)
- Define color-codes
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

The script checks if the terminal is big enough to comfortably print everything. If not it will ask the user if they want to resize or not.

If the user entered "y" or "yes"
--> Terminal will output updated size of terminal to enable the user to resize the terminal. The resizing program will automatically quit when the desired size has been reached.

If the user entered "n" or "no"
--> User gets redirected to main program. (THIS IS ASKING FOR UNEXPECTED ERRORS and should ONLY be used when absolutely necessary)
--> IF DATA DOESN'T PRINT IT IS MOST LIKELY BECAUSE YOUR TERMINAL IS TOO SMALL!, THIS IS ESPECIALLY LIKELY TO HAPPEN IN MENU 4.2!

This is due to the fact that I made a checker to see if there is any room left to print another table next to another table (see menu 4.1). But because menu 4.2 is a single big table it is quite easy run out of space resulting in the program printing infinite empty lists. (you probably need at least 130 characters horizontally)

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
- Colorcoded
- NULL values regarding the position will result in DSQ's

Menu 4.2:
- Shows winner, runner-up and third person in the driver standings of that year
- Colorcoded

** if you want to request the standings of more years at the same time, try to make your terminal bigger. The maximum amount of years is dependent on the available lines in your terminal, and yes it updates.

--------------- SOURCES -------------------------

- Internet for documentation purposes