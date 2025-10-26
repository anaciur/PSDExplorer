import os

base_path = "C:\\Users\\User\\PycharmProjects\\pythonProject5"  # Adjust the base path as necessary
'''
for i in range(4, 7):  # 1786 because range is exclusive at the upper bound
    file_path = os.path.join(base_path, f"{i}th_layer#.tsv")

    if os.path.exists(file_path) and os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
    else:
        print(f"File does not exist: {file_path}")

    file_path = os.path.join(base_path, "2nd_layer#.tsv")

    if os.path.exists(file_path) and os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
    else:
        print(f"File does not exist: {file_path}")

    file_path = os.path.join(base_path, '3rd_layer#.tsv')

    if os.path.exists(file_path) and os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
    else:
        print(f"File does not exist: {file_path}")

    file_path = os.path.join(base_path, 'scaffolds#.tsv')

    if os.path.exists(file_path) and os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
    else:
        print(f"File does not exist: {file_path}")
    
    '''


def delete_file(i):
    file_path = os.path.join(base_path, f"up_to_layer{i}_cumulative.tsv")
    if os.path.exists(file_path) and os.path.isfile(file_path):
        os.remove(file_path)

    file_path = os.path.join(base_path, f"up_to_layer_{i}.tsv")
    if os.path.exists(file_path) and os.path.isfile(file_path):
        os.remove(file_path)


for i in range(8):
    delete_file(i)
