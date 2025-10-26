from File_processor import InteractionProcessor
from Protein_attributes import Protein
#from main import create_nested_list_of_layers_selective


def is_in_list_of_lists(input_list, pr):
    for lt in input_list:
        for item in lt:
            if item == pr.name:
                return True
    return False


class NestedList:

    #nested_list = []

    #nested_list = None

    def __init__(self, nested_list):

        self.nested_list = nested_list

    def create_nested_list_of_layers_selective1(self, file_path, min_nb_of_int):
        A = self.nested_list
        sublist = []
        count = 0
        add = 0
        interaction_processor = InteractionProcessor(file_path)
        interaction_processor.process_interactions()
        # network_visualizer = NetworkVisualizer(interaction_processor.total_proteins)
        new_A = interaction_processor.total_proteins
        for protein in new_A:
            ok = 0
            for l in A:
                for p in l:
                    if protein.name == p:
                        ok = 1
                        break
            if ok == 0:
                add = 0
                count = 0
                if not any(A):
                    add = 1
                for l in A:
                    for p in l:
                        for i in protein.interactions:
                            if p == i.name:
                                count += 1
                                if count >= min_nb_of_int:
                                    add = 1
                                    break


            if add == 1:
                if not is_in_list_of_lists(self.nested_list, protein):
                    sublist.append(protein.name)
        self.nested_list.append(sublist)


n_l = NestedList([])
n_l.create_nested_list_of_layers_selective1('scaffolds.tsv', 0)
#n_l.create_nested_list_of_layers_selective1('scaffolds#.tsv', 1)
#n_l.create_nested_list_of_layers_selective1('2nd_layer#.tsv', 1)
n_l.create_nested_list_of_layers_selective1('scaffolds_2_layer_combined_interactions_within.tsv', 1)
#n_l.create_nested_list_of_layers_selective1('scaffolds#-1_2_layer_combined_interactions_within#.tsv', 1)
for lst in n_l.nested_list:
    l = []
    for el in lst:
        l.append(el)
        #print(el)
    print(l)
    print(len(l))
    #print(len(n_l.nested_list))

