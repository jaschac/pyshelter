# -*- coding: utf-8 -*-

'''
The Inventory class represents items that are currently stored in the Vault and
that are not assigned to anyone. These items can be either Junk, Outfits, Pets
or Weapons, and are provided as a list of dictionaries, each with the mandatory
'id' and 'type' keys.
'''


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