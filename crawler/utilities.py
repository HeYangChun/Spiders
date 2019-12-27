import os


def fileAppend(file, content):
    with open(file,"a") as fw:
        # fw.read()
        fw.write(content+"\n")

def readFile(file):
    if not os.path.exists(file):
        return []

    with open(file,"r") as fr:
        #last is a "\n", remove it
        return [ str[0:-1] for str in list(fr) ]