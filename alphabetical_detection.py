import cv2
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split as tts
from sklearn.linear_model import LogisticRegression as LR
from sklearn.metrics import accuracy_score as acs
import time

# import os
# directory_path = os.path.dirname(__file__)
# file_path = os.path.join(directory_path, 'C:/Users/rajbi/OneDrive/Desktop/Coding Stuff/Python/Project/P123/image.npz')
# print(file_path)

X = np.load('image.npz')['arr_0']
y = pd.read_csv("labels.csv")["labels"]
print(pd.Series(y).value_counts())
classes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
nclasses = len(classes)

samples_per_class = 5
figure = plt.figure(figsize=(nclasses*2,(1+samples_per_class*2)))

idx_cls = 0
for cls in classes:
  idxs = np.flatnonzero(y == cls)
  idxs = np.random.choice(idxs, samples_per_class, replace=False)
  i = 0
  for idx in idxs:
    plt_idx = i * nclasses + idx_cls + 1
    p = plt.subplot(samples_per_class, nclasses, plt_idx)
    p = sns.heatmap(np.reshape(X[idx], (22, 30)), cmap = plt.cm.gray, xticklabels = False, yticklabels = False, cbar = False)
    p = plt.axis('off')
    i+=1

idx_cls+=1
idxs = np.flatnonzero(y == '0')

X_train, X_test, y_train, y_test = tts(X, y, random_state = 9, train_size = 7500, test_size = 2500)
X_train_scaled = X_train / 255.0
X_test_scaled = X_test / 255.0

clf = LR(solver='saga',multi_class='multinomial').fit(X_train_scaled, y_train)

y_pred = clf.predict(X_test_scaled)
accuracy = acs(y_test, y_pred)
print(accuracy)

cm = pd.crosstab(y_test, y_pred, rownames = ['Actual'], colnames = ['Preditcted'])
p = plt.figure(figsize = (10, 10))
p = sns.heatmap(cm, annot = True, fmt = 'd', cbar = False)

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()

    roi = gray[upper_left1[1]:bottom_right[1], upper_left1[0]:bottom_right[0]]

    image_bw = im_pil.convert('L') 
    image_bw_resized = image_bw.resize((28,28), Image.ANTIALIAS)
    image_bw_resized_inverted = PIL.ImageOps.invert(image_bw_resized)
    pixel_filter = 20 
    min_pixel = np. percentile(image_bw_resized_inverted, pixel_filter) 
    image_bw_resized_inverted_scaled = np.clip(image_bw_resized_inverted-min_pixel, 0, 255) 
    max_pixel = np.max(image_bw_resized_inverted) 
    image_bw_resized_inverted_scaled = np.asarray(image_bw_resized_inverted_scaled)/max_pixel 
    test_sample = np.array(image_bw_resized_inverted_scaled).reshape(1,784) 
    test_pred = clf.predict(test_sample) 
    print("Predicted class is: ", test_pred)

    cv2.imshow("video", frame) 
    cv2.imshow("mask", frame) 
  
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 

video.release()
cv2.destroyAllWindows()

