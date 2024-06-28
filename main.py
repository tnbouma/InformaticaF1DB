## ------------------------------------------------------
## --------------------- IMPORT -------------------------
## ------------------------------------------------------

import sqlite3
import os

if os.name == "posix":
    def WaitForUserInput():
        print("\nPress Enter to return to main menu")
        input()
if os.name == "nt":
    from msvcrt import getch as getch
    def WaitForUserInput():
        print("\nPress a key to return to main menu")
        getch()

## ------------------------------------------------------
## ------------------- END IMPORT -----------------------
## ------------------------------------------------------

## ------------------------------------------------------
## -------------------- CLASSES  ------------------------
## ------------------------------------------------------

## colors to support printing colored output
class colors: 
    ENDL = '\033[0m'
    WARNING = '\033[38;2;255;255;0m' ## 38 = Change TextColor, 2 == <r>;<g>;<b>
    FAIL = '\033[38;2;255;0;0m' 

    yellow = '\033[38;2;255;255;0m'
    lightgrey = '\033[38;2;200;200;200m'
    brown = '\033[38;2;150;75;0m'
    white = '\033[38;2;255;255;255m'
    black = '\033[38;2;0;0;0m'

## ------------------------------------------------------
## ------------------ END CLASSES -----------------------
## ------------------------------------------------------

## ------------------------------------------------------
## ---------------- GLOBAL VARIABLES --------------------
## ------------------------------------------------------

cur = 0
conn = 0

## ------------------------------------------------------
## --------------- END GLOBAL VARIABLES -----------------
## ------------------------------------------------------

## ------------------------------------------------------
## ----------------- BASIC FUNCTIONS --------------------
## ------------------------------------------------------

# closes program with an errormessage
def error(errormessage):
    CloseProgram(errormessage)

# prints a warning to the terminal, and waits for user to read it
def warning(errormessage):
    print(colors.WARNING+"WARNING: "+str(errormessage)+colors.ENDL)
    print("Press any key to continue")
    WaitForUserInput()

# clears the terminal
def clearterminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Closes program
def CloseProgram(errormessage):
    clearterminal()
    print("Terminating script...")

    # print errormessage if it exists
    if errormessage != 0:
        print(colors.FAIL+"ERROR: "+str(errormessage)+colors.ENDL)

    # closing database connection if it exists
    try:
        conn.close()
    except:
        pass
    
    print("Script Ended")
    # end program
    quit()

## ------------------------------------------------------
## --------------- END BASIC FUNCTIONS ------------------
## ------------------------------------------------------

## ------------------------------------------------------
## ---------------- START-UP FUNCTIONS ------------------
## ------------------------------------------------------

## resizes terminal
def TryResizeTerminal(terminalrows, terminalcolumns):
    if os.name == "posix":
        return
    try:
        size = os.get_terminal_size()
    except:
        error("Couldn't get terminal handle, are you sure you're running this inside the terminal?")
    # try to resize terminal
    os.system(f"mode {terminalcolumns},{terminalrows}")
    print(os.get_terminal_size())
    if (os.get_terminal_size().columns != terminalcolumns) or (os.get_terminal_size().lines != terminalrows):
        # if the resizing failed, print warning
        warning("couldn't resize terminal properly, reverting process")
        os.system(f"mode {size.columns},{size.lines}")
        if (os.get_terminal_size().columns != size.columns) or (os.get_terminal_size().lines != size.lines):
            # if the revert failed, throw error
            error("reversion process went wrong!")

def StartUp():
    global cur
    global conn

    ## trying to resize terminal to assure data gets printed 
    terminalrows = 30
    terminalcolumns = 100
    TryResizeTerminal(terminalrows,terminalcolumns)

    ## trying to connect database
    script_dir = os.path.dirname(__file__) # <-- Returns parent of main.py (tnbouma_db)
    relative_path = 'f1db.db'
    path = os.path.join(script_dir, relative_path)

    ## securing the given path leads to our database
    if not (os.path.isfile(path)):
        error("cannot find "+relative_path+" in "+script_dir)

    ## connecting database
    conn = sqlite3.connect(path) 
    cur = conn.cursor()

## ------------------------------------------------------
## -------------- END START-UP FUNCTIONS ----------------
## ------------------------------------------------------

## ------------------------------------------------------
## -------------------- MENU SCRIPT ---------------------
## ------------------------------------------------------

