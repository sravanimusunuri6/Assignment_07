#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# Sravani Musunuri, 2020-Aug-14, Updating the file
# Sravani Musunuri, 2020-Aug-20, Updating the file to add pickling and error handling
#------------------------------------------#

import pickle 

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    """Processing the data to add and delete an item from the List of Dictionaries"""
    
    @staticmethod
    def add_item(strID,strTitle,strArtist):
        """Function to manage user input ingestion to a list of dictionaries

        User Input is added to a 2D table.
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            strID (string): ID of CD Inventory
            strTitle (string): Title of CD Inventory
            strArtist (string): Artist of the CD Inventory

        Returns:
            None.
        """
        
        intID = int(strID)
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
        lstTbl.append(dicRow)
        
    @staticmethod 
    def delete_item(lstTbl,intIDDel):
        """Function to manage deletion of an item from a list of dictionaries

        Delete an item by parsing thru the 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            lstTbl (list of dictionaries): List of CD inventories
            intIDDel (int): ID of CD Inventory

        Returns:
            2D table (list of dict).
            
        """
        
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
            
        return lstTbl
    
    pass


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name,table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            2D table (list of dict)
        """
        try:
            with open(file_name, 'rb') as fileObj:
                table = pickle.load(fileObj)
                
        except FileNotFoundError:
            print()
            print('[ERROR] ',file_name,'does not exit in current directory')
            print()
        
        return table

    @staticmethod
    def write_file(file_name, table):
        """Function to manage data ingestion from List of dictionaries to a file.

        Reads the data from 2D table and saves to a file identified by file_name.
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        
        try:
            with open(file_name, 'wb') as objFile:
                pickle.dump(table, objFile)
                
        except FileNotFoundError:
            print()
            print('[ERROR] ',file_name,'does not exit in current directory')
            print()


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""
    
    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice
    
    @staticmethod
    def user_input():
        """Gets user input for CD Inventory

        Args:
            None.

        Returns:
            strID (string): ID of CD Inventory
            strTitle (string): Title of CD Inventory
            strArtist (string): Artist of the CD Inventory

        """
        while True:
            try:
                strID = int(input('Enter ID: ').strip())
                
                if strID <= 0:
                    print()
                    raise Exception('[ERROR] Inventory ID cannot be 0 or less. Please enter valid Inventory details.')
                
                
                strTitle = input('What is the CD\'s title? ').strip()
                
                if strTitle == "":
                    print()
                    raise Exception('[ERROR] CD Title cannot be NULL. Please enter valid Inventory details.')
                
                strArtist = input('What is the Artist\'s name? ').strip()          
                
                
                if strArtist == "":
                    raise Exception('[ERROR] Artist Name cannot be NULL. Please enter valid Inventory details.')

                print()
                
                return strID,strTitle,strArtist
                
            except ValueError:
                print()
                print("[ERROR] That is not an integer! Please enter an integer when prompted to enter ID.")
                print()
                
            except Exception as e:
                print()
                print(e)
                print()

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        try:
            if table == []:
                raise Exception('[WARNING] The 2D Inventory table is empty')
            else:
                print()
                print('======= The Current Inventory: =======')
                print('ID\tCD Title (by: Artist)\n')
                for row in table:
                    print('{}\t{} (by:{})'.format(*row.values()))
                    print('======================================')
                    
        except Exception as e:
            print()
            print(e)
            print()
        
        print()

# 1. When program starts, read in the currently saved Inventory
lstTbl = FileProcessor.read_file(strFileName,lstTbl)

# 2. start main loop
while True:
    
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    
    # 3.2 process load inventory
    if strChoice == 'l':
        
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl = FileProcessor.read_file(strFileName,lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
            
        continue  # start loop back at top.
        
    # 3.3 process add a CD
    elif strChoice == 'a':
        
        #Getting User Input
        strID,strTitle,strArtist = IO.user_input()
        
        #Calling the function to add item to the table
        DataProcessor.add_item(strID,strTitle,strArtist)
        
        #Display the CD Inventory
        IO.show_inventory(lstTbl)
        
        continue  # start loop back at top.
        
    # 3.4 process display current inventory
    elif strChoice == 'i':
        
        IO.show_inventory(lstTbl)
        
        continue  # start loop back at top.
        
    # 3.5 process delete a CD
    elif strChoice == 'd':
        
        #Get Userinput for which CD to delete
        #Display Inventory to user
        IO.show_inventory(lstTbl)
        
        #Ask user which ID to remove
        intIDDel = input('Which ID would you like to delete? ').strip()
        
        try:
            #Ask user which ID to remove
            intIDDel = int(intIDDel)
            
        except ValueError:
            print()
            print("[ERROR] That is not an integer! Please enter an integer when prompted to enter ID.")
            print()
            continue
        
        #Calling the function to delete an item from the Inventory table
        lstTbl = DataProcessor.delete_item(lstTbl,intIDDel)
        
        #Display remaining items in the list.
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
        
    # 3.6 process save inventory to file
    elif strChoice == 's':
        
        #Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        
        print()
        
        #Process choice
        if strYesNo == 'y':
            
            #Calling the function to write Inventory details to a file
            FileProcessor.write_file(strFileName, lstTbl)
            
        else:
            
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
            
        continue  # start loop back at top.
        
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




