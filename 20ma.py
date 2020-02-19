import driver5 as dr5
from datetime import datetime
import stock_library2 as lib2
import pdb
lib2.head_offset = 0

df = dr5.get_a_across_b(period_of_days=1, cross_above=("close", "ma20"), cross_type="binary-cmp")
df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("ma20", "low", 0.01, 0.01), cross_type="binary-cmp")
df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("ma5", "ma10", "ma20"), cross_type="conv")
df1 = dr5.get_a_across_b(df, period_of_days=16, cross_type="vol-pct", period_type="15")
df["p2"] = df1["p2"]
df.sort_values(by="p2", inplace=True)
df.to_csv(r"result/ma20-{}.csv".format(datetime.today().strftime('%Y-%m-%d')))
#df.to_csv(r"result/ma20-2020-02-17.csv")

df = df[df["p2"] < 0.8]
df = df[df["p2"] >= 0.6]
df = df[df["p_change"] >=6]
df.to_csv(r"result/ma20-{}-6p.csv".format(datetime.today().strftime('%Y-%m-%d')))
"""
df_final = dr5.get_a_across_b(df, period_of_days=1, cross_above=("ma5", "ma20"), cross_type="binary-cmp")
df_final = dr5.get_a_across_b(df_final, period_of_days=1, cross_above=("ma10", "ma20"), cross_type="binary-cmp")
df_final = dr5.get_a_across_b(df_final, period_of_days=1, cross_above=("ma5", "ma10", "ma20"), cross_type="conv")
df_final = df_final.sort_values(by="p1")
df_final.to_csv(r"result/ma20-final-{}.csv".format(datetime.today().strftime('%Y-%m-%d')))
"""
