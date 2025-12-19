### Quantitative Risk Engine for CCR & XVA
A hybrid C++/Python risk engine that performs Monte Carlo simulations for Risk factor Simulations. Uses the simulated factors to price traded derivatives to generate the mark-to-market (MtM) matrices. The matrices are used to generate exposure profiles and aggregated to give Counterparty Credit Risk and XVA measures. It uses Apache Beam (python) to orchestrate the runs.


### Architecture Core: 
C++17 (Monte Carlo Simulation, Pricing)

### Orchestration: 
Python 3.9+ (Apache Beam)


### Data Contract: 
Protocol Buffers (protobuf)

### Binding: 
PyBind11

### Prerequisites
Visual Studio 2022 (Desktop Development with C++)
CMake 3.15+
Python 3.9+
Protoc Compiler (Must match the Python protobuf package version - recommended is 5.29.0)
May need to use vcpkg manager to install dependencies for C++ build (e.g., protobuf, pybind11). The protbuf package needs to be downloaded from google.
### Setup Instructions
#### 1. Install Dependencies: 
	pip install apache-beam numpy protobuf pybind11

#### 2. Generate Python Data Contracts:
##### The C++ build handles the C++ protos automatically, but you must generate the Python ones manually: 
	cd src/proto 
	protoc --python_out=../python risk_models.proto

#### 3. Build the C++ Engine:
Open the project in Visual Studio 2022. Select x64-Release configuration. Build -> Build All.
Verify that CppRiskEngine.pyd was created in src/python

#### 4. Run the Pipeline 
	cd src/python 
	python beam_pipeline.py
