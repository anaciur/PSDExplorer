import csv
from pyvis.network import Network

import Combined_file_creator
import List_Creator
import delete_after_filename
from Combined_file_creator import Create_combined_interactions_file
from Nested_list_of_layers import NestedList
from Visualize_Protein_Network import NetworkVisualizer, generate_random_color, rgb_to_hex
from File_processor import InteractionProcessor

graph = Network(notebook=True, cdn_resources="remote", height="600px", width="100%", bgcolor="#ffffff",
                font_color="black")
graph1 = Network(notebook=True, cdn_resources="remote", height="600px", width="100%", bgcolor="#ffffff",
                 font_color="black")
total_proteins = []
total_proteins_nested_list = []
total_proteins_nested_list_selective = []
n_l = NestedList([])


def is_in_list_of_lists(input_list, pr):
    for lt in input_list:
        for item in lt:
            if item.name == pr.name:
                return True
    return False


def create_nested_list_of_layers(file_path):
    A = total_proteins_nested_list
    sublist = []
    interaction_processor = InteractionProcessor(file_path)
    interaction_processor.process_interactions()
    # network_visualizer = NetworkVisualizer(interaction_processor.total_proteins)
    new_A = interaction_processor.total_proteins
    for protein in new_A:
        ok = 0
        for l in A:
            for p in l:
                if protein.name == p.name:
                    ok = 1
                    break
        if ok == 0:
            sublist.append(protein)
    total_proteins_nested_list.append(sublist)


def create_nested_list_of_layers_selective(file_path, min_nb_of_int):
    A = total_proteins_nested_list_selective
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
                if protein.name == p.name:
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
                        if p.name == i.name:
                            count += 1
                            if count >= min_nb_of_int:
                                add = 1
                                break
            for pr in total_proteins_nested_list[len(total_proteins_nested_list) - 1]:
                if any(pr.name == x.name for x in protein.interactions):
                    count += 1
                    if count >= min_nb_of_int:
                        add = 1
                        break

        if add == 1:
            if not is_in_list_of_lists(total_proteins_nested_list_selective, protein):
                sublist.append(protein)
    total_proteins_nested_list_selective.append(sublist)


def extend_graph(file_path, s, Graph):
    interaction_processor = InteractionProcessor(file_path)
    interaction_processor.process_interactions()
    total_proteins.extend(interaction_processor.total_proteins)

    # this is a trial
    if Graph == graph1:
        create_nested_list_of_layers(file_path)

    random_color = generate_random_color()
    hex_color = rgb_to_hex(*random_color)
    # Add nodes to the network
    for protein in total_proteins:
        Graph.add_node(protein.name, label=protein.name, shape="dot", size=s, color=hex_color)
    # Add edges to the network
    for protein in total_proteins:
        for interacting_protein in protein.interactions:
            Graph.add_edge(protein.name, interacting_protein.name,
                           label=protein.interactions[interacting_protein],
                           title=protein.interactions[interacting_protein])


def extend_graph_selective(file_path, s, Graph, nb_of_min_int, color=None):
    # file_path = 'scaffolds.tsv'
    interaction_processor = InteractionProcessor(file_path)
    interaction_processor.process_interactions()
    # network_visualizer = NetworkVisualizer(interaction_processor.total_proteins)

    total_proteins.extend(interaction_processor.total_proteins)
    '''for pr in interaction_processor.total_proteins:
        if len(pr.interactions) >= nb_of_min_int:
            total_proteins.append(pr)'''

    # this is a trial
    if Graph == graph1:
        create_nested_list_of_layers(file_path)
        create_nested_list_of_layers_selective(file_path, nb_of_min_int)
        n_l.create_nested_list_of_layers_selective1(file_path, nb_of_min_int)
    # this is a trial
    if color == None:
        random_color = generate_random_color()
        hex_color = rgb_to_hex(*random_color)
    else:
        hex_color = color
    # Add nodes to the network
    #trial#####
    for protein in interaction_processor.total_proteins:
        Graph.add_node(protein.name, label=protein.name, shape="dot", size=s, color=hex_color)
    # Add edges to the network

    # for protein in total_proteins:
    for lst in total_proteins_nested_list:
        for protein in lst:
            # if len(protein.interactions) >= nb_of_min_int:
            # if is_in_list_of_lists(total_proteins_nested_list_selective, protein):
            for interacting_protein in protein.interactions:
                #trial####
                for pr in interaction_processor.total_proteins:
                    if interacting_protein.name == pr.name:
                        Graph.add_edge(protein.name, interacting_protein.name,
                                       label=protein.interactions[interacting_protein],
                                       title=protein.interactions[interacting_protein])


