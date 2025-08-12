#include <algorithm>
#include <iostream>
#include <iterator>
#include <limits>
#include <sstream>
#include <string>
#include <vector>

template<typename T>
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

Node<int>* lca(Node<int>* root, Node<int>* node1, Node<int>* node2) {
    // WRITE YOUR BRILLIANT CODE HERE
    return nullptr;
}

// this function builds a tree from input
// learn more about how trees are encoded in https://algo.monster/problems/serializing_tree
template<typename T, typename Iter, typename F>
Node<T>* build_tree(Iter& it, F f) {
    std::string val = *it;
    ++it;
    if (val == "x") return nullptr;
    Node<T>* left = build_tree<T>(it, f);
    Node<T>* right = build_tree<T>(it, f);
    return new Node<T>{f(val), left, right};
}

Node<int>* find_node(Node<int>* root, int target) {
    if (root == nullptr || root->val == target) return root;
    Node<int>* left_search = find_node(root->left, target);
    if (left_search != nullptr) {
        return left_search;
    }
    return find_node(root->right, target);
}

template<typename T>
std::vector<T> get_words() {
    std::string line;
    std::getline(std::cin, line);
    std::istringstream ss{line};
    ss >> std::boolalpha;
    std::vector<T> v;
    std::copy(std::istream_iterator<T>{ss}, std::istream_iterator<T>{}, std::back_inserter(v));
    return v;
}

void ignore_line() {
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

int main() {
    std::vector<std::string> tree_vec = get_words<std::string>();
    auto tree_it = tree_vec.begin();
    Node<int>* root = build_tree<int>(tree_it, [](auto s) { return std::stoi(s); });
    int target;
    std::cin >> target;
    ignore_line();
    Node<int>* node1 = find_node(root, target);
    std::cin >> target;
    ignore_line();
    Node<int>* node2 = find_node(root, target);
    Node<int>* res = lca(root, node1, node2);
    if (res == nullptr) {
        std::cout << "null" << '\n';
    } else {
        std::cout << res->val << '\n';
    }
}
