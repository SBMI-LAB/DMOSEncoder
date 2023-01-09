rm *.unpunctured

#~ python3 LDPC-library/make-pchk.py --output-pchk-file myCode.pchk --code-type regular --n-checks 128 --n-bits 640 --checks-per-col 3 --seed 43

python3 LDPC-library/make-pchk.py --output-pchk-file myCode.pchk  --code-type regular --n-checks 373 --n-bits 853 --checks-per-col 3 --fraction-transmitted 0.75 --seed 43

./LDPC-codes/make-gen myCode.pchk myCode.gen sparse

./LDPC-codes/rand-src myMessage.txt 43 480x10

python3 LDPC-library/encode.py --pchk-file myCode.pchk --gen-file myCode.gen --input-file myMessage.txt --output-file myCodewords.txt

./LDPC-codes/transmit myCodewords.txt myReceived.txt 43 bsc 0.001

python3 LDPC-library/decode.py --pchk-file myCode.pchk --received-file myReceived.txt --output-file myDecoded.txt --channel bsc --channel-parameters 0.01

./LDPC-codes/extract myCode.gen myDecoded.txt.unpunctured myExtracted.txt




design=LDPC02  # encoder name

cp myCode.pchk Designs/$design.pchk
cp myCode.pchk.transmitted Designs/$design.pchk.transmitted
cp myCode.gen Designs/$design.gen

