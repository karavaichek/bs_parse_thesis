import os
import shutil

bs_folder = 'E:/Thesis/Excel files/Output_bs/'
pl_folder = 'E:/Thesis/Excel files/Output_pl/'

for filename in os.listdir(bs_folder):
    file_path = os.path.join(bs_folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

for filename in os.listdir(pl_folder):
    file_path = os.path.join(pl_folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))
for i in range(2020, 2024):
    os.mkdir(os.path.join(bs_folder, str(i)))
    os.mkdir(os.path.join(pl_folder, str(i)))
os.mkdir(os.path.join(bs_folder, "raw"))
os.mkdir(os.path.join(pl_folder, "raw"))
