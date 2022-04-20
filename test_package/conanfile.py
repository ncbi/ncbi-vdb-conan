import os
from conans import ConanFile, CMake, tools

class NcbiVdbTest(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "cmake_find_package"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.sra", src=self.recipe_folder)

    def test(self):
        if not tools.cross_building(self):
            self.run(os.path.join("bin", "ncbi-vdb-test"),  run_environment=True)
