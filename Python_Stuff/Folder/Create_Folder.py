import os

fodler_path = '/home/nikita/Desktop/sqldeveloper/temp/temp2'

if not os.path.exists(fodler_path):
    os.makedirs(fodler_path)
    print(f"Directory " , fodler_path , " Created ")
else:
    print(f"Directory " , fodler_path , " already exists")