from tree import Tree


def preorder(root):
    """先序遍历"""
    if not root:
        return
    print(root.elem, end=" ")
    preorder(root.left_child)
    preorder(root.right_child)


def inorder(root):
    """中序遍历"""
    if not root:
        return
    inorder(root.left_child)
    print(root.elem, end=" ")
    inorder(root.right_child)


def postorder(root):
    """后序遍历"""
    if not root:
        return
    postorder(root.left_child)
    postorder(root.right_child)
    print(root.elem, end=" ")


def get_height(root):
    """求二叉树高度"""
    if root:
        hl = get_height(root.left_child)
        hr = get_height(root.right_child)
        return max(hl, hr) + 1
    else:
        return 0


if __name__ == '__main__':
    tree = Tree()
    for i in range(10):
        tree.add(i)
    preorder(tree.root)
    print("")
    inorder(tree.root)
    print("")
    postorder(tree.root)
    print("")
    print(get_height(tree.root))
