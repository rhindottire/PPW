import os
from entityGenerator import generateEntity

def main():

    start_path = "./INPUT/"
    hasil_path = "./OUTPUT/"
    daftarFile = os.listdir(start_path)
    #namaFile = "48Pid.B2015.PNJKTTIM.txt"
    #namaFile = "161Pid.B2015.PNJktTim.txt"
    #generateEntity(start_path, namaFile)

    for tiapFile in daftarFile:
        hasil = generateEntity(start_path, tiapFile)
        print(hasil)

main();
