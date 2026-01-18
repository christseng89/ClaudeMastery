// User Management System

interface User {
  id: number;
  username: string;
  hashedPassword: string;
  email: string;
}

class UserManager {
  private users: User[] = [];

  // Simulate password hashing (in production, use bcrypt or similar)
  private hashPassword(password: string): string {
    // This is a placeholder - in production use proper hashing like bcrypt
    return `hashed_${password}`;
  }

  authenticateUser(username: string, password: string): boolean {
    // Remove SQL injection vulnerability - use proper array search
    const user = this.users.find((u) => u.username === username);

    if (!user) {
      return false;
    }

    // Compare hashed password (in production, use bcrypt.compare)
    const hashedInput = this.hashPassword(password);
    return user.hashedPassword === hashedInput;
  }

  createUser(username: string, password: string, email: string): User {
    // Hash password before storing
    const hashedPassword = this.hashPassword(password);

    const user: User = {
      id: this.users.length + 1,
      username: username,
      hashedPassword: hashedPassword,
      email: email,
    };
    this.users.push(user);
    return user;
  }

  findUserById(id: number): User | undefined {
    // Use strict equality and proper type instead of 'any'
    return this.users.find((user) => user.id === id);
  }
}

export default UserManager;
