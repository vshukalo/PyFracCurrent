import numpy as np

global condNumA
condNumA = []
global k
k = 0

def initCondNumOutput(A, filename):
    global condNumA
    condNumA = []


def CondNumOutput (A, filename):
    global condNumA
    condNumA.append(np.linalg.cond(A))
    """ with open ('C:/Users/VShukalo/myFolder/work/PF_output_info/Bigstab_info/New_folder/' + 'condNum' + filename + '.txt', 'a') as f:
                f.write(  repr(np.linalg.cond(A)) + '\n') """

global i 
i = 0
global j 
j = 0

def initialCondNumbers(A, matrixName):
    global MincondNumA
    global MincondNumFinDif
    global MaxcondNumA
    global MaxcondNumFinDif
    currentCond = np.linalg.cond(A)
    if(matrixName == 'A'):
        MincondNumA = currentCond    
        MaxcondNumA = currentCond
    if(matrixName == 'FinDiffOprtr'):  
        MincondNumFinDif = currentCond  
        MaxcondNumFinDif = currentCond           

def MinMaxcond(A, matrixName):
    global MincondNumA
    global MincondNumFinDif
    global MaxcondNumA
    global MaxcondNumFinDif
    currentCond = np.linalg.cond(A)
    if(matrixName == 'A'):
            if(MaxcondNumA < currentCond):
                MaxcondNumA = currentCond
            if(MincondNumA >= currentCond):
                MincondNumA = currentCond          
    if(matrixName == 'FinDiffOprtr'):
            if(MaxcondNumFinDif < currentCond):
                MaxcondNumFinDif = currentCond   
            if(MincondNumFinDif > currentCond):
                MincondNumFinDif = currentCond                

global numToSolv 
numToSolv = 0 

global BigstabIterNumb
BigstabIterNumb = dict()

global NumbBigsCalls
NumbBigsCalls = 0 

global infoinEachIt
infoinEachIt = []

global ListA
ListA = []

import time

class Timers:

    def __init__(self, name):
        self.name = name
        self.timers = dict()
        self._start_time = dict() 
        self.info = ''     

    def tic (self, timername):
        self._start_time[timername] =  time.time_ns()
        if ( timername not in self.timers.keys()):
            self.timers[timername] = 0

    def toc (self, timername):
        self.timers[timername] +=  time.time_ns() - self._start_time[timername]

    def changeName (self, newName):
        self.name = newName

    def addInfo (self, info):
        self.info = self.info + info + '\n'

    def GetInfo(self, name):
        return ( self.timers[name] )    
             
             
    def print (self):
       
        with open ( directory + self.name + '.txt', 'w') as f:
            f.write( 'info:' + '\n' + self.info + '\n')
        with open ( directory + self.name + '.txt', 'a') as f:
            f.write('times:' + '\n')
        sorted_tuple = sorted(self.timers.items(), key=lambda x: x[1])
        self.timers = dict(sorted_tuple)
        for key, value in self.timers.items():
            with open ( directory + self.name + '.txt', 'a') as f:
                f.write( repr(value * 1e-9 / (self.timers['all program time']*1e-9+0.01)*100 ) + '%  ' + repr(value * 1e-9) + "     " +  repr(key) + ' ' + '\n')


T = Timers(" ")

global toler
toler = 0 

global r
r = 0 

global Csimple
Csimple = 0

global AndersonIter
AndersonIter = 0

global directory
directory = ' '

global numLinalgCalls
numLinalgCalls = 0 

global itersolve
itersolve = False

global normalize
normalize = False

global solush
solush = np.arange(1, 2, 1)

global to_solv_lst_st
to_solv_lst_st = [0]

global Ctemplate
Ctemplate = ' '


global counter
counter = 0 

global A_inv_saved
A_inv_saved = np.ones((2,3))

global NNN
NNN = 0

global reused
reused = False

global tolerReuse
tolerReuse = 0

global cmapp
cmapp = 0

def plot_w (Fr_lstTmStp, Gks):
    x = Fr_lstTmStp.mesh.CenterCoor[Fr_lstTmStp.EltChannel][:,0]
    y = Fr_lstTmStp.mesh.CenterCoor[Fr_lstTmStp.EltChannel][:,1]
    z = np.ones(len(Fr_lstTmStp.EltChannel))
    for i in range(0, len(Fr_lstTmStp.EltChannel)):
        z[i] = Gks[i]
    fig = plt.figure()
    plt.title( repr(NumbBigsCalls))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z)
    plt.show()

