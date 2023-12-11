import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
import os
from flask import render_template

def load_model(location):
    """
    input is a string to file location of the model
    output is the model
    """
    f = open(location, "rb")
    model = pickle.load(f)
    f.close()
    return model

def make_prediction(X: np.array) -> np.array:
    """
    Input is 2d array and output is 1d array
    Loads model and returns prediction 
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    MODEL_LOCATION = os.path.join(current_dir, 'model.pickle')
    
    model = load_model(MODEL_LOCATION)
    return (model.predict(X))


def main():
    #Base prediction to check if correct prediction was made 
    decoder = ["clear-day", "cloudy", "partly-cloudy-day", "rain", "snow"]
    temp = [32, 70]
    humidity = [80, 60]
    precip = [0.5, 0.01]
    windspeed = [15, 8]
    sealevelpressure = [1010, 1020]

    datapoint1 = [temp[0], humidity[0], precip[0], windspeed[0], sealevelpressure[0]]
    datapoint2 = [temp[1], humidity[1], precip[1], windspeed[1], sealevelpressure[1]]
    encoded_predictions = make_prediction(np.array([datapoint1, datapoint2]))

    print(list(round(prediction) for prediction in encoded_predictions))
    for prediction in encoded_predictions:
        print(decoder[round(prediction)])

if __name__ == "__main__":
    main()

