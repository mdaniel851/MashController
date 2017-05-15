OVERVIEW
--------------------------------------------------------------------------

*controller.py

The purpose of this software is to implement pid control of a heat exchange
recirculating mash system (HERMS).  The idea is to control a heater in a 
standard kettle to hold a specific temperature.  A copper coil is immeresed
in the hot water bath and water/wort is pumped out of the mash tun through 
that coil and back to the mash tun.      

I am running a python script on a raspberry pi and using the GPIO PWM 
outputs to control the duty cycle of the heater.  For now the pump is just 
allowed to run at its full output since it is relatively small.

