Experimental Program: exp1.py

---------------------------------------------------------------------------
exp1.py <temp> <time> <pump duty cycle>

or 

exp1.py

This uses default settings
--------------------------------------------------------------------------

This program is intended to measure the difference in temerperature between 
the herms section of the mash system and the mash tun itself.  This will
give a measure of the thermal properties of the system.  Given that a 
1500W element is used, the rate of change in the temperature of the mash
tun will indicate the system loss rate or in other words efficiency.

For 15 kg of water, a 1500W element should increase the temperature by
approximately 1.4 *C per minute.  I had measured a loss of 4.5 *C from the
mash tun (Mash King) in 1 hour, for about 0.075 *C/min.  I will estimate
that the system should be able to raise the temperature of the mash 1 *C
per minute.  

The pump duty cycle may have something to do with the rate, so this
must be investigated.  If the pump is not pushing water through fast enough,
the heater hit its temperature and shut off with no heat transfer occurring.
since this could at most happen for a few seconds at a time, this may only
lead to a small loss of efficiency.  The reason the pump needs to be cycled
is that the mash can become stuck causing damage to the pump and halting
the mash process.  If the pump is only run intermittantly there is less 
chance of this happening.  This can be mitigated by increasing the roller
distance of the grain crusher.  This must also be watched as too wide a 
grind will result in low mash efficiency and hazy wort (particulate).

Results of this experiment will be written to a file called results.txt
   
