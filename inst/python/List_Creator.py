import combine_files
import get_files1
import make_n_l_new_layer_list
import move_files_to_directory
# from main import n_l
from move_files_to_directory import add_tsv_extension


def Update_List_using_last_layer_interactions(new_list, source_directory, extension, destination_directory,
                                              new_file_path, n_l):
    get_files1.get_files_from_list(new_list)
    files_to_move = add_tsv_extension(new_list)

    move_files_to_directory.move_files_with_extension(source_directory, destination_directory, extension, files_to_move)
    combine_files.search_files(destination_directory, new_file_path)
    a = make_n_l_new_layer_list.create_whole_list(new_file_path, n_l)

    print(make_n_l_new_layer_list.make_list_without_quotes(a))
    print(f'The number of layers is {len(n_l.nested_list)}')
    c = 0
    for l in n_l.nested_list:
        print(f'the number of protein in layer{n_l.nested_list.index(l) + 1} is {len(l)}')
        c += len(l)
    print(len(a)-c)
    print(len(a))

    return a
