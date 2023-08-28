import sys, os
slot_table = "Best Push,Sink Fast,Once Uncut,Twice Uncut,Once Ok,Twice Ok,Gambler,Anti-Arrows,Sleeping Pill,Guts,Outstanding,Float Reverse,Vibration Up 1,Vibration Down 1,Smell Up 1,Smell Down 1,Light Up 1,Light Down 1,Sound Up 1,Sound Down 1,Vibration Up 2,Vibration Down 2,Smell Up 2,Smell Down 2,Light Up 2,Light Down 2,Sound Up 2,Sound Down 2,Vibration Up 3,Vibration Down 3,Smell Up 3,Smell Down 3,Light Up 3,Light Down 3,Sound Up 3,Sound Down 3".split(",")
item_table = "Cicada Shell,Dragonfly Wing,Waterweed,Leaf,White Flower,Orange Flower,Pink Flower,Unknown Fossil A,Rain Crystal,Beautiful Small Stone,Fang,Bird Wing,Emerald,Ruby,Piece of Ruin A,Piece of Ruin B,Diamond,Squid Grass,Tree Honey,Ancient Tools A,Ancient Tools B,Tin Toy,Aquamarine,Scent Bag,Nut,Propeller Grass,Weight,Turquoizo Husk,Crystallized Thunder,Piece of Shooting Star,Stray Shooting Star,Unknown Fossil B,Ancient Water,Shrimp Barbel,Button,Small Fire,Sapphire,Ancient Spoon,Mysterious Lithograph 1,Mysterious Lithograph 2,Mysterious Lithograph 3,Bone A,Bone B,Big Fallen Leaf,Honey,Snail Shell,Pearl,Small Web,Wooden Board,Aromatic Mushroom,Fountainhead Water,Golden Apple,Pebble,Cheese,Scorpion Trail,Green Axe Carapace,Small Mountain,Small Wind,Balloon Flower,Dried Nuts,Tackle Box,Rod,Diary,Diary Page,Recipe".split(",")
environments = "The Lost Ruins,The Missing Jungle,The Big Tree,The Dish Pond,The Haunted Cave,The Bush River,Map 6,The Pocket Sea,The Final Jungle".split(",")
lures = "Dragonflew,Froggy,Quest Worm,Pointer,Cicadar,Glass Star,Rain Dolphin,Emerald Leaf,Spinny Fin,Shad Blade,Dig Deep,Frogger,Hopper,Shooting Flower,Bug Worm,Kraken,Femme,Squid Lure,Lily,Old Stuff,Laura,Flame Toy,Ballith,Squiddy,Spinnow,Ballista,Jeweler,Buster,Sharky,Tifoss,Daram,Rabbit,Kurokuro,Verge,Scorpy,Buzz,Death Witch,Buggy".split(",")
env_count = len(environments)
lurecount = len(lures)
debug = False

for i in range(256-len(environments)):
    environments.append("Invalid (ID: " + str(i+env_count) + ")")
for i in range(256-len(lures)):
    lures.append("Invalid (ID: " + str(i+lurecount) + ")")
lures[255] = "No lure"
def process_file(filename, mode, slot_sel, output):
    with open(filename, 'rb') as f:
        byte_s = f.read(7)
        empty = False
        if not byte_s:
            return
        try:
            if not byte_s.decode("ascii") == "BuzzRod":
                print("Not a BuzzRod game save")
                return
            else:
                f.seek(slot_sel*0x820+8)
                empty = not int.from_bytes(f.read(1), "little") == 3
                if empty:
                    print("This save is empty.")
                    return
                if mode == "area":
                    f.seek(slot_sel*0x820+0xC)
                    area = int.from_bytes(f.read(1), "little")
                    print(environments[area] + " (ID: " + str(area) + ", bytes: " + hex(slot_sel*0x820+0xC) + ", " + hex(slot_sel*0x820+0x21F) + ")")
                    return
                if mode[:4] == "list":
                    print("ID".ljust(10), "Name".ljust(30), "Count".ljust(10), "Type".ljust(20), "Byte".ljust(10), "Raw".ljust(5))
                if mode == "list slots" or mode == "list":
                    f.seek(0x589+(slot_sel*0x820))
                    seek = 0x589+(slot_sel*0x820)
                    for i in range(len(slot_table)):
                        byte_s = f.read(4)
                        count = int(int.from_bytes(byte_s, "little") / 2)
                        consumptive = False
                        if count >= 32:
                            count = count - 32
                            consumptive = True
                        if (count > 0 and not consumptive) or debug:
                            print(str(i).ljust(10), slot_table[i].ljust(30), "".ljust(10), "Slot".ljust(20), hex(seek).ljust(10), int.from_bytes(byte_s, "little"))
                        if (count > 0 and consumptive) or debug:
                            print(str(i).ljust(10), slot_table[i].ljust(30), str(count).ljust(10), "Slot (consumptive)".ljust(20), hex(seek).ljust(10), int.from_bytes(byte_s, "little"))
                        seek += 4
                if mode == "list items" or mode == "list":
                    f.seek(0x589+(slot_sel*0x820)+(4*len(slot_table)))
                    seek = 0x589+(slot_sel*0x820)+(4*len(slot_table))
                    for i in range(len(item_table)):
                        byte_s = f.read(4)
                        count = int(int.from_bytes(byte_s, "little") / 2)
                        if count >= 32:
                            count = count - 32
                        if count > 0 or debug:
                            print(str(i).ljust(10), item_table[i].ljust(30), str(count).ljust(10), "Item".ljust(20), hex(seek).ljust(10), int.from_bytes(byte_s, "little"))
                        seek += 4
        except:
            print("Not a BuzzRod game save")

