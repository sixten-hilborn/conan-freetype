[![Build Status](https://travis-ci.org/sixten-hilborn/conan-freetype.svg?branch=release/2.6.3)](https://travis-ci.org/sixten-hilborn/conan-freetype)
[![Build status](https://ci.appveyor.com/api/projects/status/3ojrl9s1umgr09jw?svg=true)](https://ci.appveyor.com/project/sixten-hilborn/conan-freetype)

# conan-freetype

[Conan.io](https://conan.io) package for freetype library

The packages generated with this **conanfile** can be found in [conan.io](https://conan.io/source/freetype/2.6.3/hilborn/stable).

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py

## Upload packages to server

    $ conan upload freetype/2.0.3@hilborn/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install freetype/2.0.3@hilborn/stable
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    freetype/2.0.3@hilborn/stable

    [options]
    freetype:shared=True # False
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install .

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
