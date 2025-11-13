#' Run the Python-based PSD network generator
#'
#' @description
#' Initializes Python (via reticulate), runs `main.py`, and opens the resulting HTML network.
#'
#' @param input_tsv  Path to the scaffold protein TSV file (default = "scaffolds.tsv").
#' @param out_html   Name or path of the output HTML file (default = "main.html").
#' @param workdir    Directory where outputs and intermediate files are stored.
#'                   Defaults to the current working directory.
#' @param open_html  Logical; whether to automatically open the HTML after creation (default = TRUE).
#'
#' @return The path to the generated HTML file.
#' @export
#'
#' @examples
#' \dontrun{
#' runPythonPSD()
#' }

runPythonPSD <- function(input_tsv = "scaffolds.tsv",
                         out_html = "main.html",
                         workdir = getwd(),
                         open_html = TRUE) {

  message("Initializing Python environment...")

  # --- 🔄 Clear old environment variables ---
  Sys.unsetenv(c("PSD_LAYERS", "PSD_MIN_INT", "PSD_LAYER_MIN_INTS",
                 "PSD_INPUT", "PSD_OUT", "PSD_WORK_DIR"))

  # Locate Python script within the installed package
  py_dir <- system.file("python", package = "PSDExplorer")
  main_file <- file.path(py_dir, "main.py")

  if (!file.exists(main_file))
    stop(paste0("❌ main.py not found at: ", main_file))

  if (!dir.exists(workdir))
    stop(paste0("❌ Working directory not found: ", workdir))

  message("📂 Using working directory: ", workdir)

  # Input TSV
  input_path <- file.path(workdir, basename(input_tsv))
  if (!file.exists(input_path))
    stop(paste0("❌ Input file not found at: ", input_path))

  # === Ask user for number of layers and thresholds ===
  layers <- NA
  while (is.na(layers) || layers <= 0) {
    layers_input <- readline("Enter the number of layers to expand: ")
    if (grepl("^[0-9]+$", layers_input)) {
      layers <- as.integer(layers_input)
    } else {
      cat("❌ Please enter a valid positive integer for layers.\n")
    }
  }

  repeat {
    min_int_input <- readline(
      paste0("Enter the minimum number of interactions required for each of the ",
             layers, " layers (comma-separated, e.g., 3,2,4):\n→ ")
    )
    if (grepl("^[0-9, ]+$", min_int_input)) break
    cat("❌ Please enter valid comma-separated numbers.\n")
  }

  # Normalize paths
  normalized_out <- normalizePath(file.path(workdir, out_html), winslash = "/", mustWork = FALSE)
  normalized_workdir <- normalizePath(workdir, winslash = "/", mustWork = FALSE)

  message("🧭 R is telling Python to write HTML to: ", normalized_out)

  # Activate Python environment
  reticulate::use_miniconda("psd_env", required = TRUE)

  # --- Inject environment variables directly into Python (no indentation errors) ---
  py_code <- sprintf(
    "import os; os.environ['PSD_LAYERS'] = '%s'; os.environ['PSD_LAYER_MIN_INTS'] = '%s'; os.environ['PSD_INPUT'] = r'%s'; os.environ['PSD_OUT'] = r'%s'; os.environ['PSD_WORK_DIR'] = r'%s'; print('[DEBUG from R] PSD_LAYER_MIN_INTS set to:', os.getenv('PSD_LAYER_MIN_INTS'))",
    layers, gsub(' ', '', min_int_input), input_path, normalized_out, normalized_workdir
  )
  reticulate::py_run_string(py_code)

  # --- Run the main Python file ---
  message("🚀 Running Python script: ", main_file)
  reticulate::py_run_file(main_file)

  # --- Verify output ---
  if (file.exists(normalized_out)) {
    message("✅ Finished. Network saved to: ", normalized_out)
    if (open_html) {
      message("🌐 Opening network in your default browser...")
      utils::browseURL(normalized_out)
    }
  } else {
    message("⚠️ Python ran successfully but no output HTML was found at: ", normalized_out)
  }

  invisible(normalized_out)
}
