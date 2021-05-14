import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import activations


def regress(uv, ref, tgt):
    dist = np.sum((ref - uv) ** 2, axis=1)
    dist = -10 * dist / np.max(np.sqrt(dist))
    dist = np.exp(dist)
    weight = dist / np.sum(dist)
    weight = np.repeat(np.reshape(weight, (-1, 1)), 6, axis=1)
    out = np.sum(tgt * weight, axis=0)
    return weight, out

if __name__ == '__main__':
    df = pd.read_excel(open('Collections.xlsx', 'rb'), sheet_name='工作表1')
    new_df = df.drop(columns=['格子編號'])
    print(new_df)
    data = new_df.to_numpy()
    print(data.shape)

    coord = data[:, 2:4]
    target = data[:, 4:]
    w, o = regress([31.64180153,39.01868634], coord, target)
    print(np.argmax(w, axis=0))
    print(np.round(o).astype(np.int32))

