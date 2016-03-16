'''
Created on 10 lut 2016
@author: milosz.klosowicz
'''

# ***** BEGIN GPL LICENSE BLOCK *****
#
# Script copyright (C) Pawel Adawmoicz 
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ***** END GPL LICENCE BLOCK *****
# --------------------------------------------------------------------------


"""  code adoptet from midi_driver072.py bledner add-on : http://blendit.xaa.pl/ 
     by Pawel Adamowicz (adamowicz_pawel0@gmail.com) 
    2016.02.10 Milosz Klosowicz (miklobit@gmail.com) - adaptation for python3, blender 2.7
"""

class Note:
    """Hold data of a single note, have access to the note related constants.
    Instance variables:
    val -- note pitch value
    instr -- id of the instrument
    channel -- id of the a channel
    startT -- the time of the beginning of the note [millisec]
    stopT -- the time of the ens of the note [millisec]
    startVel -- initial velocity of the note
    stopVel -- finishing velocity of the note
    isSelected -- flag marking the selected note
    
    Static constants:
    vals -- dictionary translating the numerical note value to the name of
    the pitch
    instruments -- dictionary translating the numerical note instrument
    value to its name
    
    Public methods:
    __init__
    __cmp__ (overloaded)
    __str__ (overloaded)
    Important:
    Due to the different instrument set and note naming for MIDI channel 10
    (percusion) they are assigned a number above 127 (by adding 128 to
    the actual number)
        
    """    
    vals = {0:"C-2",1:"C#-2",2:"D-2",3:"D#-2",4:"E-2",5:"F-2",6:"F#-2",\
            7:"G-2",8:"G#-2",9:"A-2",10:"A#-2",11:"B-2",12:"C-1",13:"C#-1",\
            14:"D-1",15:"D#-1",16:"E-1",17:"F-1",18:"F#-1",19:"G-1",\
            20:"G#-1",21:"A-1",22:"A#-1",23:"B-1",24:"C",25:"C#",26:"D",\
            27:"D#",28:"E",29:"F",30:"F#",31:"G",32:"G#",33:"A",34:"A#",\
            35:"B",36:"C1",37:"C#1",38:"D1",39:"D#1",40:"E1",41:"F1",\
            42:"F#1",43:"G1",44:"G#1",45:"A1",46:"A#1",47:"B1",48:"C2",\
            49:"C#2",50:"D2",51:"D#2",52:"E2",53:"F2",54:"F#2",55:"G2",\
            56:"G#2",57:"A2",58:"A#2",59:"B2",60:"C3",61:"C#3",62:"D3",\
            63:"D#3",64:"E3",65:"F3",66:"F#3",67:"G3",68:"G#3",69:"A3",\
            70:"A#3",71:"B3",72:"C4",73:"C#4",74:"D4",75:"D#4",76:"E4",\
            77:"F4",78:"F#4",79:"G4",80:"G#4",81:"A4",82:"A#4",83:"B4",\
            84:"C5",85:"C#5",86:"D5",87:"D#5",88:"E5",89:"F5",90:"F#5",\
            91:"G5",92:"G#5",93:"A5",94:"A#5",95:"B5",96:"C6",97:"C#6",\
            98:"D6",99:"D#6",100:"E6",101:"F6",102:"F#6",103:"G6",104:"G#6",\
            105:"A6",106:"A#6",107:"B6",108:"C7",109:"C#7",110:"D7",\
            111:"D#7",112:"E7",113:"F7",114:"F#7",115:"G7",116:"G#7",\
            117:"A7",118:"A#7",119:"B7",120:"C8",121:"C#8",122:"D8",\
            123:"D#8",124:"E8",125:"F8",126:"F#8",127:"G8",\
            163:"Acoustic Bass Drum",164:"Bass Drum 1",165:"Side Stick",\
            166:"Acoustic Snare",167:"Hand Clap",168:"Electric Snare",\
            169:"Low Floor Tom",170:"Closed Hi-Hat",171:"High Floor Tom",\
            172:"Pedal Hi-Hat",173:"Low Tom",174:"Open Hi-Hat",\
            175:"Low-Mid Tom",176:"Hi-Mid Tom",177:"Crash Cymbal 1",\
            178:"High Tom",179:"Ride Cymbal 1",180:"Chinese Cymbal",\
            181:"Ride Bell",182:"Tambourine",183:"Splash Cymbal",\
            184:"Cowbell",185:"Crash Cymbal 2",186:"Vibraslap",\
            187:"Ride Cymbal 2",188:"Hi Bongo",189:"Low Bongo",\
            190:"Mute Hi Conga",191:"Open Hi Conga",192:"Low Conga",\
            193:"High Timbale",194:"Low Timbale",195:"High Agogo",\
            196:"Low Agogo",197:"Cabasa",198:"Maracas",199:"Short Whistle",\
            200:"Long Whistle",201:"Short Guiro",202:"Long Guiro",\
            203:"Claves",204:"Hi Wood Block",205:"Low Wood Block",\
            206:"Mute Cuica",207:"Open Cuica",208:"Mute Triangle",\
            209:"Open Triangle"}

    instruments = {0:"Acoustic Grand Piano",1:"Bright Acoustic Piano",\
               2:"Electric Grand Piano",3:"Honky-tonk Piano",\
               4:"Electric Piano 1",5:"Electric Piano 2",6:"Harpsichord",\
               7:"Clavinet",8:"Celesta",9:"Glockenspiel",10:"Music Box",\
               11:"Vibraphone",12:"Marimba",13:"Xylophone",14:"Tubular Bells",\
               15:"Dulcimer",16:"Drawbar Organ",17:"Percussive Organ",\
               18:"Rock Organ",19:"Church Organ",20:"Reed Organ",\
               21:"Accordion",22:"Harmonica",23:"Tango Accordion",\
               24:"Acoustic Guitar (nylon)",25:"Acoustic Guitar (steel)",\
               26:"Electric Guitar (jazz)",27:"Electric Guitar (clean)",\
               28:"Electric Guitar (muted)",29:"Overdriven Guitar",\
               30:"Distorted Guitar",31:"Guitar Harmonics",32:"Acoustic Bass",\
               33:"Acoustic Bass (finger)",34:"Acoustic Bass (pick)",\
               35:"Fretless Bass",36:"Slap Bass 1",37:"Slap Bass 2",\
               38:"Synth Bass 1",39:"Synth Bass 2",40:"Violin",41:"Viola",\
               42:"Cello",43:"Contrabass",44:"Tremolo Strings",\
               45:"Pizzicato Strings",46:"Orchestral Harp",47:"Timpani",
               48:"String Ensemble 1",49:"String Ensemble 2",\
               50:"Synth Strings 1",51:"Synth Strings 2",52:"Choir Aahs",\
               53:"Voice Oohs",54:"Synth Voice",55:"Orchestra Hit",\
               56:"Trumpet",57:"Trombone",58:"Tuba",59:"Muted Trumpet",\
               60:"French Horn",61:"Brass Section",62:"Synth Brass 1",\
               63:"Synth Brass 2",64:"Soprano Sax",65:"Alto Sax",\
               66:"Tenor Sax",67:"Baritone Sax",68:"Oboe",69:"English Horn",\
               70:"Bassoon",71:"Clarinet",72:"Piccolo",73:"Flute",\
               74:"Recorder",75:"Pan Flute",76:"Blown Bottle",77:"Shakuhachi",\
               78:"Whistle",79:"Ocarina",80:"Lead 1 (square)",\
               81:"Lead 2 (sawtooth)",82:"Lead 3 (calliope)",\
               83:"Lead 4 (chiff)",84:"Lead 5 (charang)",85:"Lead 6 (voice)",\
               86:"Lead 7 (fifths)",87:"Lead 8 (bass + lead)",\
               88:"Pad 1 (new age)",89:"Pad 2 (warm)",90:"Pad 3 (polysynth)",\
               91:"Pad 4 (choir)",92:"Pad 5 (bowed)",93:"Pad 6 (metallic)",\
               94:"Pad 7 (halo)",95:"Pad 8 (sweep)",96:"FX 1 (rain)",\
               97:"FX 2 (soundtrack)",98:"FX 3 (crystal)",\
               99:"FX 4 (atmosphere)",100:"FX 5 (brightness)",\
               101:"FX 6 (goblins)",102:"FX 7 (echoes)",103:"FX 8 (sci-fi)",\
               104:"Sitar",105:"Banjo",106:"Shamisen",107:"Koto",108:"Kalimba",\
               109:"Bag Pipe",110:"Fiddle",111:"Shanai",112:"Tinkle Bell",\
               113:"Agogo",114:"Steel Drums",115:"Woodblock",116:"Taiko Drum",\
               117:"Melodic Tom",118:"Synth Drum",119:"Reverse Cymbal",\
               120:"Guitar Fret Noise",121:"Breath Noise",122:"Seashore",\
               123:"Bird Tweet",124:"Telephone Ring",125:"Helicopter",\
               126:"Applause",127:"Gunshot",128:"Standard Drum Set",\
               136:"Room Set",144:"Power Set",152:"Electronic Set",\
               153:"TR-808 Set",160:"Jazz Set",168:"Brush Set",\
               176:"Orchestral Set",184:"SFX Set",255:"CM-64/32 C Set"}

    
    def __init__(self,_val,_instr,_channel,_startT,_stopT,_startVel,_stopVel):
        """Constructor.
        Set the note values and initially mark it as selected.
        """
        self.val = _val
        self.instr = _instr
        self.channel = _channel
        self.startT = _startT
        self.stopT = _stopT
        self.startVel = _startVel
        self.stopVel = _stopVel
        self.isSelected = True
                
    def __lt__(self, other):        
        """Comparator.
        Compares two notes taking into account the starting time of the note,
        its channel number and pitch value
        
        """
        if self.startT != other.startT:
            return (self.startT < other.startT)
        elif self.channel != other.channel:
            return (self.channel < other.channel)
        else:
            return (self.val < other.val)
        
    def __gt__(self, other):        
        """Comparator.
        Compares two notes taking into account the starting time of the note,
        its channel number and pitch value
        
        """
        if self.startT != other.startT:
            return (self.startT > other.startT)
        elif self.channel != other.channel:
            return (self.channel > other.channel)
        else:
            return (self.val > other.val)        
        
    def __eq__(self, other):        
        """Comparator.
        Compares two notes taking into account the starting time of the note,
        its channel number and pitch value
        
        """
        return (self.startT == other.startT and 
           self.channel == other.channel and 
           self.val == other.val )
           
    def __ne__(self, other):        
        """Comparator.
        Compares two notes taking into account the starting time of the note,
        its channel number and pitch value
        
        """
        return (self.startT != other.startT or 
           self.channel != other.channel or 
           self.val != other.val )        
        
                
    def __str__(self):
        """Form a string listing the properties of this note."""
        return "%d\t%d\t%d\t%s\t%s\t%s" % \
                (self.startT,self.stopT,self.channel+1,self.vals[self.val],\
                 self.instruments[self.instr],str(self.isSelected))
                
    __repr__ = __str__


