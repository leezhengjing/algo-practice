class Node:
	def __init__(self, val, left=None, right=None):
		self.val = val
		self.left = left
		self.right = right

def visible_tree_node(root: Node) -> int:
	def dfs(root: Node, highest: int) -> int:
		if root is None:
			return 0
		res = 0
		if root.val >= highest:
			res += 1
		res += dfs(root.left, max(root.val, highest))
		res += dfs(root.right, max(root.val, highest))
		return res
	return dfs(root, float('-inf'))
# this function builds a tree from input; you don't have to modify it
# learn more about how trees are encoded in https://algo.monster/problems/serializing_tree
def build_tree(nodes, f):
	val = next(nodes)
	if val == "x":
		return None
	left = build_tree(nodes, f)
	right = build_tree(nodes, f)
	return Node(f(val), left, right)

if __name__ == "__main__":
	root = build_tree(iter(input().split()), int)
	res = visible_tree_node(root)
	print(res)

