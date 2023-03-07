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
            bindir = os.path.join(self.build_folder, str(self.settings.build_type))
            bin = bindir if os.path.exists(bindir) else self.build_folder
            self.run(os.path.join(bin, "ncbi-vdb-test") + " \"" + os.path.join(self.recipe_folder, "SRR.sra\""),  run_environment=True)
