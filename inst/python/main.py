import os
import csv
from pyvis.network import Network

import Combined_file_creator
import List_Creator
import delete_after_filename
from Combined_file_creator import Create_combined_interactions_file
from Nested_list_of_layers import NestedList
from Visualize_Protein_Network import NetworkVisualizer, generate_random_color, rgb_to_hex
from File_processor import InteractionProcessor

# Allow R to override working directory
WORK_DIR = os.getenv("PSD_WORKDIR", os.path.dirname(__file__))
os.makedirs(WORK_DIR, exist_ok=True)
print(f"[DEBUG] Working directory: {WORK_DIR}")

# === Read parameters sent from R (via Sys.setenv) ===
layers = int(os.getenv("PSD_LAYERS", 3))
min_int = int(os.getenv("PSD_MIN_INT", 2))
input_tsv = os.getenv("PSD_INPUT", "scaffolds.tsv")  # ✅ full path from R
out_html = os.getenv("PSD_OUT", "main.html")

print("📂 Using input file:", input_tsv)

# === Dynamic working directory ===
BASE_DIR = os.path.dirname(__file__)
source_directory = BASE_DIR
extension = ".tsv"

# === Global variables ===
graph = Network(notebook=True, cdn_resources="remote", height="600px", width="100%", bgcolor="#ffffff", font_color="black")
graph1 = Network(notebook=True, cdn_resources="remote", height="600px", width="100%", bgcolor="#ffffff", font_color="black")
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
    new_A = interaction_processor.total_proteins
    for protein in new_A:
        if not any(p.name == protein.name for l in A for p in l):
            sublist.append(protein)
    total_proteins_nested_list.append(sublist)


def create_nested_list_of_layers_selective(file_path, min_nb_of_int):
    A = total_proteins_nested_list_selective
    sublist = []
    interaction_processor = InteractionProcessor(file_path)
    interaction_processor.process_interactions()
    new_A = interaction_processor.total_proteins

    for protein in new_A:
        if any(p.name == protein.name for l in A for p in l):
            continue
        add = False
        count = 0
        if not any(A):
            add = True
        for l in A:
            for p in l:
                for i in protein.interactions:
                    if p.name == i.name:
                        count += 1
                        if count >= min_nb_of_int:
                            add = True
                            break
        if total_proteins_nested_list:
            for pr in total_proteins_nested_list[-1]:
                if any(pr.name == x.name for x in protein.interactions):
                    count += 1
                    if count >= min_nb_of_int:
                        add = True
                        break
        if add and not is_in_list_of_lists(total_proteins_nested_list_selective, protein):
            sublist.append(protein)
    total_proteins_nested_list_selective.append(sublist)


def extend_graph(file_path, s, Graph):
    interaction_processor = InteractionProcessor(file_path)
    interaction_processor.process_interactions()
    total_proteins.extend(interaction_processor.total_proteins)

    if Graph == graph1:
        create_nested_list_of_layers(file_path)

    random_color = generate_random_color()
    hex_color = rgb_to_hex(*random_color)

    for protein in total_proteins:
        Graph.add_node(protein.name, label=protein.name, shape="dot", size=s, color=hex_color)
    for protein in total_proteins:
        for interacting_protein in protein.interactions:
            Graph.add_edge(protein.name, interacting_protein.name,
                           label=protein.interactions[interacting_protein],
                           title=protein.interactions[interacting_protein])


def extend_graph_selective(file_path, s, Graph, nb_of_min_int, color=None):
    interaction_processor = InteractionProcessor(file_path)
    interaction_processor.process_interactions()
    total_proteins.extend(interaction_processor.total_proteins)

    if Graph == graph1:
        create_nested_list_of_layers(file_path)
        create_nested_list_of_layers_selective(file_path, nb_of_min_int)
        n_l.create_nested_list_of_layers_selective1(file_path, nb_of_min_int)

    hex_color = rgb_to_hex(*generate_random_color()) if color is None else color
    for protein in interaction_processor.total_proteins:
        Graph.add_node(protein.name, label=protein.name, shape="dot", size=s, color=hex_color)

    for lst in total_proteins_nested_list:
        for protein in lst:
            for interacting_protein in protein.interactions:
                for pr in interaction_processor.total_proteins:
                    if interacting_protein.name == pr.name:
                        Graph.add_edge(protein.name, interacting_protein.name,
                                       label=protein.interactions[interacting_protein],
                                       title=protein.interactions[interacting_protein])


