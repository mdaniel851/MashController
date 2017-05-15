class Settings:

	hold_temp = 80.0
	offset_big = 3.0
	offset_small = 1.0
	hold_time = 15
	pdc = 75
	p = 1.25
	i = 0.3 	
	d = 1.0

	# original values p = 3, i = 0.4, d = 1.2
	def hold(self,setup):
		if setup == 'big':
			return hold_temp + offset_big
		else:
			return hold_temp + offset_small
