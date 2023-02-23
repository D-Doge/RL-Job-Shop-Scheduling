FROM nvidia/cuda:11.2.0-devel-ubuntu18.04
WORKDIR /jobshop

#We could also build the repository into the workdir instead of mounting
#COPY . .

#Install Python 3.7
RUN apt update && apt install software-properties-common -y
RUN add-apt-repository 'ppa:deadsnakes/ppa'
RUN apt install python3.7 -y

#Install pip
RUN apt-get install python3-pip -y

#Install cmake
RUN apt-get install wget -y
RUN apt-get install build-essential libssl-dev -y
RUN cd /tmp && wget https://github.com/Kitware/CMake/releases/download/v3.20.0/cmake-3.20.0.tar.gz && tar -zxvf cmake-3.20.0.tar.gz && cd cmake-3.20.0 && ./bootstrap && make && make install

#Install zlib1g
RUN apt install zlib1g -y

#Install zlib1g-dev
RUN apt install zlib1g-dev -y

#Upgrade pip
RUN python3.7 -m pip install --upgrade pip

#Install requermtens
COPY ./requirements.txt /tmp
RUN cd /tmp && python3.7 -m pip install -r requirements.txt

RUN apt-get install ffmpeg libsm6 libxext6  -y

CMD ["/bin/bash"]