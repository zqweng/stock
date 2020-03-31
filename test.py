import pandas as pd
import stock_library2 as lib2
import driver5 as dr5
import api as myapi
import boll
import plot
import pdb

def week_price():
    df=pd.DataFrame()
    for i in range(6,10):
        lib2.head_offset = i
        df1 = dr5.get_price_up_with_percentage(period_of_days=1, p_change=(40, 100), period_type='week')
        if not df.empty:
            df = pd.concat([df, df1])
        else:
            df = df1

    df.to_csv(r"result\week610.csv")


def find_history_ma20_up():
    #df_all=pd.DataFrame()
    df_all = myapi.read_csv(r"result\ma20-up.csv")
    for i in range(2,10):
        lib2.head_offset = i
        df = dr5.get_price_up_with_percentage(period_of_days=1, p_change=(9.5, 10))
        df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("close", "ma20"), cross_type="binary-cmp")
        df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("ma20", "low", 0.01, 0.01), cross_type="binary-cmp")
        if not df.empty:
            df_all = pd.concat([df_all, df])
        else:
            df_all = df

    df_all.to_csv(r"result\ma20-up.csv")

def update_hisotry_ma20_up():
    df_old = myapi.read_csv(r"result\ma20-up.csv")
    df = dr5.get_price_up_with_percentage(period_of_days=1, p_change=(9.5, 10))
    df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("close", "ma20"), cross_type="binary-cmp")
    df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("ma20", "low", 0.01, 0.01), cross_type="binary-cmp")
    df = df[df["outstanding"] <= 5]
    df_new = pd.concat([df, df_old])
    plot.start_plot("day", df_new.index.to_list(), "ma20-")
    df_old.to_csv(r"result\ma20-up-bak.csv")
    df_new.to_csv(r"result\ma20-up.csv")

def update_upper():
    df_old = myapi.read_csv(r"result\upper.csv")
    df = boll.first_cross_above_upper(rise=0.01, silence=4, market="China")
    df_new = pd.concat([df, df_old])
    plot.start_plot("day", df.index.to_list(), "upper-")
    df_old.to_csv(r"result\upper-bak.csv")
    df_new.to_csv(r"result\upper.csv")

#update_hisotry_ma20_up()
#update_upper()

df_orig = myapi.read_csv(r"mystocklist-detail.csv")
df = dr5.get_a_across_b(df_orig, period_of_days=1, cross_above=("close", "ma20"), cross_type="binary-cmp-pct")
df.sort_values(by="p1", inplace=True)
plot.start_plot("day", df.index.to_list(), "pct-")
df.to_csv(r"result\pct.csv")

df = dr5.get_a_across_b(df_orig, period_of_days=1, cross_above=("close", "ma20"), cross_type="binary-cmp-pct", period_type="60")
df.sort_values(by="p1", inplace=True)
plot.start_plot("60", df.index.to_list(), "pct-")
df.to_csv(r"result\pct-60.csv")

