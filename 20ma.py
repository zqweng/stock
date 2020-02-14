import driver5 as dr5
from datetime import datetime
import pdb

df = dr5.get_a_across_b(period_of_days=1, cross_above=("close", "ma20"), cross_type="binary-cmp")
df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("ma20", "low", 0.01, 0.01), cross_type="binary-cmp")
df.to_csv(r"result/ma20-{}.csv".format(datetime.today().strftime('%Y-%m-%d')))

df_6p = dr5.get_price_up_with_percentage(df, period_of_days=1, p_change=(6, 11), period_type='day')
df_6p = dr5.get_a_across_b(df_6p, period_of_days=1, cross_above=("ma5", "ma10", "ma20"), cross_type="conv")
df_6p = df_6p.sort_values(by="p1")
df_6p.to_csv(r"result/ma20-6p-{}.csv".format(datetime.today().strftime('%Y-%m-%d')))

df_3p = dr5.get_price_up_with_percentage(df, period_of_days=1, p_change=(3.5, 11), period_type='day')
df_3p = dr5.get_a_across_b(df_3p, period_of_days=1, cross_above=("ma5", "ma10", "ma20"), cross_type="conv")
df_3p = df_3p.sort_values(by="p1")
df_3p.to_csv(r"result/ma20-3p-{}.csv".format(datetime.today().strftime('%Y-%m-%d')))

df_final = dr5.get_a_across_b(df_3p, period_of_days=1, cross_above=("ma5", "ma20"), cross_type="binary-cmp")
df_final = dr5.get_a_across_b(df_final, period_of_days=1, cross_above=("ma10", "ma20"), cross_type="binary-cmp")
df_final = dr5.get_a_across_b(df_final, period_of_days=1, cross_above=("ma5", "ma10", "ma20"), cross_type="conv")
df_final = df_final.sort_values(by="p1")
df_final.to_csv(r"result/ma20-final-{}.csv".format(datetime.today().strftime('%Y-%m-%d')))