def modify_byte(f, output, index, value):
    with open(output, 'wb') as of:
        f.seek(0)
        idx = 0
        while 1:
            byte_s = f.read(1)
            if not byte_s:
                break
            if not idx == index:
                of.write(byte_s)
            else:
                of.write(value.to_bytes(1, 'little'))
            idx += 1
    print("Changes written to " + output)

def fix_file(filename):
    idx = 8
    output = filename + ".fixed"
    key_bytes = [0x8, 0x828, 0x1048, 0x1868, 0x2088]
    with open(filename, 'rb') as inp:
        with open(output, 'wb') as out:
            # fix save file header
            out.write(str.encode("BuzzRod"))
            out.write(int(0).to_bytes(1, 'little'))
            inp.seek(8)
            size = 8
            while size < 10408:
                byte_s = inp.read(1)
                if not byte_s:
                    break
                if idx in key_bytes and not int.from_bytes(byte_s, "little") == 1:
                    out.write(int(3).to_bytes(1, 'little'))
                else:
                    out.write(byte_s)
                idx += 1
                size += 1
    print("Fixed save file written to " + output)


def list_saves(f):
    print("Slot".ljust(10), "Total weight".ljust(20), "Area".ljust(20), "Date/Time".ljust(30), "Lure".ljust(10))
    for slot_sel in range(5):
        save_loc = (slot_sel*0x820)
        f.seek(save_loc+0xF)
        lure = lures[int.from_bytes(f.read(1), "little")]
        f.seek(save_loc+0x10)
        weight = int.from_bytes(f.read(4), "little")
        f.seek(save_loc+0xC)
        area = environments[int.from_bytes(f.read(1), "little")]
        f.seek(save_loc+0x18)
        date_year = int.from_bytes(f.read(4), "little")
        f.seek(save_loc+0x1C)
        daymonth = int.from_bytes(f.read(4), "little")
        day = int(bin((daymonth >> 4) & 0b1111), 2)
        month = int(bin((daymonth >> 0) & 0b1111), 2)
        f.seek(save_loc+0x1d)
        registers = int.from_bytes(f.read(1), "little")
        add2min = int(bin((registers >> 0) & 0b1), 2) == 1
        add1min = int(bin((registers >> 1) & 0b1), 2)  == 1
        add12hour = int(bin((registers >> 2) & 0b1), 2)  == 1
        add8hour = int(bin((registers >> 3) & 0b1), 2)  == 1
        add2hour = int(bin((registers >> 4) & 0b1), 2)  == 1
        add2hour2 = int(bin((registers >> 5) & 0b1), 2)  == 1
        add1hour = int(bin((registers >> 6) & 0b1), 2)  == 1
        secondhalf = int(bin((registers >> 7) & 0b1), 2)  == 1
        if secondhalf:
            day = day + 16
        hour = 0
        if add12hour: hour += 16
        if add8hour: hour += 8
        if add2hour: hour += 4
        if add2hour2: hour += 2
        if add1hour: hour += 1
        f.seek(save_loc+0x1e)
        minute = ((int.from_bytes(f.read(1), "little") >> 4) & 15) * 4
        if add2min: minute += 2
        if add1min: minute += 1
        full_date = str(date_year).zfill(4) + "/" + str(month).zfill(2) + "/" + str(day).zfill(2)
        full_time = str(hour).zfill(2) + ":" + str(minute).zfill(2)
        print(str(slot_sel+1).ljust(10), (str(weight) + " g").ljust(20), area.ljust(20), (full_date + " " + full_time).ljust(30), lure.ljust(20))
    

