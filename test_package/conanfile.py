import os
from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.build import cross_building

class NcbiVdbTest(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain", "VirtualBuildEnv", "VirtualRunEnv"
    apply_env = False
    test_type = "explicit"
    requires = [
        ("ncbi-vdb/3.0.0")
    ]

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if not cross_building(self):
            self.run(os.path.join(self.cpp.build.bindirs[0], "ncbi-vdb-test") + " \"" + os.path.join(self.recipe_folder, "SRR.sra\""),  env="conanrun")
