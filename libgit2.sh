#!/usr/bin/env bash
cd ~
wget https://github.com/libgit2/libgit2/archive/v0.20.0.tar.gz
tar -xf v0.20.0.tar.gz
mv libgit2{-0.20.0,} && cd libgit2
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../_install -DBUILD_CLAR=OFF
cmake --build . --target install
