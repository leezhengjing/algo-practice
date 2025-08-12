"use strict";

class Node {
    constructor(val, left = null, right = null) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}

function dfs(root) {
	if (root === null) {
		return 0;
	}
	return Math.max(dfs(root.left), dfs(root.right)) + 1;
}

function treeMaxDepth(root) {
    // WRITE YOUR BRILLIANT CODE HERE
    return root !== null ? dfs(root) - 1 : 0;
}

// this function builds a tree from input; you don't have to modify it
// learn more about how trees are encoded in https://algo.monster/problems/serializing_tree
function buildTree(nodes, f) {
	const val = nodes.next().value;
	if (val === "x") return null; 
	const left = buildTree(nodes, f);
	const right = buildTree(nodes, f);
	return new Node(f(val), left, right);
}

function splitWords(s) {
	return s === "" ? [] : s.split(" ");
}

function* main() {
    const root = buildTree(splitWords(yield)[Symbol.iterator](), parseInt);
	const res = treeMaxDepth(root);
    console.log(res);
}

class EOFError extends Error {}
{
    const gen = main();
    const next = (line) => gen.next(line).done && process.exit();
    let buf = "";
    next();
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (data) => {
        const lines = (buf + data).split("\n");
        buf = lines.pop();
        lines.forEach(next);
    });
    process.stdin.on("end", () => {
        buf && next(buf);
        gen.throw(new EOFError());
    });
}

