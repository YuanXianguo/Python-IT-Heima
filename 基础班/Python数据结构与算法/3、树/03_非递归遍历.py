from tree import Tree


def preorder(root):
    stack = []
    # 根结点不为空或堆栈不为空
    while root or len(stack):
        while root:
            print(root.elem, end=" ")
            stack.append(root)
            root = root.left_child
        if len(stack):
            root = stack.pop()
            root = root.right_child


def inorder(root):
    stack = []
    while root or len(stack):
        while root:
            stack.append(root)
            root = root.left_child
        if len(stack):
            root = stack.pop()
            print(root.elem, end=" ")
            root = root.right_child


def postorder(root):
    stack = []
    last_root = ""  # 记录上一个访问的结点
    while root:
        stack.append(root)
        root = root.left_child
    while len(stack):
        root = stack.pop()
        # 一个根结点被访问的前提是：无右子树或右子树已被访问过
        if not root.right_child or root.right_child == last_root:
            print(root.elem, end=" ")
            last_root = root
        else:  # 右子树不为空，访问右子树
            stack.append(root)
            root = root.right_child
            while root:
                stack.append(root)
                root = root.left_child


if __name__ == '__main__':
    tree = Tree()
    for i in range(10):
        tree.add(i)
    preorder(tree.root)
    print("")
    inorder(tree.root)
    print("")
    postorder(tree.root)
