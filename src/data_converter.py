import pandas as pd
import json

with open('./data/medal_table.json') as file:
    df_dict = json.load(file)

for i in range(3):
    df = pd.DataFrame(df_dict[str(i+1)])
    df_file_path = f"./data/medal_table_day{i+1}.csv"
    df.to_csv(df_file_path, index=False)
    

    