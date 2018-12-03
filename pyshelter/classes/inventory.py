# -*- coding: utf-8 -*-

'''
The Inventory class represents items that are currently stored in the Vault and
that are not assigned to anyone. These items can be either Junk, Outfits, Pets
or Weapons, and are provided as a list of dictionaries, each with the mandatory
'id' and 'type' keys.
'''

from pprint import pprint as pp

from pyshelter.utils.io import load_static_data


class Inventory(list):
    '''
    The Inventory class represents items that are currently stored in the Vault
    and that are not assigned to anyone.
    '''
    def __init__(self, raw_data=None):
        """
        Initializes the Inventory of the Vault.
        """
        if raw_data is None:
        	raise ValueError('Inventory requires raw_data to be provided.')
        if not isinstance(raw_data, list):
        	raise TypeError("Inventory requires raw_data to be provided as a "\
        		"list, not %s." % (type(raw_data).__name__))
        for raw_data_entry in raw_data:
            if not isinstance(raw_data_entry, dict):
                raise TypeError("Each entry of raw_data is expected as a "    \
                "dictionary, not %s." % (type(raw_data_entry).__name__))
            if 'id' not in raw_data_entry.keys():
                raise KeyError('Each entry of raw_data is expected to have '  \
                'an \'id\' key.')
            if 'type' not in raw_data_entry.keys():
                raise KeyError('Each entry of raw_data is expected to have '  \
                'a \'type\' key.')

        super(Inventory, self).__init__(raw_data)
        self.sort(key=lambda x:x['id'])


    def drop_junk(self, threshold=30):
        '''
        Drops excess junk from the storage, based on its quality. The method
        iterates over the whole Inventory, checking types, quality and
        quantity. Items are kept until the conditions are true for a given
        item.
        '''
        static_data_junk = load_static_data('junk')

        items_to_keep = []
        
        item_id = None
        item_count = 0
       
        for item in self:

            # not junk
            if item['type'] != 'Junk':
                items_to_keep.append(item)
                continue

            # not dropping rare and legendary items
            if static_data_junk[item['id']]['rarity'] != 'normal':
                items_to_keep.append(item)
                continue

            # new item
            if item.get('id') != item_id:
                item_id = item.get('id')
                item_count = 0

            # within limits
            if item_count <= threshold:
                items_to_keep.append(item)
            item_count += 1

        self.__init__(raw_data=items_to_keep)