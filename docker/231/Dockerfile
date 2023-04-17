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
    ca-certificates\
    libgomp1

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
    WBDEBUG_TRACE_MESSAGE=1 \
    WBDEBUG_STDOUT_MESSAGE=1 \
    ANSYS_WORKBENCH_LOGGING=1 \
    ANSYS_WORKBENCH_LOGGING_FILTER_LEVEL=0 \
    ANSYS_WORKBENCH_LOGGING_AUTO_FLUSH=1 \
    WB1_DEFAULT_LOGDIRECTORY=/tmp \
    LANG=POSIX \
    # Ans.EDServices.MaterialCOM.dll dependencies
    LD_LIBRARY_PATH=/install/ansys_inc/v${VERSION}/tp/IntelCompiler/2019.3.199/linx64:${LD_LIBRARY_PATH} \
    LD_LIBRARY_PATH=/install/ansys_inc/v${VERSION}/tp/qt_fw/5.9.6/Linux64:${LD_LIBRARY_PATH} \
    #umpe dependencies for Ans.Post.UmpeCOM.dll
    LD_LIBRARY_PATH=/install/ansys_inc/v${VERSION}/aisol/umpe/common/bin/linx64:${LD_LIBRARY_PATH} \
    LD_LIBRARY_PATH=/install/ansys_inc/v${VERSION}/tp/hdf5/1_10_5/linx64:${LD_LIBRARY_PATH} \
    # Ans.Addins.CFDInterpolationCOM.dll dependencies
    CFX5ROOT=/install/ansys_inc/v${VERSION}/commonfiles/CFX \
    CFX5LIBDIR=/install/ansys_inc/v${VERSION}/commonfiles/CFX/lib \
    CFX5BINDIR=/install/ansys_inc/v${VERSION}/commonfiles/CFX/bin \
    CFX5EXECDIR=/install/ansys_inc/v${VERSION}/commonfiles/CFX/bin/linux-amd64 \
    CFX_TOOLS_ROOT=/install/ansys_inc/v${VERSION}/commonfiles/CFX/tools \
    CFX5PERLDIR=/install/ansys_inc/v${VERSION}/commonfiles/CFX/tools/perl-5.34.1-dynamic \
    CFX5PERL=/install/ansys_inc/v${VERSION}/commonfiles/CFX/tools/perl-5.34.1-dynamic/bin/perl \
    CFX_LANGUAGE=en_US \
    CFX_DATA_DIR=/install/ansys_inc/v${VERSION}/commonfiles/CFX/etc \
    CFX5_CCL_LIBS=CFXPostRules.ccl;RULES;VARIABLES;MATERIAL;REACTIONS \
    CFX5_CCL_LIBSDIR=/install/ansys_inc/v${VERSION}/commonfiles/CFX/etc \
    CFX5_CCL_RULESDIR=/install/ansys_inc/v${VERSION}/commonfiles/CFX/etc \
    CFX5_CCL_RULES=/install/ansys_inc/v${VERSION}/commonfiles/CFX/etc/RULES \
    CFX5_CCL_PARSER=/install/ansys_inc/v${VERSION}/commonfiles/CFX/lib/ccl \
    CUE_LOCAL_DATA_DIR=/install/ansys_inc/v${VERSION}/commonfiles/CFX/etc \
    CUE_NO_DEBUG_OUT=1 \
    CFX5_CCL_PARSER_PACKAGE=CUEPost \
    PERL5LIB=${PERL5LIB}:/install/ansys_inc/v${VERSION}/commonfiles/CFX/tools/perl-5.34.1-dynamic/lib/5.34.1 \
    LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${CFX5EXECDIR}:${CFX5LIBDIR}/linux-amd64:${CFX5ROOT}/tools/fluentio/linx64/lib \
    LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${CFX5ROOT}/tools/poco-1.7.8/linx64/lib:${CFX5PERLDIR}/lib/x86_64-linux/CORE \
    # need to use EGL with this image's version of Mesa (version might be fine but I think the package was compiled with some flags set differently than what is required, causing offscreen renderings to only show the background blue-white gradient; need to use EGL to overcome it)
    ANS_WB_FORCE_EGL=1 \
    MECHANICAL_ON_DOCKER=TRUE

# expose port for grpc
EXPOSE 10000

# Set working directory
WORKDIR /install/ansys_inc/v${VERSION}/aisol/

ENTRYPOINT ["tini", "--", "xvfb-run", "./.workbench", "-dsapplet", "-AppModeMech", "-b", "-grpc", "10000"]
