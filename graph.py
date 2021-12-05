import node
import graphviz

dot = graphviz.Graph(format='png')
nodes_without_value = ['+', '-', '*', '/', '(', ')', 'n']

def create_gv(root: node.Node):
    if not root: return # Base case ...
    label = f'{root.token}' if root.token in nodes_without_value else f'{root.token}.val = {root.value}'
    dot.node(str(hash(root)), label, shape='plaintext') # Create the node
    if not root.children: return # the node has no children
    for ch in root.children: # and edge for each children
        dot.edge(str(hash(root)), str(hash(ch)))
    for child in root.children: # call recurs...
        create_gv(child)

def view_gv(title="tltle goes here."):
    dot.attr(label=title)
    dot.attr(labelloc="top")
    dot.attr(labeljust="left")
    dot.view()
    dot.clear()