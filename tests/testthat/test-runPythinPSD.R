# =========================================================
# Test: runPythonPSD() end-to-end connection
# =========================================================

test_that("Python PSD pipeline runs and generates main.html", {

  skip_if_not_installed("reticulate")
  skip_if_not_installed("PSDExplorer")

  # --- Setup ---
  workdir <- tempdir()  # use a temporary writable directory
  file.copy(
    system.file("extdata", "scaffolds.tsv", package = "PSDExplorer"),
    file.path(workdir, "scaffolds.tsv"),
    overwrite = TRUE
  )

  input_tsv <- file.path(workdir, "scaffolds.tsv")
  expect_true(file.exists(input_tsv))

  # --- Run ---
  message("🔧 Testing Python integration in: ", workdir)

  output_html <- PSDExplorer::runPythonPSD(
    input_tsv = input_tsv,
    layers = 2,
    min_int = 2,
    out_html = "main.html",
    workdir = workdir
  )

  # --- Check output ---
  expect_true(file.exists(output_html),
              info = paste("Expected output file not found:", output_html))

  # --- Clean up ---
  if (file.exists(output_html)) {
    message("✅ Test succeeded: HTML generated at ", normalizePath(output_html))
  } else {
    message("⚠️ Test failed: No HTML generated.")
  }
})
