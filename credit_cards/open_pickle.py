import pickle
import os

print(os.listdir())

with open('Santander-Free.pkl', 'rb') as handle:
    cc = pickle.load(handle)