FROM ubuntu:22.04 AS build
WORKDIR /usr/local/src

RUN apt-get update && \
    apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN apt update

RUN apt install -y git ffmpeg make g++ vim wget

RUN git clone https://github.com/karanpraharaj/legalease.git --depth 2

# whisper.cpp setup
WORKDIR /usr/local/src/legalease/components/whisper.cpp
RUN make

FROM ubuntu:22.04 AS runtime
WORKDIR /usr/local/src/legalease/components/whisper.cpp

# Copy the built binary from the build stage
COPY --from=build /usr/local/src/legalease/components/whisper.cpp /usr/local/src/legalease/components/whisper.cpp

RUN apt-get update && \
    apt-get install -y curl ffmpeg \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

ENTRYPOINT [ "bash", "-c" ]