'''from feature_selection.train_test_split import  split
from read_data.get_data import  get_data
import pandas as pd
desired_width=320
pd.set_option('display.width', desired_width)
#np.set_printoption(linewidth=desired_width)
pd.set_option('display.max_columns',10)


class data_after_feature_selection:
    def __init__(self):
        data_after_removing_unnecessary_column = get_data(path='../feature_selection/data_after_removing_unnecessary_column')
        object_of_train_test_split= split(data_after_removing_unnecessary_column)

        self.x_train = object_of_train_test_split.X_train()
        self.y_train = object_of_train_test_split.y_train()
        self.x_test = object_of_train_test_split.X_test()
        self.y_test = object_of_train_test_split.y_test()


    def remove_per_month_emi(self,data):
        new_data = data.drop(['per_month_emi'], axis=1)
        return new_data

    def x_train(self):
        data = self.x_train
        new_x_train = self.remove_per_month_emi(data)
        return new_x_train

    def x_test(self):
        new_x_train = self.remove_per_month_emi(self,self.x_test)
        return new_x_train

    def y_train(self):
        return self.y_train

    def y_test(self):
        return self.y_test


o = data_after_feature_selection()
print(o.y_train())
'''