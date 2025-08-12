def dfs(root, target):
	if root is None:
		return None
	if root.val == target:
		return root
	left = dfs(root.left, target)
	if left is not None:
		return left
	right = dfs(root.right, target)
	return right
