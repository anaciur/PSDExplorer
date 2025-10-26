import os
import shutil


def delete_dir(i):
    for i in range(i):  # 587 because range is exclusive at the upper bound
        try:
            # Get the list of files in the directory
            files = os.listdir(f'directory{i}')

            # Iterate through each file and delete it
            for file_name in files:
                file_path = os.path.join(f'directory{i}', file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    #print(f"Deleted: {file_path}")

            #print("All files in the directory have been deleted.")
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"An error occurred: {e}")

delete_dir(8)