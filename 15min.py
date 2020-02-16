import driver5 as dr5
import pdb

df = dr5.get_a_across_b(period_of_days=16, cross_type="vol-pct", period_type="15")
df.sort_values(by="p2", inplace=True)
pdb.set_trace()
