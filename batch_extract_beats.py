import os
from beat_this.inference import File2Beats
from beat_this.utils import save_beat_tsv

# instantiate an instance of the File2Beats class that encapsulates the model
# along with pre- and postprocessing
file2beats = File2Beats(checkpoint_path="final0", device="cuda", dbn=False)

# Obtain list of beats and downbeats for an audio file
indir = "../dlfm25-data/dlfm25-mp3"
outdir = "beat-maps"
inext = ".mp3"
outext = ".beats"

if not os.path.exists(outdir):
    os.makedirs(outdir)

for f in os.listdir(indir):

    src = os.path.join(indir, f)
    dst = os.path.join(outdir, f.replace(inext, outext))
    
    beats, downbeats = file2beats(src)
    save_beat_tsv(beats, downbeats, dst)

#beats, downbeats = file2beats(audio_path)
#
## Save to .beats file
#outpath = "rojas_danza-paraguaya_2008.beats"
#print(type(beats))
#save_beat_tsv(beats, downbeats, outpath)
