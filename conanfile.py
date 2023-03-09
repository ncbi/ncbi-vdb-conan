from conan import ConanFile
from conan.tools.cmake import CMakeDeps, CMakeToolchain, CMake, cmake_layout
from conan.errors import ConanInvalidConfiguration
from conan import tools
import os
import yaml

class NcbiVdb(ConanFile):
    name = "ncbi-vdb"
    license = "CC0-1.0"
    homepage = "https://github.com/ncbi/ncbi-vdb"
    url = "https://github.com/conan-io/conan-center-index"
    description = "The SRA Toolkit and SDK from NCBI is a collection of tools and libraries for using data in the INSDC Sequence Read Archives."
    topics = ("ncbi", "biotechnology", "bioinformatics", "genbank", "gene", "genome", "genetic", "sequence", "alignment", "biological", "toolkit")
    settings = "os", "compiler", "build_type", "arch"

    options = {
        "shared":     [True, False],
        "fPIC":       [True, False]
    }
    default_options = {
        "shared":     False,
        "fPIC":       True
    }

#----------------------------------------------------------------------------
    @property
    def _requirements_filename(self):
        return "requirements.yml"

    def export(self):
        tools.files.copy(self, self._requirements_filename, self.recipe_folder, self.export_folder)

    def export_sources(self):
        tools.files.export_conandata_patches(self)

    def validate(self):
        if self.settings.os not in ["Linux", "Macos", "Windows"]:   
            raise ConanInvalidConfiguration("This operating system is not supported")
        if not tools.microsoft.is_msvc(self) and self.settings.compiler not in ["gcc", "apple-clang"]:
            raise ConanInvalidConfiguration("This compiler is not supported")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)
        self.folders.source = "."

    def requirements(self):
        requirements_filepath = os.path.join(self.recipe_folder, self._requirements_filename)
        data = yaml.safe_load(open(requirements_filepath))
        req = data["requirements"][self.version]
        for pkg in req:
            self.requires(pkg)

    def source(self):
        tools.files.get(self, **self.conan_data["sources"][self.version], strip_root = True)
        tools.files.apply_conandata_patches(self)

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
            self.cpp_info.includedirs.append( os.path.join("include", "cc", "gcc", str(self.settings.arch)))
            self.cpp_info.includedirs.append( os.path.join("include", "cc", "gcc"))
        elif self.settings.compiler == "apple-clang":
            self.cpp_info.includedirs.append( os.path.join("include", "cc", "clang", str(self.settings.arch)))
            self.cpp_info.includedirs.append( os.path.join("include", "cc", "clang"))
        elif tools.microsoft.is_msvc(self):
            self.cpp_info.includedirs.append( os.path.join("include", "cc", "vc++", str(self.settings.arch)))
            self.cpp_info.includedirs.append( os.path.join("include", "cc", "vc++"))

        if self.settings.os == "Windows":
            self.cpp_info.system_libs = ["ws2_32", "crypt32"]
        else:
            self.cpp_info.system_libs = ["m", "dl", "pthread"]
        self.cpp_info.libs = tools.files.collect_libs(self)

