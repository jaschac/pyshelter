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


    def dweller_coffee_break(self, dweller_index=None):
        '''
        Sets a Dweller on coffee break. This is achieved setting his savedRoom
        attribute to -1. This also requires iterating the rooms of the Vault,
        finding the one that has the ID of the dweller assigned to it, removing
        that entry.
        ''' 
        if dweller_index is None:
            raise ValueError('The Dweller index is expected.')
        if not isinstance(dweller_index, int):
            raise TypeError("The Dweller index is expected as an int, not %s."   \
                % (type(dweller_index).__name__))

        try:
            dw_id = self.dwellers[dweller_index]['serializeId']
            for room_id, room_dws in shelter.root['happinessManager'].items():
                _room_dws = []
                for dw in room_dws:
                    if dw['dc'] != dw_id:
                        _room_dws.append(dw)
            shelter.root['happinessManager'][room_id] = _room_dws
            self.dwellers[dweller_index]["savedRoom"] = -1
        except Exception as e:
            raise


    def dwellers_bad_weapons(self, min_dmg=16):
        '''
        Returns name and surname of any Dweler holding a weapon whose damage is
        below the minimum threshold set.
        '''
        dws_bad_weapons = []
        for dw in self.dwellers:
            dw_equipped_weapon = dw['equipedWeapon']['id']
            dw_equipped_weapon_dmg = self.sd['Weapon'][dw_equipped_weapon]['dmg']
            dw_equipped_weapon_dmg = int(dw_equipped_weapon_dmg.split('-')[0])
            if dw_equipped_weapon_dmg < min_dmg:
                dws_bad_weapons.append("%s %s" % (dw['name'], dw['lastName']))
        return dws_bad_weapons

    @property
    def dwellers_no_makeup(self):
        '''
        Returns name and surname of any Dweller that did not pass from the
        Barber shop, yet. These do not have the faceMask property.
        '''
        return["%s %s" % (dw['name'], dw['lastName'])
            for dw in self.dwellers if 'faceMask' not in dw]


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

            dweller_stats_sum = sum(stat['value'] \
                for stat in dweller['stats']['stats'][1:])

            if max_health_ratio < float(cutoff) and dweller_stats_sum == 70:
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


    def reset_daily(self, daily_type='lunchbox'):
        '''
        Resets the daily quest, so that it can be replayed again. The daily can
        be reset to be a level 50 lunchbox, weapon, outfit, dweller rescue, or
        pet rescue one. It defaults to a lunchbox.The method first checks if
        there is an history of daily quests. If so, the last one is removed
        from the history and added as a new daily. The quest type is finally
        replaced with the one desired. If no history is present, then the
        current daily's type is replaced.
        '''
        dailies_map = {
            'dweller' : 'Daily_05_Diff_50_C',
            'junk' : 'Daily_03_Diff_50_C',
            'lunchbox' : 'Daily_06_Diff_50_C',
            'outfit' : 'Daily_02_Diff_50_C',
            'pet' : None,
            'weapon' : 'Daily_01_Diff_50_C'
        }

        f_history = self.root['completedQuestDataManager']['dailyQuestPicker']['historyDailies'] != []

        if f_history:
            daily = self.root['completedQuestDataManager']['dailyQuestPicker']['historyDailies'][-1]
            dailies_history = self.root['completedQuestDataManager']['dailyQuestPicker']['historyDailies'][:-1]
            self.root['completedQuestDataManager']['dailyQuestPicker']['historyDailies'] = dailies_history
        else:
            daily = self.root['completedQuestDataManager']['dailyQuestPicker']['currentDailies']
        
        daily['questName'] = dailies_map[daily_type]
        self.root['completedQuestDataManager']['dailyQuestPicker']['currentDailies'] = [daily]


    def reset_weekly(self):
        '''
        Resets the weekly quest so that it is always one that gives a lunchbox.
        '''

        f_history = self.root['completedQuestDataManager']['weeklyQuestPicker']['historyWeeklies'] != []

        if f_history:
            weekly = self.root['completedQuestDataManager']['weeklyQuestPicker']['historyWeeklies'][-1]
            weekly_history = self.root['completedQuestDataManager']['weeklyQuestPicker']['historyWeeklies'][:-1]
            self.root['completedQuestDataManager']['weeklyQuestPicker']['historyWeeklies'] = weekly_history
        else:
            weekly = self.root['completedQuestDataManager']['weeklyQuestPicker']['currentWeeklies']
        
        weekly['questName'] = 'Weekly_05_Diff_54 '
        self.root['completedQuestDataManager']['weeklyQuestPicker']['currentWeeklies'] = [weekly]


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


    def retrain(self, dwellers=0, cutoff=85.0):
        '''
        Identifies N dwellers with max stats that need retrain, resets their
        experience and assigns them to coffee break. Returns name and surname
        of the candidates.
        '''
        dwellers_to_retrain = self.dwellers_to_retrain(cutoff=cutoff)
        dwellers_to_retrain = list(dwellers_to_retrain.values())
        retrained_dwellers = []
        for dweller in dwellers_to_retrain[:dwellers]:
            self.reset_dweller(dweller['index'])
            self.dweller_coffee_break(dweller['index'])
            retrained_dwellers.append("%s %s" % (dweller['name'], dweller['lastName']))
        return retrained_dwellers

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
            dump(self.root, f_output_file, indent=4, separators=(',', ':'))


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