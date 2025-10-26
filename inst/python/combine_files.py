def add_proteins_to_layer(input_file, layer_file):
    with open(input_file, 'r') as file:
        file_content = file.readlines()[1:]
    with open(layer_file, 'a') as file1:
        file1.writelines(file_content)


import os


def search_files(directory, new_file_path):
    with open(new_file_path, 'w') as new_file:
        new_file.write("#node1	node2	node1_string_id	node2_string_id	neighborhood_on_chromosome	gene_fusion	"
                       "phylogenetic_cooccurrence	homology	coexpression	"
                       "experimentally_determined_interaction	database_annotated	automated_textmining	"
                       "combined_score\n")
        # Iterate over all files in the specified directory
        for file in os.listdir(directory):
            # Construct the full file path
            file_path = os.path.join(directory, file)
            # add_proteins_to_layer(file, new_file_path)
            # Check if it's a file and not a directory
            if os.path.isfile(file_path):
                # Open each file for reading
                with open(file_path, 'r') as f:
                    # Read the file content
                    content = f.readlines()[1:]

                    # Write the content to the new file
                    new_file.writelines(content)


# Example usage
search_files('C:\\Users\\User\PycharmProjects\pythonProject5\scaffolds_layer_Proteins_and_their_interactions',
             'scaffolds#.tsv')  # Searching for .txt files
search_files('C:\\Users\\User\PycharmProjects\pythonProject5\\2nd_layer_Proteins_and_their_interactions',
             '2nd_layer#.tsv')  # Searching for .txt files
'''
search_files('C:\\Users\\User\PycharmProjects\pythonProject5\\3rd_layer_Proteins_and_their_interactions',
             '3rd_layer#.tsv')
search_files('C:\\Users\\User\PycharmProjects\pythonProject5\\4th_layer_Proteins_and_their_interactions',
             '4th_layer#.tsv')
search_files('C:\\Users\\User\PycharmProjects\pythonProject5\\5th_layer_Proteins_and_their_interactions',
             '5th_layer#.tsv')
search_files('C:\\Users\\User\PycharmProjects\pythonProject5\\6th_layer_Proteins_and_their_interactions',
             '6th_layer#.tsv')'''

'''
add_proteins_to_layer('QDPR.tsv', '6th_layer.tsv')
add_proteins_to_layer('ASPH.tsv', '6th_layer.tsv')

add_proteins_to_layer('6th_layer_Proteins_and_their_interactions/CACNA1A.tsv', '6th_layer.tsv')
add_proteins_to_layer('6th_layer_Proteins_and_their_interactions/CACNA1D.tsv', '6th_layer.tsv')
add_proteins_to_layer('6th_layer_Proteins_and_their_interactions/CACNA1F.tsv', '6th_layer.tsv')
add_proteins_to_layer('6th_layer_Proteins_and_their_interactions/CACNA1S.tsv', '6th_layer.tsv')
add_proteins_to_layer('CACNA2D1.tsv', '6th_layer.tsv')
add_proteins_to_layer('CACNA2D2.tsv', '6th_layer.tsv')
add_proteins_to_layer('CACNA2D4.tsv', '6th_layer.tsv')
add_proteins_to_layer('CACNB2.tsv', '6th_layer.tsv')
add_proteins_to_layer('CACNB1.tsv', '6th_layer.tsv')
add_proteins_to_layer('CACNB3.tsv', '6th_layer.tsv')
add_proteins_to_layer('CACNG3.tsv', '6th_layer.tsv')
add_proteins_to_layer('TRDN.tsv', '6th_layer.tsv')
add_proteins_to_layer('FKBP1A.tsv', '6th_layer.tsv')
add_proteins_to_layer('FKBP1B.tsv', '6th_layer.tsv')
add_proteins_to_layer('RYR3.tsv', '6th_layer.tsv')
add_proteins_to_layer('CALML5.tsv', '6th_layer.tsv')
add_proteins_to_layer('CALML6.tsv', '6th_layer.tsv')
add_proteins_to_layer('CALM1.tsv', '6th_layer.tsv')
add_proteins_to_layer('HDAC4.tsv', '6th_layer.tsv')
add_proteins_to_layer('HDAC5.tsv', '6th_layer.tsv')
add_proteins_to_layer('MYH11.tsv', '6th_layer.tsv')
add_proteins_to_layer('MYL9.tsv', '6th_layer.tsv')
add_proteins_to_layer('MYL12A.tsv', '6th_layer.tsv')
add_proteins_to_layer('MYL12B.tsv', '6th_layer.tsv')
add_proteins_to_layer('CAMKK1.tsv', '6th_layer.tsv')
add_proteins_to_layer('CREB1.tsv', '6th_layer.tsv')
add_proteins_to_layer('CAV1.tsv', '6th_layer.tsv')
add_proteins_to_layer('HSP90AA1.tsv', '6th_layer.tsv')
add_proteins_to_layer('HSP90AB1.tsv', '6th_layer.tsv')
#add_proteins_to_layer('AKT1.tsv', '6th_layer.tsv')
add_proteins_to_layer('NOSIP.tsv', '6th_layer.tsv')
add_proteins_to_layer('PRKAB1.tsv', '6th_layer.tsv')
add_proteins_to_layer('PRKAB2.tsv', '6th_layer.tsv')
add_proteins_to_layer('PRKAG1.tsv', '6th_layer.tsv')
add_proteins_to_layer('PRKAG2.tsv', '6th_layer.tsv')
add_proteins_to_layer('PRKAA2.tsv', '6th_layer.tsv')
add_proteins_to_layer('CNTNAP2.tsv', '6th_layer.tsv')
#add_proteins_to_layer('ADAM23.tsv', '6th_layer.tsv')
add_proteins_to_layer('ADAM28.tsv', '6th_layer.tsv')
add_proteins_to_layer('LGI1.tsv', '6th_layer.tsv')
add_proteins_to_layer('LGI2.tsv', '6th_layer.tsv')
add_proteins_to_layer('LGI3.tsv', '6th_layer.tsv')
add_proteins_to_layer('LGI4.tsv', '6th_layer.tsv')

add_proteins_to_layer('TH.tsv', '7th_layer.tsv')

add_proteins_to_layer('SNCA.tsv', '8th_layer.tsv')
'''
