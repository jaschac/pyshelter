# -*- coding: utf-8 -*-

'''
This module provides I/O utilities to PyShelter.
'''

from yaml import load


def load_static_data(input_filename=None):
	'''
	Returns the data read from the desired static file. Available options are
	'junk', 'outfits', 'rooms' and 'weapons'.
	'''
	if input_filename is None:
		raise ValueError('The name of the file to load must be provided.')
	if not isinstance(input_filename, str):
		raise TypeError("The name of the file to load must be provided as     \
			a string, not %s" % (type(input_filename).__name__))
	if input_filename not in ('junk', 'outfits', 'rooms', 'weapons'):
		raise ValueError("The static data file to load must be either "       \
			"'junk', 'outfits', 'rooms' or 'weapons', not %s."				  \
			% (input_filename))

	try:
		with open("pyshelter/static/%s.yaml" % (input_filename), 'r') as f:
			return load(f)
	except Exception as e:
		print("%s.yaml could not be loaded." % (input_filename))
		raise
