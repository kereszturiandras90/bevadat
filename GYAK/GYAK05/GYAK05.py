import numpy as np
from typing import Tuple
from scipy.stats import mode
from sklearn.metrics import confusion_matrix

csv_path = "iris.csv"

class KNNClassifier:
    k_neighbors = 0

    def __init__(self, k:int, test_split_ratio :float) -> None:
        self.k = k
        self.test_split_ratio = test_split_ratio
        KNNClassifier.k_neighbors = k

    @staticmethod
    def load_csv(csv_path:str) ->Tuple[np.ndarray,np.ndarray]:
     np.random.seed(42)
     dataset = np.genfromtxt(csv_path,delimiter=',')
     np.random.shuffle(dataset,)
     x,y = dataset[:,:4],dataset[:,-1]
     return x,y  

    def train_test_split(self, features: np.array, labels: np.array) -> tuple:
        
     test_size = int(len(features) * self.test_split_ratio)
     train_size = len(features) - test_size
     assert len(features) == test_size + train_size, "Size mismatch!"

     self.x_train, self.y_train = features[:train_size,:], labels[:train_size]
     self.x_test, self.y_test = features[train_size:train_size+test_size,:], labels[train_size:train_size+test_size]
     return (self.x_train, self.y_train, self.x_test, self.y_test)

    def euclidean(self, element_of_x:np.ndarray) -> np.ndarray:
     return np.sqrt(np.sum((self.x_train - element_of_x)**2,axis=1))

    def predict(self, x_test:np.ndarray) -> np.ndarray:
     labels_pred = []
     for x_test_element in x_test:
        distances = self.euclidean(x_test_element)
        distances = np.array(sorted(zip(distances,self.y_train)))
        label_pred = mode(distances[:self.k,1],keepdims=False).mode
        labels_pred.append(label_pred)
     self.y_preds = np.array(labels_pred,dtype=np.int32)   
     return np.array(labels_pred,dtype=np.int32)

    def accuracy(self) -> float:
     true_positive = (self.y_test == self.y_preds).sum()
     return true_positive / len(self.y_test) * 100

    def confusion_matrix(self) -> np.ndarray:
        conf_matrix = confusion_matrix(self.y_test,self.y_preds)
        return conf_matrix 




