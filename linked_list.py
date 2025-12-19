
class Node():
    def __init__(self, value, next = None):
        self.value = value
        self.next = next

class LinkedList():
    def __init__(self):
        self.head = None
    
    def append(self, value):
        if self.head:
            new_node = Node(value=value)

            actual_node = self.head
            while actual_node.next:
                actual_node = actual_node.next

            actual_node.next = new_node
        else:
            new_node = Node(value=value)
            self.head = new_node

    def print_list(self):
        actual_node = self.head
        while actual_node:
            print(actual_node.value)
            actual_node = actual_node.next

l = LinkedList()
l.append("a")
l.append("b")
l.append(1)

l.print_list()