#include <algorithm>
#include <iostream>
#include <iterator>
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

std::string serialize(Node<int>* root) {
    // WRITE YOUR BRILLIANT CODE HERE
    return "";
}

Node<int>* deserialize(const std::string& root) {
    // AND HERE
    return nullptr;
}

template<typename T, typename Iter, typename F>
Node<T>* build_tree(Iter& it, F f) {
    std::string val = *it;
    ++it;
    if (val == "x") return nullptr;
    Node<T>* left = build_tree<T>(it, f);
    Node<T>* right = build_tree<T>(it, f);
    return new Node<T>{f(val), left, right};
}

template<typename T, typename F>
void format_tree(Node<T>* node, F f, std::vector<std::string>& out) {
    if (node == nullptr) {
        out.emplace_back("x");
        return;
    }
    out.emplace_back(f(node->val));
    format_tree(node->left, f, out);
    format_tree(node->right, f, out);
}

template<typename T>
std::vector<T> get_words() {
    std::string line;
    std::getline(std::cin, line);
    std::istringstream ss{line};
    std::vector<T> v;
    std::copy(std::istream_iterator<T>{ss}, std::istream_iterator<T>{}, std::back_inserter(v));
    return v;
}

template<typename T>
void put_words(const std::vector<T>& v) {
    if (!v.empty()) {
        std::copy(v.begin(), std::prev(v.end()), std::ostream_iterator<T>{std::cout, " "});
        std::cout << v.back();
    }
    std::cout << '\n';
}

int main() {
    std::vector<std::string> tree_vec = get_words<std::string>();
    auto tree_it = tree_vec.begin();
    Node<int>* tree = build_tree<int>(tree_it, [](auto s) { return std::stoi(s); });
    Node<int>* res = deserialize(serialize(tree));
    std::vector<std::string> res_vec;
    format_tree(res, [](auto v) { return std::to_string(v); }, res_vec);
    put_words(res_vec);
}
