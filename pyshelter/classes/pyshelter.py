# -*- coding: utf-8 -*-

'''
The PyShelter class represents the interface of the whole application to a
saved Fallout Shelter game. It is responsible to handle I/O as well as to
represent the game data.
'''

from collections import defaultdict
from json import dump, loads
from pprint import pprint as pp

from pyshelter import Dummy, Dwellers, Expeditions, Inventory, Resources, Vault


class PyShelter(object):
    '''
    The PyShelter class represents the interface to a saved Fallout Shelter
    game.
    '''
    def __init__(self, f_in=None):
        '''
        Initializes a PyShelter instance. The class has a root which allows to
        control the whole JSON. All the top-level keys are first turned into
        dummies, which are merely references to subsections of the root, then,
        if needed, initialized as real class instances.
        '''
        self.root = f_in
        self.dwellers = self.root['dwellers']['dwellers']
        self.expeditions = self.root['vault']['wasteland']['teams']
        self.inventory = self.root["vault"]["inventory"]["items"]
        self.resources = self.root["vault"]["storage"]["resources"]
        self.vault = self.root['vault']


    @property
    def dwellers(self):
        '''
        Returns the dwellers tree.
        '''
        return self._dwellers


    @dwellers.setter
    def dwellers(self, value):
        '''
        Updates the dwellers tree.
        '''
        self._dwellers = Dwellers(value)


    @property
    def expeditions(self):
        '''
        Returns the expeditions tree.
        '''
        return self._expeditions


    @expeditions.setter
    def expeditions(self, value):
        '''
        Updates the expeditions tree.
        '''
        self._expeditions = Expeditions(value)


    @property
    def inventory(self):
        '''
        Returns the inventory tree.
        '''
        return self._inventory


    @inventory.setter
    def inventory(self, value):
        '''
        Updates the inventory tree.
        '''
        self._inventory = Inventory(value)


    @property
    def resources(self):
        '''
        Returns the resources tree.
        '''
        return self._resources


    @resources.setter
    def resources(self, value):
        '''
        Updates the resources tree.
        '''
        self._resources = Resources(value)
    


    @property
    def root(self):
        '''
        Returns the root of the JSON.
        '''
        return self._root


    @root.setter
    def root(self, value):
        '''
        Initializes the root of the JSON.
        '''
        if value is None:
            raise ValueError('An input file must be provided.')
        
        with open(value) as f_input_file:
            self._root = loads(f_input_file.read())


    def to_json(self, output_file=None):
        '''
        Writes back the data to the original JSON.
        '''
        with open(output_file, 'w') as f_output_file:
            dump(self.root, f_output_file)


    @property
    def vault(self):
        '''
        Returns the vault tree.
        '''
        return self._vault


    @vault.setter
    def vault(self, value):
        '''
        Updates the vault tree.
        '''
        self._vault = Vault(value)