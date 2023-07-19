# project: p7
# submitter: kenigsztein
# partner: none
# hours: 5


from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
import numpy as np

class UserPredictor:
    def __init__(self):
        self.model = None
        self.scaler = preprocessing.StandardScaler()
        
    def fit(self,train_users, train_logs, train_y):
        
        x = np.stack((train_users['past_purchase_amt'], self.gentime(train_users["user_id"], train_logs)), axis = 1)
        X = self.scaler.fit_transform(x)
        Y = np.array(train_y["y"])
        self.model = LogisticRegression().fit(X,Y)
        
    def predict(self, test_users, test_logs):
        x = np.stack((test_users['past_purchase_amt'], self.gentime(test_users['user_id'], test_logs)), axis = 1)
        X = self.scaler.transform(x)
        
        return np.array(self.model.predict(X))
    
    
    def gentime(self, users, logs):
        time =[]
        for user in users:
            time.append(logs.loc[logs["user_id"] == user, "seconds"].sum())
        return time
        