class MidiFormatError(Exception):
    """Exception regarding faulty MIDI file.
    
    Currently three kinds of this exception are available:
    NOT_MIDI -- selected file is not a MIDI and cannot be processed
    BAD_FORMAT -- selected file has unsupported format (other than SMF0
    and SMF1)
    BAD_TIMEDIV -- selected file has an unsupported time base (other
    than bits per quarternote)
    
    Public methods:
    __init__
    __str__ (overloaded)
    
    """

    NOT_MIDI,BAD_FORMAT,BAD_TIMEDIV = range(3)

    def __init__(self, _val = 0):
        """Constructor.
        Allow defining the exception kind. By default it is NOT_MIDI
        """
        self.val = _val
        

    def __str__(self):
        """Form a string description of this exception."""
        if self.val == self.NOT_MIDI:
            return "File is not a MIDI"
        if self.val == self.BAD_FORMAT:
            return "Not supported MIDI SMF2 format"
        if self.val == self.BAD_TIMEDIV:
            return "Not supported FPS timing"
        
        
class MidiFile:
    """Hold data of a single MIDI file.

    Instance variables:
    data -- byte string holding the file content
    instrument -- the last instrument used in particular channel (listed 
    by a channel)
    noteList -- the list of all notes existing in this file
    tempoList -- list of all tempo changes which occured in this 
    sequence
    offest -- current file pointer position counting from the beginning
    of the file, allows naviation over the data string
    tickDiv -- current time division base (bits per quarternote)
    timing -- current time position when reading the file   
    tracksCount -- number of tracks in this file

    Static constants:
    maxInt -- maximum integer, to limit the time value in broken files
    maxVelocity -- maximum note velocity allowed
    
    Public methods:
    __init__
    selectNotes -- select notes with attributes fitting to the arguments
    given
    extractSelectedNotes -- form a new list of notes from a given list 
    using only the elements marked as selected.
        
    """

    maxInt = 2147483647
    maxVelocity = 127

    def str2Number(self,length):
        """Extract from a file an integer value of a fixed length.

        After number extraction offset attribute is enlarged by 
        the length of the number.

        """
        result = 0
        for byte in self.data[self.offset:self.offset+length]:
            result = (result << 8) + byte
        self.offset += length
        return result

    def strvlq2Number(self):
        """Extract VLQ (variable length quantity) from a file.

        File offset is enlarged by the size of the number
        retrieved.

        """
        result = 0
        while 1:
            byte = self.data[self.offset]
            self.offset += 1
            result = (result << 7) + (byte & 0x7F)
            if not (byte & 0x80):
                break
        return result

    def finishNote(self,noteVal,channel,velocity):
        """Search for the last unfinished note and fill out the missing 
        parameters.

        Attributes noteVal and channel are required to find find the 
        appropriate note. Its stopT attribute will be assigned the current
        timing and stopVel will be replaced with velocity given. In case the
        timing of the note (startT, stopT) or the file timing exceed the 
        maxInt value, the note is deleted.

        """
        if self.noteList:
            for note in self.noteList[-1::-1]:
                if (note.val == noteVal) and (note.channel == channel):
                    if (note.startT == self.timing)\
                        or (note.startT>self.maxInt)\
                        or (self.timing>self.maxInt):
                        self.noteList.remove(note)
                        break
                    note.stopT = self.timing
                    note.stopVel = velocity
                    break


    def handleMidiEvent(self,midiEvent,time):
        """Parse the MIDI events found in the file.

        Only following events are handled:
        noteOn - when encoutered, create the new note with provided parameters
        or if the velocity was 0, invoke finishNote() with provided parameters
        noteOff - when encoutered, invoke finishNote() with provided 
        parameters
        programChange - when encoutered, change the instrument of a given 
        channel

        Other events are skipped while they are unnecessary for the script 
        purpose.

        """
        hiBits = midiEvent >> 4
        loBits = midiEvent & 0xF
        if hiBits == 0x8:
            channel = loBits
            note = self.str2Number(1)
            if channel == 9:
                note += 0x80
            velocity = self.str2Number(1)
            self.finishNote(note,channel,velocity)
        elif hiBits == 0x9:
            channel = loBits
            note = self.str2Number(1)
            if channel == 9:
                note += 0x80
            velocity = self.str2Number(1)
            if velocity == 0:
                self.finishNote(note,channel,velocity)
            else:
                self.noteList.append(Note(note,self.instrument[loBits],\
                channel,self.timing,self.timing,velocity,velocity))
        elif hiBits == 0xC:
            channel = loBits
            instrument = self.str2Number(1)
            if channel == 9:
                instrument += 0x80
            self.instrument[channel] = instrument
        elif hiBits == 0xD:
            self.offset += 1
        else:
            self.offset += 2

    def readTrackChunk(self):
        """Parse the track chunk (MTrk).

        If this chunk has an invalid id, it is skipped.

        Reset the timing attribute and the instrument list.

        Handle events:
        MIDI events - passed to the handleMidiEvents
        meta-events - tempo change (addsnew to the tempo list) and EndOfTrack
        (finishes reading this track)
        Other events are skipped. Last MIDI event id is hold in case of 
        running status bytes occurence.

        """
        chunkId = self.str2Number(4)
        chunkLength = self.str2Number(4)
        if not (chunkId == 0x4D54726B):
            self.offset = chunkLength + self.offset
            return
        chunkLength += self.offset
        self.tracksCount -= 1
        self.timing = 0
        lastMidiEvent = 0
        self.instrument = [0]*16
        self.instrument[9] = 0x80
        while 1:
            ## read current track time
            self.timing += self.strvlq2Number( )
            byte = self.str2Number(1)
            if (byte & 0x80):
                hiBits = byte >> 4
                loBits = byte & 0xF
                if hiBits == 0xF:
                    if loBits == 0xF:
                        metaEvent = self.str2Number(1)
                        eventLength = self.strvlq2Number()
                        if metaEvent == 0x2F:
                            return
                        elif metaEvent == 0x51:
                            tempo = self.str2Number(eventLength)
                            self.tempoList.append([self.timing,\
                                                tempo/(self.tickDiv*1000)])
                        else:
                            self.offset += eventLength
                    else:
                        eventLength = self.strvlq2Number()
                        self.offset += eventLength
                else:
                    lastMidiEvent = byte
                    self.handleMidiEvent(byte,self.timing)
            else:
                ## handle running state
                self.offset -= 1
                self.handleMidiEvent(lastMidiEvent,self.timing)   

    def readHeaderChunk(self):
        """Parse the header (MThd) chunk.

        Retrieves the inforamtion about the file id, MIDI format, number of 
        tracks and initial time base resolution. Raises MidiFormatException
        if any parameter refers to the unsuported MIDI file type.

        """
        if not (self.str2Number(4) == 0x4d546864):
            raise MidiFormatError(MidiFormatError.NOT_MIDI)
        self.offset += 4
        if self.str2Number(2) > 1:
            raise MidiFormatError(MidiFormatError.BAD_FORMAT)
        self.tracksCount = self.str2Number(2)
        self.tickDiv = self.str2Number(2)
        if self.tickDiv & 0x8000:
            raise MidiFormatError(MidiFormatError.BAD_TIMEDIV)
        self.tickDiv = float(self.tickDiv)

    def calcRealTime(self,bitTime):
        """Convert bitTime into miliseconds.
    
        Time given in MIDI bits is calculated into miliseconds
        according to the tempo changes stored in the tempo list

        """
        result = 0
        prevTempo = self.tempoList[0]
        for tempo in self.tempoList:
            if tempo[0] < bitTime:
                result += (tempo[0] - prevTempo[0]) * prevTempo[1]
                prevTempo = tempo
            else:
                break
        result += (bitTime - prevTempo[0]) * prevTempo[1]
        return int(result)
        
    def __init__(self, fileName):
        """Constructor.

        Open and parse MIDI file. Retrieve all available notes and
        recalculate their timing into miliseconds. Sort note list.
        """
        self.totalTime = 0
        self.offset = 0
        self.tracksCount = 0
        self.tickDiv = 500000
        self.noteList = []
        self.tempoList = []
        f = open(fileName, 'rb')
        self.data = f.read()
        self.readHeaderChunk( )
        while self.tracksCount > 0:
            self.readTrackChunk( )    
        if not self.tempoList:
            self.tempoList.append([self.timing,500/self.tickDiv])
        else:
            self.tempoList.sort()
        for note in self.noteList:
            note.startT = self.calcRealTime(note.startT)
            note.stopT = self.calcRealTime(note.stopT)
            if note.stopT > self.totalTime:
                self.totalTime = note.stopT
        self.noteList.sort()       
        
    def selectNotes(notes,channel=-1,instrument=-1,noteVal=-1\
                    ,timeRange=[-1,-1],order=[0,1]):
        """Select notes with attributes fitting to the arguments given

        Each note which attributes equals the respective given values
        is marked as selected.

        Arguments:
        notes -- note list to be processed
        channel -- requested channel value, skipped if -1
        instrument -- requested instrument type value, skipped if -1
        noteVal -- reqested pitch value, skipped if -1
        timeRange -- restrict selected notes to those which at least partially
        fit into given time interval; timeRange[0] has to be greater than 
        timeRange[1]
        order -- from selected notes choose every order[1]-th element 
        beginning from the order[0]-th element
        
        """
        result = []
        for id, note in enumerate(notes):
            note.isSelected = False
            if (channel == -1) or (note.channel == channel):
                if (instrument == -1) or (note.instr == instrument):
                    if (noteVal == -1) or (note.val == noteVal):
                        if (timeRange[0] == -1) and  (timeRange[1] == -1):
                            if (id < order[0]) or (((id-order[0])%order[1])!=0):
                                continue
                            else:
                                note.isSelected = True
                        elif ((note.startT<timeRange[0])\
                            and (note.stopT<timeRange[0]))\
                            or ((note.startT>timeRange[1])\
                            and (note.stopT>timeRange[1])):
                            continue
                        else:
                            note.isSelected = True
    selectNotes = staticmethod(selectNotes)

    def extractSelectedNotes(notes):
        """Form a new list of notes from a given list using only the elements
        marked as selected.
        
        """
        result = []
        for note in notes:
            if note.isSelected:
                result.append(note)
        return result
    extractSelectedNotes = staticmethod(extractSelectedNotes)
        
        
        
def test():
    import sys
    
    print('testing midi module:')     
    note1 = Note(1,0,0,0,10,20,20)
    note2 = Note(0,0,0,0,10,20,20)
    print(note1)
    print(note2)    
    print( (note1 > note2) )
    
    if len(sys.argv) > 1 :
        print("midi file: ", sys.argv[1])
        midi_track = MidiFile(sys.argv[1])
        print(midi_track.totalTime)
        print(midi_track.offset)
        print(midi_track.tracksCount)
        print(midi_track.tickDiv)
        for note in midi_track.noteList:
            print(note)
        print(midi_track.tempoList)
    
if __name__ == "__main__": 
    test()
