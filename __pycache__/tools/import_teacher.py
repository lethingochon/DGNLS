import pandas as pd

# Đường dẫn file Excel
file_path = "CSDL NĂNG LỰC SỐ GV.xlsx"

# Đọc sheet GIAOVIEN
df = pd.read_excel(file_path, sheet_name="GIAOVIEN")

print("Đọc thành công!")
print(df.head())