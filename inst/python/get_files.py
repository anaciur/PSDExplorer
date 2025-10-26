import argparse


from stringdb import STRINGdb


def get_protein_interactions(version, species, score_threshold, protein_list, limit):
    string_db = STRINGdb(version=version, species=species, score_threshold=score_threshold)
    #string_db = STRINGdb()
    # protein_list = ["GNAQ"]
    for protein_name in protein_list:
        protein_id = string_db.get_string_id([protein_name])
        protein_interactions = string_db.get_interactions(protein_id, limit=limit)
        with open(f"{protein_name}.tsv", "w") as f:
            f.write(protein_interactions.to_csv(sep="\t", index=False))


'''string_db = STRINGdb(version="11.5", species=9606, score_threshold=200, network_type="full", input_directory="")
protein_list = ["protein1", "protein2"]
for protein in protein_list:
    interactions = string_db.get_interactions(protein)
    with open(f"{protein}.tsv", "w") as f:
        f.write(interactions.to_csv(sep="\t", index=False))'''


def main():
    parser = argparse.ArgumentParser(description="Retrieve protein interactions from STRINGdb and save to a file.")
    parser.add_argument("--version", type=str, default="12.0", help="STRINGdb version")
    parser.add_argument("--species", type=int, default=9606, help="Species ID")
    parser.add_argument("--score_threshold", type=int, default=400, help="Score threshold")
    parser.add_argument("--limit", type=int, default=10, help="Limit interactions")
    parser.add_argument("protein_list", nargs="*", help="List of protein names")

    args = parser.parse_args()
    #args.protein_list = ["ADORA2A"]
    get_protein_interactions(args.version, args.species, args.score_threshold, args.protein_list, args.limit)


if __name__ == "__main__":
    main()
