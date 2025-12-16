import pretty_midi
import csv

def csv_to_midi_bar_map(csvpath, midpath, timesig, resolution=960, tempo=120.0):

    # Create pretty midi object
    pm = pretty_midi.PrettyMIDI(midi_file=None, resolution=resolution, initial_tempo=tempo) 
    # Create an empty pm Instrument instance
    inst = pretty_midi.Instrument(program=0)

    # Iterate through csv file
    with open(csvpath, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        # Extract downbeat times and add 
        for col in csvreader:
            # Create time location value for 'note star/end' (downbeat duration set to 0.1s) 
            start = float(col[0])
            end = float(col[0]) + 0.1 
            # Save downbeat as MIDI note event 127
            downbeat = pretty_midi.Note(velocity=127, pitch=127, start=start, end=end)
            inst.notes.append(downbeat)

    # Add the inst data to the pm object and return object
    pm.instruments.append(inst)

    # Save to MIDI file
    pm.write(midpath)

if __name__ == "__main__":

    csvpath = "danza-paraguaya_rojas_downbeats.csv"
    midpath = "danza-paraguaya_rojas_downbeats.mid"

    # time signature
    timesig = [3,4]

    csv_to_midi_bar_map(csvpath, midpath, timesig)
