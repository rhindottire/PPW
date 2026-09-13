import os
from newEntityGenerator import generateEntity

def main():

    start_path = "./INPUT/"
    hasil_path = "./OUTPUT/"
    listFile = os.listdir(start_path)
    #namaFile = "48Pid.B2015.PNJKTTIM.txt"
    #namaFile = "161Pid.B2015.PNJktTim.txt"
    #generateEntity(start_path, namaFile)

    for eachFile in listFile:
        result = generateEntity(start_path, eachFile)
        print(result)

main();
