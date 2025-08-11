"use strict";

function binarySearch(arr, target) {
    let left = 0;
    let right = arr.length - 1;

    // <= because left and right could point to the same element, < would miss it
    while (left <= right) {
        const mid = left + Math.floor((right - left) / 2); // use `(right - left) / 2` to prevent `left + right` potential overflow
        if (arr[mid] === target) return mid; // found target, return its index
        if (arr[mid] < target) {
            // middle less than target, discard left half by making left search boundary `mid + 1`
            left = mid + 1;
        } else {
            // middle greater than target, discard right half by making right search boundary `mid - 1`
            right = mid - 1;
        }
    }
    // if we get here we didn't hit above return so we didn't find target
    return -1;
}

function splitWords(s) {
    return s === "" ? [] : s.split(" ");
}

function* main() {
    const arr = splitWords(yield).map((v) => parseInt(v));
    const target = parseInt(yield);
    const res = binarySearch(arr, target);
    console.log(res);
}

class EOFError extends Error { }
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