# -*- coding: utf-8 -*-

'''
The Resources class represents the current values of the resources available in
the Vault: Caps, Food, Energy, etc. All values are provided as floats, even if
they are presented to the end-user as integers.
'''


class Resources(dict):
    '''
    The Resources class represents the current values of the resources
    available in the Vault.
    '''
    def __init__(self, raw_data=None):
        """
        Initializes the Resources of the Vault. The data is stored in a
        dictionary, which is mandatory.
        """
        if raw_data is None:
            raise ValueError('Resources requires raw_data to be provided.')
        if not isinstance(raw_data, dict):
            raise TypeError("Resources requires raw_data to be provided as a "\
                "dictionary, not %s." % (type(raw_data).__name__))

        super(Resources, self).__init__(raw_data)

        self.caps = self['Nuka']
        self.food = self['Food']
        self.quantum = self['NukaColaQuantum']
        self.radaways = self['RadAway']
        self.stimpacks = self['StimPack']
        self.water = self['Water']

    @property
    def caps(self):
        '''
        Returns the currently available caps.
        '''
        return self._caps


    @caps.setter
    def caps(self, value=None):
        '''
        Updates the currently available caps.
        '''
        if value is None:
            raise ValueError('The available caps must be provided.')
        if not isinstance(value, (int, float)):
            raise TypeError("The available caps must be provided as a float,  \
                not as %s." % (type(value).__name__))
        self._caps = value


    @property
    def food(self):
        '''
        Returns the currently available food.
        '''
        return self._food


    @food.setter
    def food(self, value):
        '''
        Updates the currently available food.
        '''
        if value is None:
            raise ValueError('The available food must be provided.')
        if not isinstance(value, (int, float)):
            raise TypeError("The available food must be provided as a float,  \
                not as %s." % (type(value).__name__))
        self._food = value


    @property
    def quantum(self):
        '''
        Returns the currently available quantum.
        '''
        return self._quantum


    @quantum.setter
    def quantum(self, value):
        '''
        Updates the currently available quantum.
        '''
        if value is None:
            raise ValueError('The available quantum must be provided.')
        if not isinstance(value, (int, float)):
            raise TypeError("The available quantum must be provided as a float,\
                not as %s." % (type(value).__name__))
        self._quantum = value


    @property
    def radaways(self):
        '''
        Returns the currently available radaways.
        '''
        return self._radaways


    @radaways.setter
    def radaways(self, value):
        '''
        Updates the currently available radaways.
        '''
        if value is None:
            raise ValueError('The available radaways must be provided.')
        if not isinstance(value, (int, float)):
            raise TypeError("The available radaways must be provided as a "   \
                "float, not as %s." % (type(value).__name__))
        self._radaways = value


    @property
    def stimpacks(self):
        '''
        Returns the currently available stimpacks.
        '''
        return self._stimpacks


    @stimpacks.setter
    def stimpacks(self, value):
        '''
        Updates the currently available stimpacks.
        '''
        if value is None:
            raise ValueError('The available stimpacks must be provided.')
        if not isinstance(value, (int, float)):
            raise TypeError("The available stimpacks must be provided as a "   \
                "float, not as %s." % (type(value).__name__))
        self._stimpacks = value


    @property
    def water(self):
        '''
        Returns the currently available water.
        '''
        return self._water


    @water.setter
    def water(self, value):
        '''
        Updates the currently available water.
        '''
        if value is None:
            raise ValueError('The available water must be provided.')
        if not isinstance(value, (int, float)):
            raise TypeError("The available water must be provided as a "       \
                "float, not as %s." % (type(value).__name__))
        self._water = value