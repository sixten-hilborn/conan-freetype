from conans import ConanFile, CMake
from conans.errors import ConanException
from conans.tools import download, unzip, replace_in_file
import os
import shutil

class FreetypeConan(ConanFile):
    name = "freetype"
    version = "2.6.3"
    folder = "freetype-%s" % version
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = '''shared=False
    fPIC=True'''
    generators = "cmake"
    url="http://github.com/sixten-hilborn/conan-freetype"
    license="MIT"
    requires = "libpng/1.6.23@lasote/ci", "bzip2/1.0.6@lasote/stable"

    def config(self):
        del self.settings.compiler.libcxx 
        if self.settings.compiler == "Visual Studio" and self.options.shared:
            raise ConanException("The freetype lib does not support creation of SHARED libs with Visual Studio")

    def source(self):
        zip_name = "%s.tar.gz" % self.folder
        download("http://downloads.sourceforge.net/project/freetype/freetype2/2.6.3/%s" % zip_name, zip_name)
        unzip(zip_name)
        fPIC = "set(CMAKE_POSITION_INDEPENDENT_CODE ON)" if self.options.fPIC else ""
        replace_in_file("freetype-%s/CMakeLists.txt" % self.version,
                        "project(freetype)",
                        """project(freetype)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
%s""" % fPIC)

    def build(self):
        cmake = CMake(self.settings)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        self.run('cmake freetype-%s %s %s -DWITH_ZLIB=ON -DWITH_PNG=ON' % (self.version, cmake.command_line, shared))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        """ Define your conan structure: headers, libs and data. After building your
            project, this method is called to create a defined structure:
        """
        self.copy(pattern="*.h", dst="include", src="%s/include" % self.folder, keep_path=True)
        self.copy("*freetype*.lib", dst="lib", keep_path=False)
        if self.options.shared:
            self.copy(pattern="*.so*", dst="lib", keep_path=False)
            self.copy(pattern="*.dylib*", dst="lib", keep_path=False)
            self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.build_type == "Debug":
            libname = "freetyped"
        else:
            libname = "freetype"
        self.cpp_info.libs = [libname]
