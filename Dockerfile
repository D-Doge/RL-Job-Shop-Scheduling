FROM nvidia/cuda:11.2.0-devel-ubuntu18.04
WORKDIR /jobshop
#COPY . .
#Install Python 3.7
RUN apt update && apt install software-properties-common -y
RUN add-apt-repository 'ppa:deadsnakes/ppa'
RUN apt install python3.7 -y

#Install pip
RUN sudo apt-get install python3-pip -y

#Install cmake
RUN apt-get install wget -y
RUN apt-get install build-essential libssl-dev
RUN cd /tmp && wget https://github.com/Kitware/CMake/releases/download/v3.20.0/cmake-3.20.0.tar.gz && tar -zxvf cmake-3.20.0.tar.gz && cd cmake-3.20.0 && ./bootstrap && make && make install

#Install zlib1g
RUN apt install zlib1g

#Install zlib1g-dev
RUN apt install zlib1g-dev

CMD ["/bin/bash"]