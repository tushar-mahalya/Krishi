from tensorflow.data import AUTOTUNE
from keras.callbacks import EarlyStopping
from keras import Sequential, layers, models
from keras.layers import Resizing, Rescaling
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from keras.losses import SparseCategoricalCrossentropy
from keras.utils import image_dataset_from_directory

import sys
from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging
import os

@dataclass
class ModelTrainingConfig:
    dataset_info_path: str = '/home/studio-lab-user/Krishi/artifacts/dataset_info.json'
    
    
    
class ModelTraining:
    
    def __init__(self):
        config = ModelTrainingConfig()
        self.dataset_info_path = config.dataset_info_path
        
        # Image Dimentionality and Input shape
        self.image_dim = (256, 256)
        self.batch_size = 32
        self.num_channels = 3
        self.input_shape = (self.batch_size, self.image_dim[0], self.image_dim[1], self.num_channels)
  

    def load_dataset(self):
        
        try:
            with open(self.dataset_info_path) as f:
                self.data_info_dict = json.load(f)

            self.train_dataset = {}
            self.val_dataset = {}
            self.test_dataset = {}

            logging.info('Model Training Initiated ! Plants Dataset loading.')

            for plant in self.data_info_dict.keys():
                self.train_dataset[plant] = image_dataset_from_directory(self.data_info_dict[plant]['data_split']['train'],
                                                                    shuffle = True,
                                                                    labels = 'inferred',
                                                                    label_mode = 'int',
                                                                    image_size = self.image_dim,
                                                                    batch_size = self.batch_size)

                self.val_dataset[plant] = image_dataset_from_directory(self.data_info_dict[plant]['data_split']['val'],
                                                                    shuffle = True,
                                                                    labels = 'inferred',
                                                                    label_mode = 'int',
                                                                    image_size = self.image_dim,
                                                                    batch_size = self.batch_size)

                self.test_dataset[plant] = image_dataset_from_directory(self.data_info_dict[plant]['data_split']['test'],
                                                                    shuffle = True,
                                                                    labels = 'inferred',
                                                                    label_mode = 'int',
                                                                    image_size = self.image_dim,
                                                                    batch_size = self.batch_size)

                logging.info(f'Training, Testing and Validation data is read from \'{plant}\' directory')

            # Prefetch, Cache and Shuffle the dataset for optimized training
            for plant in self.data_info_dict.keys():
                self.train_dataset[plant] = self.train_dataset[plant].cache().shuffle(1000).prefetch(buffer_size = AUTOTUNE)
                self.test_dataset[plant] = self.test_dataset[plant].cache().shuffle(1000).prefetch(buffer_size = AUTOTUNE)
                self.val_dataset[plant] = self.val_dataset[plant].cache().shuffle(1000).prefetch(buffer_size = AUTOTUNE)
            logging.info('Prefetch, Cache and Shuffling all datasets completed.')
            
        except Exception as e:
            raise CustomException(e,sys)

    def baseline_model(self, plant:str, classes:dict):
    
        n_classes = len(classes[f'{plant}'])
        
        resize_rescale_layer = Sequential([
            Resizing(self.image_dim[0],
                     self.image_dim[0]),
            Rescaling(1.0/255)
        ])

        model = models.Sequential([
            resize_rescale_layer,
            Conv2D(32, kernel_size = (3,3), activation='relu', input_shape=input_shape),
            MaxPooling2D((2, 2)),
            Conv2D(64,  kernel_size = (3,3), activation='relu'),
            MaxPooling2D((2, 2)),
            Conv2D(64,  kernel_size = (3,3), activation='relu'),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(64, activation='relu'),
            Dense(n_classes, activation='softmax'),
        ], name = f'{plant}_Model')

        model.build(input_shape=input_shape)

        return model
    
    
    def model_training(self):
        
        try:
            model_info = {}

            early_stopping = EarlyStopping(monitor='val_accuracy',
                                   patience=3,
                                   restore_best_weights=True)

            os.makedirs('/home/studio-lab-user/Krishi/models', exist_ok = True)

            for plant in self.data_info_dict.keys():

                classes = len(self.data_info_dict[plant]['classes'])
                model = baseline_model(plant, classes)
                model.compile(
                    optimizer='adam',
                    loss=SparseCategoricalCrossentropy(from_logits=False),
                    metrics=['accuracy']
                )

                logging.info(f'Model loaded and compiled for {plant} Dataset')

                history = mode.fit(
                    self.train_dataset[plant],
                    batch_size=self.batch_size,
                    validation_data=self.val_dataset[plant],
                    verbose=0,
                    epochs=50,
                    callbacks=[early_stopping]
                                  )
                model.save(f'/home/studio-lab-user/Krishi/models/{plant}.h5')

                logging.info(f'{plant} Model Training finished. Model saved in \'models/{plant}.h5\'')

                train_loss, train_acc = model.evaluate(self.train_dataset[plant])
                test_loss, test_acc = model.evaluate(self.test_dataset[plant])
                val_loss, val_acc = model.evaluate(self.val_dataset[plant])

                logging.info(f'{plant} Model Evaluation Completed')

                acc_metrics = {
                    'Train Accuracy' : train_acc,
                    'Test Accuracy' : test_acc,
                    'Val Accuracy' : val_acc
                }

                loss_metrics = {
                    'Train Loss' : train_loss,
                    'Test Loss' : test_loss,
                    'Val Loss' : val_loss
                }

                model_info[plant] = {
                    'Saved Path': f'/home/studio-lab-user/Krishi/models/{plant}.h5',
                    'Accuracy Metrics': acc_metrics,
                    'Loss Metrics': loss_metrics,
                    'Training History': history.history
                }

                logging.info('Evaluation metrics, Training history and model path recorded')

            with open('/home/studio-lab-user/Krishi/artifacts/model_info.json', "w") as outfile:
                json.dump(model_info, outfile)

            logging.info('All models trained on datasets available. Evaluation metrics, Training History and Model Path saved in \'artifacts/model_info.json\'.')
            
        except Exception as e:
            raise CustomException(e,sys)    