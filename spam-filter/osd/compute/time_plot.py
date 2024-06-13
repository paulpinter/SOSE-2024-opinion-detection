import datetime

import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from functools import reduce


def calculate_y(
    path,
):
    df = pd.read_csv(path, header=None, parse_dates=[0, 6, 7])
    df = df.sort_values(by=7)
    total = pd.Series(df.iloc[:][7] - df.iloc[:][6].min()).astype("timedelta64[s]")
    total = total / np.timedelta64(1, "m")
    print(pd.Series(df.iloc[:][7].max() - df.iloc[:][6].min()).astype("timedelta64[s]"))
    # smoothed_total = total.rolling(window=50, center=True).mean()
    print(df[6].dtype, df[7].dtype)  # Check data types of datetime columns
    print((df[7] - df[6].min()).head())  # See some outputs of the subtraction

    return total.to_numpy().flatten()


def draw_plot(config):
    matplotlib.rcParams.update({"font.size": 22})
    fig, ax = plt.subplots(figsize=(16, 10), layout="constrained")
    for i in range(3):
        y = calculate_y(config["data"][i])
        print(y)
        x = np.arange(1, 3001)
        ax.plot(x, y, linewidth=5.0, label=config["label"][i])

    plt.style.use("_mpl-gallery")
    ax.set(xlabel="Request", ylabel=config["y_label"])
    plt.grid(visible=True)
    plt.ylim(config["ylim"])
    plt.legend(loc="upper left")
    plt.savefig(config["target"])
    plt.show()


def run():
    constant_time = {
        "y_label": "Time(Min)",
        "label": ["SYNCH", "BATCH", "QUEUE"],
        "data": [
            "/Users/paulpinter/Repository/ba/app/Tables/time_synch_constant.csv",
            "/Users/paulpinter/Repository/ba/app/Tables/time_batch_constant.csv",
            "/Users/paulpinter/Repository/ba/app/Tables/time_queue_constant.csv",
        ],
        "target": "constant_time.pdf",
        "ylim": [0, 2],
    }
    draw_plot(constant_time)
    variable_time = {
        "y_label": "Time(Min)",
        "label": ["SYNCH", "BATCH", "QUEUE"],
        "data": [
            "/Users/paulpinter/Repository/ba/app/Tables/time_synch_variable.csv",
            "/Users/paulpinter/Repository/ba/app/Tables/time_batch_variable.csv",
            "/Users/paulpinter/Repository/ba/app/Tables/time_queue_variable.csv",
        ],
        "target": "variable_time.pdf",
        "ylim": [0, 10],
    }
    draw_plot(variable_time)
    return 0


if __name__ == "__main__":
    run()
