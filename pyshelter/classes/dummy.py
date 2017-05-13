# -*- coding: utf-8 -*-

'''
The Dummy class represents a generic key of the raw JSON of Fallout Shelter's
save game. It is used to hold data of keys that are not used at all.
'''

class Dummy(object):
    '''
    The Dummy class represents any unused key.
    '''
    def __init__(self, raw_data=None):
        '''
        Initializes a Dummy instance.
        '''
        self._raw_data = raw_data

    @property
    def raw_data(self):
        '''
        Returns the raw JSON data of this key.
        '''
        return self._raw_data

    @raw_data.setter
    def raw_data(self, value):
        '''
        Updates the value of this specific key.
        '''
        if value is not None and not isinstance(dict, list, str):
            raise ValueError("The value is expected as a dictionary, list     \
                or string, or is not expected ad all, not %s."                \
                % (type(value).__name__))
        self._raw_data = value