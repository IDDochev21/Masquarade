#include "Login.h"
#include "Utility.h"

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