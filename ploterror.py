from matplotlib import pyplot as pl
from block_averaging import block
from scipy import stats as st

from matplotlib import lines

from importdiffusions import filesdiff
from autocorrelation import *

import numpy as np

ddof = 0
regular, multiple = filesdiff('../export/')

runs = list(set(regular['run']))
print(runs)

indexes = {}
for run in runs:
    indexes[run] = regular.index[run == regular['run']]

print(indexes)

temps = []
averages = []
error = []
for temp in regular:
    temps.append(temp)
    averages.append(np.mean(regular[temp]['all']))
    error.append(st.sem(regular[temp]['all'], ddof=ddof))

pl.plot(temps, error, 'ob', markerfacecolor='none', markersize=12)

temps = []
blockedaverages = []
blockederror = []
for temp in blockedruns:
    temps.append(temp)
    blockedaverages.append(blockedruns[temp]['all'][0])
    blockederror.append(blockedruns[temp]['all'][1])

pl.plot(temps, blockederror, '.r', markersize=10)

temps = []
autoerror = []
for temp in regular:
    temps.append(temp)
    autoerror.append(standarderror(regular[temp]['all'], 0))

pl.plot(temps, autoerror, '*y')

temps = []
autoerror = []
for temp in regular:
    temps.append(temp)
    lout, values, lcut = correlationlength(regular[temp]['all'])
    autoerror.append(standarderror(regular[temp]['all'], lcut))

pl.plot(temps, autoerror, 'xk')

regularval = lines.Line2D(
                         [],
                         [],
                         color='blue',
                         marker='o',
                         linestyle='None',
                         markersize=8,
                         markerfacecolor='none',
                         label='Scipy SEM'
                         )

regularblocks = lines.Line2D(
                             [],
                             [],
                             color='red',
                             marker='.',
                             linestyle='None',
                             markersize=8,
                             label='10 Block Averaging SEM'
                             )

autocorrelation0 = lines.Line2D(
                                [],
                                [],
                                color='y',
                                marker='*',
                                linestyle='None',
                                markersize=8,
                                label='Autocorrelation (l=0)'
                                )

autocorrelation = lines.Line2D(
                               [],
                               [],
                               color='k',
                               marker='x',
                               linestyle='None',
                               markersize=8,
                               label='Autocorrelation (l=lcut)'
                               )

plotlables = [regularval, regularblocks, autocorrelation0, autocorrelation]

pl.xlabel('Temperature [K]')
pl.ylabel('Diffusion SEM [*10^-4 cm^2 s^-1]')
pl.legend(handles=plotlables, loc='best')
pl.grid()
pl.tight_layout()
pl.savefig('../errorcheck')
pl.clf()

temps = []
runs = {}
for temp in multiple:
    count = 0
    temps.append(temp)
    for item in multiple[temp]['all']:
        if runs.get(count) is None:
            runs[count] = []

        runs[count].append(block(item)[1])
        count += 1

for run in runs:
    pl.plot(temps, runs[run], 'b.')

runs = {}
for temp in multiple:
    count = 0
    for item in multiple[temp]['all']:
        if runs.get(count) is None:
            runs[count] = []

        runs[count].append(st.sem(item, ddof=ddof))
        count += 1

for run in runs:
    pl.plot(temps, runs[run], 'rx')

one = lines.Line2D(
                   [],
                   [],
                   color='b',
                   marker='.',
                   linestyle='None',
                   markersize=8,
                   label='Block Averaging (n=10) SEM'
                   )

two = lines.Line2D(
                   [],
                   [],
                   color='r',
                   marker='x',
                   linestyle='None',
                   markersize=8,
                   label='Scipy SEM'
                   )

plotlabels = [one, two]

pl.xlabel('Temperature [K]')
pl.ylabel('Diffusion SEM [*10^-4 cm^2 s^-1]')
pl.legend(handles=plotlabels, loc='best')
pl.grid()
pl.tight_layout()
pl.savefig('../blockvsscipy')
pl.clf()

runs = {}
temps = []
for temp in multiple:
    count = 0
    temps.append(temp)
    for item in multiple[temp]['all']:
        if runs.get(count) is None:
            runs[count] = []

        lout, values, lcut = correlationlength(item)
        runs[count].append(standarderror(item, lcut))
        count += 1

for run in runs:
    pl.plot(temps, runs[run], 'b.')

