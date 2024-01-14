#include "Chose.h"
#include "Register.h"
#include "Login.h"

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