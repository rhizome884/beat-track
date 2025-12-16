import jams
import os
import pretty_midi

def jams_beat_position_to_midi(jams_file, resolution=960, tempo=120.0):
    
    # Load jams data
    jam = jams.load(jams_file)

    # Create pretty midi object
    pm = pretty_midi.PrettyMIDI(midi_file=None, resolution=resolution, initial_tempo=tempo) 

    # Create an empty pm Instrument instance
    inst = pretty_midi.Instrument(program=0)
    
    # Iterate through the beat_position data in the jams object 
    for data in jam.search(namespace='beat_position')[0]:
        # Create time location value for 'note end' (beat and downbeat duration set to 0.1s) 
        end = data.time + 0.1 
        # Add relevant downbeat and beat data to pm note objects then pm inst
        if data.value['position'] == 1:
            downbeat = pretty_midi.Note(velocity=127, pitch=127, start=data.time, end=end)
            inst.notes.append(downbeat)
        beat = pretty_midi.Note(velocity=96, pitch=126, start=data.time, end=end)
        inst.notes.append(beat)

    # Add the inst data to the pm object and return object
    pm.instruments.append(inst)

    return pm


if __name__ == "__main__":

    # Dir name for jams annotations var
    indir = "annotation"
    outdir = "beat-annotation-midi"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    # Iterate through jams files
    for f in os.listdir(indir):
        # Create src and dst filepaths
        src = os.path.join(indir, f)
        dst = os.path.join(outdir, f.replace('.jams', '.mid'))
        # Process jams data and return beats/downbeats in pm object
        pm = jams_beat_position_to_midi(src)
        # Save pm data in midi file
        pm.write(dst)
        break
