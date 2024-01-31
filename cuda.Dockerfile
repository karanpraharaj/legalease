ARG UBUNTU_VERSION=22.04
# This needs to generally match the container host's environment.
ARG CUDA_VERSION=12.3.1
# Target the CUDA build image
ARG BASE_CUDA_DEV_CONTAINER=nvidia/cuda:${CUDA_VERSION}-devel-ubuntu${UBUNTU_VERSION}
# Target the CUDA runtime image
ARG BASE_CUDA_RUN_CONTAINER=nvidia/cuda:${CUDA_VERSION}-runtime-ubuntu${UBUNTU_VERSION}

FROM ${BASE_CUDA_DEV_CONTAINER} AS build

WORKDIR /usr/local/src

RUN apt-get update && \
    apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN apt update

RUN apt install -y git ffmpeg make g++ vim wget

RUN git clone https://github.com/karanpraharaj/legalease.git --depth 2

# Unless otherwise specified, we make a fat build.
ARG CUDA_DOCKER_ARCH=sm_75
# Set nvcc architecture
ENV CUDA_DOCKER_ARCH=${CUDA_DOCKER_ARCH}
# Enable cuBLAS
ENV WHISPER_CUBLAS=1

RUN apt-get update && \
    apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Ref: https://stackoverflow.com/a/53464012
ENV CUDA_MAIN_VERSION=12.3
ENV LD_LIBRARY_PATH /usr/local/cuda-${CUDA_MAIN_VERSION}/compat:$LD_LIBRARY_PATH

# COPY .. .
WORKDIR /usr/local/src/legalease/components/whisper.cpp
RUN make

FROM ${BASE_CUDA_RUN_CONTAINER} AS runtime
WORKDIR /usr/local/src/legalease/components/whisper.cpp

# Copy the built binary from the build stage
COPY --from=build /usr/local/src/legalease/components/whisper.cpp /usr/local/src/legalease/components/whisper.cpp

RUN apt-get update && \
    apt-get install -y curl ffmpeg \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

ENTRYPOINT [ "bash", "-c" ]
