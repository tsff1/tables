import numpy as np
import pandas as pd

np.random.seed(1)
df = pd.DataFrame(np.random.randn(8, 4),
                  columns=['A', 'B', 'C', 'D'])

print(df)
df.rename(columns=[0,1,2,3])
print(df)