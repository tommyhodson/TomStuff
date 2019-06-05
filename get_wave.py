from pithy import * # Prof. Steingart has a Python package named `pithy` that is basically a bundle of a bunch of Python packages that we use frequently in lab (e.g. NumPy, SciPy)
import requests as req
from time import sleep,time
import json

# This code is used to connect to our ultrasound equipment, then send out an ultrasonic frequency pulse of sound through the connected battery, and then receieve the output ultrasonic signal and store it as a Python dictionary (a dictionary is a type of Python element, similar to an array but with labels).


# Actual code starts here

settings = json.load(open("files/settings.json")) # this line opens a JSON file containing information related to the equipment that we are trying to connect to
cp = "http://"+settings['nfcp']['ip']+":"+settings['nfcp']['port']+"/" # this line connects the script to the Compact Pulser (cp), which is the machine that sends out the ultrasonic pulse
pico = "http://"+settings['pico']['ip']+":"+settings['pico']['port']+"/" # this line connects the script to the PicoScope (pico), which interprets the output signal 

# we are going to create a Python definiton that will allow us to call a function (named `now`) any time we want to take an ultrasonic 'snapshot' of the battery.
def now(sets,delay=29,voltage=0.03,duration=5,save=False,toDB=None): # the line to define `now` as a function. `sets` is simply the specific settings for the experimental run (it is an input, which is defined later on). `delay` is the delay in microsec for the PicoScope to start recording data, `voltage` is the input voltage to the pulser (changes how much noise there is at output), `duration` is how long in microsec to record after the initial delay. `save` saves a local JSON file of the output (initially set to False, can be set to True) and `toDB` sends the output to our database (again, initially said to None but will be set to our database when actually running)
    for s in sets: req.get(cp+'writecf/%s' % s).text # this writes the settings to the pulser
    sleep(.5)
    
    # below, we create a dictionary, `d`, that contains some information
    d = {}
    d['delay']    = delay     #in us
    d['voltage']  = voltage #in V
    d['duration'] = duration #in us 
    
    # now we pull the output signal from the PicoScope and load it into a dict, `r`
    r = req.post(pico+'get_wave',data=d).text
    req.get(cp+"writecf/P0").text
    r = json.loads(r)
    
    data = array(r['data'])
    # have to mess with the settings to get output time values correct (1st point of output is 0 when it should be the initial delay time)
    t = linspace(d['delay'],d['delay']+d['duration'],len(data))
        
    #log data
    out = {}
    out = d
    out['sets'] = sets
    out['data'] = list(data)
    out['_id']  = time()

    # below saves the file locally, if save is set to True
    fn = "files/acoustic_%i.json" % out['_id']
    if save: json.dump(out,open(fn,'w'))
    
    #return the output dict
    return out

# below is just a way to test the definition `now` that we have created
if __name__ == "__main__":
    #cp_settings
    sets = ['W125','M0','D0','V300','P100']
    
    d = now(sets)
    data = d['data']
    t = linspace(d['delay'],d['delay']+d['duration'],len(data))
    
    plot(t,data)
    xlabel("Time ($\mu s$)")
    ylabel("Amplitude ($V$)")
    
    
    # text(30,0.025,"1")
    # text(48,0.025,"2")
    # text(61,0.025,"3")
    # text(82,0.025,"4")
    
    
    showme()
    clf()

