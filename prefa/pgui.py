from prefa import dfa, nfa, ere
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

        # Generate states and transitions attributes.
        self.state_list = [(s, {'role': input_fa.getRole(s)}) \
                            for s in input_fa.states]
        self.trans_dict = dict([(s1, dict([(s2, [])      \
                            for s2 in input_fa.states])) \
                            for s1 in input_fa.states])

        # Add dummy hyperinit node.
        self.trans_dict['start'] = {input_fa.initial: [' ']}

        # Pack these things into the directed graph.
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

        # Save extra infos for correct formatting.
        self.acceptings = input_fa.acceptings
        self.normals = [s for s in input_fa.states if s not in self.acceptings]

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

        # Fix the size of popping-out figure.
        plt.figure(figsize=(16, 9))

        # Draw states.
        nx.draw_networkx_nodes(self.Graph, nodelist=self.normals,
            node_size=700, node_color='#ffffff', edgecolors='#000000',
            pos=nx.kamada_kawai_layout(self.Graph))
        nx.draw_networkx_nodes(self.Graph, nodelist=self.acceptings,
            node_size=700, node_color='#ffffff', edgecolors='#000000',
            pos=nx.kamada_kawai_layout(self.Graph), linewidths=4)
        nx.draw_networkx_nodes(self.Graph, nodelist=['start'],
            node_size=700, node_color='#ffffff', edgecolors='#ffffff',
            pos=nx.kamada_kawai_layout(self.Graph))

        # Put state names, and records the labels positions.
        state_dict = nx.draw_networkx_labels(self.Graph,
            pos=nx.kamada_kawai_layout(self.Graph))

        # Draw Transition edges, and make them to be arcs, which result in
        # much more prettier displaying result.
        edges_list = nx.draw_networkx_edges(self.Graph, arrowstyle='-|>',
            arrowsize=20, width=0.9, edge_color='#000000',
            pos=nx.kamada_kawai_layout(self.Graph))
        for edge in edges_list:     # Handle self loops.
            start_x, start_y = edge._posA_posB[0]
            end_x  , end_y   = edge._posA_posB[1]
            if start_x == end_x and start_y == end_y:   # True iff self loop.
                edge.set_positions((start_x-0.03, start_y),
                                   (end_x  +0.03, end_y  ))
                edge.set_connectionstyle('angle', angleA=-82, angleB=82,
                                         rad=120)
            else:
                edge.set_connectionstyle('arc3', rad=0.2)

        # Put transition symbols, and then update the symbol text's position
        # to match the arced edges. Updated according to the following
        # mathematical relationship:
        #
        #   new_x = old_x + 0.16 * ( end_y - start_y)
        #   new_y = old_y + 0.16 * (start_x - end_x )
        #
        # A special case is for self loops. Since self loops are forced to
        # be a loop downside the state, so force the label to have a
        # downward offset is enough.
        trans_dict = nx.draw_networkx_edge_labels(self.Graph, font_size=13,
            pos=nx.kamada_kawai_layout(self.Graph))
        for tup in trans_dict:
            if tup[0] == tup[1]:
                text_x , text_y  = trans_dict[tup].get_position()
                trans_dict[tup].set_position((text_x, text_y-0.12))
            else:
                start_x, start_y = state_dict[tup[0]].get_position()
                end_x  , end_y   = state_dict[tup[1]].get_position()
                text_x , text_y  = trans_dict[tup].get_position()
                trans_dict[tup].set_position((text_x+0.16*(end_y-start_y),
                                              text_y+0.16*(start_x-end_x)))
            trans_dict[tup].set_bbox(dict(alpha=0))
            trans_dict[tup].set_text(boreStr(self.trans_dict[tup[0]][tup[1]]))

        # Hide pyplot axis and show the figure.
        plt.axis('off')
        plt.show()

if __name__ == '__main__':
    my_nfa = nfa.NFiniteAutomata(ere.Regex('(a|~)b*c[0-2]?'))
    FADrawer(my_nfa).staticShow()

    my_dfa = dfa.DFiniteAutomata(ere.Regex('0*(1|10|100)*1'))
    FADrawer(my_dfa).staticShow()
