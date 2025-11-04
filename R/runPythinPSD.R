#' Run the Python-based PSD network generator
#'
#' @description
#' Initializes the Python environment (via reticulate),
#' locates and runs the embedded Python script (`main.py`),
#' and executes the flexible postsynaptic density (PSD) mapping pipeline.
#' This version automatically detects or sets a writable working directory
#' where all intermediate TSVs and HTML outputs are stored.
#'
#' @param input_tsv Path to the TSV file containing scaffold protein interactions.
#'        Defaults to "scaffolds.tsv" (must exist in your project folder).
#' @param layers Integer, number of layers to expand (default = 3).
#' @param min_int Minimum number of interactions required for inclusion in each layer (default = 2).
#' @param out_html Name of the HTML output file (default = "main.html").
#' @param workdir Optional path to your writable project directory.
#'        Defaults to "C:/Users/User/PycharmProjects/pythonProject5".
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
                         out_html = "main.html",
                         workdir = "C:/Users/User/PycharmProjects/pythonProject5") {

  message("Initializing Python environment...")

  # Path to Python code inside the package
  py_dir <- system.file("python", package = "PSDExplorer")
  main_file <- file.path(py_dir, "main.py")

  if (!file.exists(main_file)) {
    stop(paste0("❌ main.py not found at: ", main_file))
  }

  # Verify working directory
  if (!dir.exists(workdir)) {
    stop(paste0("❌ Working directory not found: ", workdir))
  }
  message("📂 Using working directory: ", workdir)

  # Check input TSV in the working directory
  input_path <- file.path(workdir, basename(input_tsv))
  if (!file.exists(input_path)) {
    stop(paste0("❌ Input file not found at: ", input_path))
  }

  # Activate Python env
  reticulate::use_miniconda("psd_env", required = TRUE)

  # Pass environment variables to Python
  Sys.setenv(
    PSD_LAYERS = layers,
    PSD_MIN_INT = min_int,
    PSD_INPUT = input_path,
    PSD_OUT = file.path(workdir, out_html),
    PSD_WORKDIR = workdir
  )

  # Run main.py directly
  message("🚀 Running Python script: ", main_file)
  reticulate::py_run_file(main_file)

  output_path <- file.path(workdir, out_html)
  if (file.exists(output_path)) {
    message("✅ Finished. Network saved to: ", output_path)
  } else {
    message("⚠️ Python ran successfully but no output HTML was found.")
  }

  invisible(output_path)
}
