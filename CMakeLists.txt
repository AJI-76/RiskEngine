cmake_minimum_required(VERSION 3.15)
project(RiskEngine)

set(CMAKE_CXX_STANDARD 17)

# 1. Find Dependencies
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(Protobuf CONFIG REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

# 2. Setup Protobuf generation for C++
file(GLOB PROTO_FILES "src/proto/*.proto")
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ${PROTO_FILES})

# 3. Create the Python Extension Module
pybind11_add_module(CppRiskEngine
    src/cpp/Bindings.cpp
    src/cpp/Engine.cpp
    ${PROTO_SRCS}
    ${PROTO_HDRS}
)

# 4. Link Libraries
target_include_directories(CppRiskEngine PRIVATE src/cpp ${CMAKE_CURRENT_BINARY_DIR})
target_link_libraries(CppRiskEngine PRIVATE protobuf::libprotobuf pybind11::module)

# 5. Output Location (so Python can find the .pyd file easily)
set_target_properties(CppRiskEngine PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/python"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/python"
    ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
)

if(MSVC)
    # Emit PDBs into the build directory rather than the source deployment directory
    set_target_properties(CppRiskEngine PROPERTIES
        PDB_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/pdb"
    )
endif()

add_custom_command(TARGET CppRiskEngine POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
    $<TARGET_FILE:CppRiskEngine>
    "${CMAKE_SOURCE_DIR}/src/python/$<TARGET_FILE_NAME:CppRiskEngine>"
    COMMENT "Copying compiled Python extension to src/python..."
)