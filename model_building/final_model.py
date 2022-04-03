import pickle
import lightgbm as lgb

from feature_selection.train_test_split import  split
from read_data.get_data import  get_data


def remove_per_month_emi(data):
    new_data = data.drop(['per_month_emi'], axis=1)
    return new_data


class finalizing_model:

    def __init__(self):


        data_after_removing_unnecessary_column = get_data(
            path='../feature_selection/data_after_removing_unnecessary_column')
        object_of_train_test_split = split(data_after_removing_unnecessary_column)

        self.x_train = object_of_train_test_split.X_train()
        self.y_train = object_of_train_test_split.y_train()
        self.x_test = object_of_train_test_split.X_test()
        self.y_test = object_of_train_test_split.y_test()

        self.new_x_train = remove_per_month_emi(self.x_train)
        self.new_x_test = remove_per_month_emi(self.x_test)

    # create an iterator object with write permission - model.pkl

    def my_model(self):
        model = lgb.LGBMRegressor(subsample_for_bin=100000, num_leaves=10, n_estimators=500, learning_rate=0.1,
                                  importance_type='split', boosting_type='dart')
        my_model = model.fit(self.new_x_train, self.y_train)
     #   model.score(self.new_x_test, self.y_test)

        return model


    def save_model(self):

        return pickle.dump(self.my_model(),open('houseing_model', 'wb'))


    def load_model(self):
        loaded_model = pickle.load(open('houseing_model', 'rb'))
        result = loaded_model.score(self.new_x_test,self.y_test)
        return result


    def predict_model(self,data):
        try:
            loaded_model = pickle.load(open('houseing_model', 'rb'))
           # print(loaded_model.predict(data))

            return loaded_model.predict(data)[0]
        except Exception as e:
            pass

o= finalizing_model()
print(o.my_model())
o.save_model()
print(o.load_model())
print(o.predict_model([[1,	0	,3.0	,1550.0	,35.636953]]))
