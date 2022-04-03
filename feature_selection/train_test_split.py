from sklearn.model_selection import train_test_split



class split:

    def __init__(self,data):
        self.data = data



    def train_test_spliting(self):
        try:
            X = self.data.drop('price', axis=1)
            target = self.data['price']


            X_train, X_test, y_train, y_test = train_test_split(X, target, test_size=0.2, random_state=42)

            return X_train, X_test, y_train, y_test
        except  Exception as e:
            pass

    def X_train(self):
        return self.train_test_spliting()[0]

    def X_test(self):
        return self.train_test_spliting()[1]
    def y_train(self):
        return self.train_test_spliting()[2]
    def y_test(self):
        return self.train_test_spliting()[3]
