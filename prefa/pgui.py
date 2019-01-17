##############################################################################
# Author: Jose, Robert & King                                                #
#  Date:  2019.01.15                                                         #
##############################################################################

from prefa import dfa, nfa, ere
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
# import dfa, nfa, ere

class FADrawer(object):
    """Class which serves displaying of Finite Automatas.

    Wraps the `NetworkX` package and thus provides a really clean and pretty
    way of drawing, simulating and displaying automatas.

    Attributes:
        state_list - list, the nodes list
        trans_dict - dict, the edges dict, containing all state pairs
        trans_list - list, the edges list, only containing existing edges
        Graph      - nx.MultiDiGraph, `NetworkX` multi-directed graph
        acceptings - set , the set of accepting states
        normals    - set , the set of all non-accepting states
        to_bend    - list, list of state pairs where edges need bending
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

        # Form the transition list and put all states and edges into the
        # graph. Will record state pairs where edges need bending. Also,
        # to prevent the situations that two states are put in the same
        # place in the layout, add invisible edges for state pairs where:
        #
        #   1. They have a direct common predeccesor.
        #   2. No edges between two of them.
        #
        # So that they will be separated in the graph layout.
        for s in input_fa.states:
            for a in input_fa.alphabet:
                for s_end in input_fa.table[s][a]:
                    self.trans_dict[s][s_end].append(a)
        self.trans_list, self.to_bend, self.invisibles = [], [], []
        for s1 in self.trans_dict:
            for s2 in self.trans_dict[s1]:
                if len(self.trans_dict[s1][s2]) > 0:
                    self.trans_list.append((s1, s2,
                        {'syms': self.trans_dict[s1][s2]}))
                    if s1 != 'start' and s1 != s2 and \
                       len(self.trans_dict[s2][s1]) > 0:
                        self.to_bend.append((s1, s2))
                else:
                    for sp in input_fa.states:
                        if len(self.trans_dict[sp][s1]) > 0 and \
                           len(self.trans_dict[sp][s2]) > 0:
                           self.invisibles.append((s1, s2))

        # Build the networkx graph.
        self.Graph = nx.DiGraph()  # Use directed graph.
        self.Graph.add_nodes_from(self.state_list)
        self.Graph.add_edges_from(self.trans_list)
        self.Graph.add_edges_from(self.invisibles)

        # Save extra infos for correct formatting.
        self.acceptings = list(input_fa.acceptings)
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

        def needBending(start_x, end_x, start_y, end_y, state_dict, to_bend):
            """Judger for whether and edge needs bending.

            If an edge has a counterpart (whose endpoint equals to its
            point, and the startpont equals to its endpoint), then both of
            them needs to bend to their right side for the same angle, to
            ensure no overlapping.

            Args:
                start_x    - float, x coordinate of startpoint
                end_x      - float, x coordinate of endpoint
                start_y    - float, y coordinate of startpoint
                end_y      - float, y coordinate of endpoint
                state_dict - dict, the dict recording state positions
                to_bend    - previously generated pairs of bending edges

            Returns:
                Bool, True if needs bending, and False otherwise
            """
            for tup in to_bend:
                start_x0, start_y0 = state_dict[tup[0]].get_position()
                end_x0  , end_y0   = state_dict[tup[1]].get_position()
                if (start_x == start_x0 and end_x == end_x0 and \
                    start_y == start_y0 and end_y == end_y0):
                    return True
            return False

        def loopOffset(x, y):
            """Calculates self loop layout offset.

            Calculates edge and text label offset for self loops. Intends
            to make self loops bending on the outer side of the graph, so
            handle self loops at different places of the graph
            differently. Divide by the following principle:

                                  |      |
                            ______|______|______
                                  |      |
                            ______|______|______
                                  |      |
                                  |      |

            Args:
                x - float, x coordinate of self loop state
                y - float, y coordinate of self loop state

            Returns:
                (x1_ofs, y1_ofs, x2_ofs, y2_ofs, text_x_ofs, text_y_ofs) -
                    tuple of six elements, where the first four are for
                    edge offsets and the last two are for text labels.
            """
            xe, ye, xt, yt, aj = 0.0216, 0.0384, 0.1, 0.178, 1.5
            if x <= -0.33:
                if y <= -0.33:                          # Lower  Left
                    return -xe,    ye,  xe,    -ye,    -xt, -yt
                elif -0.33 < y <= 0.33:                 # Center Left
                    return   0, ye*aj,   0, -ye*aj, -xt*aj,   0
                else:                                   # Upper  Left
                    return  xe,    ye, -xe,    -ye,    -xt,  yt
            elif -0.33 < x <= 0.33:
                if y <= -0.33:                          # Lower  Center
                    return -xe*aj, 0,  xe*aj, 0, 0, -yt*aj
                elif -0.33 < y <= 0.33:                 # Center Center
                    return -xe*aj, 0,  xe*aj, 0, 0, -yt*aj
                else:                                   # Upper  Center
                    return  xe*aj, 0, -xe*aj, 0, 0,  yt*aj
            else:
                if y <= -0.33:                          # Lower  Right
                    return -xe,    -ye,  xe,    ye,    xt, -yt
                elif -0.33 < y <= 0.33:                 # Center Right
                    return   0, -ye*aj,   0, ye*aj, xt*aj,   0
                else:                                   # Upper  Right
                    return  xe,    -ye, -xe,    ye,    xt,  yt

        # Fix the size of popping-out figure, therefore ensures a relatively
        # stable performance. Uses a fixed kamada-kawai layout.
        plt.figure(figsize=(16, 9))
        layout = nx.kamada_kawai_layout(self.Graph)
        x_min, x_max = float('inf'), -float('inf')
        y_min, y_max = float('inf'), -float('inf')
        for s in layout:
            x_min = layout[s][0] if layout[s][0] < x_min else x_min
            x_max = layout[s][0] if layout[s][0] > x_max else x_max
            y_min = layout[s][1] if layout[s][1] < y_min else y_min
            y_max = layout[s][1] if layout[s][1] > y_max else y_max
        for s in layout:
            layout[s][0] *= 2. / (x_max - x_min)
            layout[s][1] *= 2. / (y_max - y_min)

        # Draw states.
        nx.draw_networkx_nodes(self.Graph, nodelist=self.normals,
            node_size=1000, node_color='#ffffff', edgecolors='#000000',
            pos=layout)
        nx.draw_networkx_nodes(self.Graph, nodelist=self.acceptings,
            node_size=1000, node_color='#ffffff', edgecolors='#000000',
            pos=layout, linewidths=5)
        nx.draw_networkx_nodes(self.Graph, nodelist=['start'],
            node_size=1000, node_color='#ffffff', edgecolors='#ffffff',
            pos=layout)

        # Draw anchor states to control the canvas.
        nx.draw_networkx_nodes(self.Graph, node_size=1000,
            node_color='#ffffff', edgecolors='#ffffff',
            nodelist=['anchor1', 'anchor2', 'anchor3', 'anchor4'],
            pos={'anchor1': np.array([-1.5, -1.5]),
                 'anchor2': np.array([-1.5,  1.5]),
                 'anchor3': np.array([ 1.5, -1.5]),
                 'anchor4': np.array([ 1.5,  1.5])})

        # Put state names, and records the labels positions.
        state_dict = nx.draw_networkx_labels(self.Graph, pos=layout)

        # Draw Transition edges, and make them to be arcs, which result in
        # much more prettier displaying result.
        edges_to_draw = [(tup[0], tup[1]) for tup in self.trans_list]
        edges_list = nx.draw_networkx_edges(self.Graph, edgelist=edges_to_draw,
            arrowstyle='-|>', arrowsize=26, width=0.9, edge_color='#8a8a8a',
            pos=layout)
        for edge in edges_list:     # Handle self loops.
            start_x, start_y = edge._posA_posB[0]
            end_x  , end_y   = edge._posA_posB[1]
            if start_x == end_x and start_y == end_y:   # True iff self loop.
                x1_ofs, y1_ofs, x2_ofs, y2_ofs, _, _ = loopOffset(end_x, end_y)
                edge.set_positions((start_x+x1_ofs, start_y+y1_ofs),
                                   ( end_x +x2_ofs,  end_y +y2_ofs))
                edge.set_connectionstyle('arc3', rad=4)
            elif needBending(start_x, end_x, start_y, end_y, state_dict,
                             self.to_bend):
                edge.set_connectionstyle('arc3', rad=0.2)
            edge.set_arrowstyle('-|>', head_length=0.5, head_width=0.1)

        # Put transition symbols, and then update the symbol text's position
        # to match the arced edges. Updated according to the following
        # mathematical quadratic bezier curve relationship:
        #
        # For bent edges:
        #   new_x = mid-point_x of edge + 0.09 * 0.5 rad * (end_y - start_y)
        #   new_y = mid-point_y of edge + 0.16 * 0.5 rad * (start_x - end_x)
        #
        # For straight edges:
        #   new_x = 0.5 * (start_x + end_x) i.e. Unchanged.
        #   new_y = 0.5 * (start_y + end_y) i.e. Unchanged.
        #
        # For self loops:
        #   See `loopOffset` function.
        #
        # A special case is for self loops. Since self loops are forced to
        # be a loop downside the state, so force the label to have a
        # downward offset is enough.
        trans_dict = nx.draw_networkx_edge_labels(self.Graph, font_size=13,
            pos=layout)
        for tup in trans_dict:
            start_x, start_y = state_dict[tup[0]].get_position()
            end_x  , end_y   = state_dict[tup[1]].get_position()
            if start_x == end_x and start_y == end_y:
                _, _, _, _, x_ofs, y_ofs = loopOffset(end_x, end_y)
                new_x, new_y = start_x + x_ofs, start_y + y_ofs
            elif needBending(start_x, end_x, start_y, end_y, state_dict,
                             self.to_bend):
                new_x = (start_x + end_x) / 2. + 0.09 * (end_y - start_y)
                new_y = (start_y + end_y) / 2. + 0.16 * (start_x - end_x)
            else:
                new_x = (start_x + end_x) / 2.
                new_y = (start_y + end_y) / 2.
            trans_dict[tup].set_position((new_x, new_y))
            trans_dict[tup].set_bbox(dict(alpha=0.3, color='#e6e6e6', linewidth=0))
            trans_dict[tup].set_text(boreStr(self.trans_dict[tup[0]][tup[1]]))

        # Hide pyplot axis and show the figure.
        plt.axis('off')
        plt.show()

if __name__ == '__main__':
    # rexpr = ere.Regex('0*10*10*10*')
    # rexpr = ere.Regex('(a|~)b*c[0-2]?')
    rexpr = ere.Regex('0*(1|10|100)*0*1')
    my_nfa = nfa.NFiniteAutomata(rexpr)
    FADrawer(my_nfa).staticShow()

    my_dfa = dfa.DFiniteAutomata(my_nfa)
    FADrawer(my_dfa).staticShow()

    min_dfa = my_dfa.minimalDFA()
    FADrawer(min_dfa).staticShow()

    my_nfa = nfa.NFiniteAutomata('../input/NFA2')
    my_dfa = dfa.DFiniteAutomata(my_nfa)
    FADrawer(my_nfa).staticShow()
