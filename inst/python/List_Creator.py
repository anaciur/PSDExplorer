from pathlib import Path
import os
import combine_files
import get_files1
import make_n_l_new_layer_list
import move_files_to_directory
from move_files_to_directory import add_tsv_extension

# Determine package base directory dynamically
BASE_DIR = Path(__file__).resolve().parent

def Update_List_using_last_layer_interactions(
    new_list,
    source_directory,
    extension,
    destination_directory,
    new_file_name,
    n_l
):
    """
    Update the list of proteins/interactions using the last layer.
    Ensures that intermediate TSVs are written into BASE_DIR for consistency.
    """

    # Step 1: Gather and move files
    get_files1.get_files_from_list(new_list)
    files_to_move = add_tsv_extension(new_list)
    move_files_to_directory.move_files_with_extension(
        source_directory,
        destination_directory,
        extension,
        files_to_move
    )

    # Step 2: Combine moved files into one TSV
    # Build a full output path under BASE_DIR
    output_path = BASE_DIR / new_file_name
    combine_files.search_files(destination_directory, output_path)

    # Step 3: Build new layer list
    a = make_n_l_new_layer_list.create_whole_list(output_path, n_l)

    # Step 4: Logging and stats
    print(make_n_l_new_layer_list.make_list_without_quotes(a))
    print(f"The number of layers is {len(n_l.nested_list)}")

    c = 0
    for l in n_l.nested_list:
        print(f"Proteins in layer {n_l.nested_list.index(l) + 1}: {len(l)}")
        c += len(l)
    print(len(a) - c)
    print(len(a))

    print(f"[INFO] Wrote combined list TSV: {output_path}")
    return a, output_path
