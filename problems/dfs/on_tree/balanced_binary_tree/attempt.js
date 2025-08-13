"use strict";

class Node {
	constructor(val, left = null, right = null) {
		this.val = val;
		this.left = left;
		this.right = right;
	}
}

function dfs(tree) {
	if (tree === null) return 0;
	const left = dfs(tree.left);
	const right = dfs(tree.right);
	if (left === -1 || right === -1) return -1;
	if (Math.abs(left - right) > 1) return -1;
	return Math.max(left, right) + 1;
}

function isBalanced(tree) {
	return dfs(tree) !== -1;
}

function buildTree(nodes, f) {
	const val = nodes.next().value;
	if (val === "x") return null;
	const left = buildTree(nodes, f);
	const right = buildTree(nodes, f);
	return new Node(f(val), left, right);
};

function splitWords(s) {
	return s === "" ? [] : s.split(" ");  
};

function* main() {
	const tree = buildTree(splitWords(yield)[Symbol.iterator](), parseInt);
	const res = isBalanced(tree);
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
