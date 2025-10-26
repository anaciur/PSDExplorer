#import main
from File_processor import InteractionProcessor
#from main import n_l


def create_whole_list(new_layer_file, nested_lst):
    interaction_processor = InteractionProcessor(new_layer_file)
    interaction_processor.process_interactions()
    new_list = [pr.name for pr in interaction_processor.total_proteins]

    for layer in nested_lst.nested_list:
        for pr in layer:
            new_list.append(pr)

    return new_list

'''scaffold_2_layer_list= create_whole_list('scaffolds#.tsv', n_l)
for el in scaffold_2_layer_list:
    print(el)
print(len(scaffold_2_layer_list))'''



'''scaffold_2_3_layer_list = create_whole_list('2nd_layer#.tsv', n_l)
# for el in scaffold_2_3_layer_list:
#    print(el)
print(len(scaffold_2_3_layer_list))
lst_str = ["{}".format(pr) for pr in scaffold_2_3_layer_list]
joined_str = ','.join(lst_str)
print(joined_str)
print(len(lst_str))'''


'''
    
    for lst in n_l.nested_list:
    lst_str = ["{}".format(pr) for pr in lst]
    joined_str = ','.join(lst_str)
    print(f"layer {n_l.nested_list.index(lst)}")
    print(joined_str)
    print(len(lst_str))
    '''
'''lst_str = ["{}".format(pr) for pr in n_l.nested_list[len(n_l.nested_list) - 1]]
joined_str = ','.join(lst_str)
print(f"layer {len(n_l.nested_list)}")
print(joined_str)
print(len(lst_str))'''



# print(n_l.nested_list[len(n_l.nested_list)-1])

def make_list_without_quotes(list1):
    lst_str = ["{}".format(pr) for pr in list1]
    joined_str = ','.join(lst_str)
    return joined_str

#print(make_list_without_quotes(n_l.nested_list[len(n_l.nested_list) - 1]))
