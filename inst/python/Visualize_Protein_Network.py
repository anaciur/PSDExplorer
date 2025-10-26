from pyvis.network import Network
from File_processor import InteractionProcessor
import random

from Protein_attributes import Protein
import random


def generate_random_color():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    return red, green, blue


def rgb_to_hex(red, green, blue):
    return "#{:02X}{:02X}{:02X}".format(red, green, blue)


# Example usage
random_color = generate_random_color()
hex_color = rgb_to_hex(*random_color)
#print(hex_color)


class NetworkVisualizer:
    def __init__(self, proteins):

        self.proteins = proteins
        self.network = Network(notebook=True, cdn_resources="remote", height="600px", width="100%", bgcolor="#ffffff",
                               font_color="black")

    def visualize_network(self):
        # Add nodes to the network
        for protein in self.proteins:
            self.network.add_node(protein.name, label=protein.name, color=Color.generate_random_color)

        # Add edges to the network
        for protein in self.proteins:
            for neighbor, likelihood in protein.interactions.items():
                self.network.add_edge(protein.name, neighbor.name, value=likelihood)

        # Visualize the network
        self.network.set_options(
            """
            var options = {
                "physics": {
                    "enabled": true,
                    "barnesHut": {
                        "springLength": 100
                    }
                }
            }
            """
        )
        self.network.show('Visualize_Protein_Network.html')
