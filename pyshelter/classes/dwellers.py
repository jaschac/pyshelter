# -*- coding: utf-8 -*-

'''
The Dwellers class represents the human inhabitants of the Vault. It references
the key 'dwellers' of the top-level key 'dwellers'. It no longer references
other inhabitants of the Vault, such as pets and/or robots.
'''

from collections import defaultdict
from pprint import pprint as pp


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


    def coffee_break(self, dweller_index=None):
        '''
        Sets a Dweller on coffee break. This is achieved setting his savedRoom
        attribute to -1.
        ''' 
        if dweller_index is None:
            raise ValueError('The Dweller index is expected.')
        if not isinstance(dweller_index, int):
            raise TypeError("The Dweller index is expected as an int, not %s."   \
                % (type(dweller_index).__name__))

        try:
            self[dweller_index]["savedRoom"] = -1
        except Exception as e:
            print(e)
            raise


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


    def to_retrain(self, cutoff=85.0):
        '''
        Returns the Dwellers that are have less than 'cutoff' of their maximum
        potential health. These Dwellers should be reset to level 1, train
        their Endurance to 10, then sent to the Wasteland with a +7 Endurance
        outfit until they reach level 50.

        For each Dweller the following information is returned:
        {id : {name, lastName, level, max_health_ratio, index}}
        '''
        if not isinstance(cutoff, (int, float)):
            raise TypeError("The cutoff must be provided either as an "       \
                "integer or a float, not %s." % (type(cutoff).__name__))

        best_gear_end_bonus = 7
        dwellers_to_retrain = defaultdict(dict)

        for dweller in self:

            dweller_max_health = dweller['health']['maxHealth']

            dweller_max_potential_health = 105 +                              \
                (dweller['experience']['currentLevel'] - 1) *                 \
                (2.5 + 0.5 * (dweller['stats']['stats'][3]['value'] +         \
                    best_gear_end_bonus))

            max_health_ratio = (dweller_max_health * 100) /                   \
                dweller_max_potential_health

            if max_health_ratio < float(cutoff):
                dwellers_to_retrain[dweller['serializeId']] = {
                    'currentLevel' : dweller['experience']['currentLevel'],
                    'index' : self.id_to_index(dweller['serializeId']),
                    'lastName' : dweller['lastName'],
                    'name' : dweller['name'],
                    'max_health_ratio' : round(max_health_ratio, 2)
                }

        return dwellers_to_retrain
