import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
import pickle

def train(dataset: pd.DataFrame) -> None:
    data = dataset[["temp", "humidity", "precip", "windspeed", "sealevelpressure", "icon"]]
    target = "icon"
    encoder = preprocessing.LabelEncoder()
    weather = encoder.fit_transform(data[target])
    X = np.array(data.drop(labels=target, axis=1))
    y = np.array(weather)
    print(X)
    print(y)

    best_acc = 0
    best_model = None
    for _ in range(100):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
        model = RandomForestClassifier(n_estimators=100, random_state=0)
        model.fit(X_train, y_train)
        acc = model.score(X_test, y_test)
        print(acc)

        if acc > best_acc:
            best_acc = acc 
            best_model = model
    
    f = open("model.pickle", "wb")
    pickle.dump(best_model, f)
    f.close()


def main():
    dataset = pd.read_csv("dataset.csv")
    train(dataset)

if __name__ == "__main__":
    main()
