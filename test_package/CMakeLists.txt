cmake_minimum_required(VERSION 3.9)
project(NCBIVDBTest)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
#conan_basic_setup(TARGETS)
find_package(ncbi-vdb REQUIRED)

add_executable(ncbi-vdb-test ncbi-vdb-test.cpp)
target_link_libraries(ncbi-vdb-test ${CONAN_LIBS})

enable_testing()
add_test(NAME ncbi-vdb-test COMMAND ncbi-vdb-test
         WORKING_DIRECTORY ${CMAKE_CURRENT_DIRECTORY})