def printKeuzeMenu(km, l):
    ## for every element in keuzemenu print title of next menu or the string.
    if (l == 0):
        # only print this in the main menu
        print("0: Terminate Process")
    for i in range(len(km)):
        if type(km[i]) == type('string'):
            name = km[i]
        elif type(km[i]) == type(["test"]):
            name = km[i][0]
        else:
            error("element in 'keuzemenu' isn't a list or a string")
        print(str(i+1)+": "+name) ## e.g. '1: Drivers'

def ChooseMenu(m, i, path):
    i += 1
    printKeuzeMenu(m, len(path))
    if i > 15:
        print("\ntry to enter a valid number :(\n")
    answer = input("choose a menu: ")

    ## if choice is to terminate program
    if answer == "0" and len(path) == 0:
        while True:
            clearterminal()
            ans = input("Are you sure you want to exit the program? (y/n): ")
            if (ans.lower() == "y" or ans.lower() == "yes"):
                CloseProgram(0)
            elif (ans.lower() == "n" or ans.lower() == "no"):
                clearterminal()
                return ChooseMenu(m, i-1, path)
            
    try:
        ## try if answer is an integer
        answer = int(answer) - 1
        if answer >= 0 and answer < len(m):
            ## if it is a valid answer
            if (type(m[answer]) == type('string')):
                ## if there is only one path available,
                path.append(answer)
                return path
            if (type(m[answer]) == type(["test"])):
                ## if there are more paths available, continue choosing menu's
                path.append(answer)
                m = m[answer]
                m.remove(m[0])
                clearterminal()
                return ChooseMenu(m, i, path)
            ## if m[answer] somehow isn't a list or string
            error("m[answer] isn't a list or string!")
        clearterminal()
        print("Sorry! This menu doesn't exist! Try typing a number from a menu instead.")
        return ChooseMenu(m, i, path)
    except:
        clearterminal()
        print("Sorry! This isn't an integer! Try typing the number before the menu.")
        return ChooseMenu(m, i, path)
    
## ------------------------------------------------------
## ------------------ END MENU SCRIPT -------------------
## ------------------------------------------------------

## ------------------------------------------------------
## ----------------- VISUAL SCRIPTS ---------------------
## ------------------------------------------------------
    
def VisualizePrint(substrings, modifiers):
    if len(substrings) == 0:
        return
    sorted(substrings, key=len)
    for i in range(len(substrings[0])):
        substring = ""
        for table in substrings:
            try:
                ## if it has an element
                substring += str(table[i]) + " | "
            except:
                ## if it ran out of elements
                pass
        substring = substring[:-3] ## get rid of last " | "
        if "gold-silver-bronze" in modifiers:
            if i == 1:
                print(colors.yellow+substring+colors.ENDL)
            elif i == 2:
                print(colors.lightgrey+substring+colors.ENDL)
            elif i == 3:
                print(colors.brown+substring+colors.ENDL)
            else:
                print(substring)
        else:
            print(substring)
    
def Visualize(datas):
    clearterminal()

    modifiers = []
    # look for special modifiers
    while type(datas[-1]) == type("str"):
        modifiers.append(datas[-1])
        datas.remove(datas[-1])

    # calculate space being taken from each element from data
    maxis = []
    for index in range(len(datas)):
        maxis.append([])
        for e in datas[index]:
            for i in range(len(e)):
                try:
                    if len(str(e[i])) > maxis[index][i]:
                        maxis[index][i] = len(str(e[i]))
                except:
                    maxis[index].append(len(str(e[i])))

    # make separate substrings
    substrings = []
    for index in range(len(datas)):
        substrings.append([])
        # for every data table
        maxi = maxis[index]
        for i in range(len(maxi)):
            maxi[i] = "{:<"+str(maxi[i])+"}"
        
        BASEsubstring = ""
        maxisubstring = ""
        for i in range(len(datas[index][0])):
            BASEsubstring += r"{} "
            maxisubstring += f"maxi[{i}], "
        maxisubstring = maxisubstring[:-2]
        BASEsubstring.strip()
        BASEsubstring = eval(f"BASEsubstring.format({maxisubstring})")
        ## substring looks something like '{:3}, {:30}, {:5}'
        for e in datas[index]:
            # for every line of data
            elementsubstring = ""
            for element in e:
                elementsubstring += f"'{element}', "
            elementsubstring = elementsubstring[:-2]
            substring = eval(f"BASEsubstring.format({elementsubstring})")
            substrings[index].append(substring)
    
    ## print substrings
    while len(substrings) > 0:
        currentsubstrings = []
        currentsize = 0
        for i in range(len(substrings)):
            currentsize += len(substrings[0][0])
            if currentsize <= os.get_terminal_size().columns:
                currentsize += 3 # this is the size of the separator symbol " | "
                currentsubstrings.append(substrings[0])
                substrings.remove(substrings[0])
            else:
                break
        VisualizePrint(currentsubstrings, modifiers)

