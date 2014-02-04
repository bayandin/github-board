#!/usr/bin/env bash

LIBGIT2_VERSION="0.20.0"

cd ~/
wget https://github.com/libgit2/libgit2/archive/v${LIBGIT2_VERSION}.tar.gz
tar -xf v${LIBGIT2_VERSION}.tar.gz
mv libgit2{-${LIBGIT2_VERSION},}

cd libgit2
mkdir build && cd $_
cmake .. -DCMAKE_INSTALL_PREFIX=../_install -DBUILD_CLAR=OFF
cmake --build . --target install
