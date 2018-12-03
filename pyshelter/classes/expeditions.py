# -*- coding: utf-8 -*-

'''
The Expeditions class represents Teams of 1 to 3 Dwellers sent into the
Wasteland to either explore or on a mission. On their time outside the Vault,
the Team can find items, as well as rescue and recruit other Dwellers. Each
Team can carry a maximum number of items. If this limit is hit, the Team is
forced to return to the Vault.
'''

from pyshelter.utils.io import load_static_data


class Expeditions(list):
    '''
    The Expedition class represents Teams of Dwellers sent to the Wasteland.
    '''
    def __init__(self, value=None):
        """
        Initializes the Expedition Teams.
        """
        if value is None:
            raise ValueError('Expedition data must be provided.')
        if not isinstance(value, list):
            raise TypeError("Expeditions mustbe provided as a list, not "\
                "%s." % (type(value).__name__))

        super(Expeditions, self).__init__(value)


    def drop_junk(self, quality='normal'):
        '''
        Drops excess junk collected during Expeditions, based on its quality.
        '''
        sd = {
            'Junk' : load_static_data('junk'),
            'Outfit' : load_static_data('outfits'),
            'Weapon' : load_static_data('weapons')
        }

        for expedition in self:

            loot_to_keep = []

            for item in expedition['teamEquipment']['inventory']['items']:
                if sd[item['type']][item['id']]['rarity'] not in ('common', 'normal'):
                    loot_to_keep.append(item)
                    continue

            expedition['teamEquipment']['inventory']['items'] = loot_to_keep