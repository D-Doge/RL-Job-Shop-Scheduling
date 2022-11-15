FROM nvidia/cuda:11.2.0-devel-ubuntu18.04
WORKDIR /jobshop
#COPY . .
RUN apt update && apt install software-properties-common -y
RUN add-apt-repository 'ppa:deadsnakes/ppa'
RUN apt install python3.7 -y

RUN python3.7 --version
CMD ["/bin/bash"]