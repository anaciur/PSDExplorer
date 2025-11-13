#!/usr/bin/env python3
import os
from pathlib import Path
import shutil
from pyvis.network import Network

import Combined_file_creator
import List_Creator
import delete_after_filename
from Combined_file_creator import Create_combined_interactions_file
from Nested_list_of_layers import NestedList
from Visualize_Protein_Network import NetworkVisualizer, generate_random_color, rgb_to_hex
from File_processor import InteractionProcessor


# =========================================================
# === RESET STALE OR INVALID ENVIRONMENT VARIABLES =========
# =========================================================
def clean_env_var(var_name):
    """Unset variable if missing, empty, or invalid."""
    val = os.getenv(var_name)
    if not val or val.strip().lower() in ["none", "na", "null"]:
        if var_name in os.environ:
            del os.environ[var_name]

# Clean all key PSD vars before use
for var in ["PSD_LAYERS", "PSD_MIN_INT", "PSD_LAYER_MIN_INTS", "PSD_INPUT", "PSD_OUT", "PSD_WORK_DIR"]:
    clean_env_var(var)


# =========================================================
# === DEBUG ENVIRONMENT & PATHS ============================
# =========================================================
print("========== PYTHON ENV DEBUG ==========")
for k in ["PSD_OUT", "PSD_WORK_DIR", "PSD_LAYERS", "PSD_LAYER_MIN_INTS"]:
    print(f"{k} =", os.getenv(k))
print("======================================")


# =========================================================
# === WORKING DIRECTORY & PARAMETERS =======================
# =========================================================
# Fallback if R didn't set values properly
if not os.getenv("PSD_OUT"):
    os.environ["PSD_OUT"] = str(Path.cwd() / "main.html")
if not os.getenv("PSD_WORK_DIR"):
    os.environ["PSD_WORK_DIR"] = str(Path.cwd())

# Resolve paths
BASE_WORK_DIR = Path(os.getenv("PSD_WORK_DIR")).resolve()
os.makedirs(BASE_WORK_DIR, exist_ok=True)
os.chdir(BASE_WORK_DIR)

PSD_OUT = Path(os.getenv("PSD_OUT")).resolve()
BASE_DIR = PSD_OUT.parent
extension = ".tsv"

print(f"[DEBUG] Working directory set to: {BASE_WORK_DIR}")
print(f"[DEBUG] Output will be saved to: {PSD_OUT}")
print(f"[DEBUG] Base directory for outputs: {BASE_DIR}")


# =========================================================
# === CLEAN OLD RUN FILES =================================
# =========================================================
print("[CLEANUP] Removing old directories and TSVs from previous runs...")
for item in BASE_WORK_DIR.iterdir():
    try:
        if item.is_dir() and item.name.startswith("directory"):
            shutil.rmtree(item, ignore_errors=True)
        elif item.is_file() and item.name.startswith("up_to_layer") and item.suffix == ".tsv":
            item.unlink()
    except Exception as e:
        print(f"[CLEANUP] ⚠️ Could not remove {item}: {e}")
print("[CLEANUP] ✅ Done.")

# =========================================================
# === PARAMETERS FROM R ====================================
# =========================================================
layers_env = os.getenv("PSD_LAYERS")
if not layers_env or not layers_env.strip().isdigit():
    raise ValueError("[ERROR] PSD_LAYERS not provided or invalid. Make sure R passes it correctly.")
layers = int(layers_env)

input_tsv = os.getenv("PSD_INPUT", "scaffolds.tsv")

# Read layer thresholds passed by R (once only)
layer_thresholds_env = os.getenv("PSD_LAYER_MIN_INTS", "")
min_int_per_layer = [int(x) for x in layer_thresholds_env.split(",") if x.strip().isdigit()] if layer_thresholds_env else []
print(f"[INFO] Using per-layer thresholds: {min_int_per_layer}")


# =========================================================
# === INITIALIZE GRAPHS & GLOBALS ==========================
# =========================================================
graph = Network(notebook=True, cdn_resources="remote",
                height="600px", width="100%", bgcolor="#ffffff", font_color="black")
graph1 = Network(notebook=True, cdn_resources="remote",
                 height="600px", width="100%", bgcolor="#ffffff", font_color="black")

