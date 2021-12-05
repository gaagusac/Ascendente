import node
# This evaluates de cts ... it's better to work with ast...
def evaluate(root: node.Node):
    if not root: return
    if root.token == 'number': # node is a number
        return root.value
    elif root.token == 'E': # E productions
        # E -> E + T | E - T
        if len(root.children) == 3:
            root.value = {
                '+': evaluate(root.children[0]) + evaluate(root.children[2]),
                '-': evaluate(root.children[0]) - evaluate(root.children[2]),
            }[root.children[1].token]
            return root.value
        else: # E -> T
            root.value = evaluate(root.children[0])
            return root.value
    elif root.token == 'T': # T productions
        # T -> T * F | T / F
        if len(root.children) == 3:
            root.value = {
                '*': evaluate(root.children[0]) * evaluate(root.children[2]),
                '/': evaluate(root.children[0]) / evaluate(root.children[2]),
            }[root.children[1].token]
            return root.value
        else: # T -> F
            root.value = evaluate(root.children[0])
            return root.value
    elif root.token == 'F': # F productions
        if len(root.children) == 3: # F -> ( E )
            root.value = evaluate(root.children[1])
            return root.value
        else: # F -> digit
            root.value = evaluate(root.children[0])
            return root.value
    else: # L -> E
        root.value = evaluate(root.children[0])
        return root.value