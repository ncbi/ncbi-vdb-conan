from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
from conan.tools import files
import os

class NcbiVdb(ConanFile):
    name = "ncbi-vdb"
    license = "CC0-1.0 todo"
    homepage = "https://github.com/ncbi/ncbi-vdb"
    url = "https://github.com/conan-io/conan-center-index"
    description = "The SRA Toolkit and SDK from NCBI is a collection of libraries for using data in the INSDC Sequence Read Archives."
    topics = ("ncbi", "todo")
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

#----------------------------------------------------------------------------
    def set_version(self):
        if self.version == None:
            self.version = "3.0.0"
#----------------------------------------------------------------------------
    @property
    def _source_subfolder(self):
        return self.name + "-" + self.version

    @property
    def _build_subfolder(self):
        return "b"

#----------------------------------------------------------------------------
    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["LIBS_ONLY"] = "TRUE"
        return cmake

#----------------------------------------------------------------------------
    def validate(self):
        if self.settings.os not in ["Linux", "Macos", "Windows"]:   
            raise ConanInvalidConfiguration("This operating system is not supported")
        if self.settings.compiler not in ["gcc", "apple-clang", "Visual Studio"]:   
            raise ConanInvalidConfiguration("This compiler is not supported")
        if hasattr(self, "settings_build") and tools.cross_building(self, skip_x64_x86=True):
            raise ConanInvalidConfiguration("Cross compilation is not supported")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

#----------------------------------------------------------------------------
    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root = False)

#----------------------------------------------------------------------------
    def build(self):
        cmake = self._configure_cmake()
        cmake.configure(source_folder=self._source_subfolder, build_folder = self._build_subfolder)
        cmake.build()

#----------------------------------------------------------------------------
    def package(self):
        self.copy("*.*", "include", os.path.join(self._source_subfolder, "interfaces"))
        self.copy("LICENSE", "licenses", self._source_subfolder)
        if self.settings.compiler == "Visual Studio":
            if self.options.shared:
                self.copy("ncbi*.dll", "bin", os.path.join(self._build_subfolder, str(self.settings.build_type),"bin"))
                self.copy("ncbi*.lib", "lib", os.path.join(self._build_subfolder, str(self.settings.build_type),"bin"))
                self.copy("ncbi*.exp", "lib", os.path.join(self._build_subfolder, str(self.settings.build_type),"bin"))
            else:
                self.copy("ncbi*.*", "lib", os.path.join(self._build_subfolder, str(self.settings.build_type),"lib"))
        else:
            prefix = "lib"
            suffix = ".a" if not self.options.shared else (".dylib" if self.settings.os == "Macos" else ".so")
            src_suffix = ("." + self.version + suffix) if (self.options.shared and self.settings.os == "Macos") else (suffix + "." + self.version)
            package_libs = ["ncbi-vdb", "ncbi-wvdb"]
            files.mkdir(self, os.path.join(self.package_folder, "lib"))
            for lib in package_libs:
                src  = os.path.join(self.build_folder, self._build_subfolder, "lib", prefix + lib + src_suffix)
                dest = os.path.join(self.package_folder, "lib", prefix + lib + suffix)
                files.rename(self,src,dest)

#----------------------------------------------------------------------------
    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.system_libs = ["ws2_32", "crypt32"]
        else:
            self.cpp_info.system_libs = ["m", "dl", "pthread"]
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
            self.cpp_info.libs = tools.collect_libs(self)
        elif self.settings.compiler == "apple-clang":
            self.cpp_info.includedirs.append( os.path.join("include", "cc", "clang", str(self.settings.arch)))
            self.cpp_info.includedirs.append( os.path.join("include", "cc", "clang"))
            self.cpp_info.libs = tools.collect_libs(self)
        elif self.settings.compiler == "Visual Studio":
            self.cpp_info.includedirs.append( os.path.join("include", "cc", "vc++", str(self.settings.arch)))
            self.cpp_info.includedirs.append( os.path.join("include", "cc", "vc++"))
            if not self.options.shared  or "MT" in self.settings.compiler.runtime:
                self.cpp_info.libs = ["ncbi-vdb", "ncbi-wvdb"]
            else:
                self.cpp_info.libs = ["ncbi-vdb-md", "ncbi-wvdb-md"]

