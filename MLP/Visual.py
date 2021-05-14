import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.backends.backend_qt5agg
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import activations

if __name__ == '__main__':

    df = pd.read_excel(open('Collections.xlsx', 'rb'), sheet_name='工作表1')
    new_df=df.drop(columns=['格子編號'])
    print(new_df)
    data = new_df.to_numpy()

    coord = data[:, :2]
    target = data[:, 2:]

    minv = np.min(coord, axis=0)
    maxv = np.max(coord, axis=0)
    res = 2
    x = int(np.linspace(minv[0], maxv[0], res*(maxv[0]-minv[0]+1)))
    y = np.linspace(minv[1], maxv[1], res*(maxv[1]-minv[1]+1))
    xv, yv=np.meshgrid(x, y)
    xxv, yyv = np.reshape(xv, (-1,)), np.reshape(yv, (-1,))
    xys = zip(xxv, yyv)
    out = []
    for i, xy in enumerate(xys):
        if i%10000==0 or i==len(xxv)-1:
            print(i)
        w, o = regress(xy, coord, target)
        out.append(o)
    out = np.vstack(out)
    print(out.shape)
    out = np.reshape(out, (len(y), len(x), out.shape[1]))
    print(out.shape)

    fig = plt.figure()
    fig.set_figheight(15)
    fig.set_figwidth(20)
    for k in range(6):
        ax = fig.add_subplot(2, 3, k + 1, projection='3d')
        ax.plot_wireframe(xv, yv, out[:, :, k], color='black')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('S%d' % (k + 1));
    plt.show()