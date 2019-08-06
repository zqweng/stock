import pandas as pd
import os
import pdb

mystock_file = 'stocklist.csv'
allstock_file = 'basic-no3.csv'

if not os.path.isfile(allstock_file):
    print('全部股票清单 not exist, create one')
    quit()
else:
    print('全部股票清单 exists, load it')
    df_all = pd.read_csv(allstock_file, converters={'code': lambda x: str(x)})
    index = df_all['code']

if not os.path.isfile(mystock_file):
    print('自选股票清单, not exist, create one')
    quit()
else:
    print('自选股票清单, exist, load it')
    df = pd.read_csv(mystock_file)

new_df = df_all[df_all['name'].isin(df['名称'])]
new_df.to_csv('mystocklist-detail.csv', encoding='ansi')