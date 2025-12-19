from mido import MidiFile, MidiTrack, MetaMessage, Message, bpm2tempo
import csv

def merge_downbeats_with_notes(db_csvfile, nt_csvfile, midfile, time_signature=[4,4], sample_rate=44100, ticks_per_beat=480):
    
    midi = MidiFile(type=2)
    track = MidiTrack()
    midi.tracks.append(track)
    track.append(MetaMessage('time_signature', numerator=time_signature[0], denominator=time_signature[1]))
    
    # set note file midi tempo
    bpm = 120
    track.append(MetaMessage('set_tempo', tempo=bpm2tempo(bpm)))
    
    current_ticks = 0
    
    # Append note data
    with open(nt_csvfile, 'r', newline='') as file:
        reader = csv.DictReader(file, delimiter=',')
        for line in reader:
            position, pitch, dur, vel = int(line['FRAME']), int(line['VALUE']), int(line['DURATION']), int(line['LABEL'].split(' ')[-1])
            time_seconds = position / sample_rate
            dur_seconds = dur / sample_rate
            # Midi tempo from Sonic Visualiser csv export should be default 120 BPM I think 
            time_ticks = int(time_seconds * ticks_per_beat * 120 / 60)
            #dur_ticks = int(dur_seconds * ticks_per_beat * 120 / 60)
            delta_ticks = max(0, time_ticks - current_ticks)
            track.append(Message('note_on', note=pitch, velocity=vel, time=0))
            track.append(Message('note_off', note=pitch, time=delta_ticks))
            current_ticks = time_ticks
    
    ## Append downbeat data
    #with open(db_csvfile, 'r', newline='') as file:
    #    reader = csv.DictReader(file, delimiter=',')
    #    for line in reader:
    #        position, tempo, dur = int(line['FRAME']), float(line['VALUE']), int(line['DURATION'])
    #        if tempo == 0.0:
    #            continue
    #        bpm_to_microseconds = 60_000_000 / tempo
    #        time_seconds = position / sample_rate
    #        dur_seconds = dur / sample_rate
    #        time_ticks = int(time_seconds * ticks_per_beat * tempo / 60)
    #        delta_ticks = int(dur_seconds * ticks_per_beat * tempo / 60)
    #        track.append(MetaMessage('set_tempo', tempo=int(bpm_to_microseconds), time=delta_ticks))

    track.append(MetaMessage('end_of_track', time=0))
    midi.save(midfile)

if __name__ == "__main__":

    db_csvfile = "danza-rojas-downbeats.csv"
    nt_csvfile = "danza-rojas-notes.csv"
    midfile = "danza-rojas-merge.mid"

    merge_downbeats_with_notes(db_csvfile, nt_csvfile, midfile, time_signature=[3,4], sample_rate=44100, ticks_per_beat=480)
