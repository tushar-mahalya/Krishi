import os
import sys
import json

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

    
def get_data_info(data_dir_path:str):
    '''
    This Function accepts the path of data directory as input and returns the
    dictionary having all the details about it.
    
    '''
    try:
        plant_dirs = list(os.listdir(data_dir_path))
        plants_data = {}
        for plant in plant_dirs:
            data_split_path = {
                'train': get_path(plant, 'Train'),
                'test': get_path(plant, 'Test'),
                'val': get_path(plant, 'Val')
            }
            
            classes_lst = []
            for cat in os.listdir(get_path(plant,'Train')):
                classes_lst.append(cat)
            
            plants_data[plant] = {
            	'data_split':data_split_path,
                'classes':classes_lst
            }
            
            os.makedirs('/home/studio-lab-user/Krishi/artifacts', exist_ok = True)
            
            with open("/home/studio-lab-user/Krishi/artifacts/dataset_info.json", "w") as outfile:
                json.dump(plants_data, outfile)
                
        print('Successfully saved Dataset Information in \'artifacts/dataset_info.json\'')
        
    
    except Exception as e:
        raise CustomException(e, sys)