runs = {}
for temp in multiple:
    count = 0
    for item in multiple[temp]['all']:
        if runs.get(count) is None:
            runs[count] = []

        runs[count].append(st.sem(item, ddof=ddof))
        count += 1

for run in runs:
    pl.plot(temps, runs[run], 'rx')

one = lines.Line2D(
                   [],
                   [],
                   color='b',
                   marker='.',
                   linestyle='None',
                   markersize=8,
                   label='Autocorrelation (l=lcut)'
                   )

two = lines.Line2D(
                   [],
                   [],
                   color='r',
                   marker='x',
                   linestyle='None',
                   markersize=8,
                   label='Scipy SEM'
                   )

plotlabels = [one, two]


pl.xlabel('Temperature [K]')
pl.ylabel('Diffusion SEM [*10^-4 cm^2 s^-1]')
pl.legend(handles=plotlabels, loc='best')
pl.grid()
pl.tight_layout()
pl.savefig('../autovsscipy')
pl.clf()

'''
runs = {}
for temp in multiple:
    if runs.get(temp) is None:
        runs[temp] = []
    for item in multiple[temp]['all']:
        runs[temp] += item

temps = []
megablock1 = []
megablock10 = []
megablock50 = []
megablock100 = []
megablock150 = []
scipysem = []
for temp in runs:
    temps.append(temp)
    megablock1.append(block(runs[temp], 1)[1])
    megablock10.append(block(runs[temp], 10)[1])
    megablock50.append(block(runs[temp], 50)[1])
    megablock100.append(block(runs[temp], 100)[1])
    megablock150.append(block(runs[temp], 150)[1])

    scipysem.append(st.sem(runs[temp]))

pl.plot(temps, megablock1, 'bx', label='Block Average (n=1)')
pl.plot(temps, megablock10, 'g+', label='Block Average (n=10)')
pl.plot(temps, megablock50, 'm*', label='Block Average (n=50)')
pl.plot(temps, megablock100, 'yo', label='Block Average (n=100)')
pl.plot(temps, megablock150, 'k.', label='Block Average (n=150)')

pl.plot(temps, scipysem, 'rx', label='Scipy SEM for All')

pl.xlabel('Temperature [K]')
pl.ylabel('Diffusion SEM [*10^-4 cm^2 s^-1]')
pl.legend(loc='best')
pl.grid()
pl.tight_layout()
pl.savefig('../blocksizechange')
pl.clf()
'''

runs = {}
for temp in multiple:
    if runs.get(temp) is None:
        runs[temp] = []
    for item in multiple[temp]['all']:
        runs[temp] += item

temps = []
megablock = []
autocorr = []
scipysem = []
blockdiff = []
actualldiff = []
for temp in runs:
    temps.append(temp)

    res = block(runs[temp])
    megablock.append(res[1])
    blockdiff.append(res[0])

    lout, values, lcut = correlationlength(runs[temp])
    autocorr.append(standarderror(runs[temp], lcut))

    scipysem.append(st.sem(runs[temp]))

pl.plot(temps, megablock, 'b.', label='Block Average for All')
pl.plot(temps, autocorr, '*k', label='Autoccorrelation for All')
pl.plot(temps, scipysem, 'rx', label='Scipy SEM for All')

pl.xlabel('Temperature [K]')
pl.ylabel('Diffusion SEM [*10^-4 cm^2 s^-1]')
pl.legend(loc='best')
pl.grid()
pl.tight_layout()
pl.savefig('../megaset')
pl.clf()

temps2 = []
averages = []
for temp in regular:
    temps2.append(temp)
    averages.append(np.mean(regular[temp]['all']))


pl.plot(temps2, averages, 'rx', label='Average Diffusion')
pl.plot(temps, blockdiff, 'b.', label='Block Average Diffusion')

pl.xlabel('Temperature [K]')
pl.ylabel('Diffusion SEM [*10^-4 cm^2 s^-1]')
pl.legend(loc='best')
pl.grid()
pl.tight_layout()
pl.savefig('../diffusioncheck')
pl.clf()


cut = 100
for temp in runs:
    lout, values, lcut = correlationlength(runs[temp])

    pl.plot(lout[:cut], values[:cut], label=temp)

pl.legend(loc='best')
pl.grid()
pl.tight_layout()
pl.xlabel('l [-]')
pl.ylabel('Autocorrelation [*10^-4 cm^2 s^-1]^2')
pl.show()
pl.clf()
