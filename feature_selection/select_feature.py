import pandas as pd
def join_df(data1, data2):
    df = pd.concat([data1, data2], axis=1)
    return df


class feature_selection():
    def __init__(self, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train

        self.df = join_df(self.x_train, self.y_train)

    def correlation_matrix(self):
        corr = self.df.corr()
        return corr.style.background_gradient(cmap='coolwarm')

    def vif_score(self):
        from statsmodels.stats.outliers_influence import variance_inflation_factor
        vif = pd.DataFrame()
        vif["features"] = self.x_train.columns
        vif["vif_Factor"] = [variance_inflation_factor(self.x_train.values, i) for i in range(self.x_train.shape[1])]
        return vif

    def information_gain(self):
        from sklearn.feature_selection import mutual_info_regression
        mutual_info = mutual_info_regression(self.x_train, self.y_train)
        return mutual_info

    def plot_information_gain(self):
        mutual_info = pd.Series(self.information_gain())
        mutual_info.index = self.x_train.columns
        mutual_info.sort_values(ascending=False)

        return mutual_info.sort_values(ascending=False).plot.bar(figsize=(15, 5))