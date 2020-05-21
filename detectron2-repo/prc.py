import pickle
import os.path as osp
import matplotlib.pyplot as plt

PR_path = '/Users/sunbowen/Desktop/detectron2_result/resnet101_final_model/output/instances_predictions.pth'
f = open(PR_path, 'rb')
info = pickle.load(f)
precision = info['prec']
recall = info['rec']
plt.plot(recall, precision)
plt.show()
