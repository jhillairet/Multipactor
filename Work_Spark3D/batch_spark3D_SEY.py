# -*- coding: utf-8 -*-
"""
Repeat a Spark3D Simulation NB_OF_SIMULATION times, 
and for different SEY files.

Save the results into a text file. 

@author: JH218595
"""
import numpy as np
from spark3d import *

NB_OF_SIMULATION = 3

project_path = '/home/JH218595/Multipactor/Work_Spark3D/Projects/K-S8'
EMfields_file = '../../EM_Fields/K-S8/K-S8_fields.mfe'

RESULT_FILE = project_path+'/RESULTS_vs_SEY.txt'

# List of the SEY files to run
sey_files = ['"../../SEY/K-S8_Courbe_SEY_REF_modif_Ec1_19eV.csv"', 
             '"../../SEY/K-S8_Courbe_SEY_REF_modif_Ec1_30eV.csv"', 
             '"../../SEY/K-S8_Courbe_SEY_REF_modif_Ec1_70eV.csv"']
             
# Creates the dummy project
spk = Spark3d(project_path, EMfields_file, file_type='fest')

for sey_file in sey_files:
    # set the sey file in the current project
    spk.set_config_parameter('sey_input_file', sey_file)
    print('Current SEY file:', spk.get_config_parameter('sey_input_file'))
    
    # run spark NB_OF_SIMULATION times and save the results
    counter = 0
    while counter < NB_OF_SIMULATION:
        spk.run(show_stdout=True)
        # Append the results to a text file
        freq, power = spk.get_results()
        with open(RESULT_FILE,'ab') as f_handle:
            # below, the reshape is a trick to write the array into a single
            # row instead of two. 
            np.savetxt(f_handle, np.array([sey_file, power]).reshape(1, 2), 
                       fmt="%s")
        counter = counter + 1
