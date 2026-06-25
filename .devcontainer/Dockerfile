ARG MECHANICAL_IMAGE=ghcr.io/ansys/mechanical:26.1.0
FROM ${MECHANICAL_IMAGE}

# xvfb and tini are already present in the base image.
# Install git and curl for repo operations and uv bootstrap.
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Etc/UTC
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        curl \
        ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install uv into /usr/local/bin so it is on PATH for all users.
ARG UV_VERSION=0.7.0
RUN curl -LsSf https://astral.sh/uv/install.sh | UV_INSTALL_DIR=/usr/local/bin sh

# Pre-download the target CPython version so postCreateCommand is fast.
ARG PYTHON_VERSION=3.12
RUN uv python install ${PYTHON_VERSION}

# Override the Workbench gRPC entrypoint so the container can idle in bash.
ENTRYPOINT []
CMD ["sleep", "infinity"]

# Work from /workspaces (standard Codespaces mount point).
WORKDIR /workspaces
