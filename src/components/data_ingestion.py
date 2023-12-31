import os 
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainer
from src.components.model_trainer import ModelTrainerConfig


class DataIndestionConfig:
    train_data_path:str=os.path.join('artifacts',"train.csv")
    test_data_path:str=os.path.join('artifacts',"test.csv")
    raw_data_path:str=os.path.join('artifacts',"data.csv")

class DataIndegestion:
    def __init__(self):
        self.ingestion_congif=DataIndestionConfig()
    
    def initiate_data_indegestion(self):
        logging.info("Entered the data indegestion method or component")
        try:
            df=pd.read_csv('data\StudentsPerformance.csv')
            logging.info('Read the dataset as dataframe')
            os.makedirs(os.path.dirname(self.ingestion_congif.train_data_path),exist_ok=True)
            df.to_csv(self.ingestion_congif.raw_data_path,index=False,header=True)
            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.25,random_state=42)
            train_set.to_csv(self.ingestion_congif.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_congif.test_data_path,index=False,header=True)
            logging.info("Ingestion of the data is completed")
            return{
                self.ingestion_congif.train_data_path,
                self.ingestion_congif.test_data_path

            }
        except Exception as e:
            raise CustomException(e,sys)

if __name__=="__main__":
    obj=DataIndegestion()
    train_data,test_data=obj.initiate_data_indegestion()

    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)
    
    model_trainer=ModelTrainer()
    print(model_trainer.initiate_model_training(train_arr,test_arr))
