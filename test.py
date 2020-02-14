import driver5 as dr5
import api as myapi
from datetime import datetime
import pdb

df = myapi.read_csv(r"result\ma20-6p-2020-02-14.csv")
df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("ma5", "ma10", "ma20"), cross_type="conv")

pdb.set_trace()
df.to_csv(r"result/ma20-4p-{}.csv".format(datetime.today().strftime('%Y-%m-%d')))
