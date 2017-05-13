# -*- coding: utf-8 -*-

'''
The Vault class represents a Vault, a collection of rooms, people and items. It
merely represents a reference to the 'vault' top-level key of the root and, as
such, it subclasses the dict class.
'''

from pprint import pprint as pp

from pyshelter import Rooms

class Vault(dict):
    '''
    The Vault class represents a collection rooms, people and items.
    '''
    def __init__(self, raw_data):
        """
        Initializes a Vault.
        """
        self.update(raw_data)
        self.mode = self["VaultMode"]
        self.name = self["VaultName"]
        self.rooms = self["rooms"]
        self.pets = self["inventory"]["items"]                 # filter in Pets with a lambda
        self.storage = self["inventory"]["items"]             # At this point the rooms are in place. pass in the max storage


    @property
    def mode(self):
        '''
        Returns the gameplay mode.
        '''
        return self._mode


    @mode.setter
    def mode(self, value=None):
        '''
        Updates the gameplay mode.
        '''
        if value is None:
            raise ValueError('The game mode must be provided.')
        if not isinstance(value, str):
            raise TypeError("The game mode is expected as a string, not %s."
                % (type(value).__name__))
        if value not in ('Normal', 'Survival'):
            raise ValueError("The game mode must be either 'Normal' or "      \
                "'Survival', not %s." % (type(value).__name))
        self._mode = value


    @property
    def name(self):
        '''
        Returns the name of the Vault.
        '''
        return self._name


    @name.setter
    def name(self, value=None):
        '''
        Updates the name of the Vault.
        '''
        if value is None:
            raise ValueError('The Vault\'s name must be provided.')
        if not isinstance(value, str):
            raise TypeError("The Vault's name is expected as a string, not %s."
                % (type(value).__name__))
        self._name = value


    @property
    def rooms(self):
        '''
        Returns the rooms of the Vault.
        '''
        return self._rooms


    @rooms.setter
    def rooms(self, value=None):
        '''
        Updates the rooms of the Vault.
        '''
        self._rooms = Rooms(value)
