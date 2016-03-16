# ##### BEGIN GPL LICENSE BLOCK #####
#
#  SCA Tree Generator, a Blender addon
#  (c) 2013, 2014 Michel J. Anders (varkenvarken)
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

"""  code adoptet from midi_driver072.py bledner add-on : http://blendit.xaa.pl/ 
     by Pawel Adamowicz (adamowicz_pawel0@gmail.com) 
    2016.02.10 Milosz Klosowicz (miklobit@gmail.com) - adaptation for python3, blender 2.7
"""

bl_info = {
    "name": "Midi driver",
    "author": "Milosz Klosowicz (miklobit)",
    "version": (0, 1, 0),
    "blender": (2, 76, 0),
    "location": "View3D > Add > Mesh",
    "description": "Adds a tree created with the space colonization algorithm starting at the 3D cursor",
    "warning": "",
    "wiki_url": "https://github.com/miklobit/blender/wiki",
    "tracker_url": "",
    "category": "Animation driver"}


from .midi import Note, MidiFile

class SyncError(Exception):
    """Exception regarding synchronisation errors.

    Currently one kind of this error is available:
    SRCIPO -- object selected to be synchronise already yields the Ipo
    or Action which was specified as the source - race condition.

    """
    SRCIPO = range(1)
    def __init__(self, _val):
        self.val = _val
    def __str__(self):
        if self.val == self.SRCIPO:
            return "Source Ipo/Action cannot be overwritten"

