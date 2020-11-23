from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import random

from __init__ import Metric


def __read_data():

    truth = pd.read_csv('data/class-path.csv', '\t', )

    df = pd.read_csv('data/file-metrics.csv', '\t')

    sets = df.path.unique()

    data = {}
    columns = [e.value for e in Metric]
    columns.append('date')

    for set in sets:

        tmp = df[df.path == set]
        tmp = tmp[columns]
        data[set] = tmp.sort_values('date')

    return truth, data


def go():

    truth, data = __read_data()

    train_truth = truth.sample(frac=0.75).reset_index()
    test_truth = truth.copy().drop(index=train_truth.index).reset_index()

    num_classes = 2

    print(data['src/main/java/net/sf/jabref/MetaData.java'].values.shape)

    y_train = np.array(train_truth.good)

    x_train = None

    for k in train_truth.path:

        if x_train is None:
            x_train = np.array([np.array(data[k].values)])
            print(x_train)
            print(x_train.shape)
            continue

        print(np.array([np.array(data[k].values)]))
        print(np.array([np.array(data[k].values)]).shape)

        x_train = np.concatenate([x_train, np.array([np.array(data[k].values)])])

    y_test = np.array(test_truth.good)
    x_test = np.array([[].extend(data[k].values.tolist()) for k in test_truth.path])

    # print(x_train)
    print(x_train.shape)

    idx = np.random.permutation(len(x_train))

    x_train = x_train[idx]
    y_train = y_train[idx]

    y_train[y_train == -1] = 0
    y_test[y_test == -1] = 0

    def make_model(input_shape):

        print(input_shape)

        input_layer = keras.layers.Input(input_shape)

        conv1 = keras.layers.Conv1D(filters=64, kernel_size=3, padding="same")(input_layer)
        conv1 = keras.layers.BatchNormalization()(conv1)
        conv1 = keras.layers.ReLU()(conv1)

        conv2 = keras.layers.Conv1D(filters=64, kernel_size=3, padding="same")(conv1)
        conv2 = keras.layers.BatchNormalization()(conv2)
        conv2 = keras.layers.ReLU()(conv2)

        conv3 = keras.layers.Conv1D(filters=64, kernel_size=3, padding="same")(conv2)
        conv3 = keras.layers.BatchNormalization()(conv3)
        conv3 = keras.layers.ReLU()(conv3)

        gap = keras.layers.GlobalAveragePooling1D()(conv3)

        output_layer = keras.layers.Dense(num_classes, activation="softmax")(gap)

        return keras.models.Model(inputs=input_layer, outputs=output_layer)

    model = make_model(input_shape=x_train.shape[1:])
    keras.utils.plot_model(model, show_shapes=True)
