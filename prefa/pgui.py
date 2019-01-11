from prefa import nfa, ere
import networkx as nx
import matplotlib.pyplot as plt
# import dfa, nfa, ere

class FADrawer(object):
    """Class which serves displaying of Finite Automatas.

    Wraps the `NetworkX` package and thus provides a really clean and pretty
    way of drawing, simulating and displaying automatas.

    Attributes:
        state_list - list, the nodes list
        trans_dict - dict, the edges dict
        Graph      - nx.MultiDiGraph, `NetworkX` multi-directed graph
    """

    def __init__(self, input_fa):
        self.state_list = [(s, {'role': input_fa.getRole(s)}) \
                            for s in input_fa.states]
        self.trans_dict = dict([(s1, dict([(s2, [])      \
                            for s2 in input_fa.states])) \
                            for s1 in input_fa.states])
        for s in input_fa.states:
            for a in input_fa.alphabet:
                for s_end in input_fa.table[s][a]:
                    self.trans_dict[s][s_end].append(a)
        trans_list = []
        for s1 in self.trans_dict:
            for s2 in self.trans_dict[s1]:
                if len(self.trans_dict[s1][s2]) > 0:
                    trans_list.append((s1, s2,
                                      {'syms': self.trans_dict[s1][s2]}))
        self.Graph = nx.DiGraph()  # Use directed graph.
        self.Graph.add_nodes_from(self.state_list)
        self.Graph.add_edges_from(trans_list)
        self.initial = input_fa.initial
        self.acceptings = input_fa.acceptings
        self.normals = [s for s in input_fa.states if s != self.initial \
                          and s not in self.acceptings]

    def staticShow(self):
        """Plot the structure of a Finite Automata.
        
        Plot the structure of the Finite Automata statically. Uses `NetworkX`
        tools and the "Kamada Kawai" force-directed layout algorithm to
        arrange the layout.
        """

        def boreStr(l):
            """Clean string representations for a list.

            Re formatts the input list into a clean string of its elements.

            Args:
                l - list, the list to re-format

            Returns:
                output_str - str, the re-formatted string
            """
            output_str = ''
            for element in l:
                output_str += str(element) + ','
            if output_str.endswith(','):
                output_str = output_str[:-1].strip()
            return output_str

        # `NetworkX` package is really powerful!
        plt.figure(figsize=(16, 9))
        nx.draw_networkx_nodes(self.Graph, nodelist=self.normals,
                               pos=nx.kamada_kawai_layout(self.Graph),
                               node_size=700, node_color='#ffffff',
                               edgecolors='#000000')
        nx.draw_networkx_nodes(self.Graph, nodelist=[self.initial],
                               pos=nx.kamada_kawai_layout(self.Graph),
                               node_size=700, node_color='#f0f0f0',
                               edgecolors='#bbbbbb')
        nx.draw_networkx_nodes(self.Graph, nodelist=self.acceptings,
                               pos=nx.kamada_kawai_layout(self.Graph),
                               node_size=800, node_color='#ffffff',
                               edgecolors='#000000', linewidths=3)
        nx.draw_networkx_labels(self.Graph,
                                pos=nx.kamada_kawai_layout(self.Graph))
        nx.draw_networkx_edges(self.Graph, arrowstyle='-|>', arrowsize=20,
                               pos=nx.kamada_kawai_layout(self.Graph),
                               width=0.9, edge_color='#000000')
        pos_dict = nx.draw_networkx_edge_labels(self.Graph, font_size=13,
                        label_pos=0.38, pos=nx.kamada_kawai_layout(self.Graph))
        for edge in pos_dict:   # Tune properties for edge labels.
            pos_dict[edge].set_text(boreStr(self.trans_dict[edge[0]][edge[1]]))
            pos_dict[edge].set_rotation(pos_dict[edge].get_rotation()-93)
        plt.axis('off')
        plt.show()

if __name__ == '__main__':
    my_nfa = nfa.NFiniteAutomata(ere.Regex('(a|~)*b*a|ba'))
    FADrawer(my_nfa).staticShow()

    my_dfa = dfa.DFiniteAutomata(my_nfa)
    FADrawer(my_dfa).staticShow()
