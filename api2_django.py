import pandas as pd

def get_stock_list():
    df = pd.read_csv("blog/github/basic-no3.csv", converters={'code': lambda x: str(x)})
    #df = pd.read_csv("basic-no3.csv", converters={'code': lambda x: str(x)})
    return df.to_html(classes='table " id = "table_id')

if __name__ == '__main__':
    ret = get_stock_list()
    print(ret)