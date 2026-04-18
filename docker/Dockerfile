# Stage 1: install L4D2 Dedicated Server via SteamCMD (appid 222860)
# Ships the `vpk` command-line tool used to build addon VPKs.
FROM steamcmd/steamcmd:ubuntu-24 AS sdk

RUN steamcmd \
    +force_install_dir /opt/sdk \
    +login anonymous \
    +app_update 222860 validate \
    +quit

# Sanity-check: show what vpk binaries were installed
RUN find /opt/sdk/bin -name "vpk*" -type f

# Stage 2: minimal runtime image
FROM ubuntu:24.04

# lib32 shims needed because the Source SDK vpk binary is 32-bit
RUN apt-get update && apt-get install -y --no-install-recommends \
    lib32gcc-s1 \
    lib32stdc++6 \
    && rm -rf /var/lib/apt/lists/*

# NOTE: Claude wrote this only with trained data but looks sus
# Copy whole bin dir: vpk wrapper depends on vpk_linux32, libtier0.so, libvstdlib.so
COPY --from=sdk /opt/sdk/bin /opt/sdk/bin
RUN ln -s /opt/sdk/bin/vpk /usr/local/bin/vpk

WORKDIR /workspace
ENTRYPOINT ["/bin/bash"]
