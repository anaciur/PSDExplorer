#!/usr/bin/env python3
import os

################################################################
## For each protein in the given list print the names of
## their 5 best interaction partners.
##
## Requires requests module:
## type "python -m pip install requests" in command line (win)
## or terminal (mac/linux) to install the module
################################################################


import requests  ## python -m

import delete_after_filename


def is_file_empty(file_name):
    """ Check if file is empty by confirming if its size is 0 bytes"""
    # Check if file exist and it is empty
    return os.path.exists(file_name) and os.path.getsize(file_name) == 0


def delete(file_name):
    import os

    # Check if the file exists
    if os.path.exists(file_name):
        # Delete the file
        os.remove(file_name)


def create_file_if_not_exists(file_name):
    """ Create a file with a header if it does not exist """
    if not os.path.exists(file_name):
        with open(file_name, 'w') as file:
            file.write("#node1\tnode2\tnode1_string_id\tnode2_string_id\tneighborhood_on_chromosome\tgene_fusion\t"
                       "phylogenetic_cooccurrence\thomology\tcoexpression\t"
                       "experimentally_determined_interaction\tdatabase_annotated\tautomated_textmining\t"
                       "combined_score\n")




def get_files_from_list(my_genes):
    #version-11-5.
    string_api_url = "https://string-db.org/api"
    # string_api_url = "https://version-12.string-db.org/api"
    output_format = "tsv-no-header"
    method = "interaction_partners"

    request_url = "/".join([string_api_url, output_format, method])
    ##
    ## Set parameters
    ##

    params = {

        "identifiers": "%0d".join(my_genes),  # your protein
        "species": 9606,  # species NCBI identifier
        "limit": 10,
        "caller_identity": "www.awesome_app.org"  # your app name

    }

    ##
    ## Call STRING
    ##

    response = requests.post(request_url, data=params)

    ##
    ## Read and parse the results
    ##

    for line in response.text.strip().split("\n"):

        l = line.strip().split("\t")
        if len(l) >= 6:
            query_ensp = l[0]
            query_name = l[2]
            partner_ensp = l[1]
            partner_name = l[3]
            combined_score = l[5]
            file_path = f"{query_name}.tsv"
            #delete(file_path)

            # Create the file if it does not exist
            create_file_if_not_exists(file_path)

            with open(file_path, 'a') as new_file:
                # output_string = "\t".join([query_name, partner_name + " " + "0\t" * 9 + "0", combined_score])
                output_string = "\t".join([query_name, partner_name] + ["0"] * 10 + [combined_score])

                # Write the result to the file
                new_file.write(output_string + "\n")

            print("\t".join([query_name, partner_name, combined_score]))
        else:
            print(l)

    ## print


# delete_after_filename.delete_after_name(my_genes)

#get_files_from_list(my_genes1)
