class Node(object):
    """结点"""
    def __init__(self, elem):
        self.elem = elem
        self.left_child = None
        self.right_child = None


class Tree(object):
    """二叉树"""

    def __init__(self, node=None):
        self.root = node

    def add(self, elem):
        """层序添加"""
        node = Node(elem)
        if not self.root:
            self.root = node
            return
        queue = [self.root]
        while queue:
            cur_node = queue.pop(0)
            if not cur_node.left_child:  # 如果左子树为空
                cur_node.left_child = node
                return
            elif not cur_node.right_child:
                cur_node.right_child = node
                return
            else:    # 如果左右子树都不为空，压进堆栈，判断子树的子树
                queue.append(cur_node.left_child)
                queue.append(cur_node.right_child)

    def breadth_travel(self):
        """广度遍历，层序遍历"""
        if not self.root:
            return
        queue = [self.root]
        while queue:
            cur_node = queue.pop(0)
            print(cur_node.elem, end=" ")
            if cur_node.left_child:
                queue.append(cur_node.left_child)
            if cur_node.right_child:
                queue.append(cur_node.right_child)
        print("")

    def preorder(self):
        """先序遍历"""
        if not self.root:
            return
        print(self.root.elem, end=" ")
        Tree(self.root.left_child).preorder()
        Tree(self.root.right_child).preorder()

    def inorder(self):
        """中序遍历"""
        if not self.root:
            return
        Tree(self.root.left_child).inorder()
        print(self.root.elem, end=" ")
        Tree(self.root.right_child).inorder()

    def postorder(self):
        """后序遍历"""
        if not self.root:
            return
        Tree(self.root.left_child).postorder()
        Tree(self.root.right_child).postorder()
        print(self.root.elem, end=" ")

    def get_height(self):
        """求二叉树高度"""
        if self.root:
            hl = Tree(self.root.left_child).get_height()
            hr = Tree(self.root.right_child).get_height()
            return max(hl, hr) + 1
        else:
            return 0


if __name__ == '__main__':
    tree = Tree()
    for i in range(10):
        tree.add(i)
    tree.breadth_travel()
    tree.preorder()
    print("")
    tree.inorder()
    print("")
    tree.postorder()
    print("")
    print(tree.get_height())