def create_lst_from_nl(nl: list[list]):
    li = []
    for l in nl:
        for pr in l:
            li.append(pr)
    return li


extension = '.tsv'  # Replace with the desired file extension
source_directory = 'C:\\Users\\User\PycharmProjects\pythonProject5'  # Replace with the actual source directory path

# add the scaffolds - layer 1
extend_graph_selective('scaffolds.tsv', 35, graph1, 0)


# add the interactions between scaffolds and layer2 proteins cumulative
# extend_graph_selective('scaffolds_2_layer_combined_interactions_within.tsv', 25, graph1, 1)


def Graph_Expansion_one_more_layer(i, s, min_int):
    #last_list = n_l.nested_list[len(n_l.nested_list) - 1]
    last_list = [pr.name for pr in total_proteins_nested_list_selective[len(total_proteins_nested_list_selective) - 1]]
    directory = f'C:\\Users\\User\PycharmProjects\pythonProject5\\directory{i}'
    a = List_Creator.Update_List_using_last_layer_interactions(last_list, source_directory, extension, directory,
                                                               f'up_to_layer_{i + 1}.tsv', n_l)
    Combined_file_creator.Create_combined_interactions_file(f'up_to_layer{i + 1}_cumulative', a)
    extend_graph_selective(f'up_to_layer{i + 1}_cumulative.tsv', s, graph1, min_int)


def make_n_layer_graph(in_size, n, min_int):
    s = in_size
    for i in range(1, 2):
        # expansion from  scaffolds(layer 0) to layer 1
        #ai = 1
        Graph_Expansion_one_more_layer(i, s,3)
        s = s - in_size / n


    for i in range(2,3):
        # expansion from layer 1 to layer 2
        #aj = 2
        Graph_Expansion_one_more_layer(i, s, 2)
        s = s - in_size / n


    for i in range(3, 4):
        Graph_Expansion_one_more_layer(i, s, 3)
        s = s - in_size / n
        min_int = min_int+0
    for i in range(4, n):
        Graph_Expansion_one_more_layer(i, s, 6)
        s = s - in_size / n
        min_int = min_int + 0

    ''' a=ai
        b=aj
        ai=b
        aj=a+b
        # min_int = min_int +3'''
    '''
    for i in range(6, n):
        m = 2
        Graph_Expansion_one_more_layer(i, s, m)
        s = s - in_size / n
        min_int = min_int +0'''


make_n_layer_graph(20, 4,2)


def find_max_protein():
    l = []
    l1= []
    max1 = 0
    for pr in total_proteins:
        len=0
        for i in pr.interactions:
            len +=1
        if len > max1:
            max1 = len
        if len not in l1:
            l1.append(len)
    for pr in total_proteins:
        len = 0
        for i in pr.interactions:
            len += 1
        if len == max1:
            l.append(pr.name)
    print(l)
    print(max1)
    print(l1)


find_max_protein()


