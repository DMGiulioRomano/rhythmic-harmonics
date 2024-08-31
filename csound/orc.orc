sr=96000
ksmps=32
0dbfs=1
nchnls=2

instr 1
al, ar diskin2 p4, 1
aenv cosseg 0,p3/20,1,p3-p3/40,1,p3/20,0
outs al*aenv,ar*aenv
endin