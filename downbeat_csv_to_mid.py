from mido import MidiFile, MidiTrack, MetaMessage
import csv

def downbeat_csv_to_mid(csvfile, midfile, time_signature[1,1], sample_rate=44100, ticks_per_beat=480):
    
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    track.append(MetaMessage('time_signature', numerator=time_signature[0], denominator=time_signature[1]))
    # track.append(MetaMessage('set_tempo', tempo=500000, time=0))
    current_ticks = 0
    
    with open(csvfile, 'r', newline='') as file:
        reader = csv.DictReader(file, delimiter=',')
        for line in reader:
            position, tempo, dur = int(line['FRAME']), float(line['VALUE']), int(line['DURATION'])
            if tempo == 0.0:
                continue
            else:
                bpm_to_microseconds = 60_000_000 / tempo
            time_seconds = position / sample_rate
            dur_seconds = dur / sample_rate
            time_ticks = int(time_seconds * ticks_per_beat * tempo / 60)
            delta_ticks = int(dur_seconds * ticks_per_beat * tempo / 60)
            #delta_ticks = max(0, time_ticks - current_ticks)
            track.append(MetaMessage('set_tempo', tempo=int(bpm_to_microseconds), time=delta_ticks))
            current_ticks = time_ticks

    track.append(MetaMessage('end_of_track', time=0))
    midi.save(midfile)

if __name__ == "__main__":

    csvfile = "danza-paraguaya_rojas_downbeats.csv"
    midfile = "danza-paraguaya_rojas_downbeats.mid"

    downbeat_csv_to_mid(csvfile, midfile, time_signature=[1,1], sample_rate=44100, ticks_per_beat=480)
