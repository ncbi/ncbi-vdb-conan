from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
from conan.tools import files
import os

class NcbiVdb(ConanFile):
    name = "ncbi-vdb"
    license = "CC0-1.0"
    homepage = "https://github.com/ncbi/ncbi-vdb"
    url = "https://github.com/conan-io/conan-center-index"
    description = "The SRA Toolkit and SDK from NCBI is a collection of tools and libraries for using data in the INSDC Sequence Read Archives."
    topics = ("ncbi", "biotechnology", "bioinformatics", "genbank", "gene", "genome", "genetic", "sequence", "alignment", "biological", "toolkit")
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "cmake_find_package"

    options = {
        "shared":     [True, False],
        "fPIC":       [True, False]
    }
    default_options = {
        "shared":     False,
        "fPIC":       True
    }
    requires = [
        ("bzip2/1.0.8"),
        ("zlib/1.2.12"),
        ("zstd/1.5.2")
    ]
#----------------------------------------------------------------------------
    def set_version(self):
        if self.version == None:
            self.version = "3.0.0"
#----------------------------------------------------------------------------
    @property
    def _source_subfolder(self):
#        return self.name + "-" + self.version
# with git clone, use dot
        return "."

    @property
    def _build_subfolder(self):
        return "b"

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["LIBS_ONLY"] = "TRUE"
        cmake.definitions["_NCBIVDB_CFG_PACKAGING"] = "TRUE"
        return cmake

    def validate(self):
        if self.settings.os not in ["Linux", "Macos", "Windows"]:   
            raise ConanInvalidConfiguration("This operating system is not supported")
        if self.settings.compiler not in ["gcc", "apple-clang", "Visual Studio"]:   
            raise ConanInvalidConfiguration("This compiler is not supported")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def source(self):
#        tools.get(**self.conan_data["sources"][self.version], strip_root = False)

# see also _source_subfolder
        tk_git = self.conan_data["sources"][self.version]["git"] if "git" in self.conan_data["sources"][self.version].keys() else ""
        git = tools.Git()
        git.clone(tk_git, branch = "master", args = "--single-branch", shallow = True)

    def build(self):
        cmake = self._configure_cmake()
        cmake.configure(source_folder=self._source_subfolder, build_folder = self._build_subfolder)
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install(build_dir = self._build_subfolder)

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
        elif self.settings.compiler == "Visual Studio":
            self.cpp_info.includedirs.append( os.path.join("include", "cc", "vc++", str(self.settings.arch)))
            self.cpp_info.includedirs.append( os.path.join("include", "cc", "vc++"))

        if self.settings.os == "Windows":
            self.cpp_info.system_libs = ["ws2_32", "crypt32"]
        else:
            self.cpp_info.system_libs = ["m", "dl", "pthread"]
        self.cpp_info.libs = tools.collect_libs(self)

