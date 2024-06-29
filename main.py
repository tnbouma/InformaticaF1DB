## ------------------------------------------------------
## --------------------- IMPORT -------------------------
## ------------------------------------------------------

import sqlite3
import os
import time

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
    grey = '\033[38;2;75;75;75m'
    green = '\033[38;2;0;255;0m'

## ------------------------------------------------------
## ------------------ END CLASSES -----------------------
## ------------------------------------------------------

## ------------------------------------------------------
## ----------------- BASIC FUNCTIONS --------------------
## ------------------------------------------------------

# closes program with an errormessage
def error(errormessage):
    CloseProgram(errormessage)

# prints a warning to the terminal, and waits for user to read it
def warning(errormessage, wait):
    print(colors.WARNING+"WARNING: "+str(errormessage)+colors.ENDL)
    if wait:
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

def CheckTerminalSizeManual():
    recommendedterminalwidth = 120
    recommendedterminalheight = 30

    if os.get_terminal_size().columns < recommendedterminalwidth:
        if os.get_terminal_size().lines < recommendedterminalheight:
            warning("Your terminal width and height ("+str(os.get_terminal_size().columns)+", "+str(os.get_terminal_size().lines)+") are lower than recommended! ("+str(recommendedterminalwidth)+", "+str(recommendedterminalheight)+")", False)
        else:
            warning("Your terminal width ("+str(os.get_terminal_size().columns)+") is lower than recommended! ("+str(recommendedterminalwidth)+")", False)
        return 1
    if os.get_terminal_size().lines < recommendedterminalheight:
        warning("Your terminal height ("+str(os.get_terminal_size().lines)+") is lower than recommended! ("+str(recommendedterminalheight)+")", False)
        return 1
    print(colors.green+"terminal height and width are ok!"+colors.ENDL)
    WaitForUserInput()
    return 0

def CheckTerminalSize():
    repeat = False
    if CheckTerminalSizeManual() > 0:
        repeat = input("Do you want to resize your terminal? (y/n): ")
        if repeat.lower() == "y" or repeat.lower() == "yes":
            repeat = True
        else:
            repeat = False
    while repeat:
        if CheckTerminalSizeManual() == 0:
            break


## ------------------------------------------------------
## --------------- END BASIC FUNCTIONS ------------------
## ------------------------------------------------------

## ------------------------------------------------------
## ---------------- START-UP FUNCTIONS ------------------
## ------------------------------------------------------

def StartUp():
    global cur
    global conn

    ## trying to connect database
    script_dir = os.path.dirname(__file__) # <-- Returns parent of main.py (tnbouma_db)
    relative_path = 'f1db.db'
    path = os.path.join(script_dir, relative_path)

    ## making sure the given path leads to our database
    if not (os.path.isfile(path)):
        error("cannot find "+relative_path+" in "+script_dir)

    ## connecting database
    try:
        conn = sqlite3.connect(path) 
    except:
        error("Couldn't open database!, Make sure you are running this program as an admin in the terminal!")
    cur = conn.cursor()

    CheckTerminalSize()


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
        zerofound = False
        substring = ""
        for index in range(len(substrings)):
            table = substrings[index]
            try:
                ## if it has an element
                if (str(table[i]).strip() == "0" or str(table[i]).strip() == "None"):
                    if index == 1 and "Grey1" in modifiers:
                        zerofound = True
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
        elif zerofound:
            print(colors.grey+substring+colors.ENDL)
        else:
            print(substring)

def ColorSubstring(b, e, substring, color):
    beginsubstring = substring[:b]
    cursubstring = substring[b:e]
    endsubstring = substring[e:]

    substring = beginsubstring+color+cursubstring+colors.ENDL+endsubstring
    return substring

