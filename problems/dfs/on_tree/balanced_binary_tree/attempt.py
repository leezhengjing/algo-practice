class Node:
	def __init__(self, val, left, right):
		self.val = val
		self.left = left
		self.right = right

def dfs(tree: Node):
	if tree is None:
		return 0
	left = dfs(tree.left)
	right = dfs(tree.right)
	if (left == -1 or right == -1):
		return -1
	if (abs(left - right) > 1):
		return -1
	return max(left, right) + 1

def is_balanced(tree: Node):
	return dfs(tree) != -1;

def build_tree(nodes, f):
    val = next(nodes)
    if val == "x":
        return None
    left = build_tree(nodes, f)
    right = build_tree(nodes, f)
    return Node(f(val), left, right)

if __name__ == "__main__":
    tree = build_tree(iter(input().split()), int)
    res = is_balanced(tree)
    print("true" if res else "false")

