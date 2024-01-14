#include <iostream>
#include <fstream>
#include <string>

bool doesUserExist(const std::string& username, std::ifstream& file) {
    file.clear();
    file.seekg(0);
    std::string line;
    while (getline(file, line)) {
        if (line == username) {
            return 1;
        }
    }
    return 0;
}

void printLine() {
    std::cout << "\n------------------------\n";
}


void registerUser(std::ofstream& file) {
    std::string username, password;

    printLine();
    std::cout << "Enter a new username: ";
    std::cin >> username;

    std::ifstream inFile("credentials.txt");
    if (inFile.is_open()) {
        if (doesUserExist(username, inFile)) {
            std::cout << "Username already exists. Choose another username.\n";
            printLine();
            return;
        }
    }

    std::cout << "Enter a password: ";
    std::cin >> password;

    file << username << '\n' << password << '\n';
    file.flush();

    std::cout << "User registered successfully!\n";
    printLine();
}

void login(std::ifstream& file) {
    std::string username, password;
    bool isAuthenticated = 0;

    printLine();
    std::cout << "Enter your username: ";
    std::cin >> username;

    std::cout << "Enter your password: ";
    std::cin >> password;

    file.clear();
    file.seekg(0);

    std::string savedUsername, savedPassword;
    bool isUsernameFound = 0;
    while (getline(file, savedUsername) && getline(file, savedPassword)) {
        if (savedUsername == username && savedPassword == password) {
            isUsernameFound = 1;
            isAuthenticated = 1;
            break;
        }
    }

    if (isUsernameFound && isAuthenticated) {
        std::cout << "Login successful!\n";
    }
    else {
        std::cout << "Invalid username or password.\n";
    }
    printLine();
}
void chose() {
    std::ofstream outFile("credentials.txt", std::ios::app);
    std::ifstream inFile("credentials.txt");

    if (!outFile.is_open() || !inFile.is_open()) {
        std::cerr << "Error opening file!\n";
        return;
    }

    int choice;

    do {
        std::cout << "1. Register\n2. Login\n3. Exit\n";
        std::cout << "Enter your choice: ";
        std::cin >> choice;

        switch (choice) {
        case 1:
            registerUser(outFile);
            break;

        case 2:
            login(inFile);
            break;

        case 3:
            std::cout << "Exiting the program.\n";
            break;

        default:
            std::cout << "Invalid choice. Please try again.\n";
        }
    } while (choice != 3);

    outFile.close();
    inFile.close();

    return;
}

int main() {
    chose();
}
