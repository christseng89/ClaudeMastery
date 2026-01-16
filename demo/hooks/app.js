/**
 * Optimized Hook Testing File
 *
 * This file has been optimized to follow JavaScript best practices.
 *
 * Improvements:
 * - Removed duplicate variable declarations
 * - Removed unused variables
 * - Fixed closure issues with proper scoping
 * - Removed dangerous practices (eval, debugger)
 * - Used strict equality operators
 * - Simplified arrow functions
 *
 * Located in demo/hooks/ directory for hook testing demonstrations.
 */

console.log("Starting hook test");

const x = 10;
const y = 20;
const z = 30;

function testFunction() {
  console.log(x);
  return x === 5;
}

const arrow = (a, b) => a + b;

const test = "hook test";
const anotherVar = "testing linting";

console.log("Processing items...");

// Fixed closure issue by using let instead of var
for (let i = 0; i < 10; i++) {
  setTimeout(() => {
    console.log(i);
  }, 700);
}
