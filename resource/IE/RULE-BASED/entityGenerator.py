
def generateEntity(pathFile,fileName):

    folderData = pathFile
    folderHasil = "./OUTPUT/"
    #namaFile = "12Pid.B2015.PNJktTim.txt"
    namaFile = fileName
    namaFileHasil = "O-"+namaFile

    file_putusan = open(folderData+namaFile, "r", encoding='UTF8')
    baca_baris = file_putusan.readlines()
    #print(baca_baris)
    #print(len(baca_baris))

    terdakwa = 0
    tindak_pidana = 0
    hukuman = 0
    nomor_putusan = 0

    file_hasil = open(folderHasil+namaFileHasil, "w", encoding='UTF8') 

    for baris in baca_baris:
        panjang_baris = len(baris)
        if panjang_baris > 3:
            baris=baris.lower()
            #print(baris)
            #print("panjang baris :", panjang_baris)

            # mendapatkan nomor putusan
            if baris.find("pid.b") >= 0 and nomor_putusan == 0:
                nomor_putusan +=1
                if baris.find("nomor :") >= 0:
                    cari_nomor = baris.find("nomor :")+8
                elif baris.find("no") >= 0:
                    cari_nomor = baris.find("no")+4
                print("Nomor Putusan : ", baris[cari_nomor:panjang_baris])
                file_hasil.write("Nomor Putusan : "+baris[cari_nomor:panjang_baris])
                
            # mendapatkan terdakwa
            if baris.find("nama terdakwa :") >= 0:
                terdakwa += 1
                cari_terdakwa = baris.find("nama terdakwa :")+16
                print("Terdakwa Ke : ", terdakwa)
                print("Nama Terdakwa : ", baris[cari_terdakwa:panjang_baris])
                file_hasil.write("Terdakwa Ke : "+str(terdakwa)+"\n")    
                file_hasil.write("Nama Terdakwa : "+baris[cari_terdakwa:panjang_baris]+"\n")

            elif baris.find("nama lengkap :") >= 0:
                terdakwa += 1
                cari_terdakwa = baris.find("nama lengkap :")+14
                print("Terdakwa Ke : ", terdakwa)
                print("Nama Terdakwa : ", baris[cari_terdakwa:panjang_baris])
                file_hasil.write("Terdakwa Ke : "+str(terdakwa)+"\n")    
                file_hasil.write("Nama Terdakwa : "+baris[cari_terdakwa:panjang_baris]+"\n")
                
            # Komponen TINDAK PIDANA
            cari_pidanaTO = baris.find("menyatakan terdakwa")
            #print("cari pidana : ", cari_pidana)        
            if cari_pidanaTO >=0:
                cari_pidanaT = baris.find("bersalah melakukan tindak pidana")
                cari_pidana1T = baris.find("sebagaimana")
                cari_kuhpT = baris.find("pasal")
                cari_kuhp1T = baris.find("kuhp")
                
                if tindak_pidana == 0:
                    tindak_pidana += 1
                    print("TUNTUTAN")
                    print("Tindak Pidana : ", baris[cari_pidanaT+32:cari_pidana1T-1])
                    print("Melanggar KUHP : ", baris[cari_kuhpT:cari_kuhp1T])

                    file_hasil.write("TUNTUTAN\n")    
                    file_hasil.write("Tindak Pidana : "+baris[cari_pidanaT+32:cari_pidana1T-1]+"\n")
                    file_hasil.write("Melanggar KUHP : "+baris[cari_kuhpT:cari_kuhp1T]+"\n")    

                else:
                    print("PUTUSAN")
                    print("Tindak Pidana : ", baris[cari_pidanaT+32:cari_pidana1T-1])

                    file_hasil.write("PUTUSAN\n")    
                    file_hasil.write("Tindak Pidana : "+baris[cari_pidanaT+32:cari_pidana1T-1]+"\n")

            # mendapatkan PIDANA HUKUMAN

            if baris.find("menjatuhkan pidana") >= 0:
                cari_hukuman1T = baris.find("selama")+6
                if hukuman == 0:
                    hukuman += 1
                    print("Tuntutan Pidana : ", baris[cari_hukuman1T:panjang_baris])
                    file_hasil.write("Tuntutan Pidana : "+baris[cari_hukuman1T:panjang_baris]+"\n")
                else:
                    print("Hukuman Pidana : ", baris[cari_hukuman1T:panjang_baris])
                    file_hasil.write("Hukuman Pidana : "+baris[cari_hukuman1T:panjang_baris]+"\n")

            elif baris.find("menghukum terdakwa") >= 0:
                cari_hukuman1T = baris.find("selama")+6
                if hukuman == 0:
                    hukuman += 1
                    print("Tuntutan Pidana : ", baris[cari_hukuman1T:panjang_baris])
                    file_hasil.write("Tuntutan Pidana : "+baris[cari_hukuman1T:panjang_baris]+"\n")
                else:
                    print("Hukuman Pidana : ", baris[cari_hukuman1T:panjang_baris])
                    file_hasil.write("Hukuman Pidana : "+baris[cari_hukuman1T:panjang_baris]+"\n")

      
            # mendapatkan HAKIM KETUA MAJLIS HAKIM
            cari_hakim = baris.find("diputuskan dalam")
            if cari_hakim >= 0:
                cari_tgl_putusan = baris.find("tanggal")
                cari_tgl_putusan1 = baris.find("oleh")

                if baris.find(", se") >= 0:
                    cari_hakim_ketua1 = baris.find(", se")
                else:
                    cari_hakim_ketua1 = baris.find(". se")

                if baris.find("oleh kami") >= 0:
                    oleh = 9
                else:
                    oleh = 5

                if baris.find("ketua majelis hakim, ") >= 0:  
                    cari_hakim_anggota1 = baris.find("ketua majelis hakim, ")+21
                elif baris.find("hakim ketua majelis, ") >=0:    
                    cari_hakim_anggota1 = baris.find("hakim ketua majelis, ")+21
                elif baris.find("hakim ketua, ") >=0:
                    cari_hakim_anggota1 = baris.find("hakim ketua, ")+13

                cari_hakim_anggota2 = baris.find("masing")            
                hakim_anggota = baris[cari_hakim_anggota1:cari_hakim_anggota2-1]
                hakim_anggota1 = hakim_anggota[0:hakim_anggota.find(" dan")]
                hakim_anggota2 = hakim_anggota[hakim_anggota.find(" dan")+5:len(hakim_anggota)]

                if baris.find("dibantu oleh") >= 0:
                    cari_panitera1 = baris.find("dibantu oleh")+13
                else:    
                    cari_panitera1 = baris.find("dibantu")+8

                if baris.find("sebagai panitera pengganti") >= 0:              
                    cari_panitera2 = baris.find("sebagai panitera pengganti")
                elif baris.find("panitera pengganti") >= 0:              
                    cari_panitera2 = baris.find("panitera pengganti")
                    
                if baris.find("dihadiri oleh") >= 0:
                    cari_penuntut_umum1 = baris.find("dihadiri oleh")+13
                elif baris.find("dihadiri") >= 0:
                    cari_penuntut_umum1 = baris.find("dihadiri")+9    

                if baris.find("jaksa penuntut umum") >= 0:
                    cari_penuntut_umum2 = baris.find("jaksa penuntut umum")
                elif baris.find("penuntut umum") >= 0:
                    cari_penuntut_umum2 = baris.find("penuntut umum")    
                
                print("Tanggal Putusan : ", baris[cari_tgl_putusan+8:cari_tgl_putusan1])
                print("Hakim Ketua : ", baris[cari_tgl_putusan1+oleh:cari_hakim_ketua1])
                print("Hakim Anggota 1 : ", hakim_anggota1)
                print("Hakim Anggota 2 : ", hakim_anggota2)
                print("Panitera : ", baris[cari_panitera1:cari_panitera2])
                print("Penuntut Umum : ", baris[cari_penuntut_umum1:cari_penuntut_umum2])

                file_hasil.write("Tanggal Putusan : "+baris[cari_tgl_putusan+8:cari_tgl_putusan1]+"\n")
                file_hasil.write("Hakim Ketua : "+baris[cari_tgl_putusan1+oleh:cari_hakim_ketua1]+"\n")    
                file_hasil.write("Hakim Anggota 1 : "+hakim_anggota1+"\n")
                file_hasil.write("Hakim Anggota 2 : "+hakim_anggota2+"\n")    
                file_hasil.write("Panitera : "+baris[cari_panitera1:cari_panitera2]+"\n")
                file_hasil.write("Penuntut Umum : "+baris[cari_penuntut_umum1:cari_penuntut_umum2]+"\n")    


        #print(baris)
    file_putusan.close()
    file_hasil.close()
    berhasil = "\nExtraksi Informasi dari Dokumen Putusan Pengadilan Berhasil\n" 
    return berhasil
