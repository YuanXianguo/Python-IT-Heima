class Node(object):
    """结点"""
    def __init__(self, elem):
        self.elem = elem
        self.left_child = None
        self.right_child = None


class BinarySearchTree(object):
    """二叉搜索树"""
    def __init__(self, node=None):
        self.root = node

    def insert(self, elem):
        """二叉搜索树插入"""
        node = Node(elem)
        if not self.root:
            self.root = node
        else:
            if elem < self.root.elem:
                self.root.left_child = BinarySearchTree(
                    self.root.left_child).insert(elem)
            elif elem > self.root.elem:
                self.root.right_child = BinarySearchTree(
                    self.root.right_child).insert(elem)
        return self.root

    def find(self, elem):
        """递归查找值"""
        if not self.root:
            return "查找失败"
        if elem < self.root.elem:
            return BinarySearchTree(self.root.left_child).find(elem)
        elif elem > self.root.elem:
            return BinarySearchTree(self.root.right_child).find(elem)
        else:  # 找到了
            return self.root

    def find2(self, elem):
        """非递归查找"""
        root = self.root
        while root:
            if elem < root.elem:
                root = root.left_child
            elif elem > root.elem:
                root = root.right_child
            else:
                return root
        return "查找失败"

    def find_min(self):
        """递归查找最小值，一定是在树的最左分支的端结点上"""
        if not self.root:
            return "查找失败"
        if not self.root.left_child:
            return self.root  # 最小值没有左子树
        else:
            return BinarySearchTree(self.root.left_child).find_min()

    def find_max(self):
        """迭代查找最大值，一定是在树的最右分支的端结点上"""
        root = self.root
        if not root:
            return "查找失败"
        while root.right_child:
            root = root.right_child
        return root

    def delete(self, elem):
        """每次递归删除都把删除后的子树返回"""
        if not self.root:
            return "删除失败"
        elif elem < self.root.elem:
            self.root.left_child = BinarySearchTree(
                self.root.left_child).delete(elem)
        elif elem > self.root.elem:
            self.root.right_child = BinarySearchTree(
                self.root.right_child).delete(elem)
        else:  # 该结点为要删除结点
            # 如果左右子树都不为空
            if self.root.left_child and self.root.right_child:
                # 找到右子树最小值或左子树最大值
                right_min = BinarySearchTree(self.root.right_child).find_min()
                # 将找到的右子树最小值填充要删除的根结点
                self.root.elem = right_min.elem
                # 删除右子树最小值
                self.root.right_child = BinarySearchTree(
                    self.root.right_child).delete(right_min)
            else:  # 被删除结点有一个或无子树
                if not self.root.left_child:
                    self.root = self.root.right_child
                elif not self.root.right_child:
                    self.root = self.root.left_child
        return self.root


if __name__ == '__main__':
    bt = BinarySearchTree()
    for i in range(10):
        bt.insert(i)
    print(bt.find_min().elem)
    print(bt.find_max().elem)
    print(bt.find(10))
    bt.delete(9)
    print(bt.find_max().elem)

