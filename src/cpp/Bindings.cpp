#include <pybind11/pybind11.h>
#include "Engine.hpp"

namespace py = pybind11;

// Wrapper function to handle bytes directly
py::bytes calculate_risk_wrapper(py::bytes input_bytes) {
    std::string req_str = input_bytes;
    std::string resp_str;

    RiskEngine::Pricer::CalculateRisk(req_str, resp_str);

    return py::bytes(resp_str);
}

PYBIND11_MODULE(CppRiskEngine, m) {
    m.doc() = "High-performance C++ Risk Engine backend";
    m.def("calculate_risk", &calculate_risk_wrapper, "Calculates PV and PFE from a serialized TradeRequest");
}