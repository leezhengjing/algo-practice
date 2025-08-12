Node<int>* dfs(Node<int>* root, int target) {
    if (root == nullptr) return nullptr;
    if (root -> val == target) return root;
    Node<int>* left = dfs(root-> left, target);
    if (left != nullptr) return left;
    Node<int>* right = dfs(root-> right, target);
    return right;
}