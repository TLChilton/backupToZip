#! python3
# backupToZip.py - Allows command line zipping and unzipping of folders

import zipfile, os, sys, re, zlib

# Handles zipping files
def backupToZip(folder):
    # Back up the entire contents of "folder" into a ZIP file.

    folder = os.path.abspath(folder)    # make sure folder is absolute

    if os.path.exists(folder):
        # Figure out the filename this code should use based on
        # what files already exist
        number = 1
        while True:
            zipFilename = os.path.basename(folder) + '_' + str(number) + '.zip'
            if not os.path.exists(zipFilename):
                break
            number = number + 1

        if os.walk(folder):
            # Create the ZIP file.
            print(f'Creating {zipFilename}...')
            backupZip = zipfile.ZipFile(zipFilename, 'w')

            # Walk the entire folder tree and compress the files in each folder.
            for foldername, subfolders, filenames in os.walk(folder):
                print(f'Adding files in {foldername}...')
                # Add the current folder to the ZIP file.
                backupZip.write(foldername)

                for filename in filenames:
                    newBase = os.path.basename(folder) + '_'
                    if filename.startswith(newBase) and filename.endswith('.zip'):
                        continue  # don't back up the backup ZIP files
                    backupZip.write(os.path.join(foldername, filename), compress_type=zipfile.ZIP_DEFLATED)
            backupZip.close
            print('Done.')
    else:
        print ("ERROR: %s does not exist" % folder)

# Handles unzipping files
def unZipFolder(folder):
    filePattern = re.compile(r"^(.*)(.zip)$", re.VERBOSE)

    folder = os.path.abspath(folder)    # Convert the inputted path to an absolute path
    if os.path.exists(folder):
        mo = filePattern.search(folder)
        folderName = mo.group(1)        # We don't want the .zip extension

        newName = folderName + "_unzipped"

        # Check for if an unzipped folder by our name already exists
        # If it does exist an incremented name is created
        number = 1
        while True:
            if not os.path.exists(newName):
                break
            newName = folderName + '_unzipped_' + str(number) 
            number = number + 1

        print("Unzipping to %s..." % newName)
        unZip = zipfile.ZipFile(folder)
        unZip.extractall(newName)
        print("Done.")

    else:
        print ("ERROR: %s does not exist" % folder)

# Main, handles the command line arguments
if len(sys.argv) == 2:
    backupToZip(sys.argv[1])
    sys.exit()
elif len(sys.argv) == 3 and sys.argv[1] == "unzip":
    unZipFolder(sys.argv[2])
else:
    print("Usage:")
    print("       tzip [folder name]       - compresses that folder")
    print("       tzip unzip [folder name] - unzips that folder")
    sys.exit()


