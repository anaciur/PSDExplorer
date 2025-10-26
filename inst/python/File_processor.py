from Protein_attributes import Protein

import csv
from pyvis.network import Network


class InteractionProcessor:
    def __init__(self, file1):
        # self.file_path = file_path

        # the proteins that are going to be added from the file
        # object list
        self.file1 = file1
        self.total_proteins = []
        self.protein_name_list = []

        # the dictionary of protein interactions that is going to be formed
        # string dictionary
        self.interactions = {}

    def read_interaction_data(self):

        # read through the file_path and create a string dictionary of protein interactions
        # string dictionary
        interactions_data = {}
        with open(self.file1, 'r') as file:
            csv_reader = csv.reader(file, delimiter='\t')
            first_row = next(csv_reader)
            for line in csv_reader:
                two_proteins = tuple(line[:2])
                interaction_values = [float(val) for val in line[4:]]
                interactions_data[two_proteins] = {'combined_score': interaction_values[8]}
        return interactions_data

    def add_to_existent_proteins(self):

        # add proteins to self.total_proteins
        # add their names to the self.protein_name_list

        # this can be done with the initial file of later on, to update the map
        # this is to be done AFTER self.interactions has been updated

        for pair in self.interactions:
            if self.interactions[pair]['combined_score'] > 0.95:
                for protein_name in pair:
                    if protein_name not in self.protein_name_list:
                        self.protein_name_list.append(protein_name)
                        self.total_proteins.append(Protein(protein_name))

    def process_interactions(self):

        # read the string dictionary created from the file_path info and update self.interactions accordingly
        self.interactions.update(self.read_interaction_data())

        # convert the string interaction data to actual Protein identities
        # and add them to the self.total_proteins list and self.protein_name_list
        self.add_to_existent_proteins()

        # create Protein class interactions depending on the desired likelihood
        for pair in self.interactions:
            if self.interactions[pair]['combined_score'] > 0.95:
                protein0 = next((protein for protein in self.total_proteins if protein.name == pair[0]), None)
                protein1 = next((protein for protein in self.total_proteins if protein.name == pair[1]), None)

                if protein0 and protein1:
                    protein0.add_interaction(protein1, self.interactions[pair]['combined_score'])
                    protein1.add_interaction(protein0, self.interactions[pair]['combined_score'])