def Visualize(datas):

    clearterminal() # <--- Doesn't always clear everything for some reason

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

    indexoffsets = []
    for i in range(len(maxis)):
        indexoffsets.append([])
        dd = 0
        for e in maxis[i]:
            indexoffsets[i].append(dd)
            dd += e + 1

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
                elementsubstring += f'"{element}", '
            elementsubstring = elementsubstring[:-2]
            substring = eval(f"BASEsubstring.format({elementsubstring})")
            if "MultipleYearColor" in modifiers:
                substring = ColorSubstring(indexoffsets[index][5], indexoffsets[index][6], substring, colors.brown)
                substring = ColorSubstring(indexoffsets[index][3], indexoffsets[index][4], substring, colors.lightgrey)
                substring = ColorSubstring(indexoffsets[index][1], indexoffsets[index][2], substring, colors.yellow)
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
        if not str(row[0]).isdigit():
            row[0] = "DSQ"
        else:
            row[0] = "P"+str(row[0])
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
        else:
            row[0] = "P"+str(row[0])
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
    data = [["Year", "1st", "Points", "2nd", "Points", "3rd", "Points"]]
    
    # Select all winners from the years specified by the user
    clearterminal()
    for row in cur.execute("SELECT year, driver_id, points FROM season_driver_standing WHERE position_number == 1 AND year >= "+str(begin)+" AND year <= "+str(end)):
        row = list(row)
        data.append(row)
    for i in range(len(data)-1):
        row = data[i+1]
        for secondrow in cur.execute("SELECT driver_id, points FROM season_driver_standing WHERE position_number == 2 AND year == "+str(row[0])):
            for e in secondrow:
                row.append(e)
        for secondrow in cur.execute("SELECT driver_id, points FROM season_driver_standing WHERE position_number == 3 AND year == "+str(row[0])):
            for e in secondrow:
                row.append(e)
        data[i+1] = row

    # Replace driver_id with driver name. e.g. "max-verstappen" with "Max Verstappen"
    for i in range(len(data)):
        for name in cur.execute("SELECT name FROM driver WHERE id == '"+str(data[i][1])+"'"):
            data[i][1] = name[0]
        for name in cur.execute("SELECT name FROM driver WHERE id == '"+str(data[i][3])+"'"):
            data[i][3] = name[0]
        for name in cur.execute("SELECT name FROM driver WHERE id == '"+str(data[i][5])+"'"):
            data[i][5] = name[0]

    # Print to terminal
    Visualize([data, "MultipleYearColor"])

## -------------------- OPTION 3 ------------------------

