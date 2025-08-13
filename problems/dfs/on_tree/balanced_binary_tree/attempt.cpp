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

int tree_height(Node<int>* tree) {
	if (tree == nullptr) return 0;
	int left_height = tree_height(tree->left);
	int right_height = tree_height(tree->right);
	if (left_height == -1 || right_height == -1) return -1;
	if (std::abs(left_height - right_height) > 1) return -1;
	return std::max(left_height, right_height) + 1;
}

bool is_balanced(Node<int>* tree) {
	// WRITE YOUR BRILLIANT CODE HERE
	return tree_height(tree) != -1;
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

int main() {
	std::vector<std::string> tree_vec = get_words<std::string>();
	auto tree_it = tree_vec.begin();
	Node<int>* tree = build_tree<int>(tree_it, [](auto s) { return std::stoi(s); });
	bool res = is_balanced(tree);
	std::cout << std::boolalpha << res << '\n';
}
