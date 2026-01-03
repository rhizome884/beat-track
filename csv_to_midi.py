import pretty_midi
import csv

def csv_to_midi_notes(csvpath, midpath, tempo, resolution=960):
    # Create pretty midi object
    pm = pretty_midi.PrettyMIDI(midi_file=None, resolution=resolution, initial_tempo=tempo) 
    # Create an empty pm Instrument instance
    inst = pretty_midi.Instrument(program=0)

    # Iterate through csv file
    with open(csvpath, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        # Extract downbeat times and add 
        for line in reader:
            # Create time location value for 'note star/end' (downbeat duration set to 0.1s) 
            velocity = int(line['LABEL'].split(' ')[-1]) 
            pitch = int(line['VALUE'])
            start = float(line['TIME'])
            end = start + float(line['DURATION']) 
            note = pretty_midi.Note(velocity=velocity, pitch=pitch, start=start, end=end)
            inst.notes.append(note)

    # Add the inst data to the pm object and return object
    pm.instruments.append(inst)

    # Save to MIDI file
    pm.write(midpath)

def csv_to_midi_bar_map(csvpath, midpath, tempo, resolution=960):

    # Create pretty midi object
    pm = pretty_midi.PrettyMIDI(midi_file=None, resolution=resolution, initial_tempo=tempo) 
    # Create an empty pm Instrument instance
    inst = pretty_midi.Instrument(program=0)

    # Iterate through csv file
    with open(csvpath, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        # Extract downbeat times and add 
        for line in reader:
            # Create time location value for 'note star/end' (downbeat duration set to 0.1s) 
            start = float(line['TIME'])
            end = float(line['TIME']) + 0.1 
            # Save downbeat as MIDI note event 127
            downbeat = pretty_midi.Note(velocity=127, pitch=127, start=start, end=end)
            inst.notes.append(downbeat)

    # Add the inst data to the pm object and return object
    pm.instruments.append(inst)

    # Save to MIDI file
    pm.write(midpath)

def get_average_tempo(csvbeatpath):

    bpm_sum = 0
    item_count = 0
    
    with open(csvbeatpath, 'r', newline='') as file:
        reader = csv.DictReader(file, delimiter=',')
        data = list(reader)
        length = len(data)
        for i, item in enumerate(data):
            # Filter out start and end bpm values
            if i < 5 or (length - i) < 6:
                continue
            # Add bpm values and item counts
            else:
                bpm_sum += float(item['VALUE'])
                item_count += 1
     
    average_bpm = round(bpm_sum / item_count)
    # Return bpm as rounded integer value
    return average_bpm

if __name__ == "__main__":

    #csvpath = "danza_downbeat_test.csv"
    #midpath = "danza_downbeat_test.mid"
    notepath= 'nottamun-town/notes-gtr.csv'
    beatpath = 'nottamun-town/bpm-3-4.csv'
    beatmid = 'nottamun-town/bpm.mid'
    notemid = 'nottamun-town/note.mid'

    tempo = get_average_tempo(beatpath)
    csv_to_midi_bar_map(beatpath, beatmid, tempo)
    csv_to_midi_notes(notepath, notemid, tempo)
