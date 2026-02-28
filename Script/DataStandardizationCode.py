import pandas as pd
import ast

df = pd.read_csv("/content/Iphones7.csv")

df['Product_name'] = df['Product_name'].str.split('(').str[0].str.strip()

df['specs_dict'] = df['Specification'].apply(ast.literal_eval)

specs_df = pd.json_normalize(df['specs_dict'])

final_df = pd.concat(
    [df.drop(columns=['Specification', 'specs_dict']), specs_df],
    axis=1
)

processor_keys = ['Processor', 'chip', 'Snapdragon', 'Bionic', 'MediaTek', 'Exynos', 'helio']
camera_keys = ['camera', 'mp']

def has_battery(text):
    return isinstance(text, str) and 'mah' in text.lower()
def is_processor(text):
    return isinstance(text, str) and any(k in text.lower() for k in processor_keys)
def is_camera(text):
    return isinstance(text, str) and any(k in text.lower() for k in camera_keys)
def is_warranty(text):
    return isinstance(text, str) and ('warranty' in text.lower() or 'warrenty')

final_df['Battery'] = final_df[['Camera', 'Processor', 'Warranty']].apply(
    lambda x: next((v for v in x if has_battery(v)), None),
    axis=1
)

def clean_and_route(row):
    info = []

    # Processor
    if row.get('Processor'):
        if not is_processor(row['Processor']):
            info.append(row['Processor'])
            row['Processor'] = None

    # Camera
    if row.get('Camera'):
        if not is_camera(row['Camera']):
            info.append(row['Camera'])
            row['Camera'] = None

    # Warranty
    if row.get('Warranty'):
        if not is_warranty(row['Warranty']):
            info.append(row['Warranty'])
            row['Warranty'] = None

    row['Info'] = " | ".join(info) if info else None
    return row

final_df = final_df.apply(clean_and_route, axis=1)

final_df.to_csv("Iphones_flipkart.csv", index=False)

print("Strict standardization completed")
