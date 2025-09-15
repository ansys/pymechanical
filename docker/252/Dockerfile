FROM ubuntu:20.04

ARG VERSION

# LABELS
LABEL description="Mechanical on Ubuntu"
LABEL email="pyansys.core@ansys.com"

# OCI LABELS
LABEL org.opencontainers.image.documentation="https://mechanical.docs.pyansys.com"

RUN apt-get update && apt-get install -y \
    libxt6 \
    libsm6 \
    libice6 \
    libx11-6 \
    libx11-xcb1 \
    libxext6 \
    openssl \
    openssh-client \
    libcairo2 \
    elfutils \
    expat \
    fontconfig \
    libglib2.0-0 \
    libc-bin \
    libc6 \
    jbigkit-bin \
    libxau6 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrender1 \
    libxxf86vm1 \
    libxi6 \
    libdrm-common \
    libdrm2 \
    libjpeg-turbo8 \
    libselinux1 \
    libtiff5 \
    libxcb1 \
    libxshmfence1 \
    libglx-mesa0 \
    libosmesa6 \
    libgl1 \
    libgl1-mesa-dri \
    libgl1-mesa-glx \
    libglu1 \
    libglu1-mesa \
    libegl1-mesa \
    libglapi-mesa \
    libpcre2-8-0 \
    libpixman-1-0 \
    libmotif-common \
    libxm4 \
    libgfortran4 \
    libgfortran5 \
    xvfb \
    tini \
    ca-certificates \
    libgomp1 \
    libtirpc3 \
    locales \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && locale-gen en_US.UTF-8 \
    && locale-gen fr_FR.utf8 \
    && locale-gen de_DE.utf8 \
    && locale-gen ja_JP.utf8 \
    && locale-gen zh_CN.utf8

# Copying files
WORKDIR /install/

COPY . .

# License server
# (Optional)
# ENV LICENSE_SERVER=111.222.333.444
# ENV ANSYSLMD_LICENSE_FILE=1055@$LICENSE_SERVER

ENV ANSYS_VERSION=${VERSION} \
    ANSYS${VERSION}_DIR=/install/ansys_inc/v${VERSION}/ansys \
    AWP_ROOT${VERSION}=/install/ansys_inc/v${VERSION} \
    CADOE_LIBDIR${VERSION}=/install/ansys_inc/v${VERSION}/commonfiles/Language/en-us \
    ANSYS_WORKBENCH_LOGGING=1 \
    ANSYS_WORKBENCH_LOGGING_FILTER_LEVEL=0 \
    ANSYS_WORKBENCH_LOGGING_AUTO_FLUSH=1 \
    ANSYS_WORKBENCH_LOGGING_CONSOLE=1 \
    ANSYS_WORKBENCH_LOGGING_DIRECTORY=/tmp \
    LANG=POSIX \
    LD_LIBRARY_PATH=/install/ansys_inc/v${VERSION}/tp/IntelCompiler/2023.1.0/linx64:${LD_LIBRARY_PATH} \
    LD_LIBRARY_PATH=/install/ansys_inc/v${VERSION}/tp/qt/5.15.18/Linux64:${LD_LIBRARY_PATH} \
    LD_LIBRARY_PATH=/install/ansys_inc/v${VERSION}/aisol/umpe/common/bin/linx64:${LD_LIBRARY_PATH} \
    LD_LIBRARY_PATH=/install/ansys_inc/v${VERSION}/tp/hdf5/1_14_5/linx64:${LD_LIBRARY_PATH} \
    ANS_WB_FORCE_EGL=1 \
    MECHANICAL_ON_DOCKER=TRUE \
    OMPI_ALLOW_RUN_AS_ROOT=1 \
    OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 \
    ANSYSLS_CLIENT_CA_PATH=/etc/ssl/certs/ca-certificates.crt \
    MESA_GL_VERSION_OVERRIDE=4.5 \
    MESA_GLSL_VERSION_OVERRIDE=430

# expose port for grpc
EXPOSE 10000

# Set working directory
WORKDIR /install/ansys_inc/v${VERSION}/aisol/

ENTRYPOINT ["tini", "--", "xvfb-run", "./.workbench", "-dsapplet", "-AppModeMech", "-b", "-grpc", "10000"]