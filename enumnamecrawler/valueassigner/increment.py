# -*- coding: utf-8 -*-


class Incrementer(object):
	def __init__(self, base=-1, step=-1, *args, **kwds):
		# type: (int, int) -> None
		super(Incrementer, self).__init__(*args, **kwds)
		if step == 0:
			raise ValueError("step value must != 0: %r" % (step, ))
		self.base = base
		self.step = step

	def _compute_base(self, v_max, v_min):
		if self.step > 0:
			c = v_max
			dstep = self.step - 1
		else:
			c = v_min
			dstep = self.step + 1
		return int((c - self.base + dstep) / self.step) * self.step + self.base

	def __call__(self, enumelements):
		v_max = self.base
		v_min = self.base
		for enumelem in enumelements:
			if enumelem.value is None:
				continue
			aux = enumelem.value
			v_max = max(v_max, aux)
			v_min = min(v_min, aux)
		c = self._compute_base(v_max, v_min)
		for enumelem in enumelements:
			if enumelem.value is not None:
				continue
			enumelem.value = c
			c = c + self.step
