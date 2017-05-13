# -*- coding: utf-8 -*-

'''
The Dwellers class represents the human inhabitants of the Vault. It references
the top-level key 'dwellers'.
'''

from collections import defaultdict
from pprint import pprint as pp

from pyshelter import Dummy


class Dwellers(list):
    '''
    The Dwellers class represents the human inhabitants of the Vault.
    '''
    def __init__(self, raw_data=None):
        """
        Initializes the Dwellers of the Vault.
        """
        if raw_data is None:
            raise ValueError('Dwellers expects raw_data to be provided.')
        if not isinstance(raw_data, list):
            raise TypeError("Dwellers expects raw_data as a list, "           \
                "not %s." % (type(raw_data).__name__))

        super(Dwellers, self).__init__(raw_data)


    def id_to_index(self, dweller_id=None):
        '''
        Lazily returns the index of a Dweller given its unique ID.
        '''
        if dweller_id is None:
            raise ValueError('The Dweller unique ID is expected.')
        if not isinstance(dweller_id, int):
            raise TypeError("The Dweller ID is expected as an int, not %s."   \
                % (type(dweller_id).__name__))

        if not hasattr(self, '_ids_to_index'):
            self._ids_to_index = {dweller['serializeId'] : i                  \
                for i, dweller in enumerate(self)}

        try:
            return self._ids_to_index[dweller_id]
        except KeyError:
            raise


    @property
    def homonyms(self):
        '''
        Returns a dictionary of Dwellers (ID, name, surname) having the same
        name and surname.
        ''' 
        homonyms = defaultdict(list)
        for dweller in self:
            homonyms["%s %s" % (dweller['name'],                              \
                dweller['lastName'])].append(dweller['serializeId'])

        return {name_surname:ids for name_surname, ids in homonyms.items()    \
            if len(ids) > 1}


    def reset_dweller(self, dweller_index):
        '''
        Resets a Dweller's experience and health to level 1, given its index.
        '''
        try:
            self[dweller_index]["experience"] = {
                "accum": 0,
                "currentLevel": 1,
                "experienceValue": 605.0,
                "needLvUp": False,
                "storage": 0,
                "wastelandExperience": 0
            }
            self[dweller_index]["health"] = {
                "healthValue": 105.0,
                "lastLevelUpdated": 1,
                "maxHealth": 105.0,
                "permaDeath": False,
                "radiationValue": 0.0
            }
        except IndexError as e:
            print("There is no Dweller with ID %s." % (dweller_index))
            raise
