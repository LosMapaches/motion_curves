from PyQt5 import QtGui  # Added to be able to import ovito
from single import analize

import os

# Directories
firstdir = os.getcwd()
lammpstrjdir = firstdir+'/../data/lammpstrj/'

# Grab the file names from the lammpstrj directory
names = os.listdir(lammpstrjdir)

# Grab the names of runs to be averaged
count = 0
for name in names:
    names[count] = name.split('.lammpstrj')[0]
    count += 1

n = 25
increment = 50000
deltatemp = 50
starttemp = 1350

for item in names:

    for iteration in list(range(0, n)):

        # Parameters from the naming convention
        value = item.split('_')
        system = value[0]
        side = value[1].split('-')[1]

        hold1 = int(value[2].split('-')[1])
        hold1 += iteration*increment

        hold2 = int(value[3].split('-')[1])
        hold3 = int(value[4].split('-')[1])
        dumprate = int(value[6].split('-')[1])
        inittemp = int(value[7].split('K-')[0])
        finaltemp = int(value[7].split('K-')[1][:-1])

        timestep = ''
        ptimestep = value[5].split('-')[1]
        for letter in ptimestep:
            if letter == 'p':
                letter = '.'
            timestep += letter

        timestep = float(timestep)

        points = [hold1, hold1+hold2, hold1+hold2+hold3]

        # Do averaging for files
        value = analize(
                        item,
                        points[1],
                        points[2],
                        timestep,
                        dumprate,
                        [points[0], points[1], points[2]],
                        10,
                        50
                        )

        value.calculate_time()
        value.calculate_msd()
        value.calculate_rdf()
        value.calculate_diffusion()
        value.multiple_origins_diffusion()
        data = value.calculation_export()

        savename = str(starttemp-iteration*deltatemp)+'K'
        value.plot_msd(savename)
        value.plot_rdf(savename)
        value.save_msd(savename)
        value.save_rdf(savename)
        value.save_multiple_origins_diffusion(savename)
        value.save_diffusion(savename)