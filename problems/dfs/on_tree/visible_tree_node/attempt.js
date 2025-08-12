"use strict";

class Node {
	constructor(val, left = null, right = null) {
		this.val = val;
		this.left = left;
		this.right = right;
	}
}

function dfs(root, highest) {
	if (root === null) {
		return 0;
	}
	let total = 0;
	if (root.val >= highest) total++;

	total += dfs(root.left, Math.max(root.val, highest));
	total += dfs(root.right, Math.max(root.val, highest));
	return total;
}

function visibleTreeNode(root) {
	return dfs(root, Number.NEGATIVE_INFINITY);
}

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
	const res = visibleTreeNode(root); 
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
