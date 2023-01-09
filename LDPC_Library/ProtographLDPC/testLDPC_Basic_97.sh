#rm *.unpunctured
#rm *.transmitted

python3 LDPC-library/make-pchk.py --output-pchk-file myCode.pchk --code-type regular --n-checks 745 --n-bits 768 --checks-per-col 6 --seed 43

./LDPC-codes/make-gen myCode.pchk myCode.gen sparse

./LDPC-codes/rand-src myMessage.txt 43 308x10

python3 LDPC-library/encode.py --pchk-file myCode.pchk --gen-file myCode.gen --input-file myMessage.txt --output-file myCodewords.txt

./LDPC-codes/transmit myCodewords.txt myReceived.txt 43 bsc 0.01

python3 LDPC-library/decode.py --pchk-file myCode.pchk --received-file myReceived.txt --output-file myDecoded.txt --channel bsc --channel-parameters 0.01

./LDPC-codes/extract myCode.gen myDecoded.txt myExtracted.txt




design=LDPC_768_97  # encoder name

cp myCode.pchk Designs/$design.pchk
cp myCode.gen Designs/$design.gen

