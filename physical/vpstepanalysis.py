'''
ICO cluster analysis for all steps in a run.
The trajectories at the end of each step is used.
'''

from PyQt5 import QtGui  # Added to be able to import ovito

from matplotlib import pyplot as pl
from scipy import stats as st

import pandas as pd
import numpy as np

import logging

from setup.setup import exportdir as createfolders

from physical.ico import icofrac

# Format the logging style
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
                              '%(asctime)s - ' +
                              '%(name)s - ' +
                              '%(levelname)s - ' +
                              '%(message)s'
                              )
ch.setFormatter(formatter)


def run(param, exportdir):
    '''
    Iterate initial data analysis for all steps in all runs
    '''

    # Setup logger
    logger = logging.getLogger('Start')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    logger.info('Tool Initialized')

    # Apply for each run in the main directory
    for item in param:

        path = item.replace('traj.lammpstrj', '')  # Run directory
        folder = '/'+path.split('/')[-2]  # Run name
        outfile = path+'test.out'  # LAMMPS data export
        createfolders(exportdir+folder)  # Create relevant folders

        printname = 'Gathering Data from File: '+item

        # Print on screen the run analyzed
        print('-'*len(printname))
        print(printname)
        print('-'*len(printname))

        # Parsed parameters
        n = param[item]['iterations']
        increment = param[item]['increment']
        deltatemp = param[item]['deltatemp']
        starttemp = param[item]['tempstart']
        timestep = param[item]['timestep']
        dumprate = param[item]['dumprate']
        hold1 = param[item]['hold1']
        hold2 = param[item]['hold2']
        hold3 = param[item]['hold3']
        trajsteps = param[item]['trajectorysteps']

        # The path to save in
        savepath = exportdir+'/'+item.split('/')[-2]

        # Apply analysis on each step of run
        dfs = []
        for i in trajsteps:

            print('ICO analysis for step: '+str(i))

            # Setup logger
            logger = logging.getLogger('ICO Step: '+str(i))
            logger.setLevel(logging.DEBUG)
            logger.addHandler(ch)

            df = icofrac(item, i//dumprate)

            df.insert(loc=1, column='time', value=i*timestep)
            df.insert(loc=0, column='step', value=i)
            dfs.append(df)

        df = pd.concat(dfs, sort=False)
        df.to_csv(
                  savepath+'/datacalculated/ico/icofracs.txt',
                  sep=' ',
                  index=False
                  )

        imagepath = savepath+'/images/ico/icofrac.png'

        ax = df.plot(x='time', style='.')
        ax.set_xlabel('Time [ps]')
        ax.set_ylabel('ICO Fraction [-]')
        ax.grid()
        plot = ax.get_figure()
        plot.tight_layout()
        plot.savefig(imagepath)
        pl.close('all')