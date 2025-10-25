
# PSDExplorer

### Description

**PSDExplorer** is an R package for **layer-based exploration** of
protein–protein interaction networks within the **postsynaptic density
(PSD)**.  
It extends a Python engine that builds multi-layer interaction networks
from TSV files and renders interactive HTML graphs via **PyVis**.  
This R interface adds reproducibility, cluster detection, GO enrichment,
and a more user-friendly analysis flow.

The package’s novelty lies in its **iterative expansion** mechanism —
users can input seed PSD proteins (e.g., scaffolds), and the network
expands layer by layer, with each new layer including only proteins that
meet a **minimum shared interaction threshold** with proteins in the
previous layer.  
This reveals the hierarchical organization of the PSD, bridging
structural and functional connectivity.

*Developed on:*  
\`\`\`r utils::sessionInfo()$R.version$version.string

Installation

To install the latest version of the package:

install.packages(“devtools”) library(devtools)
devtools::install_github(“anaciur/PSDExplorer”, build_vignettes = TRUE)
library(PSDExplorer)

To run the shinyApp: Under construction. Overview
ls(“package:PSDExplorer”) \# data(package = “PSDExplorer”) \# optional
\# browseVignettes(“PSDExplorer”)

Function Purpose loadPSD() Load and preprocess PSD protein–protein
interaction data. detectClusters() Identify densely connected modules
(e.g., Louvain/Infomap via igraph). identifyHubs() Detect hub proteins
and compute degree distributions. runGOenrichment() Perform GO
enrichment on clusters or subnetworks (clusterProfiler). summaryStats()
Summarize network metrics (degree, modularity, clustering coefficient).
plotPSDnetwork() Interactive visualization of PSD networks via
visNetwork. launchApp() Launch the integrated Shiny interface (to be
added after peer review).

Python Engine (wrapped)

Core of the backend: The Python engine constructs and expands
protein–protein interaction networks using the following logic:

Input files: TSV tables (e.g., scaffolds.tsv, up_to_layer_2.tsv), where
each row represents an interaction and its confidence score.

Modules used:

File_processor.InteractionProcessor — parses TSV files and builds
protein objects with .name and .interactions.

Visualize_Protein_Network — defines network visualization and color
functions (generate_random_color, rgb_to_hex).

Nested_list_of_layers.NestedList — maintains nested lists of proteins
per layer.

List_Creator & Combined_file_creator — manage creation of new layers and
cumulative interaction files.

Visualization: Interactive HTML outputs generated using PyVis
(graph.show(“main.html”)).

Layer-based Selective Logic

The expansion algorithm iteratively adds proteins based on shared
interactions with the previous layer:

Layer 0: seed proteins (e.g., scaffolds).

Layer 1+: candidate protein is added if it shares ≥ min_nb_of_int
interactions with proteins in the previous layer.

Selective expansion: deeper layers use higher thresholds to keep
specificity.

Visualization: node size decreases with each layer (s = s - in_size /
n).

Example Python functions corresponding to this logic:

extend_graph_selective() — adds new nodes and edges to the graph.

create_nested_list_of_layers_selective() — updates the nested structure
of layers.

Graph_Expansion_one_more_layer() — adds one additional layer to the
cumulative network.

make_n_layer_graph() — automates multi-layer growth.

find_max_protein() — prints hub proteins with the highest degree.

Planned R–Python Bridge (user-transparent)

The R side will call your Python engine using reticulate, but end users
will not need to install Python manually. Example planned interface:

\#’ Expand PSD network using the Python engine \#’ @param seeds
character vector of seed proteins or path to TSV file \#’ @param layers
integer, number of expansion layers \#’ @param min_int integer, minimum
shared interaction threshold \#’ @return list with nodes, edges, nested
layers, and HTML output \#’ @export expand_psd \<- function(seeds,
layers = 3, min_int = 2) { \# reticulate::use_miniconda(“psd_env”,
required = TRUE) \# reticulate::py_install(c(“pyvis”, “pandas”), envname
= “psd_env”) \# psd_mod \<- reticulate::import(“your_python_entrypoint”)
\# psd_mod\$make_n_layer_graph(…) \# return(list(…)) }

Contributions

Author: Ana Ciur

Aspect Contribution Core idea PSDExplorer design, biological rationale,
and R package architecture Python Developed underlying simulation engine
(InteractionProcessor, NestedList, NetworkVisualizer, etc.) R Network
analysis (igraph), enrichment (clusterProfiler), and visualization
(visNetwork) AI tools Used for phrasing, documentation structure, and
style consistency only References

Csardi, G. & Nepusz, T. (2006). The igraph software package for complex
network research.

Yu, G. et al. (2012). clusterProfiler: an R package for comparing
biological themes among gene clusters.

Almende, B. et al. (2019). visNetwork: Interactive Network Visualization
for R.

PyVis: <https://pyvis.readthedocs.io>

Acknowledgements

This package was developed as part of an assessment for 2025 BCB410H:
Applied Bioinformatics at the University of Toronto, Canada. PSDExplorer
welcomes issues, enhancement requests, and other contributions. Submit
issues via GitHub Issues .

Other Topics

Planned Extensions:

Implement the reticulate bridge (automatic environment creation, no
manual Python setup).

Add Shiny-based network viewer for adjustable layer expansion and
enrichment previews.
