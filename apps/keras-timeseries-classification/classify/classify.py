from tensorflow import keras
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from __init__ import Metric


def __read_data():

    truth = pd.read_csv('data/class-path.csv', '\t', )

    df = pd.read_csv('data/file-metrics.csv', '\t')

    sets = df.path.unique()

    data = {}
    columns = [e.value for e in Metric]
    # columns = [m.value for m in [Metric.COMMENT_LINES, Metric.COMPLEXITY,
    #                              Metric.CHURN, Metric.STATEMENTS, Metric.FUNCTIONS, Metric.SQALE_INDEX]]
    print(columns)
    columns.append('date')

    for set in sets:

        tmp = df[df.path == set]
        tmp = tmp[columns]
        tmp = tmp.fillna(0)
        data[set] = tmp.sort_values('date')

    return truth, data


def __create_x_array(data, paths, max_len):

    x = None

    for k in paths:

        d = data[k].to_numpy()
        lines_append = max_len - d.shape[0]
        if lines_append > 0:
            zeros = np.array([np.zeros(d[0].shape) for _ in range(lines_append)])
            d = np.append(d, zeros, 0)

        if x is None:
            x = np.array([d])
            continue

        x = np.concatenate([x, [d]])

    return x


def __get_train_test():
    truth, data = __read_data()

    train_truth = truth.sample(frac=0.75)
    test_truth = pd.concat([train_truth, truth]).drop_duplicates(keep=False).reset_index()
    train_truth = train_truth.reset_index()

    max_len = max([d.shape[0] for d in data.values()])

    y_train = np.array(train_truth.good)
    x_train = __create_x_array(data, train_truth.path, max_len)

    y_test = np.array(test_truth.good)
    x_test = __create_x_array(data, test_truth.path, max_len)

    idx = np.random.permutation(len(x_train))

    x_train = x_train[idx]
    y_train = y_train[idx]

    unique, counts = np.unique(y_train, return_counts=True)
    print(dict(zip(unique, counts)))
    unique, counts = np.unique(y_test, return_counts=True)
    print(dict(zip(unique, counts)))

    return x_train, y_train, x_test, y_test


def train():

    num_classes = 2

    x_train, y_train, x_test, y_test = __get_train_test()

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

    epochs = 500
    batch_size = 32

    callbacks = [
        keras.callbacks.ModelCheckpoint(
            "best_model.h5", save_best_only=True, monitor="val_loss"
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss", factor=0.5, patience=20, min_lr=0.0001
        ),
        keras.callbacks.EarlyStopping(monitor="val_loss", patience=50, verbose=1),
    ]
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["sparse_categorical_accuracy"],
    )

    history = model.fit(
        x_train,
        y_train,
        batch_size=batch_size,
        epochs=epochs,
        callbacks=callbacks,
        validation_split=0.2,
        verbose=1,
    )

    model = keras.models.load_model("best_model.h5")

    test_loss, test_acc = model.evaluate(x_test, y_test)

    print("Test accuracy", test_acc)
    print("Test loss", test_loss)

    metric = "sparse_categorical_accuracy"
    plt.figure()
    plt.plot(history.history[metric])
    plt.plot(history.history["val_" + metric])
    plt.title("model " + metric)
    plt.ylabel(metric, fontsize="large")
    plt.xlabel("epoch", fontsize="large")
    plt.legend(["train", "val"], loc="best")
    plt.show()
    plt.close()
