from tree import Tree


def breadth_travel(root):
    """广度遍历"""
    if not root:
        return
    queue = [root]
    while queue:
        cur_node = queue.pop(0)
        print(cur_node.elem, end=" ")
        if cur_node.left_child:
            queue.append(cur_node.left_child)
        if cur_node.right_child:
            queue.append(cur_node.right_child)
    print("")


def breadth_travel_leaf(root):
    """广度遍历，输出叶子结点"""
    if not root:
        return
    queue = [root]
    while queue:
        cur_node = queue.pop(0)
        if not cur_node.left_child and not cur_node.right_child:
            print(cur_node.elem, end=" ")
        if cur_node.left_child:
            queue.append(cur_node.left_child)
        if cur_node.right_child:
            queue.append(cur_node.right_child)
    print("")


if __name__ == '__main__':
    tree = Tree()
    for i in range(10):
        tree.add(i)

    breadth_travel(tree.root)
    breadth_travel_leaf(tree.root)
