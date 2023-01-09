# -*- coding: utf-8 -*-
import os
import math
import subprocess


class LDPC:
    
    designs = "LDPC_768_PR"
    codelength =  768
    messagesize = 576
    Valid = False
    
    def setEncoder(self, codelength, variant = "PR"):

        self.designs = "LDPC_" + str(codelength) + "_" + variant
        
    def encodehex(self, message):
        messagebin = bytearray.fromhex(message)
        encoded = self.encodebin(messagebin)
        
        encoded = self.textbinToBinary(encoded)
        return encoded
    
    def encodetext(self, message):
        messagebin = message.encode()
        encoded = self.encodebin(messagebin)
        return encoded
    
    def encodebin(self, message):
        encoded = self.encodeLDPC(message)
        return encoded
    
    def decodehex(self, codeword):
        binaryBlock = self.decodebin(codeword)
        outHex = ""
        for bdata in binaryBlock:
            outHex += hex(bdata)[2:]
        return outHex
    
    def decodetext(self, codeword):
        binaryBlock = self.decodebin(codeword)
        outText = binaryBlock.decode('utf-8')
        return outText
    
    def decodebin(self, codeword):
        
        bcodeword = self.byteTobinStr(codeword)
        
        ncode = []
        
        N = math.ceil(len(bcodeword)/self.codelength)
        
        for k in range(N):
            ncode.append( bcodeword[k*self.codelength : self.codelength*(k+1)]  )
        
        
        decoded = self.decodeLDPC(ncode)
        binaryBlock = bytearray()
        
        for s in decoded:        
            binaryBlock += int(s, 2).to_bytes(len(s) // 8, byteorder='big')
        
        return binaryBlock
        
    
    def textbinToBinary(self, code):
        
        binaryBlock = bytearray()
        for s in code:        
            binaryBlock += int(s, 2).to_bytes(len(s) // 8, byteorder='big')
        
        return binaryBlock
        
    
    def byteTobinStr(self, code):
        salida = ""
        for byten in code:
             nd = format(byten, '#010b')[2:]
             salida += nd
        return salida 
    
    def adjust(self,text):
        """
        Adjust the length of an input text to the 8 byte constrain for Reed Solomon
        """
        n = len(text)
        
        adj = ""
        
        if n <= 8:
            for k in range(8-n):
                adj += chr(0)
        
        text = text +  adj.encode()
        return text
    
    def checkMsgSize(self, msg):
        FlagN = True
        if len(msg) < self.messagesize:
            d = self.messagesize - len(msg)
            for k in range(d):
                if FlagN:
                    msg += "0"
                else:
                    msg += "1"
#                FlagN = not FlagN
        return msg
    
    def encodeLDPC(self, content):
        DevPath = "/home/acroper/Documents/NCAT/Research/DMOS/DMOS_System/FECC/LDPC"
        ldpc_path = os.path.join(DevPath,'ProtographLDPC','LDPC-library')
        ldpc_designs = os.path.join(DevPath,'ProtographLDPC','Designs')
        
        
        pathdir = "/tmp/LDPC/"
        
        if not os.path.exists(pathdir):
            os.makedirs(pathdir)

        ### Create groups of n bits
        
        nb = self.messagesize/8
        
        n = math.ceil(len(content)/nb)
        
        words = []
        
        ### Message for LDPC
        filename =os.path.join(pathdir,"message.txt") 
        f = open( filename , 'w')        
        
        for k in range(n):
            ## Adjust to 16 bytes
            i1 =int(nb*k)
            i2 = int(nb*k+nb)
            grp = self.adjust(content[i1: i2] )
            msg = self.byteTobinStr(grp)
            msg = self.checkMsgSize(msg)
            f.write(msg + "\n")
#            print(grp)
            
        

#        f.write(message)
        f.close()    
        
        src_file = os.path.join(pathdir,"message.txt")
        out_path = os.path.join(pathdir,"encoded.txt")
        
        pchk_file = os.path.join(ldpc_designs, self.designs+".pchk")
        gen_file = os.path.join(ldpc_designs, self.designs+".gen")
    
        ldpc_encode_path = os.path.join(ldpc_path, 'encode.py')
        
        
            # first perform the encoding
        subprocess.run("python3 " + ldpc_encode_path + ' --pchk-file ' + pchk_file + ' --gen-file ' + gen_file +
                       ' --input-file ' + src_file + '  --output-file ' + out_path, shell=True)
        
#        print("python3 " + ldpc_encode_path + ' --pchk-file ' + pchk_file + ' --gen-file ' + gen_file +
#                       ' --input-file ' + src_file + '  --output-file ' + out_path)
        
        # try:
        f = open(out_path,'r')
        encoded = f.read().splitlines()
        f.close()
        try:
            os.remove(out_path)
            os.remove(out_path+".unpunctured")
        except:
            None
        #     f = open(out_path+".unpunctured",'r')
        #     encoded = f.read().splitlines()
        #     f.close()
            
        
        return encoded     
        
               
        
    def decodeLDPC(self, codeword):
        designs = self.designs
        DevPath = "/home/acroper/Documents/NCAT/Research/DMOS/DMOS_System/FECC/LDPC"
        ldpc_path = os.path.join(DevPath,'ProtographLDPC','LDPC-library')
        ldpc_designs = os.path.join(DevPath,'ProtographLDPC','Designs')
        
        extractDir=os.path.join(DevPath, "ProtographLDPC", "LDPC-codes")  
        extract_path = os.path.join(extractDir,"extract")
        
        pchk_file = os.path.join(ldpc_designs, designs+".pchk")
        gen_file = os.path.join(ldpc_designs, designs+".gen")
    
        ldpc_decode_path = os.path.join(ldpc_path, 'decode.py')
        
        
        ### Save the binary strings for decoder
        pathdir = "/tmp/LDPC/"
        
        if not os.path.exists(pathdir):
            os.makedirs(pathdir)
        
        ## Files used by the decoder
        received =os.path.join(pathdir,"received.txt")      ## Encoded message received
        decoded =os.path.join(pathdir,"decoded.txt")        ## Decoded message - after error correction
        recovered =os.path.join(pathdir,"recovered.txt")    ## Recovered binary file
        
        if os.path.isfile(recovered):
            os.remove(recovered)
        
        if os.path.isfile(decoded):
            os.remove(decoded)
        
        if os.path.isfile(received):
            os.remove(received)
            
#        print(filename)
        f = open( received , 'w')
        for line in codeword:
            if len(line) == self.codelength:
                f.write(line + "\n")
        f.close()    
        
        
            # first perform the decoding
        process = subprocess.Popen("python3 " + ldpc_decode_path + ' --pchk-file ' + pchk_file + ' --received-file ' + received +
                       '  --output-file ' + decoded + "  --channel bsc --channel-parameters 0.0001 --max-iterations 20000", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        results = process.stderr.readlines()
        nr = results[0].decode()
        
        print(nr)
        
        dOp = nr.split(" ")
        dB = dOp[1]
        vB = dOp[3]

        if dB == vB:
            self.Valid = True
        else:
            self.Valid = False
        
        if "01" not in designs:
            decoded = os.path.join(pathdir,"decoded.txt.unpunctured")
        
        
        subprocess.run( extract_path + " " + gen_file + " " + decoded + " " + recovered,  shell=True)
        
        f = open(recovered,'r')
        mrecovered = f.read().splitlines()
        f.close()
        # mrecovered=mrecovered[0:-1]
        
        if os.path.isfile(recovered):
            os.remove(recovered)
        
        
        return mrecovered 


#ldpc = LDPC()
#
#res = ldpc.encodehex(key)
#print(res)
#
#deco = ldpc.decodehex(res)
#print(deco)
#if key == deco:
#    print("Match!")