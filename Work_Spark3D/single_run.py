import spark3d 

## directory where the Spark3D project configuration file (config.min) is located
#project_path = '/home/JH218595/Multipactor/Work_Spark3D/Projects/Simple_Waveguide_WR284_3.7GHz'
## relative directory where the electromagnetic fields file (.dsp, .mfe) is located
#EMfields_file = '../../EM_Fields/data_HFSS/SimpleWaveguideFields_72.14x22mm/SimpleWaveguideFields_72.14x22mm_50mm_V2.dsp'
#
#simu = spark3d.Spark3d(project_path, EMfields_file)
#
#simu.run()
#freq, power = simu.get_results()
#print(freq/1e9, power)

# directory where the Spark3D project configuration file (config.min) is located
project_path = '/home/JH218595/Multipactor/Work_Spark3D/Projects/K-S8'
# relative directory where the electromagnetic fields file (.dsp, .mfe) is located
EMfields_file = '../../EM_Fields/K-S8/K-S8_fields.mfe'

simu = spark3d.Spark3d(project_path, EMfields_file, file_type='fest')

# get some parameter values
print(simu.get_config_parameter('sey_input_file'))
print(simu.get_config_parameter('initial_number_of_electrons'))

# to replace to parameter values:
simu.set_config_parameter('initial_number_of_electrons', '200')

# run the simulation. Use the option show_stdout=True to see Spark output
simu.run(show_stdout=True)

# display results
freq, power = simu.get_results()
print('Result are : f=' ,freq/1e9, 'GHz ; Power threshold=', power, 'W')


