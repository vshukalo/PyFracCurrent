# -------------- Post Processing -------------- #

if post_process_the_results:

    # -- loading simulation results -- #
    from visualization import *
    Fr_list, properties = load_fractures(address=save_folder, sim_name=sim_name,  step_size=1)  # load all fractures
    time_srs = get_fracture_variable(Fr_list, variable='time')  # list of times
    Solid, Fluid, Injection, simulProp = properties


    # -- FIGURE 1) plot fracture footprint VS time -- #
    # plot the solution every "tsJump" time steps
    tsJump = 10
    sol_at_selected_times = []
    for i in np.arange(0, len(Fr_list), tsJump):
        sol_at_selected_times.append(Fr_list[i])
    plot_prop = PlotProperties()
    Fig_R = plot_fracture_list(sol_at_selected_times,
                               variable='footprint',
                               plot_prop=plot_prop)
    Fig_R = plot_fracture_list(sol_at_selected_times,
                               fig=Fig_R,
                               variable='mesh',
                               mat_properties=properties[0],
                               plot_prop=plot_prop)


    # -- FIGURE 2) plot fracture radius VS time -- #
    # plot the solution every "tsJump" time steps
    tsJump = 10
    sol_at_selected_times = []
    for i in np.arange(0, len(Fr_list), tsJump):
        sol_at_selected_times.append(Fr_list[i])
    plot_prop = PlotProperties()
    plot_prop.lineStyle = '.'               # setting the linestyle to point
    plot_prop.graphScaling = 'loglog'       # setting to log log plot
    Fig_R = plot_fracture_list(sol_at_selected_times,
                               variable='d_mean',
                               plot_prop=plot_prop)


    # -- FIGURES 3) and 4) plot fracture opening VS time at a given point (my_X, my_Y)-- #
    # plot the solution every "tsJump" time steps
    tsJump = 10
    my_X = 0.0
    my_Y = 0.0
    sol_at_selected_times = []
    for i in np.arange(0, len(Fr_list), tsJump):
        sol_at_selected_times.append(Fr_list[i])

    Fig_w = plot_fracture_list_at_point(sol_at_selected_times,
                                        variable='w',
                                        point=[my_X, my_Y],
                                        plot_prop=plot_prop)


    # -- FIGURES 5) and 6) plot net fluid pressure VS time at a given point (my_X, my_Y)-- #
    # plot the solution every "tsJump" time steps
    tsJump = 10
    my_X = 0.0
    my_Y = 0.0

    sol_at_selected_times = []
    for i in np.arange(0, len(Fr_list), tsJump):
        sol_at_selected_times.append(Fr_list[i])

    Fig_pf = plot_fracture_list_at_point(sol_at_selected_times,
                                        variable='pn',
                                        point=[my_X, my_Y],
                                        plot_prop=plot_prop)


    # --  FIGURE 7) plot fracture opening along a segment cutting the fracture at given times -- #
    # --  the segment is horizontal and passing at (my_X, my_Y) -- #
    # plot the solution every "tsJump" time steps
    tsJump = 10
    my_X = 0.
    my_Y = 0.

    sol_at_selected_times = []
    for i in np.arange(0, len(Fr_list), tsJump):
        sol_at_selected_times.append(Fr_list[i])

    ext_pnts = np.empty((2, 2), dtype=np.float64)
    Fig_WS = plot_fracture_list_slice(sol_at_selected_times,
                                      variable='w',
                                      projection='2D',
                                      plot_cell_center=True,
                                      extreme_points=ext_pnts,
                                      orientation='horizontal',
                                      point1=[my_X, my_Y]
                                      )
    plt.show(block=True)


# -------------- exporting to json file -------------- #

from visualization import *
from postprocess_fracture import append_to_json_file

# 1) export general information to json
# 2) export to json the coordinates of the points defining the fracture front at each time
# 3) export the fracture opening w(t) versus time (t) at a point of coordinates myX and myY
# 4) export the fluid pressure p(t) versus time (t) at a point of coordinates myX and myY
# 5) export w(y) along a vertical line passing through mypoint for different times
# 6) export pf(x) along a horizontal line passing through mypoint for different times
# 7) export w(x,y,t) and pf(x,y,t)

to_export = [1,2,3,4,5,6,7]

