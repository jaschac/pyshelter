# -*- coding: utf-8 -*-

'''
The PyShelter class represents the interface of the whole application to a
saved Fallout Shelter game. It is responsible to handle I/O as well as to
represent the game data.
'''

from collections import defaultdict
from json import dump, loads
from pprint import pprint as pp

from pyshelter.utils.io import load_static_data


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
        #self.resources = self.root["vault"]["storage"]["resources"]
        #self.vault = self.root['vault']

        self.sd = {
            'Junk' : load_static_data('junk'),
            'Outfit' : load_static_data('outfits'),
            'Weapon' : load_static_data('weapons')
        }


    def drop_expeditions_nornmal_loot(self, quality='normal'):
        '''
        Drops all normal loot collected during Expeditions.
        '''
        for expedition in self.expeditions:

            loot_to_keep = []

            for item in expedition['teamEquipment']['inventory']['items']:
                if self.sd[item['type']][item['id']]['rarity'] not in \
                ('common', 'normal'):
                    loot_to_keep.append(item)
                    continue

            expedition['teamEquipment']['inventory']['items'] = loot_to_keep


    def drop_vault_inventory_junk(self, thr_norm=30, thr_rare=40, thr_legend=50):
        '''
        Drops excess junk from the storage, based on its quality. The method
        iterates over the whole SORTED Inventory, checking types, quality and
        quantity. Items are kept until the conditions are true for a given
        item.
        '''
        items_to_keep = []
        
        item_id = None
        item_count = 0
       
        for item in self.inventory:

            if item['type'] != 'Junk':
                items_to_keep.append(item)
                continue

            if item.get('id') != item_id:
                item_id = item.get('id')
                item_count = 0

            if self.sd['Junk'][item['id']]['rarity'] == 'normal':
                if item_count <= thr_norm:
                    items_to_keep.append(item)

            elif self.sd['Junk'][item['id']]['rarity'] == 'rare':
                if item_count <= thr_rare:
                    items_to_keep.append(item)

            elif self.sd['Junk'][item['id']]['rarity'] == 'legendary':
                if item_count <= thr_legend:
                    items_to_keep.append(item)

            item_count += 1

        self.root["vault"]["inventory"]['items'] = items_to_keep


    def dweller_id_to_idx(self, dweller_id=None):
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
                for i, dweller in enumerate(self.dwellers)}

        try:
            return self._ids_to_index[dweller_id]
        except KeyError:
            raise


    @property
    def dwellers(self):
        '''
        Returns the dwellers tree.
        '''
        return self.root['dwellers']['dwellers']


    @dwellers.setter
    def dwellers(self, value):
        '''
        Updates the dwellers tree.
        '''
        self.root['dwellers']['dwellers'] = value


    def dwellers_to_retrain(self, cutoff=85.0):
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

        for dweller in self.dwellers:

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
                    'index' : self.dweller_id_to_idx(dweller['serializeId']),
                    'lastName' : dweller['lastName'],
                    'name' : dweller['name'],
                    'max_health_ratio' : round(max_health_ratio, 2)
                }

        return dwellers_to_retrain


    @property
    def expeditions(self):
        '''
        Returns the expeditions tree.
        '''
        return self.root['vault']['wasteland']['teams']


    @expeditions.setter
    def expeditions(self, value):
        '''
        Updates the expeditions tree.
        '''
        self.root['vault']['wasteland']['teams'] = value


    @property
    def inventory(self):
        '''
        Returns the inventory tree.
        '''
        return self.root["vault"]["inventory"]['items']


    @inventory.setter
    def inventory(self, value):
        '''
        Updates the inventory tree.
        '''
        self.root["vault"]["inventory"]['items'] = value
        self.root["vault"]["inventory"]['items'].sort(key=lambda x:x['id'])


    def reset_dweller(self, dweller_index):
        '''
        Resets a Dweller's experience and health to level 1, given its index.
        '''
        try:
            self.dwellers[dweller_index]["experience"] = {
                "accum": 0,
                "currentLevel": 1,
                "experienceValue": 605.0,
                "needLvUp": False,
                "storage": 0,
                "wastelandExperience": 0
            }
            self.dwellers[dweller_index]["health"] = {
                "healthValue": 105.0,
                "lastLevelUpdated": 1,
                "maxHealth": 105.0,
                "permaDeath": False,
                "radiationValue": 0.0
            }
        except IndexError as e:
            print("There is no Dweller with ID %s." % (dweller_index))
            raise


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