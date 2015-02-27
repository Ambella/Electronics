import sys
volt=float(sys.argv[1])
maxvolt=2.04
numbits=8
print(volt)
def volt_to_bin(volt,maxvolt,numbits):
   binval=int((volt/maxvolt)*(2**numbits))
   return(binval)

print(bin((volt_to_bin(volt,maxvolt,numbits)<<4)+0b1011000000000000))
print(hex((volt_to_bin(volt,maxvolt,numbits)<<4)+0b1011000000000000))
hexv=list((str(hex((volt_to_bin(volt,maxvolt,numbits)<<4)+0b1011000000000000))))
print(hexv)
for i in range(0,3,2):
   print(i)
   print("{0:04b}".format(int('0x'+str(hexv[2+i])+str(hexv[2+i+1]),16)))


