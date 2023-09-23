import sandbox2
import cProfile, pstats


profiler = cProfile.Profile()
profiler.enable()                

num_split_x = 100
num_split_y = 100

set_input_2 = ( 
                num_split_x,     # num_split_x
                num_split_y,      # num_split_y
                1e-9, # Compressibility
                1e-6, # min_w
                250, # time
                0.053, # Q
                150, # lx
                150 # ly
                ) 

sandbox2.sand(*set_input_2)

profiler.disable()

stats = pstats.Stats(profiler).strip_dirs().sort_stats('cumtime')

stats.print_stats()
