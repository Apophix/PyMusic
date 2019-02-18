def remap(value, oldMin, oldMax, newMin, newMax):
	oldRange = (oldMax - oldMin)
	newRange = (newMax - newMin)
	return (((value - oldMin) * newRange) / oldRange) + newMin
