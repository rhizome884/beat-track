import jams
import os

def print_non_four_four_time_signatures(file, num_beats=4):

    jam = jams.load(file)
    
    for data in jam.search(namespace='beat_position')[0]:
        if data.value['beat_units'] != num_beats or data.value['num_beats'] != num_beats:
            print(file)
            print(data.value)
            break

if __name__ == "__main__":
    
    indir = "annotation"
    
    # Iterate through jams files
    for f in os.listdir(indir):
        # Create src and dst filepaths
        filepath = os.path.join(indir, f)
        # Print time sig info
        print_non_four_four_time_signatures(filepath) 
