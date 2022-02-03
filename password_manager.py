from typing import ParamSpecArgs
from cryptography.fernet import Fernet
from os.path import exists
import os
import sys
import hashlib

#TODO
'''
CHANGE PASSWORD
DELETE PASSWORD
SETTINGS MODE TO CHANGE ENCRYPTION ALGORITHM(?)
'''
#MAKE SURE WE ARE IN THE CORRECT
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#FUNCTION TO GENERATE THE MASTER KEY
def write_key():
    key = Fernet.generate_key()
    with open("key.key","wb") as key_file:
        key_file.write(key)


#FUNCTION TO LOAD THE KEY
def load_key():
    file = open("key.key","rb")
    key = file.read()
    file.close()
    return key

#SEE IF THE KEY FILE EXISTS YET.  IF IT DOES, LOAD IT.  IF NOT, GENERATE AND LOAD IT.
if exists(os.getcwd()+"/key.key"):
    key = load_key()
    fer = Fernet(key)
    print("Loading Key File.......Done!")
else:
    write_key()
    print("Generating New Key File........Done!")
    key = load_key()
    fer = Fernet(key)
    print("Loading Key File.......Done!")
    

#NEXT WE ASK FOR THE MASTER PASSWORD
master_pwd = input("Please enter your master password:")
#ENCODE THE MASTER PASSWORD
master_pwd = master_pwd.encode('utf-8') 
#HASH THE MASTER PASSWORD WITH SHA512
mpw_enc = hashlib.sha512(master_pwd).hexdigest()
#GET THE WORKING FILE NAME
working_file=mpw_enc+".txt"

#PROGRAM LOOP TO CHECK FOR AN EXISTING FILE OR CREATE A NEW ONE
while True:
    if exists(os.getcwd()+"/"+working_file):
        break
    else:
        newfile = input('Warning:  No Match For This Master Password.  Would you like to create a new file or Quit (new, q)?').lower()
        if newfile=="new":
            f = open(working_file, "w")
            f.write("")
            f.close()
        elif newfile == "q":
            print("You have chosen to quit the program.  Goodbye!")
            sys.exit()


#FUNCTIONS TO EITHER VIEW OR ADD PASSWORDS

#VIEW A SPECIFIC PASSWORD
def search():
    search = input ("Please enter the Sitename you wish to search for: ")
     #OPEN THE FILE IN READ ONLY MODE
    with open (working_file, 'r') as f:
        #LOOP THROUGH THE LINES
        for line in f.readlines():
            #STRIP CARRIAGE RETURNS
            data = line.rstrip()
            #SPLIT THE USERNAMES AND PASSWORDS BY THE PIPE
            sitename=''
            username=''
            sitename_converted=''
            sitename, username, password = data.split("|")
            # CONVERT SEARCH AND SITENAME TO FACILITATE MATCH
            # CONVERT SEARCH TO LOWERCASE
            search=search.lower()
            #print("SEARCH VALUE:  "+search+"\n")
            #DECRYPT SITENAME
            #print("SITENAME VALUE:  "+sitename+"\n")
            sitename_converted = fer.decrypt(sitename.encode()).decode()
            #CONVERT TO LOWERCASE
            #print("SITENAME VALUE:  "+sitename_converted+"\n")
            sitename_converted = sitename_converted.lower()
            #SEARCH THROUGH THE LIST
            #IF THE LINE MATCHES:
            if search == sitename_converted:
            #PRINT THE RESULTS
                print("Site: ",fer.decrypt(sitename.encode()).decode(),"\nUsername: ",fer.decrypt(username.encode()).decode(),"\nPassword: ",fer.decrypt(password.encode()).decode())
                #print("Search: ",search," -|- Sitename: ",sitename_converted,'\n')
        print('End of the list reached.  If no results were returned, please checked the spelling of your input.')

#VIEW ALL PASSWORDS
def viewall():
    #OPEN THE FILE IN READ ONLY MODE
    with open (working_file, 'r') as f:
        #LOOP THROUGH THE LINES
        for line in f.readlines():
            #STRIP CARRIAGE RETURNS
            data = line.rstrip()
            #SPLIT THE USERNAMES AND PASSWORDS BY THE PIPE
            sitename, username, password = data.split("|")
            #PRINT THE RESULTS
            print("Site: ",fer.decrypt(sitename.encode()).decode(),"\nUsername: ",fer.decrypt(username.encode()).decode(),"\nPassword: ",fer.decrypt(password.encode()).decode(),"\n")
          

#ADD A PASSWORD
def add():
    account = input ('Sitename:')
    name = input ('Username:')
    pwd = input ('Password:')

    #OPEN THE FILE IN APPEND MODE
    with open (working_file, 'a') as f:
        #WRITE THE USERNAME AND ENCRYPTED PASSWORD
        f.write (fer.encrypt(account.encode()).decode() + "|" + fer.encrypt(name.encode()).decode() + "|" + fer.encrypt(pwd.encode()).decode() + "\n")

#LOOP TO VIEW/VIEWALL/ADD PASSWORDS
while True:
    #ASK THE USER IF THEY WANT TO VIEW EXISTING PASSWORDS, OR ADD A NEW ONE
    mode = input("Would you like to add a password, or view existing ones? (add, viewall, search, or press q to quit)").lower()

    if mode == "q":
        break
    if mode == "search":
        search()
    elif mode == "viewall":
        viewall()
    elif mode == "add":
        add()
    else:
        print('Please select a valid option.')
        #BRINGS THEM BACK TO THE BEGINNING OF THE WHILE LOOP
        continue