import lazypredict
from lazypredict.Supervised import LazyRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
import  numpy as np
import lightgbm as lgb

class find_best_ml_model:
    def __init__(self,x_train,y_train,x_test,y_test):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test

    def model_comparision(self):


        reg = LazyRegressor(verbose=0, ignore_warnings=False, custom_metric=None)
        models, predictions = reg.fit(self.x_train, self.x_test, self.y_train, self.y_test)

        return models

    def randomizesearch_cv(self):
        params = {'boosting_type': ['dart', 'goss', 'rf'],
                  'num_leaves': np.arange(10, 110, 10),
                  'learning_rate': [0.1, 0.001, 0.0001, 1.0],
                  'n_estimators': [100, 200, 300, 500, 1000],
                  'subsample_for_bin ': np.arange(100000, 700000, 100000),
                  'importance_type ': ['split', 'gain']}

        LGB = lgb.LGBMRegressor()
        clf = RandomizedSearchCV(estimator=LGB,
                                 param_distributions=params,
                                 scoring='neg_mean_squared_error',
                                 n_iter=25,
                                 verbose=1)
        clf.fit(self.x_train, self.y_train)
      #  print("Best parameters:", clf.best_params_)
        print("Lowest RMSE: ", (-clf.best_score_) ** (1 / 2.0))

        return ("Best parameters:", clf.best_params_)

    def gridsearch_cv(self):

        params = {'boosting_type': ['dart', 'goss', 'rf'],
                  'num_leaves': np.arange(10, 70, 10),
                  'learning_rate': [0.1, 0.001, 0.0001],
                  'n_estimators': [100, 200, 300, 500, 1000],
                  'subsample_for_bin ': np.arange(100000, 500000, 100000),
                  'importance_type ': ['split', 'gain']}
        LGB = lgb.LGBMRegressor()
        clf = GridSearchCV(estimator=LGB, n_jobs=-1, cv=3,
                           param_grid=params,
                           scoring='neg_mean_squared_error',
                           verbose=1)
        clf.fit(self.x_train, self.y_train)
       # print("Best parameters:", clf.best_params_)
        print("Lowest RMSE: ", (-clf.best_score_) ** (1 / 2.0))

        return ("Best parameters:", clf.best_params_)