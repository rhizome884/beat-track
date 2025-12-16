import csv

infile = "rojas_danza-paraguaya_2008.beats"
outfile = "rojas_danza-paraguaya_2008.downbeats"
downbeat = []

# Get downbeat data
with open(infile, 'r', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t')
    for line in csvreader:
        if line[1] == '1':
            downbeat.append(line[0])

# Write downbeat data to new file
with open(outfile, 'w') as file:
    for beat in downbeat:
        file.write(beat + '\n')
        
