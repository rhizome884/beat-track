from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo
import csv

def write_csv_to_midi(downbeatfile, notefile, midi_path):
    """
    Function adapted from Kong et al. (2021)
    """
    downbeat_events = [] 
    note_events = []
    
    #Save downbeat event data to list
    with open(downbeatfile, 'r', newline='') as file:
        reader = csv.DictReader(file, delimiter=',')
        for line in reader:
            downbeat_events.append(line)

    # Save note event data to list
    with open(notefile, 'r', newline='') as file:
        reader = csv.DictReader(file, delimiter=',')
        for line in reader:
            note_events.append(line)

    # This configuration is the same as MIDIs in MAESTRO dataset
    ticks_per_beat = 384
    beats_per_second = 2
    ticks_per_second = ticks_per_beat * beats_per_second
    # microseconds_per_beat = int(1e6 // beats_per_second)

    # Create midi file
    midi_file = MidiFile()
    midi_file.ticks_per_beat = ticks_per_beat

    # Track 0
    track0 = MidiTrack()
    #track0.append(MetaMessage('set_tempo', tempo=microseconds_per_beat, time=0))
    track0.append(MetaMessage('time_signature', numerator=4, denominator=4, time=0))
    #track0.append(MetaMessage('end_of_track', time=1))
    #midi_file.tracks.append(track0)
    
    # Meta Message rolls of MIDI
    meta_message_roll = []

    for downbeat_event in downbeat_events:
        # Bar starts
        meta_message_roll.append({
            'time': float(downbeat_event['TIME']), 
            'bpm': float(downbeat_event['VALUE'])
            }) 

    # Sort MIDI messages by time
    meta_message_roll.sort(key=lambda note_event: note_event['time'])
    
    previous_ticks = 0
    start_time = 0 # this value is redundant for the time being
    for message in meta_message_roll:
        this_ticks = int((message['time'] - start_time) * ticks_per_second)
        if this_ticks >= 0:
            diff_ticks = this_ticks - previous_ticks
            previous_ticks = this_ticks
            if 'time' in message.keys():
                if message['bpm'] != 0:
                    track0.append(MetaMessage('set_tempo', tempo=bpm2tempo(message['bpm']), time=diff_ticks))
    
    track0.append(MetaMessage('end_of_track', time=1))
    midi_file.tracks.append(track0)

    # Track 1
    track1 = MidiTrack()
    
    # Message rolls of MIDI
    message_roll = []

    for note_event in note_events:
        # Onset
        message_roll.append({
            'time': float(note_event['TIME']), 
            'midi_note': int(note_event['VALUE']), 
            'velocity': int(note_event['LABEL'].split(' ')[-1])})

        # Offset
        message_roll.append({
            'time': float(note_event['TIME']) + float(note_event['DURATION']), 
            'midi_note': int(note_event['VALUE']), 
            'velocity': 0})

    # Sort MIDI messages by time
    message_roll.sort(key=lambda note_event: note_event['time'])

    previous_ticks = 0
    start_time = 0 # this value is redundant for the time being
    for message in message_roll:
        this_ticks = int((message['time'] - start_time) * ticks_per_second)
        if this_ticks >= 0:
            diff_ticks = this_ticks - previous_ticks
            previous_ticks = this_ticks
            if 'midi_note' in message.keys():
                track1.append(Message('note_on', note=message['midi_note'], velocity=message['velocity'], time=diff_ticks))
            # Maybe add control change data later
            #elif 'control_change' in message.keys():
            #    track1.append(Message('control_change', channel=0, control=message['control_change'], value=message['value'], time=diff_ticks))

    track1.append(MetaMessage('end_of_track', time=1))
    midi_file.tracks.append(track1)

    midi_file.save(midi_path)

if __name__ == "__main__":

    downbeatfile = 'danza_downbeat_test.csv'
    notefile = 'danza_note_test.csv'
    midi_path = 'danza_merge_test.mid'

    write_csv_to_midi(downbeatfile, notefile, midi_path)
