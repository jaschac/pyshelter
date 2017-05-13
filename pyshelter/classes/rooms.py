# -*- coding: utf-8 -*-

'''
The Rooms class holds all the rooms that are part of the Vault. Rooms have a
size, an upgrade level  Some may be inhabited by living beings; others are
purely utilities. Each Room has a location, defined through row and col. The 
'Entrance' and 'FakeWasteland' rooms always exist.

A couple of mappings are provided to support other classes. One maps the unique
ID of a room to its index in the raw's list; the other maps the ID to a
friendly room name which also reveals its relative location.
'''

from collections import defaultdict
from pprint import pprint as pp
from string import ascii_uppercase

from pyshelter.utils.io import load_static_data


class Rooms(list):
    '''
    The Rooms class represents all the rooms of the Vault. They are stored as a
    list of dictionaries.
    '''
    def __init__(self, raw_data=None):
        """
        Initializes the Rooms.
        """
        if raw_data is None:
            raise ValueError('The Rooms are expected to be provided data.')
        if not isinstance(raw_data, list):
            raise TypeError("The Rooms are expected as a list, not %s."       \
                % (type(raw_data).__name__))
        for raw_data_entry in raw_data:
            if not isinstance(raw_data_entry, dict):
                raise TypeError("Each Room must be provided as a dictionary, "\
                "not %s." % (type(raw_data_entry).__name__))
            if "col" not in raw_data_entry.keys():
                raise TypeError("A Room must have a 'col' attribute.")
            if "deserializeID" not in raw_data_entry.keys():
                raise TypeError("A Room must have a 'deserializeID' "         \
                    "attribute.")
            if "dwellers" not in raw_data_entry.keys():
                raise TypeError("A Room must have a 'dwellers' attribute.")
            if "level" not in raw_data_entry.keys():
                raise TypeError("A Room must have a 'level' attribute.")
            if "mergeLevel" not in raw_data_entry.keys():
                raise TypeError("A Room must have a 'mergeLevel' attribute.")
            if "mrHandyList" not in raw_data_entry.keys():
                raise TypeError("A Room must have a 'mrHandyList' attribute.")
            if "row" not in raw_data_entry.keys():
                raise TypeError("A Room must have a 'row' attribute.")
            if "type" not in raw_data_entry.keys():
                raise TypeError("A Room must have a 'type' attribute.")

        super(Rooms, self).__init__(raw_data)


    def id_to_index(self, value=None):
        '''
        Lazily returns the index of a room given its unique ID.
        '''
        if value is None:
            raise ValueError('The room unique ID is expected.')
        if not isinstance(value, int):
            raise TypeError("The room ID is expected as an int, not %s."      \
                % (type(value).__name__))

        if not hasattr(self, '_ids_to_index'):
            self._ids_to_index = {room['deserializeID'] : i                    \
                for i, room in enumerate(self)}
        try:
            return self._ids_to_index[value]
        except KeyError:
            raise


    def id_to_nice_name(self, value=None):
        '''
        Lazily returns the nice name of a room given its unique ID.
        '''
        if not hasattr(self, '_ids_to_nice_name'):

            # map type to rows to col and ID
            rooms_by_type_per_floor = defaultdict(lambda : defaultdict(list))
            for room in self:
                rooms_by_type_per_floor[room["type"]][room['row']].append(
                    {'deserializeID':room['deserializeID'],'col':room['col']})

            # sort rooms on the same floor by column
            for room_type, rows in rooms_by_type_per_floor.items():
                for row in rows:
                    sorted(rooms_by_type_per_floor[room_type][row],
                        key = lambda room: room['col'])

            static_data_rooms = load_static_data('rooms')

            # map ID to nice name
            self._ids_to_nice_name = defaultdict(str)
            for room_type, rows in rooms_by_type_per_floor.items():
                for i, row in enumerate(rows):
                    for j, room in enumerate(rows[row]):
                        self._ids_to_nice_name[room['deserializeID']] =       \
                            "%s %s%s" % (static_data_rooms[room_type]['name'], i+1, ascii_uppercase[j])

        try:
            return self._ids_to_nice_name[value]
        except KeyError:
            raise