def Constructor():
    data = []
    constructors = []
    i = 0
    for row in cur.execute("SELECT id FROM constructor"):
        ## total / (width / average character length) ==> total / maxelements in a row ==> elements in a column
        constructors.append(row[0])
        if i%(183 // (os.get_terminal_size().columns // 20)) == 0:
            data.append([])
        data[-1].append([row[0]])
        i += 1
    
    failed = False
    index = 0
    while True:
        Visualize(data)
        if failed:
            print("Make sure you spelled the name right.")
        ans = input("Choose a Team to inspect (type name): ").lower()
        failed = True
        for i in range(len(constructors)):
            if constructors[i].lower() == ans:
                index = i
                failed = False
                break
        if not failed:
            break
    data = [[["FullName"], ["Country"], ["BestChampionshipPosition"], ["TotalChampionshipWins"], ["TotalRaceStarts"], ["Total(1,2)finishes"], ["TotalPodiums"], ["TotalLaps"], ["TotalPoints"]]]
    for row in cur.execute(f'SELECT full_name, country_id, best_championship_position, total_championship_wins, total_race_starts, total_1_and_2_finishes, total_podiums, total_race_laps, total_championship_points FROM constructor WHERE id == "{str(constructors[index])}"'):
        data.append([])
        row = list(row)
        for i in range(len(row)):
            if i == 1:
                for r in cur.execute(f'SELECT name FROM country WHERE id == "{row[i]}"'):
                    row[i] = r[0] 
            data[-1].append([row[i]])
    data.append([["position from the list"], ["  V  "]]) 
    data.append([["tied with (*) other teams on this stat"], ["  V  "]])
    items = ['best_championship_position', 'total_championship_wins', 'total_race_starts', 'total_1_and_2_finishes', 'total_podiums', 'total_race_laps', 'total_championship_points']
    for i in range(len(items)):
        v = items[i]
        if data[1][i+2][0] == None:
            ## check how many (TOTAL - NOT NULL) to get how many NULL there are.
            for row in cur.execute(f'SELECT COUNT(*) FROM constructor WHERE {v} >= 0'):
                items[i] = row[0]+1
                data[3].append([183 - row[0]])
            continue
        if i == 0: ## less is better
            for row in cur.execute(f'SELECT COUNT(*) FROM constructor WHERE {v} < {int(data[1][i+2][0])}'):
                items[i] = row[0]+1
        else: ## more is better
            for row in cur.execute(f'SELECT COUNT(*) FROM constructor WHERE {v} > {int(data[1][i+2][0])}'):
                items[i] = row[0]+1
        for row in cur.execute(f'SELECT COUNT(*) FROM constructor WHERE {v} == {int(data[1][i+2][0])}'):
            data[3].append([row[0]-1])

            
    for e in items:
        data[2].append([e])

    data.append("Grey1")
    Visualize(data)

## -------------------- OPTION 4 ------------------------

def Driver():
    data = []
    driver = []
    i = 0
    for row in cur.execute("SELECT id FROM driver"):
        ## total / (width / average character length) ==> total / maxelements in a row ==> elements in a column
        driver.append(row[0])
        if i%(901 // (os.get_terminal_size().columns // 30)) == 0:
            data.append([])
        data[-1].append([row[0]])
        i += 1
    
    failed = False
    index = 0
    while True:
        Visualize(data)
        if failed:
             print("Make sure you spelled the name right.")
        ans = input("Choose a Driver to inspect (type name): ").lower()
        failed = True
        for i in range(len(driver)):
            if driver[i].lower() == ans:
                index = i
                failed = False
                break
        if not failed:
            break
    data = [[["FullName"], ["Abbreviation"], ["Number"], ["Nationality"], ["DateOfBirth"], ["BestChampionshipPosition"], ["BestRaceResult"], ["TotalChampionshipWins"], ["TotalRaceWins"], ["Laps"], ["Podiums"], ["TotalPoints"], ["TotalPolePositions"], ["TotalFastestLaps"], ["TotalDriverOfTheDay"]]]
    for row in cur.execute(f'SELECT full_name, abbreviation, permanent_number, nationality_country_id, date_of_birth, best_championship_position, best_race_result, total_championship_wins, total_race_wins, total_race_laps, total_podiums, total_championship_points, total_pole_positions, total_fastest_laps, total_driver_of_the_day FROM driver WHERE id == "{str(driver[index])}"'):
        data.append([])
        row = list(row)
        for i in range(len(row)):
            if i == 3:
                for r in cur.execute(f'SELECT name FROM country WHERE id == "{row[i]}"'):
                    row[i] = r[0] 
            data[-1].append([row[i]])
    data.append([["position from the list"], ["  -  "], ["  -  "], ["  -  "], ["  -  "]]) 
    data.append([["tied with (*) other drivers on this stat"], ["  -  "], ["  -  "], ["  -  "], ["  -  "]])
    items = ["best_championship_position", "best_race_result", "total_championship_wins", "total_race_wins", "total_race_laps", "total_podiums", "total_championship_points", "total_pole_positions", "total_fastest_laps", "total_driver_of_the_day"]
    for i in range(len(items)):
        v = items[i]
        if data[1][i+5][0] == None:
            ## check how many (TOTAL - NOT NULL) to get how many NULL there are.
            for row in cur.execute(f'SELECT COUNT(*) FROM driver WHERE {v} >= 0'):
                items[i] = row[0]+1
                data[3].append([901 - row[0]])
            continue
        if i == 0 or i == 1:
            for row in cur.execute(f'SELECT COUNT(*) FROM driver WHERE {v} < {data[1][i+5][0]}'):
                items[i] = row[0]+1
        else:
            for row in cur.execute(f'SELECT COUNT(*) FROM driver WHERE {v} > {data[1][i+5][0]}'):
                items[i] = row[0]+1
        for row in cur.execute(f'SELECT COUNT(*) FROM driver WHERE {v} == {data[1][i+5][0]}'):
            data[3].append([row[0]-1])

            
    for e in items:
        data[2].append([e])

    data.append("Grey1")
    #clearterminal() ## <-- for some reason it doesn't always clear everything in the Visualize function...
    Visualize(data)

## -------------------- OPTION 5 ------------------------

def Circuit():
    data = []
    circuit = []
    i = 0
    for row in cur.execute("SELECT id FROM circuit"):
        ## total / (width / average character length) ==> total / maxelements in a row ==> elements in a column
        circuit.append(row[0])
        if i%(77 // (os.get_terminal_size().columns // 30)) == 0:
            data.append([])
        data[-1].append([row[0]])
        i += 1
    failed = False
    index = 0
    while True:
        Visualize(data)
        if failed:
             print("Make sure you spelled the name right.")
        ans = input("Choose a Circuit to inspect (type name): ").lower()
        failed = True
        for i in range(len(circuit)):
            if circuit[i].lower() == ans:
                index = i
                failed = False
                break
        if not failed:
            break
    
    data = [[["FullName"],["PreviousNames"],["Type"],["Place"],["Country"],["Latitude"],["Longitude"],["TotalRacesHeld"]]]
    for row in cur.execute(f'SELECT full_name, previous_names, type, place_name, country_id, latitude, longitude, total_races_held FROM circuit WHERE id == "{str(circuit[index])}"'):
        data.append([])
        row = list(row)
        for i in range(len(row)):
            if i == 4:
                for r in cur.execute(f'SELECT name FROM country WHERE id == "{row[i]}"'):
                    row[i] = r[0] 
            if i == 1:
                if row[i] == None:
                    data[0].remove(data[0][1])
                    continue
                if ";" in str(row[i]):
                    allprevnames = str(row[i]).split(";")
                    for i in range(len(allprevnames)):
                        v = allprevnames[i]
                        if i == 0:
                            data[-1].append([v])
                            continue
                        data[0].insert(2, [''])
                        data[-1].append([v])
                    continue
                    
            data[-1].append([row[i]])
    Visualize(data)




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
            case [0]:
                ## get circuit stats
                Circuit()
            case[1]:
                ## get driver stats
                Driver()
            case[2]:
                ## get constructor stats
                Constructor()
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
