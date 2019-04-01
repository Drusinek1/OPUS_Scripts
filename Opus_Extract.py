import sys

with open(sys.argv[1], 'r') as infile, open(sys.argv[2], 'w') as outfile:
    lines = infile.readlines()
    outfile.write("Rinex" + " " + "Date" + " " + "Northing(m)" + " " + "Easting(m)" + " " + "Elevation(m)" + " " + "\n")
    for line in lines:
        if line.find("NGS OPUS SOLUTION REPORT") != -1:
            print("Starting a new day!" + line)
        elif line.find("RINEX FILE:") != -1:
            rinex = line.split()[2]
        elif line.find("START:") != -1:
            date = line.split()[6]
        elif line.find("ORTHO HGT")!= -1:
            hgt = line.split()[2].rstrip('(m)')
        elif line.find("Northing") != -1:
            northing = line.split()[3]
        elif line.find("Easting") != -1:
            east = line.split()[3]
        elif line.find("field operating procedures used") != -1:
            outfile.write(rinex + ' '+ date + ' ' + northing + ' ' + east + ' ' + hgt + ' ' + '\n')

