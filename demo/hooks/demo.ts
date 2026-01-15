// Demo TypeScript file for testing Claude Code hooks
// This file demonstrates user data processing with validation and timestamp generation
const user = { name: "John Doe", age: 30, email: "john@example.com" };
function processUser(userData: any) {
  if (userData.name && userData.age) {
    console.log(`Processing user: ${userData.name}`);
    return { ...userData, processed: true, timestamp: Date.now() };
  } else {
    throw new Error("Invalid user data");
  }
}
const result = processUser(user);
console.log(result);
console.log("Processing complete");
