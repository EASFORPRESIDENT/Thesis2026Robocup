mkdir -p ~/local/bin ~/local/lib ~/local/include

grep -q 'export PATH="$HOME/local/bin:$PATH"' ~/.profile || \
  echo 'export PATH="$HOME/local/bin:$PATH"' >> ~/.profile

grep -q 'export LD_LIBRARY_PATH="$HOME/local/lib:$LD_LIBRARY_PATH"' ~/.bashrc || \
  echo 'export LD_LIBRARY_PATH="$HOME/local/lib:$LD_LIBRARY_PATH"' >> ~/.bashrc

source ~/.profile
source ~/.bashrc

(
cd librcsc
git checkout support-v18
./bootstrap
./configure --prefix=$HOME/local --disable-unit-test
make -j"$(nproc)"
make install
)

(
cd soccerwindow2
./bootstrap
./configure --prefix="$HOME/local" --with-librcsc="$HOME/local"
make -j"$(nproc)"
make install
)

(
cd HFO
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=RelwithDebInfo -DBUILD_SOCCERWINDOW=False ..
make -j"$(nproc)"
make install
)

grep -q 'HFO/lib' ~/.bashrc || \
  echo 'export LD_LIBRARY_PATH="$(pwd)/HFO/lib:$LD_LIBRARY_PATH"' >> ~/.bashrc

source ~/.bashrc
