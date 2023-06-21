# -*- coding: utf-8 -*-
import numpy as np
import math

# -------------- Physical parameter -------------- #

# -- Solid -- #

sigma_o = 1e6
# confining stress [Pa]

E = 1e10
# Young's modulus [Pa]

nu = 0.25
# Poisson's ratio [-]

KIc = 0*1.5e6
# Fracture toughness of the solid [Pa m^(1/2)]

rho_s = 2700
# density of the solid [kg m^(-3)]

cl = 1e-10
# Carters leak of coefficient [m s^(-1/2)]

# -- Fluid -- #

mu = 1e-1
# dynamic fluid viscosity [Pa s]

rho_f = 1e3
# fluid density [kg m^(-3)]


# -- Injection -- #

t_change = [0.0, 60, 100, 160]
# times when the injection rate changes [s]
# Note: For injection histories the first entry always needs to be 0.0!

Qo = [0.02, 0.02, 0.02, 0.02]
# Injection rates in the time windows defined in t_change [m^3/s]
# Note: For a continuous injection use "Qo = your_injection_rate". For injection histories the number of entries in Qo
# must match with the number of entries in t_change. First entry of Qo is injection for t between the first and second
# entry of t_change and so on.

# -- Geometry -- #


# -------------- Essential simulation parameter -------------- #

# -- Space discretization -- #

domain_limits = [-6, 6, -6, 6]
# Limits of the simulated domain [m]. Defined as [min(x), max(x), min(y), max(y)] for the fracture in a x|y plane.

number_of_elements = [21, 21]
# Number of elements [-]. First is the number of elements in direction x, second in direction y.
# Note: We recommend to use a discretization with a minimum of 41 elements (precision) and a maximum of 101 elements
# (computational cost) per direction.

# -- Time discretization (optional) -- #
# Note: Time discretisation is optional as an automatic time-stepping is implemented. You can however specify some
# features that are important for your simulation.

fixed_times = [30, 75, 150]
# The fracture will automatically be saved at the times fixed within fixed_times [s]. If you leave it empty "fixed_times
# = []" the default scheme is applied.

max_timestep = np.inf
# The maximum a time step can take [s].
# Using np.inf means that we do not fix a maximum for the time-step


# -- Miscellaneous -- #

sim_name = 'Sample_Simulation'
# Name you want to give your simulation. The folder where the data is stored will appear as such.

save_folder = "./Data/Sample_Simulations"
# The folder where the results of your simulation get saved within.

final_time = 2e3
# The time when your simulation should stop [s]

# local imports
from mesh import CartesianMesh
from properties import MaterialProperties, FluidProperties, InjectionProperties, SimulationProperties
from fracture import Fracture
from controller import Controller
from fracture_initialization import Geometry, InitializationParameters
from utility import setup_logging_to_console
from elasticity import load_isotropic_elasticity_matrix_toepliz
from fracture_initialization import get_radial_survey_cells
import warnings
warnings.filterwarnings("ignore")

Ep = E/(1 - nu * nu)
mup = 12 * mu
Kp = np.sqrt(32/np.pi)*KIc
if type(Qo) == list:
    inj = np.asarray([t_change,
                        Qo])
else:
    inj = Qo

# setting up the verbosity level of the log at console
setup_logging_to_console(verbosity_level='info')

Mesh = CartesianMesh(
    domain_limits[:2], 
    domain_limits[2:], 
    number_of_elements[0], 
    number_of_elements[1]
)

Injection = InjectionProperties(
    inj, 
    Mesh
)

Fluid = FluidProperties(
    viscosity=mu, 
    density=rho_f
)

simulProp = SimulationProperties()
simulProp.finalTime = final_time

# Setting the folder where the simulation results are saved.
simulProp.set_outputFolder(save_folder)
simulProp.set_simulation_name(sim_name)

simulProp.useBlockToeplizCompression = True

if len(fixed_times) != 0:
    simulProp.set_solTimeSeries(np.asarray(fixed_times))

simulProp.timeStepLimit = max_timestep
    
def sigmaO_func(x, y):
    if y < 4:
        return sigma_o  
    else:
        return sigma_o*3

Solid = MaterialProperties(
    Mesh,
    Ep,
    KIc,
    Carters_coef=cl,
    confining_stress_func=sigmaO_func
)
simulProp.gravity = True

simulProp.enableRemeshing = True
simulProp.set_mesh_extension_factor(1.2)

simulProp.tolFractFront = 0.01
simulProp.toleranceEHL = 0.001

simulProp.plotVar = ['footprint']       # plotting footprint
simulProp.bckColor = 'confining stress'         # setting the parameter for the mesh color coding

# initializing fracture
Fr_geometry = Geometry( 'radial', radius=3 )

C = load_isotropic_elasticity_matrix_toepliz(Mesh, Ep)

init_param = InitializationParameters(
    Fr_geometry
)

# creating fracture object
Fr = Fracture(
    Mesh,
    init_param,
    Solid,
    Fluid,
    Injection,
    simulProp
)

# create a Controller
controller = Controller(
    Fr,
    Solid,
    Fluid,
    Injection,
    simulProp
)

simulProp.saveToDisk = False
simulProp.plotFigure = True
simulProp.log2file = False
simulProp.enableGPU = True

# run the simulation
controller.run()