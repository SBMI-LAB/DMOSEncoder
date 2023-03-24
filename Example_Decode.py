## This script must be located above DMOSEncoder folder
#
### Encode a Text File to DMOS using LDPC
## Input: Title.txt file
## Output: Encoded.txt file
## The output includes the list of mutations per register

from DMOSEncoder.DMOS_decode import *


sourceFile = "Encoded.txt"  # File to decode
decoded = "Decoded.txt" # Decoded file

encoder = "LDPC_768_PR"  # LDPC encoder for 768 bits codeword
msgSize = 72*8  ## 72 bytes message, 576 bits
codeSize = 96*8 ## 96 bytes codeword, 768 bits  

## Create the decoder
Dec = DMOSDec()
Dec.LDPC_N = codeSize  # Set the parameters
Dec.outputFile = decoded

#Decode the file

Dec.decoFileLDPC(sourceFile, encoder)

# Other decode commands
# Dec.decodeLDPC(sourceFile, encoder): Obtains the binary array of the decoded file
# Dec.decRawListLDPC(Data, encoder): Uses a list of a list of 16 elements (0s and 1s) as binary source to decode




