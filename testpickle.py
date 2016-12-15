import pickle
import os

vpath = os.environ['INSURANCE_QA']
# print(os.path.join(vpath, 'train'))
handle = open(os.path.join(vpath, 'train'), 'rb')
pickle.load(handle)
