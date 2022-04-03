from  model_building.find_best_model import  find_best_ml_model
import pandas as pd
from feature_selection.train_test_split import  split
from read_data.get_data import  get_data


desired_width=320
pd.set_option('display.width', desired_width)
#np.set_printoption(linewidth=desired_width)
pd.set_option('display.max_columns',10)


def remove_per_month_emi(data):
    new_data = data.drop(['per_month_emi'], axis=1)
    return new_data

data_after_removing_unnecessary_column = get_data(path='../feature_selection/data_after_removing_unnecessary_column')
object_of_train_test_split = split(data_after_removing_unnecessary_column)

x_train = object_of_train_test_split.X_train()
y_train = object_of_train_test_split.y_train()
x_test = object_of_train_test_split.X_test()
y_test = object_of_train_test_split.y_test()

new_x_train = remove_per_month_emi(x_train)
new_x_test = remove_per_month_emi(x_test)

object_of_best_model= find_best_ml_model(new_x_train,y_train,new_x_test,y_test)
print(object_of_best_model.model_comparision())


