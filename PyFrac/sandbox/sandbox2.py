#import postprocess_performance as pp
#pp.plot_performance('C:\\MyBackup\\workarea\\src\\PyFrac\\PyFracMP1\\1\\','tip inversion iterations','')

#pp.print_performance_data('C:\\MyBackup\\workarea\\src\\PyFrac\\PyFracMP1\\Data\\height_contained', 'simulation__2022-06-21__14_27_55')
#exit();

# imports
import os

# local imports
from mesh import CartesianMesh
from properties import MaterialProperties, FluidProperties, InjectionProperties, SimulationProperties
from fracture import Fracture
from controller import Controller
from fracture_initialization import Geometry, InitializationParameters
from utility import setup_logging_to_console

def sand (num_split_x, num_split_y, myCompressibility, min_w, time, Q, lx, ly):
    # setting up the verbosity level of the log at console
    setup_logging_to_console(verbosity_level='info')

    # creating mesh
    Mesh = CartesianMesh(lx, ly, num_split_x, num_split_y)

    # solid properties
    nu = 0.4                            # Poisson's ratio
    youngs_mod = 3.3e10                 # Young's modulus
    Eprime = youngs_mod / (1 - nu ** 2) # plain strain modulus
    K_Ic = 0                            # fracture toughness of the material

    if(mf.crackForm == 'pkn'):
        def sigmaO_func(x, y):

            if abs(y) > 25:
                return 2e+7
            else:
                return 3e+6
    if (mf.crackForm == 'sandglass'):
        # sangglass
        def sigmaO_func(x, y):
            if abs(y) > 25:
                return 2e+7
            elif (y > 5) and (y<10):
                return 0.95*2e+7
            else:
                return 3e+6
    
        

    cl = 0 # Carters leak of coefficient [m s^(-1/2)] 
    Solid = MaterialProperties(Mesh,
                            Eprime,
                            K_Ic,
                            Carters_coef=cl,
                            confining_stress_func=sigmaO_func,
                            minimum_width = min_w)

    # injection parameters
    Q0 = Q  # injection rate
    Injection = InjectionProperties(Q0, Mesh)

    mf.Q = Q0

    # fluid properties
    Fluid = FluidProperties(viscosity=1e-3, compressibility = myCompressibility)

    # simulation properties
    simulProp = SimulationProperties()
    simulProp.finalTime = time              # the time at which the simulation stops
    simulProp.bckColor = 'sigma0'           # setting the parameter according to which the mesh is color coded
    simulProp.set_outputFolder(mf.folder)
    simulProp.tmStpPrefactor = 1.0          # decreasing the size of time step
    simulProp.saveToDisk = False
    simulProp.outputTimePeriod = 50                   # to save after every time step
    simulProp.plotFigure = False
    simulProp.collectPerfData

    #simulProp.set_tipAsymptote('M')                     # tip asymptote is evaluated with the viscosity dominated assumption

    #simulProp.frontAdvancing = 'explicit'               # to set explicit front tracking
    simulProp.solveSparse = False
    simulProp.log2file = False
    #simulProp.solveStagnantTip = True

    #simulProp.plotVar = ['footprint']       # plotting footprint


    simulProp.enableRemeshing = True
    simulProp.remeshFactor = 1.1
    simulProp.collectPerfData = False

    #simulProp.meshReductionFactor = 1.5
    #simulProp.maxElementIn = 1000
    #simulProp.maxCellSize = 5

    #simulProp.set_mesh_extension_factor(1.5)
    #simulProp.verbositylevel = 'critical'

    #simulProp.meshExtensionAllDir = True
    #simulProp.set_mesh_extension_direction(['horizontal'])

    simulProp.maxSolverItrs = 2000                                   # increase the Anderson iteration limit for the
                                                                    # elastohydrodynamic solver
    simulProp.maxFrontItrs = 2000

    simulProp.toleranceEHL = mf.tolInAnders

    #simulProp.relaxation_factor = 0.5                       # relax Anderson iteration

    # initializing fracture
    Fr_geometry = Geometry(shape='radial', radius = 30.)
    init_param = InitializationParameters(Fr_geometry, regime='M')

    # creating fracture object
    Fr = Fracture(Mesh,
                init_param,
                Solid,
                Fluid,
                Injection,
                simulProp)

    # create a Controller
    controller = Controller(Fr,
                            Solid,
                            Fluid,
                            Injection,
                            simulProp)

    
    # run the simulation
    controller.run()

    return(controller.get_max_width_and_half_length(controller.fracture))

import MyFunionsFile as mf # file with Timer and global varibles

# net parameters
nn = 70
n = nn
m = nn = nn
m = n
num_split_x = n
num_split_y = m
lx = 250
ly = 250
# problem parameters
myCompressibility = 1e-9
min_w = 1e-6
time  = 300
Q0 = 0.053

