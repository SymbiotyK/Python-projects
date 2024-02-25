import pandas as pd
import numpy as np
import openpyxl

dates = pd.date_range('20240101', periods=366)
data = np.arange(len(dates) * 4).reshape(-1, 4)

df = pd.DataFrame(data, index=dates, columns=['A', 'B', 'C', 'D'])
df['sum'] = df.eval('A+B+C+D')
df['Week'] = ((df.index.dayofyear - df.index.dayofweek + 7) // 7).astype(int)
df = df.groupby("Week").sum()

ef = pd.DataFrame(data, index=dates, columns=['A', 'B', 'C', 'D'])
ef['sum'] = ef.eval('A+B+C+D')
ef.index.name = 'Day'
ef.index = ef.index.strftime("%d.%m.%Y")

file_path = 'output.xlsx'

try:
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a',if_sheet_exists="overlay") as writer:
        writer.workbook = openpyxl.load_workbook(file_path)
        ef.to_excel(writer, sheet_name='Daily', index=True)
        df.loc[0:52].to_excel(writer, sheet_name='Weekly', index=True)
except PermissionError:
    print("Zamknij excela kurwo!!")
    pass