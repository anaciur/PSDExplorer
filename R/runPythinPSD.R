#' Run the Python-based PSD network generator
#'
#' @description
#' This function initializes the Python environment (via reticulate),
#' locates and runs the embedded Python script (`main.py`) directly,
#' executing the flexible postsynaptic density (PSD) mapping pipeline
#' with the specified number of layers and interaction thresholds.
#'
#' @param input_tsv Path to the TSV file containing scaffold protein interactions.
#'        Defaults to "scaffolds.tsv" (which should exist in the package's Python directory).
#' @param layers Integer, number of layers to expand (default = 3).
#' @param min_int Minimum number of interactions required for inclusion in each layer (default = 2).
#' @param out_html Name of the HTML output file (default = "main.html").
#'
#' @return The path to the generated HTML file.
#' @export
#'
#' @examples
#' \dontrun{
#' runPythonPSD(layers = 3, min_int = 2)
#' }
runPythonPSD <- function(input_tsv = "scaffolds.tsv",
                         layers = 3,
                         min_int = 2,
                         out_html = "main.html") {

  message("Initializing Python environment...")

  # Locate package's embedded Python folder
  py_dir <- system.file("python", package = "PSDExplorer")
  input_path <- file.path(py_dir, basename(input_tsv))
  main_file  <- file.path(py_dir, "main.py")

  # Check that key files exist
  if (!file.exists(main_file)) {
    stop(paste0("❌ main.py not found at: ", main_file))
  }
  if (!file.exists(input_path)) {
    stop(paste0("❌ Input file not found at: ", input_path))
  }

  # Activate or create Python environment
  reticulate::use_miniconda("psd_env", required = TRUE)

  # Print confirmation for debugging
  message("📂 Running Python script: ", main_file)
  message("📂 Using input file: ", input_path)

  # Set environment variables to pass parameters into Python
  Sys.setenv(PSD_LAYERS = layers,
             PSD_MIN_INT = min_int,
             PSD_INPUT   = input_path,
             PSD_OUT     = file.path(py_dir, out_html))

  # Execute the Python script directly
  reticulate::py_run_file(main_file)

  # Path to output file
  output_path <- file.path(py_dir, out_html)
  message("✅ Finished. Network saved to: ", output_path)

  # 👉 Automatically open the HTML file in your default browser
  if (file.exists(output_path)) {
    browseURL(output_path)
  }

  invisible(output_path)
}