def create_lst_from_nl(nl: list[list]):
    return [pr for l in nl for pr in l]


def Graph_Expansion_one_more_layer(i, s, min_int):
    """Expands the PSD graph by one layer, verifying file creation."""
    last_list = [pr.name for pr in total_proteins_nested_list_selective[-1]]
    directory = os.path.join(BASE_DIR, f"directory{i}")
    os.makedirs(directory, exist_ok=True)

    print(f"[DEBUG] Expanding to layer {i + 1} | Output dir: {directory}")

    # Step 1: generate updated list of interactions
    a = List_Creator.Update_List_using_last_layer_interactions(
        last_list, BASE_DIR, extension, directory,
        f'up_to_layer_{i + 1}.tsv', n_l
    )

    # Step 2: create combined interaction file
    Combined_file_creator.Create_combined_interactions_file(f'up_to_layer{i + 1}_cumulative', a)

    # Step 3: verify that expected file exists
    expected_file = os.path.join(BASE_DIR, f'up_to_layer{i + 1}_cumulative.tsv')
    print(f"[DEBUG] Expected file: {expected_file}")
    print(f"[DEBUG] Exists after creation: {os.path.exists(expected_file)}")

    # Step 4: if file missing, check alternative paths
    if not os.path.exists(expected_file):
        alt_path = os.path.join(directory, f'up_to_layer{i + 1}_cumulative.tsv')
        print(f"[DEBUG] Checking fallback path: {alt_path}")
        if os.path.exists(alt_path):
            expected_file = alt_path
        else:
            print(f"⚠️ Skipped missing file for layer {i + 1}: {expected_file}")
            return  # safely skip this layer instead of crashing

    # Step 5: extend graph using the verified file
    extend_graph_selective(expected_file, s, graph1, min_int)


def make_n_layer_graph(in_size, n, min_int, input_tsv=input_tsv, out_html=out_html):
    """Main driver called by R through reticulate."""
    print("Building PSD network...")

    # ✅ Ensure we’re using a valid absolute path for input_tsv
    if not os.path.isabs(input_tsv):
        input_path = os.path.join(BASE_DIR, input_tsv)
    else:
        input_path = input_tsv

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    extend_graph_selective(input_path, 35, graph1, 0)

    s = in_size
    for i in range(1, 2):
        Graph_Expansion_one_more_layer(i, s, 3)
        s -= in_size / n
    for i in range(2, 3):
        Graph_Expansion_one_more_layer(i, s, 2)
        s -= in_size / n
    for i in range(3, 4):
        Graph_Expansion_one_more_layer(i, s, 3)
        s -= in_size / n
    for i in range(4, n):
        Graph_Expansion_one_more_layer(i, s, 6)
        s -= in_size / n

    graph.set_options("""
    var options = {"physics":{"enabled":true,"barnesHut":{"springLength":100}}}
    """)

    output_path = os.path.join(BASE_DIR, out_html)

    # === Debug section ===
    print(f"[DEBUG] Attempting to save HTML to: {os.path.abspath(output_path)}")
    print(f"[DEBUG] BASE_DIR = {BASE_DIR}")
    print(f"[DEBUG] Input file: {os.path.abspath(input_path)}")
    print(f"[DEBUG] Graph 1: {len(graph.nodes)} nodes, {len(graph.edges)} edges")
    print(f"[DEBUG] Graph 2: {len(graph1.nodes)} nodes, {len(graph1.edges)} edges")

    # Try writing both graphs
    graph.show(output_path)
    graph1.show(output_path)

    # Confirm result
    exists = os.path.exists(output_path)
    print(f"[DEBUG] File exists after write: {exists}")
    print(f"✅ Finished. Network saved to {output_path if exists else '(not created!)'}")

    return output_path

def find_max_protein():
    max1 = max((len(pr.interactions) for pr in total_proteins), default=0)
    hubs = [pr.name for pr in total_proteins if len(pr.interactions) == max1]
    print("Hub proteins:", hubs)
    print("Max interactions:", max1)
    
# === Run automatically when called from R ===
if __name__ == "__main__":
    make_n_layer_graph(
        in_size=20,
        n=layers,
        min_int=min_int,
        input_tsv=input_tsv,
        out_html=out_html
    )


