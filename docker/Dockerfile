# Stage 1: install Source SDK Base 2013 via SteamCMD (appid 244310)
# This SDK ships the `vpk` command-line tool used to build addon VPKs.
FROM steamcmd/steamcmd:ubuntu-24 AS sdk

RUN steamcmd \
    +force_install_dir /opt/sdk \
    +login anonymous \
    +app_update 244310 validate \
    +quit

# Sanity-check: show what vpk binaries were installed (useful if path changes)
RUN find /opt/sdk/bin -name "vpk*" -type f

# Stage 2: minimal runtime image — copy only the vpk binary
FROM ubuntu:24.04

# lib32 shims needed because the Source SDK vpk binary is 32-bit
RUN apt-get update && apt-get install -y --no-install-recommends \
    lib32gcc-s1 \
    lib32stdc++6 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=sdk /opt/sdk/bin/vpk /usr/local/bin/vpk
RUN chmod +x /usr/local/bin/vpk

WORKDIR /workspace
ENTRYPOINT ["/bin/bash"]