'''
last_list = n_l.nested_list[len(n_l.nested_list) - 1]
directory2 = 'C:\\Users\\User\PycharmProjects\pythonProject5\\directory2'
a = List_Creator.Update_List_using_last_layer_interactions(last_list, source_directory, extension, directory2,
                                                           'up_to_layer_3.tsv', n_l)
Combined_file_creator.Create_combined_interactions_file('up_to_layer3_cumulative', a)
extend_graph_selective('up_to_layer3_cumulative.tsv', 20, graph1, 3)

last_list = n_l.nested_list[len(n_l.nested_list) - 1]
directory3 = 'C:\\Users\\User\PycharmProjects\pythonProject5\\directory3'
a = List_Creator.Update_List_using_last_layer_interactions(last_list, source_directory, extension, directory3,
                                                           'up_to_layer_4.tsv', n_l)
Combined_file_creator.Create_combined_interactions_file('up_to_layer4_cumulative', a)
extend_graph_selective('up_to_layer4_cumulative.tsv', 10, graph1, 4)

last_list = n_l.nested_list[len(n_l.nested_list) - 1]
directory4 = 'C:\\Users\\User\PycharmProjects\pythonProject5\\directory4'
a = List_Creator.Update_List_using_last_layer_interactions(last_list, source_directory, extension, directory4,
                                                           'up_to_layer_5.tsv', n_l)
Combined_file_creator.Create_combined_interactions_file('up_to_layer5_cumulative', a)
extend_graph_selective('up_to_layer5_cumulative.tsv', 5, graph1, 5)




# extend_graph('scaffolds_2nd_3rd_layer_interactions_all#.tsv', 10, graph1)

# add the interactions of the the third ayer-i.e the 4 th layer
extend_graph_selective('3rd_layer#.tsv', 30, graph1, 1)

# add the interactions of the 4th layer - i.e the 5th layer
extend_graph_selective('4th_layer#.tsv', 20, graph1, 2)

# add the interactions of the 5th layer - i.e the 6th layer
extend_graph_selective('5th_layer#.tsv', 10, graph1, 2)

# add the interactions of the 6th layer - i.e the 7th layer
extend_graph_selective('6th_layer#.tsv', 10, graph1, 2)

'''

for lst in total_proteins_nested_list:
    print(f"layer {total_proteins_nested_list.index(lst)}")
    print(','.join(pr.name for pr in lst))
    print(f"{len(lst)}")

'''
for lst in total_proteins_nested_list_selective:
    print(f"layer {total_proteins_nested_list_selective.index(lst)}")
    print(','.join(pr.name for pr in lst))
    print(f"{len(lst)}")
'''
for lst in total_proteins_nested_list_selective:
    lst_str = ["'{}'".format(pr.name) for pr in lst]
    joined_str = ','.join(lst_str)
    print(f"layer {total_proteins_nested_list_selective.index(lst)}")
    print(joined_str)
    print(len(lst_str))

for lst in n_l.nested_list:
    lst_str = ["{}".format(pr) for pr in lst]
    joined_str = ','.join(lst_str)
    print(f"layer {n_l.nested_list.index(lst)}")
    print(joined_str)
    print(len(lst_str))
# Set the physics configuration to enable node dragging
graph.set_options(
    """
    var options = {
        "physics": {
            "enabled": true,
            "barnesHut": {
                "springLength": 100
            }
        }
    }
    """
)

# Show the graph

# Render the graphs into the HTML
graph.show("main.html")
graph1.show("main.html")


def main():
    '''file_path = 'scaffolds.tsv'

    # Task 1: Interaction Processing

    # filter through the file_path, and create a dictionary of each 2 proteins + the likelihood of their interaction
    interaction_processor = InteractionProcessor(file_path)
    interaction_processor.process_interactions()

    # Task 2: Network Visualization
    network_visualizer = NetworkVisualizer(interaction_processor.total_proteins)
    network_visualizer.visualize_network()'''

    QDPR_file_path = 'QDPR.tsv'

# if __name__ == "__main__":
# main()
# Press the green button in the gutter to run the script.
# for layer in total_proteins_nested_list:
# delete_after_filename.delete_after_name(f'{pr.name}.tsv' for pr in layer)
