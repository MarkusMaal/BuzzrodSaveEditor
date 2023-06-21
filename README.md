# BuzzrodSaveEditor
A simple save file editor, which currently allows you to modify the following:
* Current area
* Number of regular items
* Number of slot items

## Getting the save file out of a PS2 console
To obtain a save file from a real console, you need the following:
* Soft-modded PS2 console (or a way to get to uLaunchELF)
* Flash drive (use USB 2.0 flash drives if possible)
* A PS2 memory card with a Buzzrod save file (duh)
* Computer with a Python 3 compatible OS (Windows, Linux and Mac should work)

To get the save file outside your console do the following:
1. Open uLaunchElf and press circle to open a file browser
2. Go to mc0:/ or mc1:/ (depending on which memory card you have the save on)
3. Now you're going to need to find a folder with the matching game ID. You can find the game ID on the disc case spine or by putting the game disc into your computer and viewing the contents (there should be a file, which starts with SLES or something like that, note that down)
4. Open the folder on your memory card, which matches the game ID
5. It should have 3 files in it: icon.sys, icon.icn and an 11 kilobyte file, which matches the game ID. Highlight it and press R1
6. Select "Copy" from the menu
7. Exit out of the memory card by pressing triangle
8. Go to mass:/, which should have the contents of your flash drive. If it's showing as empty or getting stuck, try a different flash drive.
9. Once you find the desired folder on the flash drive, press R1 to open the menu again and select Paste. This will copy the actual save file, which this program can process, to your flash drive.
10. Once the copying process finishes, unplug the flash drive and plug it into your computer. You should now have access to the save file on your PC.

## Fixing the game breaking bug
This program allows you to get items you need to craft the Buzz lure, thus allowing you to catch Skullcanth and finish the game. To do this, do the following:
1. Open command prompt or terminal
2. Navigate to the folder with your save file and this python script (cd [path of folder])
3. Display a list of items for a specific slot you want to modify. You can do this, by typing `save_editor.py -f [filename] -li -save[slot number]`
4. This should give you a list of items. If you get a message that the slot is empty, try a different one.
5. In the Byte column, note the hex value for Mysterious Lithograph 3 and Honey
6. Run this command: `save_editor.py -f [input_file] -p [hex value for Mysterious Lithograph 3] -iv 3 -o [output_file]`. Output file can be anything except the original filename.
7. Rename the original file to something else and the modified file to the previous name of the original file
8. If you also need Honey, you can run this command: `save_editor.py -f [input_file] -p [hex value for Honey] -iv 1 -o [output_file]`. Output file can be anything except the original filename.
9. Rename the previously modified file to something else and the new modified file to the previous name of the original file
10. Make sure the modified file has the same name as the original file and copy it to your flash drive.
11. Boot up your modified PS2 console and open uLaunchELF
12. Open mass:/ and copy the modified save file
13. Open mc0:/ or mc1:/ and copy the modified save file to the same location, as the original file. Select "Yes" if you see overwrite warnings.
14. Once the copying is complete, you should now be able to boot up the game and load the save file.
15. If loading is successful, you can now load the save. If you open the item book, you should see that you now have all the required ingredients to make the Buzz lure.
