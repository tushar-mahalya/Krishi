import os
import sys

from src.exception import CustomException


def get_path(plant_dir:str, dir_test:str):
    
    '''
    This function accepts plants directory name (str)  and directory type as 
    input and returns the path of training, testing or validation directory
    whichever chosen.
    
    '''
    try:
        if dir_test == 'Test':
            return '/home/studio-lab-user/Krishi/data/' + plant_dir + '/Test'

        elif dir_test == 'Train':
            return '/home/studio-lab-user/Krishi/data/' + plant_dir + '/Train'
        
        elif dir_test == 'Val':
            return '/home/studio-lab-user/Krishi/data/' + plant_dir + '/Val'
    
    except Exception as e:
        raise CustomException(e, sys)

    