# for matrix view
mf.cmapp = 'viridis' 

# solving system parameters
mf.reused = True
mf.itersolve = True
mf.Ctemplate = '5x5point'     
mf.tolerReuse = 0.05  # tolerance for reusing
mf.toler = 1e-5*Q0 # tolerance for bisgstab iterations
mf.tolInAnders = 0.001

mf.crackForm = 'sandglass'  # 'pkn'  'sandglass'

#  simplified C templates:                                             .                .....                    ...
#                                    .                ...             ...               .....                   .....          
#   diagonal , 3point(...) , 5point(...)  , 3x3point (...) , 12point(.....) ,  5x5point(.....), peirce class II .....
#                                    .                ...             ...               .....                   .....
#                                                                      .                .....                    ...

# define derectory and name for output file
folderName = 'n_' + repr(nn) +'_'+  mf.crackForm  +'_AndrTol_' + repr(mf.tolInAnders) + '_l_' + repr(lx) + '_time_' + repr(time) 
import os
path = 'C:/Users/VShukalo/myFolder/work/current_num_results/time/d(dw)_d(dp)_drowing/'+ folderName
        

# Создаем директорию
try:
    os.makedirs(path)
except FileExistsError:
    print('Директория уже существует')

mf.folder = path +'/'



if ((mf.reused) and (mf.itersolve)):
    mf.directory =  mf.folder+' Iter_Reuse ' + ' reu_tolnorm ' + repr(mf.tolerReuse) +' ' + repr(mf.Ctemplate) + ' '
if (( not mf.reused) and (mf.itersolve)):
    mf.directory = mf.folder   + ' Iter ' + repr(mf.Ctemplate) + ' '
if (( not mf.reused) and (not mf.itersolve)):    
    mf.directory =  mf.folder   + ' standart ' 



mf.T.changeName('n = ' + repr(n) + ' tough 0' + ' lx ' + repr(lx) + ' ly '+ repr(ly) + ' time ' + repr (time)  )

# run the calculation
mf.T.tic("all program time")
w, l = sand(num_split_x, num_split_y, myCompressibility, min_w, time, Q0, lx,ly)    
mf.T.toc("all program time")

#add info to file
mf.T.addInfo ('n = ' + repr(n) + ' time ' + repr(time) + ' tosolve ' + repr(mf.numToSolv) )
mf.T.addInfo( 'w, l ' +  repr(w) + ' ' + repr(l) )
if (mf.itersolve == False):
    mf.T.addInfo ( 'numLinalgCalls ' + repr(mf.numLinalgCalls))
else:
    mf.T.addInfo( 'numBCG_Calls ' +  repr(mf.NumbBigsCalls) )    

mf.T.addInfo( 'Anderson Iter numb ' +  repr(mf.AndersonIter) )
mf.T.addInfo( 'Anderson calls numb ' +  repr(mf.NumAndersonCalls) )
mf.T.addInfo( 'Toughness Iter numb ' +  repr(mf.ToughnessIterNumb) )
mf.T.addInfo( 'Front Iter numb ' +  repr(mf.NumbFrontIter) )
mf.T.addInfo( 'Constraint Iter numb ' +  repr(mf.ConsrtaintIterNumb) )



# add to file averaged num of bicgstab iter, time of bicgstab call, time of Ainv
sum = 0
if (mf.itersolve == True):
    #with open ( mf.directory + 'bicg num iter ' + mf.T.name + '.txt', 'a') as f:
    for i in range(0, mf.NumbBigsCalls):
            #f.write( 'number of Bigstab iter: '  + repr(mf.BigstabIterNumb[i]) + '\n' )
        sum = sum + mf.BigstabIterNumb[i]
        #f.write('average num of bicgstab iter ' + repr(sum/mf.NumbBigsCalls) + '\n')
        #name = ' bicgstab(A, b, callback = countBigstabIter, M = M )'
        #f.write('average time of bicgstab call ' + repr( mf.T.GetInfo(name)* 1e-9/mf.NumbBigsCalls)+ '\n')

        #name = 'A_inv Simple = spilu(A_sp)'
        #f.write('average time of Ainv ' + repr( mf.T.GetInfo(name)* 1e-9/mf.NumbBigsCalls)+ '\n')

    mf.T.addInfo('average num of bicgstab iter ' + repr(sum/mf.NumbBigsCalls) )
    name = ' bicgstab(A, b, callback = countBigstabIter, M = M )'
    mf.T.addInfo('average time of bicgstab call ' + repr( mf.T.GetInfo(name)* 1e-9/mf.NumbBigsCalls))
    name = 'A_inv Simple = spilu(A_sp)'
    mf.T.addInfo('average time of Ainv ' + repr( mf.T.GetInfo(name)* 1e-9/mf.NumbBigsCalls))


# output info + times in file
mf.T.print()
