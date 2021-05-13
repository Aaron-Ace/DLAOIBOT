import pandas as pd
import numpy as np
import tensorflow as tf
import math
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import activations


class AttRegressor(keras.Model):
    def __init__(self, embed_dim, hidden_dim, keys, values):
        super(AttRegressor, self).__init__()
        self.embed_dim = embed_dim
        self.embed = layers.Dense(embed_dim, activation=activations.relu)
        self.hidden = layers.Dense(hidden_dim, activation=activations.relu)
        self.attend = layers.Dense(len(keys), activation=activations.softmax)
        self.keys = keys
        self.values = values

    def preprocess(self, inputs):
        out = []
        for x in inputs:
            tmp = tf.square(tf.subtract(self.keys, x))
            diff = tf.sqrt(tf.reduce_sum(tmp, axis=1))
            score = tf.exp(-10 * diff / tf.reduce_max(diff))
            s = score / tf.reduce_sum(score)
            out.append(s)
        o = tf.stack(out, axis=0)
        return o

    def call(self, inputs):
        x = self.preprocess(inputs)
        embed = self.embed(x)
        hid_out = self.hidden(embed)
        att_weight = self.attend(hid_out)
        out = tf.matmul(att_weight, self.values)
        return out

def split(data_size, skip):
#     n_selected = int(data_size * ratio)
#     selected_ind = np.random.choice(range(data_size), size=(n_selected,), replace=False)
    test = np.zeros(data_size, dtype=bool)
    test[0:data_size:skip] = True
    train = ~test
    return train, test

def train(x, y, vx, vy, max_epochs, optim, model, loss ,servonum):
    hist = []
    for e in range(max_epochs):
        with tf.GradientTape() as tape:
            out = model(x)
            l = tf.reduce_mean(loss(y, out))
        hist.append(l)
        grads = tape.gradient(l, model.trainable_variables)
        optim.apply_gradients(zip(grads, model.trainable_variables))
        if e%10==0:
            vout = model(vx)
            vl = tf.reduce_mean(loss(vy, vout))
            print('S%d :Epoch %d: train MSE = %f valid MSE = %f'%(servonum, e, l.numpy(), vl.numpy()))

def ServoLoad(servonum, data):
    all_coord = tf.convert_to_tensor(data[:, 2:4], dtype=tf.float32)
    all_target = tf.convert_to_tensor(data[:, servonum+3:servonum+4], dtype=tf.float32)

    train_ind, test_ind = split(all_coord.shape[0], 50)
    train_coord = all_coord[train_ind]
    train_target = all_target[train_ind]
    global test_coord
    test_coord = all_coord[test_ind]
    test_target = all_target[test_ind]
    #print(train_coord.shape, test_coord.shape, train_target.shape, test_target.shape)

    model = AttRegressor(16, 16, train_coord, train_target)
    modelsname = './MotorModel/S'+str(servonum)+'_model'
    model.load_weights(modelsname)
    pred = model(test_coord)
    #print(test_coord)
    #print(pred)
    return model


def MotorAngle(X,Y):

    df = pd.read_excel(open('Collections.xlsx', 'rb'), sheet_name='工作表1')
    new_df = df.drop(columns=['格子編號'])
    #print(new_df)
    data = new_df.to_numpy()
    #print(data.shape)

    S1_model = ServoLoad(1, data)
    S2_model = ServoLoad(2, data)
    S3_model = ServoLoad(3, data)
    S4_model = ServoLoad(4, data)
    S5_model = ServoLoad(5, data)
    S6_model = ServoLoad(6, data)

    pred =[]
    pred.append(round(S1_model(tf.convert_to_tensor([[X, Y]], dtype=tf.float32)).numpy()[0][0]))
    pred.append(round(S2_model(tf.convert_to_tensor([[X, Y]], dtype=tf.float32)).numpy()[0][0]))
    pred.append(round(S3_model(tf.convert_to_tensor([[X, Y]], dtype=tf.float32)).numpy()[0][0]))
    pred.append(round(S4_model(tf.convert_to_tensor([[X, Y]], dtype=tf.float32)).numpy()[0][0]))
    pred.append(round(S5_model(tf.convert_to_tensor([[X, Y]], dtype=tf.float32)).numpy()[0][0]))
    pred.append(round(S6_model(tf.convert_to_tensor([[X, Y]], dtype=tf.float32)).numpy()[0][0]))

    for prediction in pred:
        print(prediction)
    return pred

#MotorAngle(33.50270328,36.37526091)
MotorAngle(16.3742506,39.2201456)
#MotorAngle(26.33883009,39.00691897)



