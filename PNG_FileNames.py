import pandas, os

df = pandas.DataFrame([], columns=['Subclass', 'Trivial Names of Compounds'])
directory = "C:/Users/Antoine/Dropbox/UCSD/Coding/Predicted_HSQC/"

# for png_file in glob.glob(os.path.join(directory, '*.png')):
#     folder_name = os.path.basename(os.path.dirname(png_file))
#     # print(folder_name)
#     file = os.path.basename(png_file)
#     trivial_name = os.path.splitext(file)[0]
#     # print(trivial_name)
#     df = df.append(pandas.DataFrame([[folder_name, trivial_name]]))
#
# df.to_csv('FileNames', index=False, header=True)
folder_list = list()
trivial_list = list()


for root, dirs, files in os.walk(directory, topdown=True):
    for file in files:
        if file.endswith(".png"):
            file_path = (os.path.join(root, file))
            folder_name = os.path.basename(os.path.dirname(file_path))
            folder_list.append(folder_name)
            file_name = os.path.basename(file_path)
            trivial_name = os.path.splitext(file_name)[0]
            trivial_list.append(trivial_name)

data = {'Subclass': folder_list, 'Trivial Names of Compounds': trivial_list}
df = pandas.DataFrame(data)
# print(df)
# df = df.append(pandas.DataFrame([[folder_name, trivial_name]]))

df.to_csv('FileNames', index=False, header=True)

