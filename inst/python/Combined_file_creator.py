#!/usr/bin/env python3

##################################################################
## For the given list of proteins print out only the interactions
## between these protein which have medium or higher confidence
## experimental score
##
## Requires requests module:
## type "python -m pip install requests" in command line (win)
## or terminal (mac/linux) to install the module
##################################################################

import requests  ## python -m pip install requests

from get_files1 import create_file_if_not_exists
#from main import n_l

#my_genes = n_l.nested_list[0]


def Create_combined_interactions_file(up_to_layer_i, my_genes):
    string_api_url = "https://string-db.org/api"
    output_format = "tsv-no-header"
    method = "network"

    ##
    ## Construct URL
    ##

    request_url = "/".join([string_api_url, output_format, method])

    ##
    ## Set parameters
    ##

    params = {

        "identifiers": "%0d".join(my_genes),  # your protein
        "species": 9606,  # species NCBI identifier
        "caller_identity": "www.awesome_app.org"  # your app name

    }

    ##
    ## Call STRING
    ##

    response = requests.post(request_url, data=params)

    for line in response.text.strip().split("\n"):

        l = line.strip().split("\t")
        if len(l) >= 6:
            query_ensp = l[0]
            query_name = l[2]
            partner_ensp = l[1]
            partner_name = l[3]
            combined_score = l[5]
            file_path = f"{up_to_layer_i}.tsv"

            # Create the file if it does not exist
            create_file_if_not_exists(file_path)

            with open(file_path, 'a') as new_file:
                # output_string = "\t".join([query_name, partner_name + " " + "0\t" * 9 + "0", combined_score])
                output_string = "\t".join([query_name, partner_name] + ["0"] * 10 + [combined_score])

                # Write the result to the file
                new_file.write(output_string + "\n")

            #print("\t".join([query_name, partner_name, combined_score]))




#Create_combined_interactions_file('up_to_layer_none', my_genes)
