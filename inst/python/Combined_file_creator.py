#!/usr/bin/env python3
import requests
from pathlib import Path
from get_files1 import create_file_if_not_exists

# Folder where this file lives (your package's python dir)
BASE_DIR = Path(__file__).resolve().parent


def _deep_flatten_to_str(x):
    """
    Recursively flatten *anything* (lists/tuples of lists/tuples/strings)
    and return a flat list of strings.
    """
    flat = []
    if isinstance(x, (list, tuple, set)):
        for item in x:
            flat.extend(_deep_flatten_to_str(item))
    else:
        # force to string so join() never sees a non-string
        flat.append(str(x))
    return flat


def Create_combined_interactions_file(up_to_layer_i, my_genes):
    """
    Given a protein list (possibly nested), fetch STRING interactions and
    write them to <BASE_DIR>/<up_to_layer_i>.tsv
    """
    # 1) make sure it's flat strings
    flat_genes = _deep_flatten_to_str(my_genes)
    print(f"[DEBUG] Create_combined_interactions_file got genes: {flat_genes}")

    # 2) if nothing to query, just create an empty file and return
    if not flat_genes:
        output_path = BASE_DIR / f"{up_to_layer_i}.tsv"
        create_file_if_not_exists(output_path)
        print(f"[INFO] Gene list was empty, created empty file at: {output_path}")
        return output_path

    # 3) build request to STRING
    string_api_url = "https://string-db.org/api"
    output_format = "tsv-no-header"
    method = "network"
    request_url = "/".join([string_api_url, output_format, method])

    params = {
        # this is now guaranteed to be a list of strings
        "identifiers": "%0d".join(flat_genes),
        "species": 9606,          # human
        "caller_identity": "PSDExplorer",
    }

    # 4) prepare output
    #output_path = BASE_DIR / f"{up_to_layer_i}.tsv"
    output_path = Path.cwd() / f"{up_to_layer_i}.tsv"
    create_file_if_not_exists(output_path)
    print(f"[INFO] Writing interactions to: {output_path}")

    # 5) call STRING
    try:
        resp = requests.post(request_url, data=params)
        resp.raise_for_status()
    except Exception as e:
        print(f"[ERROR] STRING request failed: {e}")
        return output_path

    # 6) write results
    for line in resp.text.strip().split("\n"):
        parts = line.strip().split("\t")
        if len(parts) >= 6:
            query_name = parts[2]
            partner_name = parts[3]
            combined_score = parts[5]

            with open(output_path, "a", encoding="utf-8") as f:
                # match your previous format: 2 ids, 10 zeros, score
                row = "\t".join(
                    [query_name, partner_name] + ["0"] * 10 + [combined_score]
                )
                f.write(row + "\n")

    print(f"[INFO] ✅ Wrote combined file: {output_path}")
    return output_path
