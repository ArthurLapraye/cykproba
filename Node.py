
class Node:
    def __init__(self,type=None, head=None, children=None, value=None, leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.head = head
        self.leaf = leaf
        self.value = value

    def to_strings(self):
        headstruc = "[ .{0} {1} ]"
        if self.leaf != None:
            return headstruc.format(self.head,headstruc.format(self.leaf,""))
        else:
            return headstruc.format(self.head," ".join([child.to_string for child in self.children]))
