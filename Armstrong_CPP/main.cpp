#include <iostream>
#include <tuple>
#include <cmath>
#include <vector>
#include <chrono>
#include <iomanip>  // Für setprecision und fixed
#include <future>

//TODO: Implement Multithreading

std::tuple<bool, int> calculateArmstrongNumber(int number);
std::tuple<bool, int> calculateFastArmstrongNumber(int number);

int main() {
    
    std::vector<int> armstrongNumbers;
    
    auto start = std::chrono::high_resolution_clock::now();
    
    const int TOTALRUNS = 1000000;
    
    for (int i=0; i <= TOTALRUNS ; i++) {
        auto [isArm, total] = calculateFastArmstrongNumber(i);
        if (isArm) {
            armstrongNumbers.push_back(total);
        }
    }
    
    auto end = std::chrono::high_resolution_clock::now();

    // Umrechnung in Sekunden als double
    std::chrono::duration<double> elapsed_seconds = end - start;
    
    for (auto num: armstrongNumbers) {
        std::cout << num << ' ';
    }
    
    std::cout << "\n\nBenchmark-Ergebnis:";
    std::cout << std::fixed << std::setprecision(6); // Zeigt 6 Nachkommastellen
    std::cout << "C++ Zeit: " << elapsed_seconds.count() << " Sekunden" << std::endl;
    
    return EXIT_SUCCESS;
}

std::tuple<bool, int> calculateArmstrongNumber(int number) {
    //Guard for zero
    if (number == 0) return {false, 0};
    
    int tempNumber = number;
    double total = 0;
    int numberLength = std::floor(std::log10(number)) + 1;
    std::vector<int> digits;
    
    while (tempNumber > 0) {
        digits.push_back(tempNumber % 10);
        tempNumber /= 10;
    }
    
    for (int digit: digits) {
        total += std::pow(digit, numberLength);
    }
    
    int finalTotal = static_cast<int>(total);
    
    return { (number == finalTotal), finalTotal};
    
}

std::tuple<bool, int> calculateFastArmstrongNumber(int number) {
    if (number <= 0) return {number == 0, 0};
    
    int tempNumber = number;
    int numberLength = static_cast<int>(std::log10(number)) + 1;
    int total = 0;
    
    while (tempNumber > 0) {
        int digit = tempNumber % 10;
        
        // Schnelle Potenzierung für Integers
        int p = 1;
        for(int j = 0; j < numberLength; ++j) p *= digit;
        
        total += p;
        tempNumber /= 10;
    }
    
    return { (number == total), total };
}
