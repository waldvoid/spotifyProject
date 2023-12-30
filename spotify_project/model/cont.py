import pandas as pd

# Dosyayı oku
df = pd.read_csv('model/data/output.csv')

# Tüm sütunlarda NaN değerleri kontrol et ve sütun numarasına göre yazdır
for col_num, col_name in enumerate(df.columns):
    nan_count = df[col_name].isna().sum()
    print(f"'{col_name}' sütununda {nan_count} tane NaN değeri var.")
