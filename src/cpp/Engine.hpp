#pragma once
#include <vector>
#include <string>
#include <random>
#include <cmath>

namespace RiskEngine {

    // Helper for Monte Carlo
    class Simulator {
    public:
        // Returns a vector of simulated spot prices at maturity
        static std::vector<double> SimulateGBM(double S0, double r, double sigma, double T, int num_paths);
    };

    class Pricer {
    public:
        // Prices a trade and calculates PFE using simulations
        static void CalculateRisk(const std::string& serialized_request, std::string& serialized_response);
    };
}