from conans import ConanFile
from conans.errors import ConanException
from conans.tools import download, unzip, replace_in_file
import os
import shutil
from conans import CMake, ConfigureEnvironment

class FreetypeConan(ConanFile):
    name = "freetype"
    version = "2.6.3"
    folder = "freetype-%s" % version
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = '''shared=False
    fPIC=True'''
    generators = "cmake"
    url="http://github.com/lasote/conan-freetype"
    license="MIT"
    requires = "libpng/1.6.23@lasote/stable", "bzip2/1.0.6@lasote/stable"

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


    def build_with_make(self):
        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
        if self.options.fPIC:
            env_line = env.command_line.replace('CFLAGS="', 'CFLAGS="-fPIC ')
        else:
            env_line = env.command_line
            
        custom_vars = "LIBPNG_LIBS=0 BZIP2_LIBS=0" # Trick: This way it didn't look for system libs and take the env variables from env_line
                
        self.run("cd %s" % self.folder)
        
        self.output.warn(env_line)
        if self.settings.os == "Macos": # Fix rpath, we want empty rpaths, just pointing to lib file
            old_str = "-install_name \$rpath/"
            new_str = "-install_name "
            replace_in_file("%s/builds/unix/configure" % self.folder, old_str, new_str)
            
        libpng_libs = 'LIBPNG_LIBS=%s'
        
        configure_command = 'cd %s && %s ./configure --with-harfbuzz=no %s' % (self.folder, env_line, custom_vars)
        self.output.warn("Configure with: %s" % configure_command)
        self.run(configure_command)
        self.run("cd %s && %s make" % (self.folder, env_line))


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
