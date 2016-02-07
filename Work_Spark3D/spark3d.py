# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 16:49:00 2014

@author: JH218595
"""
import os
import numpy as np 
import subprocess  # used instead of os.system()
import shlex # used to convert Spark3d command line into a list
import logging
            
class Spark3d(object):
    """
    SPARK3D simulation object
    
    """
    DIR_PATH = '/Applications/SPARK3D/1.6.3/dist'
    BIN_PATH = '/Applications/SPARK3D/1.6.3/dist/spark3d'

    
    def __init__(self, project_path, EMfields_file, file_type='hfss', 
                 output_path='results/', tmp_path='.', config_file='config.min'):
        """
        Constructor.
        
        Arguments
        ---------
         project_path : absolute path (important!) of the project. 
         data_file : relative path of the data file
         [file_type : {'hfss' (default, .dsp), 'cst', 'fest'(.mfe), 'csv'}]
         [output_path: relative path of the output dir (default: "results/")]
         [tmp_path: temporary file absolute path (default: '/tmp/SPKTMP')]
         [config_file: name of the config file (default: 'config.min')]
        
        """
        self.project_path = project_path
        self.data_file = EMfields_file
        self.file_type = file_type
        self.tmp_path = tmp_path
        self.config_file = config_file
        self.output_path = output_path
        self.log = logging.basicConfig(filename='spark3drun.log', filemode='w')
    
    def run(self, show_stdout=False):
        """
        Run the SPARK3D modeling. 
        
        """
        cmd = self.__get_run_command__()
        print(cmd)
        
        try:
            print('Running Spark3D...')
            p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
            
            # print the output of Spark3D in the standard output 
            # untill the end of the simulation
            if show_stdout:
                while p.poll() is None:  
                    print(p.stdout.readline())
            else:
                p.wait()
                
            retcode = p.returncode
            if retcode < 0:
                print('Child was terminated by signal', retcode)
            else:
                print('Child returned', retcode)
            
            
        except OSError as e:
            print('Non existent file ? (OSError):', e)
        except ValueError as e:
            print('Invalid Argument', e)
        except FileNotFoundError as e:
            print('file not found', e)
        except Exception as e:
            print('Something else occured:', e)
        
    def __get_run_command__(self):
        cmd = self.BIN_PATH + \
              ' --mode=multipactor' + \
              ' --project_path='+self.project_path + \
              ' --tmp_path='+self.tmp_path + \
              ' --config_file='+self.config_file + \
              ' --output_path='+self.output_path + \
              ' --data_file='+self.data_file + \
              ' --file_type='+self.file_type
        #cmd = '/Applications/SPARK3D/1.6.3/dist/spark3d --config_file=config.min --output_path=results/ --HFSS_units="m" --mode=multipactor --project_path=/home/JH218595/Multipactor/Spark3D/Simple_Waveguide_WR284_3.7GHz --tmp_path=. --data_file=data_HFSS/SimpleWaveguideFields_72.14x22mm_50mm_V2.dsp --file_type=hfss'

        return(cmd)
    
    def get_results(self):
        """
        Returns the SPARK3D run results
        
        Arguments
        ----------
         none
        
        Returns
        ----------
         freq: array of frequency
         power: array of breakdown power
         
        """
        result_file = self.project_path+'/'+self.output_path+'general_results.txt'
        
        try:
            freq, power = np.loadtxt(result_file, 
                               skiprows=1, 
                               delimiter='\t', 
                               usecols=(3,4), # use only columns 3 and 4
                               unpack=True)
            return freq, power   
        except Exception as e:
            print(e)
            return None, None

    def read_config(self):
        """
        Returns the content of the configuration file
        into a python dictionary
        """
        config = {}
        with open(self.project_path+'/'+self.config_file) as config_lines:
            for line in config_lines:
                # creates a new section if line start with begin
                if 'begin' in line:
                    dummy, section_name = line.split()
                    config[section_name] = dict()
                elif 'end' in line:
                    pass
                else:
                    dummy = line.split()
                    if len(dummy) ==2: # parameter value couple
                        parameter, value = line.split()
                        config[parameter] = value
        return config
            
    def write_config(self):
        """
        TODO
        """
        pass
    
    def get_config_parameter(self, parameter):
        """
        Return the value of a parameter defined in the configuration file.
        """
        config = self.read_config()
        
        return config[parameter]
        
    
    def set_config_parameter(self, parameter, new_value):
        """
        Replace a parameter value in the configuration file
    
        """
        
        current_config = self.read_config()
        config_file = self.project_path+'/'+self.config_file
        
        with open(config_file, 'r') as config:
            config_contents = config.read()
            # replace the previous parameter value with new one
            new_config_contents = config_contents.replace(current_config[parameter], new_value)
        
        if new_config_contents is not None:
            with open(config_file, 'w') as config:
                print(new_config_contents)
                config.write(new_config_contents)
            
            
           
if __name__ == "__main__":  
    project_path = '/home/JH218595/Multipactor/Work_Spark3D/Projects/Simple_Waveguide_WR284_3.7GHz'
    data_file = '../../EM_Fields/SimpleWaveguideFields_72.14x22mm/SimpleWaveguideFields_72.14x22mm_100mm_V2.dsp'  
    spk = Spark3d(project_path, data_file)     
    spk.run()
    freq, power = spk.get_results()
    print(freq, power)
#    with open('RESULTS.txt','ab') as f_handle:
#        np.savetxt(f_handle, np.array([power]))
