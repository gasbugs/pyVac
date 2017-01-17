__author__ = 'bl4cksh33p'

import sys
def LittleEndianToInt(buf):
    val =0
    for i in range(0, len(buf)):
        multi = 1
        for j in range(0,i):
            multi *= 256
        val += buf[i] * multi
    return val

def MFTHeader(buf):
    MH_Signature = buf[0:4]
    MH_FixupOffset = buf[4:6]
    MH_FixupNumber = buf[6:8]
    MH_LSN = buf[8:16]
    MH_SequenceNum = buf[16:18]
    MH_HardLink = buf[18:20]
    MH_FirstAttribute = buf[20:22]
    MH_Flags = buf[22:24]
    MH_MFTSize = buf[24:28]
    MH_AllocatedMFTSize = buf[28:32]
    MH_FielReference = buf[32:40]
    MH_NextAttrId = buf[40:42]
    MH_Boundary = buf[42:44]
    MH_NumberMFTEntry = buf[44:48]
    
    return LittleEndianToInt(MH_FirstAttribute)

def AttributeHeader(buf):
    AH_TypeID = buf[0:4]
    AH_Length = buf[4:8]
    AH_NRF = buf[8:9]
    AH_NameLen = buf[9:10]
    AH_NameOffset = buf[10:12]
    AH_Flags = buf[12:14]
    AH_AttrID = buf[14:16]
    return AH_NRF

def ResidentAttributeHeader(buf):
    RAH_ContentSize  = buf[0:4]
    RAH_OffsetToContent  = buf[4:6]
    RAH_Flag  = buf[6:7]
    RAH_Unused  = buf[7:8]
    RAH_AttributeName  = buf[8:16]
    return LittleEndianToInt(RAH_OffsetToContent)

def NonResidentAttributeHeader(buf):
    NRAH_StartVCN  = buf[0:8]
    NRAH_EndVCN  = buf[8:16]
    NRAH_RunlistOffset  = buf[16:18]
    NRAH_sizeCompression  = buf[18:22]
    NRAH_Unused  = buf[22:26]
    NRAH_content  = buf[26:32]
    NRAH_RealSize  = buf[32:40]
    NRAH_initialzedSize  = buf[40:48]
    NRAH_AttributeName  = buf[48:56]
    return LittleEndianToInt(NRAH_RunlistOffset)

def StandardInformation(buf):
    SI_CreatedTime  = buf[0:8]
    SI_ModifiedTime  = buf[8:16]
    SI_MFTModifiedTime  = buf[16:24]
    SI_LastAccessedTime  = buf[24:32]
    SI_Flags  = buf[32:36]
    SI_version  = buf[36:40]
    SI_VersionNum  = buf[40:44]
    SI_ClassID  = buf[44:48]
    SI_OwnerID  = buf[48:52]
    SI_SecurityID  = buf[52:56]
    SI_Quota  = buf[56:64]
    SI_USN  = buf[64:72]

def FileName(buf):
    FI_FileReference  = buf[0:8]
    FI_CreatedTime  = buf[8:16]
    FI_ModifiedTime  = buf[16:24]
    FI_MFTModifiedTime  = buf[24:32]
    FI_LastAccesedTime  = buf[32:40]
    FI_AllocatedSize  = buf[40:48]
    FI_RealSize  = buf[48:56]
    FI_Flags  = buf[56:60]
    FI_ReparseValue  = buf[60:64]
    FI_LengthOfName  = buf[64:65]
    FI_Namespace  = buf[65:66]
    return LittleEndianToInt(FI_LengthOfName)

nMFTEntryNum = 0
fp = open('mft','rb')
while True:
    buf = bytearray(fp.read(0x400))
    if buf == '': break
    print nMFTEntryNum
    nOffset = 0
    header = buf[nOffset:nOffset+48]
    nOffset = MFTHeader(header)
    for i in range(0,3):
        Attribute = buf[nOffset:nOffset+16]
        nNextOffset = nOffset
        nOffset += 16
        if(AttributeHeader(Attribute) == 1): # Non Resident Attribute Header
            NRAH = buf[nOffset:nOffset+56]
            nOffset = nNextOffset + NonResidentAttributeHeader(NRAH)
        else: #Resident Attribute Header
            RAH = buf[nOffset:nOffset+16]
            nOffset = nNextOffset + ResidentAttributeHeader(RAH)
        if(Attribute[0] == 0x10): #STANDARD_INFOMAION
            SI = buf[nOffset:nOffset+72]
            #print "STANDARDINFORMATION"
            StandardInformation(SI)
        elif (Attribute[0] == 0x30): #FILE_NAME
            #print "FILENAME"
            FI  = buf[nOffset:nOffset+66]
            filenameOffset = FileName(FI)
            nOffset += 66
            fileName = buf[nOffset:nOffset+filenameOffset*2]
            print fileName 
        else:
            break
        bufAttributeLen = Attribute[4:8]
        nNextOffset += LittleEndianToInt(bufAttributeLen)
        nOffset = nNextOffset

    nMFTEntryNum += 1

        



        
