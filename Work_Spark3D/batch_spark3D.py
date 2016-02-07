# -*- coding: utf-8 -*-
"""
Repeat a Spark3D Simulation NB_OF_SIMULATION times.

Save the results into a text file. 

@author: JH218595
"""
from spark3d import *

NB_OF_SIMULATION = 5

project_path = '/home/JH218595/Multipactor/Work_Spark3D/Projects/K-S8'
EMfields_file = '../../EM_Fields/K-S8/K-S8_fields.mfe'

RESULT_FILE = project_path+'/RESULTS.txt'


spk = Spark3d(project_path, EMfields_file, file_type='fest')
counter = 0
while counter < NB_OF_SIMULATION:
    spk.run(show_stdout=False)
    # Append the results to a text file
    freq, power = spk.get_results()
    with open(RESULT_FILE,'ab') as f_handle:
        np.savetxt(f_handle, np.array([power]))
    counter = counter + 1
