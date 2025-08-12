template <typename T>
struct Node {
    T val;
    Node<T>* left;
    Node<T>* right;

    explicit Node(T val, Node<T>* left = nullptr, Node<T>* right = nullptr)
        : val{val}, left{left}, right{right} {}

    ~Node() {
        delete left;
        delete right;
    }
};

bool find(Node<int>* tree, int val) {
    if (tree == nullptr) return false;
    if (tree->val == val) return true;
    else if (tree->val < val) return find(tree->right, val);
    else {
        return find(tree->left, val);
    }
}

Node<int>* insert(Node<int>* tree, int val) {
    if (tree == nullptr) return new Node<int>(val);
    if (tree->val < val) {
        tree->right = insert(tree->right, val);
    } else if (tree->val > val) {
        tree->left = insert(tree->left, val);
    }
    return tree;
}
