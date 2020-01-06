import os


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

def countFilesInFolder(folder):
    files = os.listdir(folder)
    cntfile = 0
    cntfolder = 0
    for file in files:
        if os.path.isdir(file):
            cntfolder = cntfolder + 1
        else if os.path.isfile(file):
            cntfile = cntfile + 1
    return (cntfile,cntfolder)
        
