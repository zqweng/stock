import driver5 as dr5
from datetime import datetime
import pdb

df = dr5.get_a_across_b(period_of_days=1, cross_above=("close", "ma20"), cross_type="binary-cmp")
df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("ma20", "low", 0.01, 0.01), cross_type="binary-cmp")
df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("ma5", "ma10", "ma20"), cross_type="conv")
df = df.sort_values(by="p_change", ascending=False)
df.to_csv(r"result/ma20-{}.csv".format(datetime.today().strftime('%Y-%m-%d')))

"""
df_final = dr5.get_a_across_b(df, period_of_days=1, cross_above=("ma5", "ma20"), cross_type="binary-cmp")
df_final = dr5.get_a_across_b(df_final, period_of_days=1, cross_above=("ma10", "ma20"), cross_type="binary-cmp")
df_final = dr5.get_a_across_b(df_final, period_of_days=1, cross_above=("ma5", "ma10", "ma20"), cross_type="conv")
df_final = df_final.sort_values(by="p1")
df_final.to_csv(r"result/ma20-final-{}.csv".format(datetime.today().strftime('%Y-%m-%d')))
"""
