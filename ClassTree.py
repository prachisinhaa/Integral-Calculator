class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class Tree:
    def __init__(self):
        self.definite = False
        self.lower_bound = 0
        self.upper_bound = 0
        self.root = None

    def insert_from(self, node, lower, upper):
        if node is None:
            return Node(lower), Node(upper)
        if lower < node.value:
            left, right = self.insert_from(node.left, lower, upper)
            node.left = left
            node.right = right
        elif lower > node.value:
            left, right = self.insert_from(node.right, lower, upper)
            node.left = left
            node.right = right
        return node

    def integral_from(self, node, definite, value, stream):
        if node is None:
            return 0
        integral = 0
        if node.left:
            integral += self.integral_from(node.left, definite, value, stream)
        if node.right:
            integral += self.integral_from(node.right, definite, value, stream)
        if definite:
            integral += node.value * value
        else:
            integral += node.value
        return integral

    def insert(self, lower, upper):
        self.root = self.insert_from(self.root, lower, upper)

    def clear(self):
        self.root = None

    def fill(self, string):
        pass  

    def integral(self):
        pass  
