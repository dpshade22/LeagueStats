import pandas as pd

df = pd.DataFrame(columns=['Hi'])
newRow = pd.Series([1], index=['Hi'])

df.loc[2] = newRow

print(df)
