import os
import re

class UCR(object):
	data = {}
	def __init__(self, usi_path):
		dumpfile = os.path.join(usi_path, 'info', 'ucr-dump')
		with open(dumpfile, 'r') as fin:
			for line in fin:
				key, value = line.split(': ', 1)
				self.data[key.strip()] = value.strip()
	
	def get(self, key, default=None):
		if key in self.data:
			return self.data[key]
		return default

	def getall(self, re_key):
		cre = re.compile(re_key)
		ret = {}
		for key in self.data:
			if cre.match(key):
				ret[key] = self.data[key]
		return ret

	def is_true(self, **kwargs):
		''' Test if UCR key = value
		.is(nameserver1='127.0.0.1', hostname='localhost')

		Returns false if one condition is not true
		'''
		for key, val in kwargs.iteritems():
			if not self.get(key) == val:
				return False
		return True

# vim: set ts=4 sw=4 tw=0 noet :