def help():
    filename = os.path.basename(__file__)
    print("BuzzRod save file editor 0.3\n")
    print("Switches:\n")
    print("-f [filename]".ljust(45), "Specify the save file, which you want to access")
    print("-o [filename]".ljust(45), "Specify output path for the modified save file")
    print("-save1/-save2/-save3/-save4/-save5".ljust(45), "Selects a specific save slot")
    print("-li".ljust(45), "Lists items in the save file")
    print("-ls".ljust(45), "Lists slots in the save file")
    print("-l".ljust(45), "Lists slots and items in the save file")
    print("-fix".ljust(45), "Fixes broken save file structure, which might allow you to recover a corrupted save")
    print("-p [byte]".ljust(45), "Specify modifiable byte")
    print("-iv [count]".ljust(45), "Writes item count to specified location (check \"Byte\" column when listing items)")
    print("-sv [count]".ljust(45), "Sets slot item to be consumptive and allows you to specify the count")
    print("-nc".ljust(45), "Sets slot item to be non-consumptive")
    print("-a".ljust(45), "Shows the current area on selected save slot")
    print("-v [integer]".ljust(45), "Specifies a value to be written to the byte (do not use this for items or slots)")
    print("-saves".ljust(45), "Displays list of saves")
    print("-h".ljust(45), "Displays help screen")
    print("-d".ljust(45), "Display all values")
    print("-ca".ljust(45), "Change area for a save (Note: player position will not change)")
    print("\nExamples:\n")
    print(filename + " -f BESLES-53236 -li -save2".ljust(65), "Displays items for the second save slot")
    print(filename + " -f BESLES-53236 -a -save3".ljust(65), "Displays current area on third save slot")
    print(filename + " -f BESLES-53236 -ca 0 -save4 -o BESLES-53236.modified".ljust(65), "Sets current area to The Lost Ruins for fourth save slot")
    print(filename + " -f BESLES-53236 -fix".ljust(65), "Try to fix save file")
    print(filename + " -f BESLES-53236 -p 0x6b9 -iv 3 -o BESLES_53236.modified".ljust(65), "Set Mysterious Lithograph 3 count to 3 on save 1")
    print(filename + " -f BESLES-53236 -p 0x589 -nc -o BESLES_53236.modified".ljust(65), "Gives Best push slot item to save 1")
    print(filename + " -f BESLES-53236 -p 0x1f29 -iv 3 -o BESLES_53236.modified".ljust(65), "Set Honey count to 2 on save 4")
    print(filename + " -f BESLES-53236 -p 0x104c -v 6 -o BESLES_53236.modified".ljust(65), "Set current area on save 3 to Map 6 (normally inaccessible area)")
    print(filename + " -f BESLES-53236 -saves".ljust(65), "Display details of every save for easy identification")
def main():
    mode = "file"
    filename = ""
    output = ""
    slot = 0
    index = 0
    value = 0
    lastmode = ""
    patch = False
    charea = False
    fix_corruption = False
    for arg in sys.argv[1::]:
        if mode == "file":
            filename = arg.replace("\"", "")
            mode = lastmode
        elif mode == "output":
            output = arg.replace("\"", "")
            mode = lastmode
        elif mode == "patch":
            if "0x" in arg:
                index = int(arg[2:], 16)
            else:
                index = int(arg)
            patch = True
            mode = lastmode
        elif mode == "charea":
            value = int(arg)
            charea = True
            patch = True
            mode = lastmode
        elif mode == "setval":
            if "0x" in arg:
                value = int(arg[2:], 16)
            else:
                value = int(arg)
            mode = lastmode
        elif mode == "setvalitem":
            value = int(arg) * 2
            mode = lastmode
        elif mode == "setvalslot":
            value = int(arg) + 64
            mode = lastmode
        lastmode = mode
        if arg == "-f":
            mode = "file"
        elif arg == "-d":
            debug = True
        elif arg == "-fix":
            fix_corruption = True
        elif arg == "-p":
            mode = "patch"
        elif arg == "-v":
            mode = "setval"
        elif arg == "-iv":
            mode = "setvalitem"
        elif arg == "-sv":
            mode = "setvalslot"
        elif arg == "-nc":
            value = 2
            mode = lastmode
        elif arg == "-l":
            mode = "list"
        elif arg == "-ca":
            mode = "charea"
        elif arg == "-a":
            mode = "area"
        elif arg == "-ls":
            mode = "list slots"
        elif arg == "-li":
            mode = "list items"
        elif arg == "-f":
            mode = "fix"
        elif arg == "-s":
            mode = "select"
        elif arg == "-save2":
            slot = 1
        elif arg == "-save3":
            slot = 2
        elif arg == "-save4":
            slot = 3
        elif arg == "-save5":
            slot = 4
        elif arg == "-saves":
            with open(filename, "rb") as f:
                list_saves(f)
            return
        elif arg == "-o":
            mode = "output"
        elif arg == "-h":
            help()
            return
    if os.path.exists(filename):
        if fix_corruption:
            fix_file(filename)
            return
        if not patch:
            process_file(filename, mode, slot, output)
        else:
            if charea:
                menu_text = (slot*0x820)+0xc
                area_value = (slot*0x820)+0x21f
                with open(filename, "rb") as f:
                    modify_byte(f, ".temp", menu_text, value)
                with open(".temp", "rb") as f:
                    modify_byte(f, output, area_value, value)
                print("Deleted .temp")
                os.remove(".temp")
            else:
                with open(filename, "rb") as f:
                    modify_byte(f, output, index, value)

if __name__ == "__main__":
    main()
