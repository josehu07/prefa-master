#############################################################
# COPIED FROM "binarytree" LIBRARY (ver 4.0.0) AND MODIFIED #
#############################################################

def _buildTreeString(root, curr_index):
    """Recursively walk down the binary tree and build a pretty-print string.

    In each recursive call, a "box" of characters visually representing the
    current (sub)tree is constructed line by line. Each line is padded with
    whitespaces to ensure all lines in the box have the same length. Then the
    box, its width, and start-end positions of its root node value repr string
    (required for drawing branches) are sent up to the parent call. The parent
    call then combines its left and right sub-boxes to build a larger box etc.

    Args:
        root       - Node, root node to build string on
        curr_index - int , top-down index of root

    Returns:
        (new_box, len(new_box[0]), new_root_start, new_root_end) - tuple
    """

    # Generate representation string for current root node.
    if root is None:
        return [], 0, 0, 0
    line1 = []
    line2 = []
    if root.pos != None:
        node_repr = '{},{}'.format(root.pos, root.value)
    else:
        node_repr = str(root.value)
    new_root_width = gap_size = len(node_repr)

    # Get the left and right sub-boxes, their widths, and root repr positions.
    l_box, l_box_width, l_root_start, l_root_end = \
        _buildTreeString(root.left, 2 * curr_index + 1)
    r_box, r_box_width, r_root_start, r_root_end = \
        _buildTreeString(root.right, 2 * curr_index + 2)

    # Draw the branch connecting the current root node to the left sub-box.
    # Pad the line with whitespaces where necessary.
    if l_box_width > 0:
        l_root = (l_root_start + l_root_end) // 2 + 1
        line1.append(' ' * (l_root + 1))
        line1.append('_' * (l_box_width - l_root))
        line2.append(' ' * l_root + '/')
        line2.append(' ' * (l_box_width - l_root))
        new_root_start = l_box_width + 1
        gap_size += 1
    else:
        new_root_start = 0

    # Draw the representation of the current root node.
    line1.append(node_repr)
    line2.append(' ' * new_root_width)

    # Draw the branch connecting the current root node to the right sub-box.
    # Pad the line with whitespaces where necessary.
    if r_box_width > 0:
        r_root = (r_root_start + r_root_end) // 2
        line1.append('_' * r_root)
        line1.append(' ' * (r_box_width - r_root + 1))
        line2.append(' ' * r_root + '\\')
        line2.append(' ' * (r_box_width - r_root))
        gap_size += 1
    new_root_end = new_root_start + new_root_width - 1

    # Combine the left and right sub-boxes with the branches drawn above.
    gap = ' ' * gap_size
    new_box = [''.join(line1), ''.join(line2)]
    for i in range(max(len(l_box), len(r_box))):
        l_line = l_box[i] if i < len(l_box) else ' ' * l_box_width
        r_line = r_box[i] if i < len(r_box) else ' ' * r_box_width
        new_box.append(l_line + gap + r_line)

    # Return the new box, its width and its root repr positions.
    return new_box, len(new_box[0]), new_root_start, new_root_end

class Node(object):
    """Represents a binary tree node.

    This class provides methods and properties for managing the current node
    instance, and the binary tree in which the node is the root of. When a
    docstring in this class mentions "binary tree", it is referring to the
    current node and its descendants.

    Attributes:
        value - char, symbol / operator on this node
        left  - Node, left child
        right - Node, right child
        pos   - int , position number, only non-epsilon leaves get it,
                      otherwise will be None
    """

    def __init__(self, value, left=None, right=None):
        self.value   = value
        self.visited = False
        self.left    = left
        self.right   = right
        self.pos     = None   # Set as None at initialization, but will
                              # receive a proper one when a Regex is built

    def __str__(self):
        lines = _buildTreeString(self, 0)[0]
        return '\n' + '\n'.join((line.rstrip() for line in lines))

    def __repr__(self):
        return 'Node({})'.format(self.value)

    def _markLeafPos(self):
        """Marks leaf position numbers for subtree rooted.

        Considers the current NODE as root of a whole syntax tree for a Regex,
        then marks its non-epsilon leaves with position numbers from left to
        right. Will return back an index table as well.

        Returns:
            index - dict, pos-symbol table
        """

        # Do DFS search on the tree. Notice that right child is always prior
        # to left child when pushing into stack, therefore ensuring that the
        # left branch is always first traversed.
        mark = 1
        index = {}
        stack = [self]
        while len(stack) > 0:
            node = stack.pop()
            if (node.left is None and node.right is None and
                node.value != '~'):     # Tree iff is leaf
                node.pos = mark
                index[mark] = node.value
                mark += 1
            else:
                if node.right is not None:
                    stack.append(node.right)
                if node.left is not None:
                    stack.append(node.left)
        return index

if __name__ == '__main__':
    tree = Node('*')
    tree.left  = Node('+')
    tree.left.left  = Node('a')
    tree.left.right = Node('b')
    tree.right = Node('a')
    tree._markLeafPos()
    print(tree)
