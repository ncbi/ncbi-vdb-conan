from conans import ConanFile, CMake
from conan.tools.build import cross_building
import os

class NcbiVdbTestV1Conan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake", "cmake_find_package_multi"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if not cross_building(self):
            bin_path = os.path.join("bin", "test_package")
            bin_path += " \"" + os.path.join(self.recipe_folder, "..", "test_package", "SRR.sra\"")
            self.run(bin_path, run_environment=True)
