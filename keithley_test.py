from TH_keithley_library import *
import time
from pymongo import MongoClient as mc

# this script runs our potentiostat (a keithley)

# saving output file to a CSV locally (uploading to the database doesn't work at the moment for this script)
fdir = '~/TH_Keithley_Test/'
fn = fdir + '20190604_C10_cyc4_1.csv'

# the set up is a little janky, need to make sure the device if off before turning it on again
off()
on()

# cycle number for the battery (in this case, it was cycle number 4)
cyc=4

# readData connects this script to the keithley, reads output values via a separate script, and then creates a Python dictionary with the output values (have to read twice because if gives an error when connecting the first time)
dat = readData(cyc)
dat = readData(cyc)
# below is just data maniuplation to make sure certain outputs are in the correct format
dlist = []
dlist.append(dat)
pdat = pd.DataFrame(dlist)
# writes outputs to a CSV file named above
pdat.to_csv(fn,mode='a',header=True,index=False)


# below is pretty self-explanatory. setCurrent is a function that sets the current of the keithley, where the firts input (in this case, 0.0) is the current value in Ampres and the second value (in this case, 4.5) is a safety cutoff voltage to stop the current if the voltage of the battery gets too high (can cause fires at that point)

print "starting rest"
#rest
setCurrent(0.0,4.5)
start_time = time.time()
sleep(0.1)
dat = readData(cyc)

current_time = time.time()

# this while loop allows data to be taken every ~2 sec for 1800 seconds
while current_time - start_time < 1800.:
    dat = readData(cyc)
    sleep(0.1)
    appendData(fn,dat)
    current_time = time.time()

print "starting charge"
#charge
setCurrent(0.021,4.5)
start_time = time.time()
sleep(0.1)
dat = readData(cyc)

current_time = time.time()

while current_time - start_time < 40000.:
    dat = readData(cyc)
    sleep(0.1)
    appendData(fn,dat)
    
    # this if statement stops the charging step if the voltage gets to 4.20 V (note the safety cutoff is still 4.5, this is just where we decide to stop this battery charge step)
    if dat['voltage'] > 4.20:
        print current_time - start_time
        break
    
    current_time = time.time()
    

off()

