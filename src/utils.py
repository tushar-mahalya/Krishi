import os
import sys
import json
import matplotlib.pyplot as plt
import seaborn as sns

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

    
def plot_history(model_info_dict:dict, plant_name:str):
    
    '''
    This function plots the accuracy and loss metrics of training and validation data
    using Model Information Dictionary (artifacts/model_info.json) saved during model training.
    '''
    try:
        history = model_info_dict[plant_name]['Training History']

        # Create subplots for loss and accuracy
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # Plot training and validation loss
        sns.lineplot(x=range(1, len(history['loss'])+1), y=history['loss'], ax=ax1, label='Training Loss')
        sns.lineplot(x=range(1, len(history['val_loss'])+1), y=history['val_loss'], ax=ax1, label='Validation Loss')
        ax1.set_title('Model Loss')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss')
        ax1.legend()
        ax1.grid(True)

        # Plot training and validation accuracy
        sns.lineplot(x=range(1, len(history['accuracy'])+1), y=history['accuracy'], ax=ax2, label='Training Accuracy')
        sns.lineplot(x=range(1, len(history['val_accuracy'])+1), y=history['val_accuracy'], ax=ax2, label='Validation Accuracy')
        ax2.set_title('Model Accuracy')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Accuracy')
        ax2.legend()
        ax2.grid(True)

        # Add an overall title to the plot
        plt.suptitle(f'{plant_name} Model Training History', fontsize=16, fontweight='bold')

        # Display the plot
        plt.show()
        
    except Exception as e:
        raise CustomException(e, sys)