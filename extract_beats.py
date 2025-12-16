from beat_this.inference import File2Beats
from beat_this.utils import save_beat_tsv

# instantiate an instance of the File2Beats class that encapsulates the model
# along with pre- and postprocessing
file2beats = File2Beats(checkpoint_path="final0", device="cuda", dbn=False)

# Obtain list of beats and downbeats for an audio file
audio_path = "yt_downloads/rojas_danza-paraguaya_2008.mp3"
beats, downbeats = file2beats(audio_path)

# Save to .beats file
outpath = "rojas_danza-paraguaya_2008.beats"
print(type(beats))
save_beat_tsv(beats, downbeats, outpath)