total_proteins = []
total_proteins_nested_list = []
total_proteins_nested_list_selective = []
n_l = NestedList([])


# =========================================================
# === CORE FUNCTIONS =======================================
# =========================================================
def is_in_list_of_lists(input_list, pr):
    """Check if a protein already exists within a list of lists."""
    return any(item.name == pr.name for lt in input_list for item in lt)


def create_nested_list_of_layers(file_path):
    """Build nested protein list structure for given file path."""
    A = total_proteins_nested_list
    sublist = []
    interaction_processor = InteractionProcessor(file_path)
    interaction_processor.process_interactions()
    new_A = interaction_processor.total_proteins

    for protein in new_A:
        if not any(p.name == protein.name for l in A for p in l):
            sublist.append(protein)
    A.append(sublist)


def create_nested_list_of_layers_selective(file_path, min_nb_of_int):
    """Selectively add proteins with minimum number of interactions."""
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

        if add and not is_in_list_of_lists(A, protein):
            sublist.append(protein)

    A.append(sublist)


def extend_graph_selective(file_path, s, Graph, nb_of_min_int, color=None):
    """Extend the PyVis graph based on interaction files."""
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


def Graph_Expansion_one_more_layer(i, s, min_int):
    """Expand graph by one layer and update interaction files."""
    if not total_proteins_nested_list_selective:
        raise IndexError(
            f"[ERROR] No data found in total_proteins_nested_list_selective before layer {i}. "
            f"Ensure scaffold data '{input_tsv}' was loaded properly."
        )

    last_list = [pr.name for pr in total_proteins_nested_list_selective[-1]]
    directory = os.path.join(BASE_DIR, f"directory{i}")
    os.makedirs(directory, exist_ok=True)
    print(f"[DEBUG] Expanding to layer {i} | Output dir: {directory}")

    a = List_Creator.Update_List_using_last_layer_interactions(
        last_list, BASE_DIR, extension, directory, f"up_to_layer_{i + 1}.tsv", n_l
    )
    Combined_file_creator.Create_combined_interactions_file(
        f"up_to_layer{i + 1}_cumulative", a
    )
    extend_graph_selective(str(BASE_DIR / f"up_to_layer{i + 1}_cumulative.tsv"), s, graph1, min_int)


# =========================================================
# === BUILD INITIAL SCAFFOLD LAYER =========================
# =========================================================
print("[INFO] Building base scaffolds (Layer 0)...")

if not os.path.isabs(input_tsv):
    input_path = os.path.join(BASE_DIR, input_tsv)
else:
    input_path = input_tsv

if not os.path.exists(input_path):
    raise FileNotFoundError(f"Input file not found: {input_path}")

extend_graph_selective(input_path, 35, graph1, 0)
print("[INFO] ✅ Scaffolds layer built and registered as Layer 0.")


# =========================================================
# === MAIN GRAPH GENERATION ================================
# =========================================================
def make_n_layer_graph(in_size, n, min_int_per_layer):
    """Generate an n-layer PSD network and save it as HTML."""
    s = in_size
    print(f"[INFO] Generating {n} layers with thresholds: {min_int_per_layer}")

    for i in range(1, n + 1):
        if len(min_int_per_layer) == 0:
            threshold = 2  # fallback if R somehow failed again
        elif i - 1 < len(min_int_per_layer):
            threshold = min_int_per_layer[i - 1]
        else:
            threshold = min_int_per_layer[-1]

        print(f"[LAYER {i}] Using min interactions: {threshold}")
        Graph_Expansion_one_more_layer(i, s, threshold)
        s -= in_size / n

    graph.set_options("""
    var options = {"physics":{"enabled":true,"barnesHut":{"springLength":100}}}
    """)
    graph.show(str(PSD_OUT))
    graph1.show(str(PSD_OUT))
    print(f"[INFO] ✅ Graph saved to: {PSD_OUT}")
    return str(PSD_OUT)


# =========================================================
# === EXECUTE WHEN CALLED FROM R ===========================
# =========================================================
if __name__ == "__main__":
    make_n_layer_graph(20, layers, min_int_per_layer)
