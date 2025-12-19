import pretty_midi
import csv

def csv_to_midi_bar_map(csvpath, midpath, timesig, resolution=960, tempo=120.0):

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

if __name__ == "__main__":

    csvpath = "danza_downbeat_test.csv"
    midpath = "danza_downbeat_test.mid"

    # time signature
    timesig = [3,4]

    csv_to_midi_bar_map(csvpath, midpath, timesig)
