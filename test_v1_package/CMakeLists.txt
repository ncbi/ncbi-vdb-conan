cmake_minimum_required(VERSION 3.16)
project(NCBIVDBTest)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)
add_executable(ncbi-vdb-test ncbi-vdb-test.cpp)
target_link_libraries(ncbi-vdb-test CONAN_PKG::ncbi-vdb)
