## This script must be located above DMOSEncoder folder
#
### Encode a Text File to DMOS using LDPC
## Input: Title.txt file
## Output: Encoded.txt file
## The output includes the list of mutations per register

from DMOSEncoder.DMOS_encode import *


sourceFile = "Title.txt"  # File to encode
encoded = "Encoded.txt" # Encoded file

encoder = "LDPC_768_PR"  # LDPC encoder for 768 bits codeword
msgSize = 72*8  ## 72 bytes message, 576 bits
codeSize = 96*8 ## 96 bytes codeword, 768 bits  

## Create the encoder
Enc = DMOSEnc()
Enc.LDPC_N = codeSize  # Set the parameters
Enc.outputFile = encoded

#Encode the file
Enc.encodeFile_LDPC_DMOS(sourceFile, encoder)


### Other encode commands
# encoded = Enc.encodeFileLDPC(sourceFile, encoder): Obtains the binary array of the encoded file
#
# Deprecated commands
# Enc.encodeFileRS(sourceFile): Encode using Reed-Solomon
# Enc.encodeFileRS2D(sourceFile): Encode using 2 layers Reed-Solomon



