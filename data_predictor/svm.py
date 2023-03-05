import polars as pl
from sklearn.svm import SVC  # support vector machine classifier
from data_predictor.models import Model
from data_predictor.utils import model_evaluation
import pickle


# implement support vector machine model through the abstract model class
class SupportVectorMachine(Model):
    display_name = "SupportVectorMachine"

    def __init__(self, svc, model_params):  # can implement here to overwrite the abstract class definition
        super().__init__(model_params)  # super creates a temp object of parent class Models -
        # for example if there were methods there we would not need to redefine them here, or
        # variables that get defined in the constructor - we will likely need this to save time later
        self.svc = svc

    @classmethod
    def fit(cls, train_data, model_params):
        svc = SVC(kernel=model_params['kernel'], C=model_params['C'])
        y = train_data['y']
        X = train_data[[c for c in train_data.columns if c not in ['y']]]
        svc.fit(X, y)
        return SupportVectorMachine(svc=svc, model_params=model_params)

    def predict(self, fitted_df: pl.DataFrame, predict_df: pl.DataFrame):
        fitted_df.with_columns('data_stage' == 'history')
        predict_df.with_columns('data_stage' == 'future')
        complete_df = pl.concat([fitted_df, predict_df])  # works in polars?
        complete_df['yhat'] = self.svc.predict(complete_df.drop('y'))  # this is not polars formatting
        return complete_df

    def validation(self, predicted_df: pl.DataFrame):
        model_evaluation(predicted_df['y'], predicted_df['yhat'])
        return None

    def fetch_model(self):
        return self.svc

    def save_model(self, file):
        pickle.dump(self.svc, file)


if __name__ == '__main__':
    data = pl.read_parquet('data_storage/model_training_datframe.parquet')
    # set kernel to test model parameter json: usually we want RBF as the kernel
    model_parameters_dict = {'kernel': 'linear'}
    svm_model = SupportVectorMachine(SVC(), data, model_parameters_dict)
