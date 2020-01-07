import csv
import sys
import you_get
import time
import random

WORKSPACE="/home/andy/temp/"


def loadcsv(file):
    ls=[]
    with open(file, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in csvreader:
            ls.append(row)
    return ls

def begindownload():
    ls=loadcsv("/home/andy/workspace/crawler/crawler/dwn.csv")
    lstdownloaded=[item[0] for item in ls]
    print("%d items had been downloaded" % len(lstdownloaded))

    ls=loadcsv("/home/andy/workspace/crawler/crawler/tbd.csv")
    # ls = loadcsv("/home/andy/workspace/crawler/crawler/zipai.csv")
    lsttobedownload=[item[0] for item in ls]
    print("%d items need to be downloaded" % len(lsttobedownload))

    cnt=0
    for obj in lsttobedownload:
        cnt = cnt + 1
        if obj.startswith("#"):
            continue

        if obj in lstdownloaded:
            continue

        if obj.startswith("http://bbsimg.qq.com"):
            continue

        if not obj.startswith("http://"):
            continue

        print("downloading  %d/%d: %s ..." % (cnt,len(lsttobedownload),obj))
        try:
            sys.argv=["you-get","-o","/home/andy/temp/zipai",obj]
            you_get.main()
        except Exception as except:
            print("Failed, info:{}".format(except)
        # time.sleep(random.random()*2)
        lstdownloaded.append(obj)

if __name__ == "__main__":
    begindownload()
