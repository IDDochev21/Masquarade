#pragma once
#include <iostream>
#include <fstream>
#include <string>

void printLine();

bool doesUserExist(const std::string& username, std::ifstream& file);
