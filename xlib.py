import matplotlib.pyplot as plt
import os
import shutil
from glob import glob

"""
Copyright (c) 2023 Ben
"""
def mplplot(stream, figsize=[12.0, 8.0], linewidth=1):
    '''
    This function is used to plot waveforms
    '''
    if len(stream)==1:
        fig, ax = plt.subplots(nrows=len(stream), ncols=1, figsize=figsize)
        ax.plot(stream[0].times("matplotlib"), stream[0].data, "k-", linewidth=linewidth, label=stream[0].stats.station+'.'+stream[0].stats.channel)
        ax.legend(loc=2)
    else:
        fig, ax = plt.subplots(nrows=len(stream), ncols=1, figsize=figsize)
        for i, tr in zip(range(0,len(stream)), stream):
            ax[i].plot(tr.times("matplotlib"), tr.data, "k-", linewidth=linewidth, label=tr.stats.station+'.'+tr.stats.channel)
            ax[i].legend(loc=2)

def checkcontent_inc_hours(stream, inc_hours):
    '''
    This function return True if the stream of one
    day have more than inc_hours data.
    ----------------------------------
    stream: stream
    inc_hours: incremental hours for checking quantity of data
    '''
    # npts: number of points
    npts = 0
    for tr in stream:
        npts = npts + tr.stats.npts
    sps  = int(stream[0].stats.sampling_rate)
    # if the number of points is less than the data that can be saved
    # in the incremental hours
    # remove the trace
    if npts < sps*inc_hours*3600:
        print("Bad daily data: " + stream[0].stats.network + '.' + stream[0].stats.station + "-" +
        str(stream[0].stats.starttime.year) + '.' + str(stream[0].stats.starttime.julday))
        return False
    return True

def makefolder(fname="New Folder"):
    '''
    Remove the folder to create the new one
    '''
    if not os.path.isdir(fname):
        os.mkdir(fname)
    else:
        shutil.rmtree(fname)
        os.mkdir(fname)

def chunkwaveform(finput='input-directory', foutput='output-directory', chunklength=86400):
    """
    This function is used to create the mscut.sh to chunk the data
    Requirement: gipp + Java JRE
    -------------------------
    finput: the directory of folder that include all the continous mseed file
    foutput: the directory that you want to stores chukced file
    chunktime: duration of chunktime
    -------------------------
    return: the mscut.sh file to execute the mseedcut (gipp)
    """
    waveformname = [os.path.basename(x) for x in glob(finput+'/*')]
    f = open("mscut.sh",'w')

    # create folders for daily data
    makefolder(foutput)
    for x in waveformname:
        makefolder(foutput+'/'+x)
        # write the bash file for executing mseedcut
        f.write("mseedcut --file-length="+str(chunklength)+" --output-dir="+
                foutput+'/'+x+" "+
                finput+'/'+x+"\n")
    f.close()
