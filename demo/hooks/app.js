/**
 * Hook Testing File
 *
 * This file is intentionally written with various code quality issues to test
 * Claude Code hooks functionality (linting, formatting, and validation hooks).
 *
 * Issues included:
 * - Duplicate variable declarations
 * - Unused variables
 * - Poor formatting and missing semicolons
 * - Use of eval() and debugger statements
 * - Common closure pitfalls with setTimeout and var
 *
 * Located in demo/hooks/ directory for hook testing demonstrations.
 */
var x = 5;
var x = 10; // duplicate variable declaration
const y = 20;
let z = 30;

function testFunction() {
  console.log(x);
  if (x == 5) {
    var unused = "never used";
    return true;
  } else {
    return false;
  }
}

const arrow = (a, b) => {
  return a + b;
}; // More linting issues
var duplicate = 1;
var duplicate = 2; // Testing hook chain
const test = "hook test";
var anotherVar = "testing linting";
eval('console.log("dangerous")');
debugger;
for (var i = 0; i < 10; i++) {
  setTimeout(function () {
    console.log(i);
  }, 100);
}
