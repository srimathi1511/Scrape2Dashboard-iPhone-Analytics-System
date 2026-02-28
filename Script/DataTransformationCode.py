df = pd.read_csv("/content/Iphones_for_pandas.csv")
df.rename(columns={'ROM':'Memory'}, inplace=True)

import pandas as pd
import numpy as np
import re

def transform_rom(text):
    result = {
        "RAM": np.nan,
        "ROM": np.nan,
        "Is_Expandable": "No",
        "Expandable_Upto": np.nan
    }

    if pd.isna(text):
        return pd.Series(result)

    # RAM
    ram_match = re.search(r'(\d+\s*(?:GB|MB))\s*RAM', text)
    if ram_match:
        result["RAM"] = ram_match.group(1)

    # ROM
    rom_match = re.search(r'(\d+\s*(?:GB|MB|TB))\s*ROM', text)
    if rom_match:
        result["ROM"] = rom_match.group(1)

    # Expandable
    if "Expandable" in text:
        result["Is_Expandable"] = "Yes"
        exp_match = re.search(r'Expandable\s*Upto\s*(\d+\s*(?:GB|MB|TB))', text)
        if exp_match:
            result["Expandable_Upto"] = exp_match.group(1)

    return pd.Series(result)

df[["RAM", "ROM", "Is_Expandable", "Expandable_Upto"]] = df["Memory"].apply(transform_rom)

df.drop(columns=["Memory"], inplace=True)

df['Colour'] = df['Colour'].str.strip()

colour_agg = (
    df.groupby(['Product_name', 'ROM'])['Colour']
      .apply(lambda x: ', '.join(sorted(x.dropna().unique())))
      .reset_index(name='Colours')
)

df_base = df.drop(columns=['Colour']).drop_duplicates(subset=['Product_name', 'ROM'])

final_df = df_base.merge(
    colour_agg,
    on=['Product_name', 'ROM'],
    how='left'
)

final_df.to_csv("Iphones_transformed_data.csv")
