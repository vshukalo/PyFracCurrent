import pytest
from sandbox2 import sand

set_input_1 = (
                60,     # num_split_x
                60,     # num_split_y
                1e-9,   # Compressibility
                1e-6,   # min_w
                100.0,  # time
                0.053,  # Q
                150,    # lx
                150     # ly   
                ) 

set_expected_1 = (1.493012553383768E-003, # w_max_benchmark
                        59.6618148640412, # half_l_benchmark
                        0.5,              # eps_w
                        0.01              # eps_half_l
                )

set_input_2 = ( 
                60,     # num_split_x
                60,     # num_split_y
                1e-9,   # Compressibility
                1e-6,   # min_w
                200.0,  # time
                0.053,  # Q
                150,    # lx
                150     # ly   
                ) 

set_expected_2 = ( 1.715021064061857E-003, # w_max_benchmark
                   103.877253074320,       # half_l_benchmark
                   0.5,                    # eps_w
                   0.01                    # eps_half_l
                ) 


@pytest.mark.parametrize("test_input,expected", [ 
        (set_input_1, set_expected_1), 
        (set_input_2, set_expected_2) ])

def test_sand(test_input, expected ):
    sand_var = sand(*test_input)
    err_rel_w = abs(expected[0] - sand_var[0]) / expected[0] 
    err_rel_half_l = abs(expected[1] - sand_var[1]) / expected[1]
    
    assert (err_rel_w, err_rel_half_l)  < (expected[2], expected[3])

test_sand(set_input_1, set_expected_1)