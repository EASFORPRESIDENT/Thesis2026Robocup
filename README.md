# Thesis2026Robocup

## System requirements
- Ubuntu 24.04

- Python 3.10+

- GCC / G++ 11+

- CMake 3.20+

- Qt 5.x

- Boost 1.70+


## Dependencies


```
sudo apt update

sudo apt install -y \
build-essential \
cmake \
git \
python3 \
python3-pip \
flex \
bison \
zlib1g-dev \
libboost-dev \
libboost-system-dev \
libboost-filesystem-dev \
libboost-all-dev \
qtbase5-dev \
qt5-qmake \
libfontconfig1-dev \
libaudio-dev \
libxt-dev \
libglib2.0-dev \
libxi-dev \
libxrender-dev
```
### Step 1
Clone the repo

`git clone https://github.com/EASFORPRESIDENT/Thesis2026Robocup.git`

## 2
```
mkdir -p ~/local/bin ~/local/lib ~/local/include

grep -q 'export PATH="$HOME/local/bin:$PATH"' ~/.profile || \
  echo 'export PATH="$HOME/local/bin:$PATH"' >> ~/.profile

grep -q 'export LD_LIBRARY_PATH="$HOME/local/lib:$LD_LIBRARY_PATH"' ~/.bashrc || \
  echo 'export LD_LIBRARY_PATH="$HOME/local/lib:$LD_LIBRARY_PATH"' >> ~/.bashrc

source ~/.profile
source ~/.bashrc
```

## Step 2
OBS! All steps from here is executed from the `Thesis2026Robocup` dir.
Build librcsc
```
(
cd librcsc
git checkout support-v18
./bootstrap
./configure --prefix=$HOME/local --disable-unit-test
make -j"$(nproc)"
make install
)
```
## 3
Build Soccerwindow
```
(
cd soccerwindow2
./bootstrap
./configure --prefix="$HOME/local" --with-librcsc="$HOME/local"
make -j"$(nproc)"
make install
)
```
## 4
Build HFO environment
```
(
cd HFO
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=RelwithDebInfo -DBUILD_SOCCERWINDOW=False ..
make -j"$(nproc)"
make install
)
```



## Step 3
Link to files.

`ln -sf ~/local/bin/sswindow2 $(pwd)/HFO/bin/soccerwindow2`

```
grep -q 'HFO/lib' ~/.bashrc || \
  echo 'export LD_LIBRARY_PATH="$(pwd)/HFO/lib:$LD_LIBRARY_PATH"' >> ~/.bashrc

source ~/.bashrc
```





