from tensorflow import keras, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

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

            # row = np.average(d, axis=0)
            # rows = np.array([row for _ in range(lines_append)])
            zeros = np.array([np.zeros(d[0].shape) for _ in range(lines_append)])
            d = np.append(d, zeros, 0)

        if x is None:
            x = np.array([d])
            continue

        x = np.concatenate([x, [d]])

    return x


def get_train_test(frac=0.75, shuffle=True):
    truth, data = __read_data()

    train_truth = truth.sample(frac=frac)
    test_truth = pd.concat([train_truth, truth]).drop_duplicates(keep=False).reset_index()
    train_truth = train_truth.reset_index()

    max_len = max([d.shape[0] for d in data.values()])

    y_train = np.array(train_truth.good)
    x_train = __create_x_array(data, train_truth.path, max_len)

    y_test = np.array(test_truth.good)
    x_test = __create_x_array(data, test_truth.path, max_len)

    if shuffle:
        idx = np.random.permutation(len(x_train))

        x_train = x_train[idx]
        y_train = y_train[idx]

    unique, counts = np.unique(y_train, return_counts=True)
    print(dict(zip(unique, counts)))
    unique, counts = np.unique(y_test, return_counts=True)
    print(dict(zip(unique, counts)))

    return x_train, y_train, x_test, y_test


def train(x_train, y_train):

    num_classes = 2

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
            "best_model.h5", save_best_only=False, monitor="val_loss"
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss", factor=0.5, patience=20, min_lr=0.0001
        ),
        keras.callbacks.EarlyStopping(monitor="val_loss", patience=50, verbose=1),
        keras.callbacks.TensorBoard(
            log_dir='tensorboard', histogram_freq=0, write_graph=True, write_images=True
        )
    ]
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    model.fit(
        x_train,
        y_train,
        batch_size=batch_size,
        epochs=epochs,
        callbacks=callbacks,
        validation_split=0.2,
        verbose=1,
    )


def test(x_test, y_test):

    model = keras.models.load_model("best_model.h5")

    test_loss, test_acc = model.evaluate(x_test, y_test)

    print("Test accuracy", test_acc)
    print("Test loss", test_loss)

    predictions = model.predict(x_test)
    classes = np.argmax(predictions, axis=1)

    confusion = math.confusion_matrix(labels=y_test, predictions=classes, num_classes=2)

    df_cm = pd.DataFrame(confusion.numpy(), range(2), range(2))

    sn.heatmap(df_cm, annot=True)
    print(df_cm)
    plt.show()

    return classes


def predict(x_data):

    model = keras.models.load_model("best_model.h5")
    predictions = model.predict(x_data)
    classes = np.argmax(predictions, axis=1)

    return classes
