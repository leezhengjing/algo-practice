class Node {
    constructor(val, left = null, right = null) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}

function find(tree, val) {
    if (tree == null) return false;
    if (tree.val == val) return true;
    else if (tree.val < val) {
        return find(tree.right, val);
    }
    else {
        return find(tree.left, val);
    }
}

function insert(tree, val) {
    if (tree == null) return new Node(val);
    if (tree.val < val) {
        tree.right = insert(tree.right, val);
    } else if (tree.val > val) {
        tree.left = insert(tree.left, val);
    }
    return tree;
}