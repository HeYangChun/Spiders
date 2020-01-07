import os
import sys

def fileAppend(file, content):
    with open(file,"a") as fw:
        fw.write(content+"\n")

def readFile(file):
    if not os.path.exists(file):
        return []

    with open(file,"r") as fr:
        #last is a "\n", remove it
        return [ str[0:-1] for str in list(fr) ]

def convert2Filename(url):
    specialChar=['~',
                 '`',
                 '!',
                 '@',
                 '#',
                 '$',
                 '%',
                 '^',
                 '&',
                 '*',
                 '(',
                 ')',
                 '|',
                 '\\',
                 ',',
                 '/',
                 '?',
                 ':',
                 ';',
                 '"',
                 '<',
                 '>',
                 '.',
                 ]
    for sc in specialChar:
        url=url.replace(sc,"")

    return url


def cntfilesinfolder(folder):
    files =  os.listdir(folder)
    cntfiles = 0
    cntfolders = 0
   
    for file in files:
        file = os.path.join(folder, file)
        if os.path.isfile(file):
            cntfiles = cntfiles + 1
            
        if os.path.isdir(file):
            cntfolders = cntfolders + 1
            (tcntfile,tcntfolder) = cntfilesinfolder(file)
            cntfiles = cntfiles + tcntfile
            cntfolders = cntfolders + tcntfolder
    
    return (cntfiles,cntfolders)


if __name__ == "__main__":
    
    if len(sys.argv) <= 1:
        print("please input objective folder")
        exit()
        
    folder =  sys.argv[1]
    (filecnt,foldercnt) = cntfilesinfolder(folder)
    print("%d files and %d folders in %s" % (filecnt,foldercnt,folder))