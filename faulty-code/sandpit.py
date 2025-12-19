from mido import Message, MidiFile, MidiTrack, MetaMessage
import csv

def write_tempo_and_notes_to_midi(tempo_mid, note_csv, midi_out):
    """
    Function adapted from Kong et al. (2021)
    """

    # Open tempo map midi file
    mid0 = MidiFile(tempo_mid)
    
    # Create midi file
    midi_file = MidiFile()
    ticks_per_second = mid0.ticks_per_beat
    midi_file.ticks_per_beat = mid0.ticks_per_beat
    midi_file.tracks.append(mid0.tracks[0])
    
    note_events = []

    with open(note_csv, 'r', newline='') as file:
        reader = csv.DictReader(file, delimiter=',')
        for line in reader:
            note_events.append(line)

    ## This configuration is the same as MIDIs in MAESTRO dataset
    #ticks_per_beat = 384
    #beats_per_second = 2
    #ticks_per_second = ticks_per_beat * beats_per_second
    #microseconds_per_beat = int(1e6 // beats_per_second)

    ## Create midi file
    #midi_file = MidiFile()
    #midi_file.ticks_per_beat = ticks_per_beat

    ## Track 0
    #track0 = MidiTrack()
    #track0.append(MetaMessage('set_tempo', tempo=microseconds_per_beat, time=0))
    #track0.append(MetaMessage('time_signature', numerator=4, denominator=4, time=0))
    #track0.append(MetaMessage('end_of_track', time=1))
    #midi_file.tracks.append(track0)
    
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

    midi_file.save(midi_out)

if __name__ == "__main__":

    tempo_mid = 'danza-paraguaya_rojas_downbeats.mid'
    csv_mid = 'danza_note_test.csv'
    midi_out = 'danza_note_tempo_test.mid'
    
    write_tempo_and_notes_to_midi(tempo_mid, csv_mid, midi_out)
