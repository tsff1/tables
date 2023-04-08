import pandas as pd

stats = {"Simen": ["Reka",0,0,2], "Oscar": ["Smøreguttene", 1, 1, 0]}
df = pd.DataFrame(stats)
df = df.transpose()
print(list(df))
df = df.sort_values(by=2, ascending=False)
print(df)