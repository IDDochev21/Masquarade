#include "Utility.h"

void printLine() {
    std::cout << "\n------------------------\n";
}

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