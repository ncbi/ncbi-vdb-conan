import os
from conans import ConanFile, CMake, tools

class NcbiVdbTest(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "cmake_find_package"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self):
            if self.settings.compiler == "Visual Studio":
                self.run("ctest -C " + str(self.settings.build_type))
            else:
                self.run("ctest")

