import tushare as ts
import pandas as pd
import os
import glob
import pdb

"""
os.system('cp basic-no3.csv basic-no3-old.csv')


df = ts.get_stock_basics()

df = df[df.index.str.startswith("3") == False]
df = df[df.index.str.startswith("68") == False]
df = df.sort_index()

df.to_csv("basic-no3.csv")
"""

df = pd.read_csv("basic-no3.csv")

os.chdir("财报")
count = 0

for filepath in glob.iglob('*.csv'):
    name = filepath[:-4]
    #pdb.set_trace()
    if not name in df["name"].values:
        #os.system('mv {} ../废财报/'.format(filepath))
        print("move {} count {}".format(name, count))
        count = count + 1


