# =============================================================================================
# Copyright 2018 dgketchum
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================================

import os
import numpy as np
import tensorflow as tf
from pandas import get_dummies
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import minmax_scale


def mlp(data):
    """
    :param data: Use the prep_structured_data.StructuredData class.
    :return:
    """

    N = len(data.classes)
    data.x = minmax_scale(data.x)
    n = data.x.shape[1]
    nodes = 500
    eta = 0.05
    epochs = 1000
    seed = 128

    data.x, x_test, data.y, y_test = train_test_split(data.x, data.y, test_size=0.33,
                                                      random_state=None)

    data.y = get_dummies(data.y).values
    y_test = get_dummies(y_test).values
    X = tf.placeholder("float", [None, n])
    Y = tf.placeholder("float", [None, N])

    batch_size = 100

    weights = {
        'hidden': tf.Variable(tf.random_normal([n, nodes], seed=seed)),
        'output': tf.Variable(tf.random_normal([nodes, N], seed=seed))}
    biases = {
        'hidden': tf.Variable(tf.random_normal([nodes], seed=seed)),
        'output': tf.Variable(tf.random_normal([N], seed=seed))}

    y_pred = tf.add(tf.matmul(multilayer_perceptron(X, weights['hidden'], biases['hidden']),
                              weights['output']), biases['output'])

    loss_op = tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits(logits=y_pred, labels=Y))

    optimizer = tf.train.AdamOptimizer(learning_rate=eta).minimize(loss_op)

    correct_pred = tf.equal(tf.argmax(Y, 1), tf.argmax(y_pred, 1))

    sess = tf.InteractiveSession()
    init = tf.global_variables_initializer().run()
    loss = None

    for step in range(epochs):
        offset = np.random.randint(0, data.y.shape[0] - batch_size - 1)

        batch_data = data.x[offset:(offset + batch_size), :]
        batch_labels = data.y[offset:(offset + batch_size), :]

        feed_dict = {X: batch_data, Y: batch_labels}

        _, loss = sess.run([optimizer, loss_op],
                           feed_dict=feed_dict)

        if step % 100 == 0:
            pred = tf.nn.softmax(y_pred)
            correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(Y, 1))
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
            print("Accuracy:", accuracy.eval({X: x_test, Y: y_test}), loss)


# Create neural network
def multilayer_perceptron(x, weights, biases):
    out_layer = tf.add(tf.matmul(x, weights), biases)
    out_layer = tf.nn.sigmoid(out_layer)
    return out_layer


if __name__ == '__main__':
    home = os.path.expanduser('~')

# ========================= EOF ====================================================================
