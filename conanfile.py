from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.microsoft import is_msvc
from conan.tools.files import apply_conandata_patches, export_conandata_patches, get, copy, collect_libs
from conan.tools.cmake import CMakeDeps, CMakeToolchain, CMake, cmake_layout
from conan.tools.scm import Version
import os
import yaml

class NcbiVdb(ConanFile):
    name = "ncbi-vdb"
    description = "The SRA Toolkit and SDK from NCBI is a collection of tools and libraries for using data in the INSDC Sequence Read Archives."
    license = "CC0-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/ncbi/ncbi-vdb"
    topics = ("ncbi", "biotechnology", "bioinformatics", "genbank", "gene", "genome", "genetic", "sequence", "alignment", "biological", "toolkit")
    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared":     [True, False],
        "fPIC":       [True, False]
    }
    default_options = {
        "shared":     False,
        "fPIC":       True
    }

    @property
    def _requirements_filename(self):
        return "requirements.yml"

    @property
    def _vdb_arch(self):
        return "arm64" if str(self.settings.arch) == "armv8" else str(self.settings.arch)

    def export(self):
        copy(self, self._requirements_filename, self.recipe_folder, self.export_folder)

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        requirements_filepath = os.path.join(self.recipe_folder, self._requirements_filename)
        with open(requirements_filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            req = data["requirements"][f"{Version(self.version).major}.{Version(self.version).minor}"]
            for pkg in req:
                self.requires(pkg)

    def validate(self):
        if self.settings.os not in ["Linux", "Macos", "Windows"]:   
            raise ConanInvalidConfiguration("This operating system is not supported")
        if not is_msvc(self) and self.settings.compiler not in ["gcc", "apple-clang"]:
            raise ConanInvalidConfiguration("This compiler is not supported")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root = True)
        apply_conandata_patches(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["_NCBIVDB_CFG_PACKAGING"] = True
        tc.generate()
        cmdep = CMakeDeps(self)
        cmdep.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(variables = {"_NCBIVDB_CFG_PACKAGING" : "ON"})
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        if self.settings.os == "Linux":
            self.cpp_info.includedirs.append( os.path.join("include", "os", "linux"))
            self.cpp_info.includedirs.append( os.path.join("include", "os", "unix"))
        elif self.settings.os == "Macos":
            self.cpp_info.includedirs.append( os.path.join("include", "os", "mac"))
            self.cpp_info.includedirs.append( os.path.join("include", "os", "unix"))
        elif self.settings.os == "Windows":
            self.cpp_info.includedirs.append( os.path.join("include", "os", "win"))

        if self.settings.compiler == "gcc":
            self.cpp_info.includedirs.append( os.path.join("include", "cc", "gcc", self._vdb_arch))
            self.cpp_info.includedirs.append( os.path.join("include", "cc", "gcc"))
        elif self.settings.compiler == "apple-clang":
            self.cpp_info.includedirs.append( os.path.join("include", "cc", "clang", self._vdb_arch))
            self.cpp_info.includedirs.append( os.path.join("include", "cc", "clang"))
        elif is_msvc(self):
            self.cpp_info.includedirs.append( os.path.join("include", "cc", "vc++", self._vdb_arch))
            self.cpp_info.includedirs.append( os.path.join("include", "cc", "vc++"))

        if self.settings.os == "Windows":
            self.cpp_info.system_libs = ["ws2_32", "crypt32"]
        else:
            self.cpp_info.system_libs = ["m", "dl", "pthread"]
        self.cpp_info.libs = collect_libs(self)

