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
df1 = dr5.get_a_across_b(df, period_of_days=100, cross_above=("up", "ma20"), cross_type="unary-current-trend",
                       period_type='day')
df["ma20-up"] = df1["p1"]
df.to_csv(r"result/{}.csv".format(datetime.today().strftime('%Y-%m-%d')))
#df.to_csv(r"result/2020-02-17.csv")

df = df[df["p2"] < 0.8]
df = df[df["p2"] >= 0.6]
df = df[df["p_change"] >=4]
df.to_csv(r"result/{}-6p.csv".format(datetime.today().strftime('%Y-%m-%d')))

df2 = dr5.get_a_across_b(period_of_days=16, cross_type="vol-pct-count", period_type="15")
df2 = df2[df2["p3"] >=2]
df3 = dr5.get_a_across_b(df2, period_of_days=16, cross_type="vol-pct", period_type="15")
df3 = df3[df3["p2"] >=0.65]
df2 = df2.reindex(df3.index)
df2["p2"] = df3["p2"]
df4 = dr5.get_a_across_b(df2, period_of_days=100, cross_above=("up", "ma20"), cross_type="unary-current-trend",
                       period_type='day')
df2["ma20-up"] = df4["p1"]
df2.to_csv(r"result/15min-vol-{}.csv".format(datetime.today().strftime('%Y-%m-%d')))



df = dr5.get_a_across_b(period_of_days=1, cross_above=("close", "upper", 0.01), cross_type="binary-cmp")
lib2.head_offset = 1
df = dr5.get_a_across_b(df, period_of_days=5, cross_above=("upper", "close"), cross_type="binary-cmp")
lib2.head_offset = 1
df1 = dr5.get_a_across_b(df, cross_type="boll-band")
df["p1"] = df1["p1"]
df.sort_values(by="p1", inplace=True)
df4 = dr5.get_a_across_b(df, period_of_days=100, cross_above=("up", "ma20"), cross_type="unary-current-trend",
                       period_type='day')
df["ma20-up"] = df4["p1"]
df.to_csv(r"result/boll-{}.csv".format(datetime.today().strftime('%Y-%m-%d')))
"""
df_final = dr5.get_a_across_b(df, period_of_days=1, cross_above=("ma5", "ma20"), cross_type="binary-cmp")
df_final = dr5.get_a_across_b(df_final, period_of_days=1, cross_above=("ma10", "ma20"), cross_type="binary-cmp")
df_final = dr5.get_a_across_b(df_final, period_of_days=1, cross_above=("ma5", "ma10", "ma20"), cross_type="conv")
df_final = df_final.sort_values(by="p1")
df_final.to_csv(r"result/ma20-final-{}.csv".format(datetime.today().strftime('%Y-%m-%d')))
"""

