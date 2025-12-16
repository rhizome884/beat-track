import csv
import os 

indir = "beat-maps"
outdir = "downbeat-maps"
if not os.path.exists(outdir):
    os.makedirs(outdir)

inext = '.beat'
outext = '.downbeat'

for f in os.listdir(indir):

    downbeat = []

    src = os.path.join(indir, f) 
    dst = os.path.join(outdir, f.replace(inext, outext)) 
    
    # Get downbeat data
    with open(src, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        for line in csvreader:
            if line[1] == '1':
                downbeat.append(line[0])
    
    # Write downbeat data to new file
    with open(dst, 'w') as file:
        for beat in downbeat:
            file.write(beat + '\n')
            
