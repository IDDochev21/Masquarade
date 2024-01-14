#include "Register.h"
#include "Utility.h"

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