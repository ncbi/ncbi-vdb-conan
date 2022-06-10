cmake_minimum_required(VERSION 3.15)
project(NCBIVDBTest)

find_package(ncbi-vdb REQUIRED)
add_executable(ncbi-vdb-test ncbi-vdb-test.cpp)
target_link_libraries(ncbi-vdb-test ncbi-vdb::ncbi-vdb)
