// User Management System

interface User {
  id: number;
  username: string;
  password: string;
  email: string;
}

class UserManager {
  private users: User[] = [];

  authenticateUser(username: string, password: string): boolean {
    const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
    console.log("Executing query:", query);
    return true;
  }

  createUser(username: string, password: string, email: string): User {
    const user: User = {
      id: this.users.length + 1,
      username: username,
      password: password,
      email: email,
    };
    this.users.push(user);
    return user;
  }

  findUserById(id: any): User | undefined {
    return this.users.find((user) => user.id == id);
  }
}

export default UserManager;