## ------------------------------------------------------
## --------------- END VISUAL SCRIPTS -------------------
## ------------------------------------------------------

## ------------------------------------------------------
## ------------------ MENU OPTIONS ----------------------
## ------------------------------------------------------

## -------------------- OPTION 1 ------------------------

def Season():
    answer = int
    while True:
        answer = input("Enter the year (1958-2023): ")
        try:
            answer = int(answer)
            if (answer > 2023):
                clearterminal()
                print("This season hasn't been completed yet")
                continue
            if (answer < 1958):
                clearterminal()
                print("The year you entered is too early! Try a later year.")
                continue
            break
        except:
            clearterminal()
            print("Sorry! This isn't an integer! Try typing a number between 1958 and 2023")
    year = answer

    # get driver standings
    data = [["POS", "Driver","Points"]]
    clearterminal()
    for row in cur.execute("SELECT position_text, driver_id, points FROM season_driver_standing WHERE year == "+str(year)):
        row = list(row)
        data.append(row)

    # Replace driver_id with driver name. e.g. "max-verstappen" with "Max Verstappen"            
    for i in range(len(data)):
        for name in cur.execute("SELECT name FROM driver WHERE id == '"+str(data[i][1])+"'"):
            data[i][1] = name[0]

    data2 = [["POS", "Constructor","Points"]]

    # get constructor standings
    for row in cur.execute("SELECT position_number, constructor_id, points FROM season_constructor_standing WHERE year == "+str(year)):
        row = list(row)
        if not str(row[0]).isdigit():
            row[0] = "DSQ"
        data2.append(row)

    # Replace constructor_id with full constructor name. e.g. "ferrari" with "Scuderia Ferrari"
    for i in range(len(data2)):
        for name in cur.execute("SELECT full_name FROM constructor WHERE id == '"+str(data2[i][1])+"'"):
            data2[i][1] = name[0]
    
    # Print to terminal
    Visualize([data, data2, "gold-silver-bronze"])

## -------------------- OPTION 2 ------------------------

def MultipleSeasons():
    answer = int
    while True:
        answer = input(f"Enter two years spaced by a '-' (1958-2023, max difference: {os.get_terminal_size().lines - 5} years): ")
        try:
            answer = answer.split("-")
            begin = min(int(answer[0]), int(answer[1]))
            end = max(int(answer[0]), int(answer[1]))
            if (end > 2023):
                clearterminal()
                print("At least one of the seasons you've entered hasn't been completed yet")
                continue
            if (begin < 1958):
                clearterminal()
                print("At least one of the years you entered was too early! Try a later year.")
                continue
            if abs(begin - end) > os.get_terminal_size().lines - 5:
                clearterminal()
                print(f"The difference between years is too big! (max: {os.get_terminal_size().lines - 5})")
                continue
            break
        except:
            clearterminal()
            print("Sorry! This isn't an integer! Try typing two numbers with a '-' between 1958 and 2023. e.g. '2000-2001'")
    data = [["Year", "Winner", "Points"]]
    
    # Select all winners from the years specified by the user
    clearterminal()
    for row in cur.execute("SELECT year, driver_id, points FROM season_driver_standing WHERE position_number == 1 AND year >= "+str(begin)+" AND year <= "+str(end)):
        row = list(row)
        data.append(row)

    # Replace driver_id with driver name. e.g. "max-verstappen" with "Max Verstappen"
    for i in range(len(data)):
        for name in cur.execute("SELECT name FROM driver WHERE id == '"+str(data[i][1])+"'"):
            data[i][1] = name[0]

    # Print to terminal
    Visualize([data])

## ------------------------------------------------------
## ----------------- END MENU OPTIONS -------------------
## ------------------------------------------------------

## ------------------------------------------------------
## ---------------------- MAIN --------------------------
## ------------------------------------------------------

def main():
    while True:
        ## defining a custom menu format.
        keuzemenu = [
            "Circuits",
            "Drivers",
            "Teams",
            ["Seasons",
                "Overview of a specific year",
                "Small overview for multiple years",
            ],
        ]

        clearterminal()
        ## ask user which data to show.
        chosenmenupath = ChooseMenu(keuzemenu, 0, [])
        clearterminal()

        match chosenmenupath:
            case [3,0]:
                ## get user requested season
                Season()
            case [3,1]:
                ## get user requested seasons
                MultipleSeasons()
            case _:
                ## couldn't find path
                error("Couldn't find specified path: "+str(chosenmenupath))

        WaitForUserInput()

StartUp()
main()
