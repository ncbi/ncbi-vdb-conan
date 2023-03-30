cmake_minimum_required(VERSION 3.16)
project(test_package)

find_package(ncbi-vdb REQUIRED)
add_executable(${PROJECT_NAME} ncbi-vdb-test.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE ncbi-vdb::ncbi-vdb)
