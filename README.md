# DMOSEncoder

Use this library to encode/decode files to DMOS using LDPC.


## Encode
See Example_Encode.py 

### Import the library

from DMOSEncoder.DMOS_encode import *

sourceFile = "Title.txt"  # File to encode

encoded = "Encoded.txt" # Encoded file

encoder = "LDPC_768_PR"  # LDPC encoder for 768 bits codeword

msgSize = 72*8  ## 72 bytes message, 576 bits

codeSize = 96*8 ## 96 bytes codeword, 768 bits  

#### Create the encoder
Enc = DMOSEnc()

Enc.LDPC_N = codeSize  # Set the parameters

Enc.outputFile = encoded

#Encode the file
Enc.encodeFile_LDPC_DMOS(sourceFile, encoder)



## Decode
See Example_decode.py 

#### To obtain the binary contents from a DNA Pool, it requires the C++ library from https://github.com/SBMI-LAB/DMOSDecoder

This example uses either an encoded file generated directly with DMOS encoder, or the output from the C++ library.

### Import the library
from DMOSEncoder.DMOS_decode import *


sourceFile = "Encoded.txt"  # File to decode

decoded = "Decoded.txt" # Decoded file

encoder = "LDPC_768_PR"  # LDPC encoder for 768 bits codeword

msgSize = 72*8  ## 72 bytes message, 576 bits

codeSize = 96*8 ## 96 bytes codeword, 768 bits  

#### Create the decoder
Dec = DMOSDec()

Dec.LDPC_N = codeSize  # Set the parameters

Dec.outputFile = decoded

#Decode the file

##### Use this command to decode the file directly from the DMOS encoder

Dec.decoFileLDPC(sourceFile, encoder)

##### Use this command to decode the file from the output of the C++ library

Dec.decRawLDPC(sourceFile, encoder)
