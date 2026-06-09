### Name: Jazzbear
### Version: 202605131031

# Import the required libraries
import hashlib
import datetime
import json

# Print welcome message
print("Welcome to:\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(r"   __      ____  ____    ___   ")
print(r"  /__\    ( ___)(  _ \  / __)  ")
print(r" /(__)\    )__)  )(_) ) \__ \  ")
print(r"(__)(__)()(__)()(____/()(___/()")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nThe Automated File change Detection System.")

# Declare variables
keepLooping = True
data = []
prevHash = "" ##variable to assist with file change detection

try: ##if the log file already exists load it to data for use and re logging
    readLog = open('log.json','r')
    searchLog = readLog.read() ##reads the log so it can be closed
    readLog.close()
    data = (json.loads(searchLog)) ##temporarily saves log to the data
except:
    pass ##except expects something in it so this just makes sure it passes onto the rest of the program

# Begin main loop
while keepLooping:

    # Ask the user for the file path
    filePath = input('\nEnter the full path of the file to check (example: C:\\test.txt) or [e] to exit: ')

    # Check for exit press
    if filePath.upper() == "E" or filePath.upper() == "EXIT": ##checks for any valid variations to exit
        print("Goodbye!")
        keepLooping = False

    else:
        print("Searching for file...\n")
        try:
            # Try to calculate the SHA256 value of the file by first opening it in bytes mode
            fileToCheck = open(filePath,"rb")
            # Try to calculate SHA hash
            sha256Hash = hashlib.sha256(fileToCheck.read()).hexdigest()
            fileToCheck.close() ##close file after getting it's hash
        except:
            print("File Path could not be found! Please try again.") ##print message to user if file path is invalid
            continue

        
        # Get the time
        timeStamp = str(datetime.datetime.now())

        # Update data
        updateVar = {'file':filePath,'time_stamp':timeStamp,'hash':sha256Hash}
        data.append(updateVar)
        
        #prints logs relivant to the file just entered
        print("Hash calculations to date:")
        for check in data:
            if updateVar['file'] == check['file'] and check['hash'] == prevHash: ##if the 'file' name in the dictionary that is being checked is the same as the one just entered and no hash change
                print(f"File: {check['file']} Time Stamp: {check['time_stamp']} Hash: {check['hash']}")
                prevHash = check['hash']
            elif updateVar['file'] == check['file'] and check['hash'] != prevHash: ##if hash has changed from previous
                print(f"File: {check['file']} Time Stamp: {check['time_stamp']} Hash: {check['hash']}  <File Changed>")
                prevHash = check['hash']
                

      
        
##clear log file while opening it in write mode for the data dump(to keep json formating correctly, creates new file if required)
logFile = open('log.json','w')
##dumps data dictionary in json format to log file then closes the file
json.dump(data,logFile,indent=2)
logFile.close()
