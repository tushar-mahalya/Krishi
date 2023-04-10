import os
import sys

from src.exception import CustomException


def get_path(plant_dir:str, test:bool=False):
    
    '''
    This function accepts plants directory name (str) and returns
    the path of training or testing directory whichever chosen.
    
    '''
    try:
        if test:
            return '/home/studio-lab-user/Krishi/data/' + plant_dir + '/Test'

        else:
            return '/home/studio-lab-user/Krishi/data/' + plant_dir + '/Train'
    
    except Exception as e:
        raise CustomException(e, sys)

    
def test_val_partitions(test_ds, val_split: float, shuffle: bool, shuffle_size: int):
    
    try:
        val_size = int(len(test_ds)*val_split)

        if shuffle:
            test_ds = test_ds.shuffle(shuffle_size, seed = 42)

        val_data = test_ds.take(val_size)
        test_data = test_ds.skip(val_size)

        return test_data, val_data
    
    except Exception as e:
        raise CustomException(e, sys)