#' Load and validate PSD interaction data
#'
#' @description
#' Loads the scaffold interaction data (TSV format) used by the Python engine.
#' This function checks that the file exists, validates its format, and returns
#' the interaction table as a data frame for downstream R analysis.
#'
#' @param file Path to the TSV file (default: "scaffolds.tsv").
#' @return A data frame containing the interaction network.
#' @examples
#' \dontrun{
#' psd_data <- loadPSD("scaffolds.tsv")
#' head(psd_data)
#' }
#' @export
loadPSD <- function(file = system.file("python", "scaffolds.tsv", package = "PSDExplorer")) {
  if (!file.exists(file)) {
    stop("Interaction file not found: ", file)
  }

  message("Loading PSD interactions from: ", file)
  data <- read.delim(file, header = TRUE, sep = "\t", stringsAsFactors = FALSE)

  required_cols <- c("protein1", "protein2", "combined_score")
  if (!all(required_cols %in% names(data))) {
    warning("Missing expected columns in the interaction file. Columns found: ",
            paste(names(data), collapse = ", "))
  }

  return(data)
}
