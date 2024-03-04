import numpy as np

def remove_dups(df,col):
    platforms = df[col]
    platforms = platforms.drop_duplicates()
    platforms = platforms.sort_values(ascending=False)
    platforms.index = np.arange(len(platforms))
    return platforms