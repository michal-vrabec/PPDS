import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data.csv')

columns = df.columns
for column1 in columns:
    for column2 in columns:
        if column1 == column2 or column1 == 'produced'\
                or column2 == 'produced' or column1 == 'consumed'\
                or column2 == 'consumed':
            continue
        df[column1 + ':' + column2] = df.apply(
            lambda row: row[column1] / row[column2], axis=1)

for column in df.columns:
    df.plot(x=column, y='produced', kind='scatter')
    plt.show()
