class Node:
	def __init__(self, val, left = None, right = None):
		self.val = val;
		self.left = left;
		self.right = right;

def tree_max_depth(root):
	def dfs(root):
		if root is None:
			return 0
		return max(dfs(root.left), dfs(root.right)) + 1
	return dfs(root) - 1 if root else 0;

def build_tree(nodes, f):
    val = next(nodes)
    if val == "x":
        return None
    left = build_tree(nodes, f)
    right = build_tree(nodes, f)
    return Node(f(val), left, right)

if __name__ == "__main__":
    root = build_tree(iter(input().split()), int)
    res = tree_max_depth(root)
    print(res)
