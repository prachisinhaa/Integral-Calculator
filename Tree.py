class Node:
    def __init__(self, coefficient, power):
        self.coefficient = coefficient
        self.power = power
        self.left = None
        self.right = None

    def get_power(self):
        return self.power

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node

    def incr_coeff(self, increment):
        self.coefficient += increment

    def sign(self):
        if self.coefficient >= 0:
            return '+'
        else:
            return '-'

    def definite(self, lower_bound, upper_bound):
        return self.coefficient * (upper_bound ** (self.power + 1) - lower_bound ** (self.power + 1)) / (self.power + 1)

    def integral(self):
        if self.power == 0:
            return str(self.coefficient) if self.coefficient != 1 else ''
        elif self.power == 1:
            return 'x' if self.coefficient == 1 else str(abs(self.coefficient)) + 'x'
        else:
            return 'x^' + str(self.power) if self.coefficient == 1 else str(abs(self.coefficient)) + 'x^' + str(self.power)


class Tree:
    def __init__(self):
        self.definite = False
        self.lower_bound = 0
        self.upper_bound = 0
        self.root = None

    def insert_from(self, parent, c, p):
        if p < parent.get_power():
            if parent.get_left():
                self.insert_from(parent.get_left(), c, p)
            else:
                parent.set_left(Node(c, p))

        elif p > parent.get_power():
            if parent.get_right():
                self.insert_from(parent.get_right(), c, p)
            else:
                parent.set_right(Node(c, p))

        else:
            parent.incr_coeff(c)
            print("A term with that power already exists -- combining ... ")

    def insert(self, c, p):
        if not self.root:
            self.root = Node(c, p)
        else:
            self.insert_from(self.root, c, p)

    def clear(self):
        if self.root:
            if self.root.get_left():
                left_subtree = Tree()
                left_subtree.root = self.root.get_left()
                left_subtree.clear()

            if self.root.get_right():
                right_subtree = Tree()
                right_subtree.root = self.root.get_right()
                right_subtree.clear()

            print("Deleting node ... ")
            self.root = None

    def fill(self, line):
        self.clear()
        ss = line.split()

        if ss[0] == '|':
            print("Analyzing indefinite integral ... ")
            self.definite = False
            ss = ss[2:]
        else:
            print("Analyzing definite integral ... ")
            self.definite = True
            self.lower_bound = int(ss[0])
            print("Lower bound:", self.lower_bound)
            self.upper_bound = int(ss[2])
            print("Upper bound:", self.upper_bound)

        for i in range(len(ss)):
            if ss[i] == 'x':
                coeff = 1
                power = 1 if i == len(ss) - 1 or ss[i + 1] != '^' else int(ss[i + 2])
                print("Encountered term", coeff, "x^", power)
                self.insert(coeff, power)

            elif ss[i] == '-':
                i += 1
                while i < len(ss) and ss[i] == ' ':
                    i += 1

                if ss[i] == 'x':
                    coeff = -1
                    power = 1 if i == len(ss) - 1 or ss[i + 1] != '^' else int(ss[i + 2])
                else:
                    coeff = int(ss[i]) * -1
                    power = 1 if i == len(ss) - 1 or ss[i + 1] != '^' else int(ss[i + 3])

                print("Encountered term", coeff, "x^", power)
                self.insert(coeff, power)

            elif ss[i].isdigit():
                coeff = int(ss[i])
                power = 1 if i == len(ss) - 1 or ss[i + 1] != '^' else int(ss[i + 2])
                print("Encountered term", coeff, "x^", power)
                self.insert(coeff, power)

        print()

    def integral_from(self, node, rightmost, sum):
        if node:
            sum = self.integral_from(node.get_right(), rightmost, sum)

            if not rightmost or node.get_right():
                print(' ' + node.sign() + ' ', end='')

            elif node.sign() == '-':
                print(node.sign(), end='')

            if self.definite:
                sum += node.definite(self.lower_bound, self.upper_bound)
            print(node.integral(), end='')

            sum = self.integral_from(node.get_left(), False, sum)

        return sum

    def integral(self):
        output = ''
        def_intrg = self.integral_from(self.root, True, 0)

        if self.definite:
            output += f", {self.lower_bound}|{self.upper_bound} = {def_intrg:.3f}\n"
        else:
            output += " + C\n"

        return output


# Testing the Tree class
tree = Tree()
tree.fill("1 x^ 2 + 2 x - 3 | 5")
print("Integral:", tree.integral())
