# DMOS Encoder/Decoder library

It is a Python library to encode/decode files to and from DMOS. 

The encoder generates a file with the list of mutations to apply to each DMOS register and the output file is human readable.

The Encoder/Decoder uses LDPC for error-correction, from https://github.com/shubhamchandak94/ProtographLDPC .

The decoder recovers the binary file from the encoded file, it requires the DMOS Decoder C++ library https://github.com/SBMI-LAB/DMOSDecoder to retrieve the binary contents from nanopore sequencing analysis. 


## Prerequisites

Python 3

xlrd 

ProtographLDPC 

See https://shubhamchandak94.github.io/ProtographLDPC/installation.html to compile ProtographLPDC



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