if export_results_to_json:

    # decide the names of the Json files:
    myJsonName_1 = "./Data/Pyfrac_"+sim_name+"_export.json"

    # load the results:
    print("\n 1) loading results")
    Fr_list, properties = load_fractures(address=save_folder, sim_name=sim_name, load_all=True)
    # or Fr_list, properties = load_fractures(address=save_folder, sim_name=sim_name, time_srs=np.linspace(initial_time, final_time, steps))
    Solid, Fluid, Injection, simulProp = properties
    print(" <-- DONE\n")

    # 1) export general information to json
    if 1 in to_export:
        print("\n 2) writing general info")
        time_srs = get_fracture_variable(Fr_list, variable='time')
        time_srs = np.asarray(time_srs)

        simul_info = {'Eprime': Solid.Eprime,
                      'max_KIc': Solid.K1c.max(),
                      'min_KIc': Solid.K1c.min(),
                      'max_Sigma0': Solid.SigmaO.max(),
                      'min_Sigma0': Solid.SigmaO.min(),
                      'viscosity': Fluid.viscosity,
                      'total_injection_rate': Injection.injectionRate.max(),
                      'sources_coordinates_lastFR': Fr_list[-1].mesh.CenterCoor[Injection.sourceElem].tolist(),
                      't_max': time_srs.max(),
                      't_min': time_srs.min()}
        append_to_json_file(myJsonName_1, simul_info, 'append2keyASnewlist', key='simul_info',
                            delete_existing_filename=True)  # be careful: delete_existing_filename=True only the first time you call "append_to_json_file"

    # 2) export the coordinates of the points defining the fracture front at each time:
    if 2 in to_export:
        print("\n 2) writing fronts")
        time_srs = get_fracture_variable(Fr_list,variable='time') # get the list of times corresponding to each fracture object
        append_to_json_file(myJsonName_1, time_srs, 'append2keyASnewlist', key='time_srs_of_Fr_list')
        fracture_fronts = []
        numberof_fronts = [] #there might be multiple fracture fronts in general
        mesh_info = [] # if you do not make remeshing or mesh extension you can export it only once
        index = 0
        for fracture in Fr_list:
            fracture_fronts.append(np.ndarray.tolist(fracture.Ffront))
            numberof_fronts.append(fracture.number_of_fronts)
            mesh_info.append([Fr_list[index].mesh.Lx, Fr_list[index].mesh.Ly, Fr_list[index].mesh.nx, Fr_list[index].mesh.ny])
            index = index + 1
        append_to_json_file(myJsonName_1, fracture_fronts, 'append2keyASnewlist', key='Fr_list')
        append_to_json_file(myJsonName_1, numberof_fronts, 'append2keyASnewlist', key='Number_of_fronts')
        append_to_json_file(myJsonName_1,mesh_info,'append2keyASnewlist', key='mesh_info')
        print(" <-- DONE\n")

    # 3) export the fracture opening w(t) versus time (t) at a point of coordinates myX and myY
    if 3 in to_export:
        print("\n 3) get w(t) at a point... ")
        my_X = 0.02 ; my_Y = 0.
        w_at_my_point, time_list_at_my_point = get_fracture_variable_at_point(Fr_list, variable='w', point=[my_X, my_Y])
        append_to_json_file(myJsonName_1, w_at_my_point, 'append2keyASnewlist', key='w_at_my_point')
        append_to_json_file(myJsonName_1, time_list_at_my_point, 'append2keyASnewlist', key='time_list_W_at_my_point')
        print(" <-- DONE\n")



    # 4) export the fluid pressure p(t) versus time (t) at a point of coordinates myX and myY
    if 4 in to_export:
        print("\n 4) get pf(t) at a point... ")
        my_X = 0.02 ; my_Y = 0.
        pf_at_my_point, time_list_at_my_point = get_fracture_variable_at_point(Fr_list, variable='pf', point=[my_X, my_Y])
        append_to_json_file(myJsonName_1, pf_at_my_point, 'append2keyASnewlist', key='pf_at_my_point_A')
        append_to_json_file(myJsonName_1, time_list_at_my_point, 'append2keyASnewlist', key='time_list_pf_at_my_point_A')
        print(" <-- DONE\n")


    # 5) export w(y) along a vertical line passing through mypoint for different times
    if 5 in to_export:
        print("\n 5) get w(y) with y passing through a specific point for different times... ")
        my_X = 0.; my_Y = 0.
        ext_pnts = np.empty((2, 2), dtype=np.float64)
        fracture_list_slice = plot_fracture_list_slice(Fr_list,
                                                       variable='w',
                                                       projection='2D',
                                                       plot_cell_center=True,
                                                       extreme_points=ext_pnts,
                                                       orientation='horizontal',
                                                       point1=[my_X , my_Y],
                                                       export2Json=True,
                                                       export2Json_assuming_no_remeshing=False)
        towrite = {'w_vert_slice_': fracture_list_slice}
        append_to_json_file(myJsonName_1, towrite, 'extend_dictionary')
        print(" <-- DONE\n")



    # 6) export pf(x) along a horizontal line passing through mypoint for different times
    if 6 in to_export:
        print("\n 6) get pf(x) with x passing through a specific point for different times... ")
        my_X = 0.; my_Y = 0.
        ext_pnts = np.empty((2, 2), dtype=np.float64)
        fracture_list_slice = plot_fracture_list_slice(Fr_list,
                                                       variable='pf',
                                                       projection='2D',
                                                       plot_cell_center=True,
                                                       extreme_points=ext_pnts,
                                                       orientation='horizontal',
                                                       point1=[my_X , my_Y],
                                                       export2Json=True,
                                                       export2Json_assuming_no_remeshing=False)
        towrite = {'pf_horiz_slice_': fracture_list_slice}
        append_to_json_file(myJsonName_1, towrite, 'extend_dictionary')
        print(" <-- DONE\n")



    # 7) export w(x,y,t) and pf(x,y,t)
    if 7 in to_export:
        print("\n 7) get w(x,y,t) and  pf(x,y,t)... ")
        wofxyandt = []
        pofxyandt = []
        info = []
        jump = True #this is used to jump the first fracture
        for frac in Fr_list:
            if not jump:
                wofxyandt.append(np.ndarray.tolist(frac.w))
                pofxyandt.append(np.ndarray.tolist(frac.pFluid))
                info.append([frac.mesh.Lx,frac.mesh.Ly,frac.mesh.nx,frac.mesh.ny,frac.time])
            else:
                jump = False

        append_to_json_file(myJsonName_1, wofxyandt, 'append2keyASnewlist', key='w')
        append_to_json_file(myJsonName_1, pofxyandt, 'append2keyASnewlist', key='p')
        append_to_json_file(myJsonName_1, info, 'append2keyASnewlist', key='info_for_w_and_p')
        print(" <-- DONE\n")

    print("DONE! in " + myJsonName_1)

# -------------- END OF FILE -------------- #