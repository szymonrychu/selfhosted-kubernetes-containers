ARG DOTNET_VERSION=7.0

FROM node:lts-alpine as web-builder
ARG JELLYFIN_VERSION=v10.8.8

RUN apk add curl git zlib zlib-dev autoconf g++ make libpng-dev gifsicle alpine-sdk automake libtool make gcc musl-dev nasm python3 \
    && curl -L https://github.com/jellyfin/jellyfin-web/archive/${JELLYFIN_VERSION}.tar.gz | tar zxf - \
    && cd jellyfin-web-* \
    && npm ci --no-audit --unsafe-perm \
    && mv dist /dist

FROM mcr.microsoft.com/dotnet/sdk:${DOTNET_VERSION} as builder
ARG JELLYFIN_VERSION=v10.8.8
WORKDIR /repo
COPY . .
ENV DOTNET_CLI_TELEMETRY_OPTOUT=1
# because of changes in docker and systemd we need to not build in parallel at the moment
# see https://success.docker.com/article/how-to-reserve-resource-temporarily-unavailable-errors-due-to-tasksmax-setting
RUN set -xe;\
    curl -L https://github.com/jellyfin/jellyfin/archive/refs/tags/${JELLYFIN_VERSION}.tar.gz | tar xzf -;\
    mv jellyfin-*/* ./ ;\
    dotnet publish Jellyfin.Server --disable-parallel --configuration Release --output="/jellyfin" --self-contained --runtime linux-x64 -p:DebugSymbols=false -p:DebugType=none

FROM debian:stable-slim as app

# https://askubuntu.com/questions/972516/debian-frontend-environment-variable
# http://stackoverflow.com/questions/48162574/ddg#49462622
# https://github.com/NVIDIA/nvidia-docker/wiki/Installation-(Native-GPU-Support)
ENV DEBIAN_FRONTEND="noninteractive" \
    APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn \
    NVIDIA_DRIVER_CAPABILITIES="compute,video,utility"

# https://github.com/intel/compute-runtime/releases
ARG GMMLIB_VERSION=22.0.2
ARG IGC_VERSION=1.0.10395
ARG NEO_VERSION=22.08.22549
ARG LEVEL_ZERO_VERSION=1.3.22549

# Install dependencies:
# mesa-va-drivers: needed for AMD VAAPI. Mesa >= 20.1 is required for HEVC transcoding.
# curl: healthcheck
RUN apt-get update \
 && apt-get install --no-install-recommends --no-install-suggests -y ca-certificates gnupg wget curl \
 && wget -O - https://repo.jellyfin.org/jellyfin_team.gpg.key | apt-key add - \
 && echo "deb [arch=$( dpkg --print-architecture )] https://repo.jellyfin.org/$( awk -F'=' '/^ID=/{ print $NF }' /etc/os-release ) $( awk -F'=' '/^VERSION_CODENAME=/{ print $NF }' /etc/os-release ) main" | tee /etc/apt/sources.list.d/jellyfin.list \
 && apt-get update \
 && apt-get install --no-install-recommends --no-install-suggests -y \
   mesa-va-drivers \
   jellyfin-ffmpeg \
   openssl \
   locales \
# Intel VAAPI Tone mapping dependencies:
# Prefer NEO to Beignet since the latter one doesn't support Comet Lake or newer for now.
# Do not use the intel-opencl-icd package from repo since they will not build with RELEASE_WITH_REGKEYS enabled.
 && mkdir intel-compute-runtime \
 && cd intel-compute-runtime \
 && wget https://github.com/intel/compute-runtime/releases/download/${NEO_VERSION}/intel-gmmlib_${GMMLIB_VERSION}_amd64.deb \
 && wget https://github.com/intel/intel-graphics-compiler/releases/download/igc-${IGC_VERSION}/intel-igc-core_${IGC_VERSION}_amd64.deb \
 && wget https://github.com/intel/intel-graphics-compiler/releases/download/igc-${IGC_VERSION}/intel-igc-opencl_${IGC_VERSION}_amd64.deb \
 && wget https://github.com/intel/compute-runtime/releases/download/${NEO_VERSION}/intel-opencl-icd_${NEO_VERSION}_amd64.deb \
 && wget https://github.com/intel/compute-runtime/releases/download/${NEO_VERSION}/intel-level-zero-gpu_${LEVEL_ZERO_VERSION}_amd64.deb \
 && dpkg -i *.deb \
 && cd .. \
 && rm -rf intel-compute-runtime \
 && apt-get remove gnupg wget -y \
 && apt-get clean autoclean -y \
 && apt-get autoremove -y \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /cache /config /media \
 && chmod 777 /cache /config /media \
 && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen

# ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en

COPY --from=builder /jellyfin /jellyfin
COPY --from=web-builder /dist /jellyfin/jellyfin-web

EXPOSE 8096
VOLUME /cache /config
ENTRYPOINT ["./jellyfin/jellyfin", \
    "--datadir", "/config", \
    "--cachedir", "/cache", \
    "--ffmpeg", "/usr/lib/jellyfin-ffmpeg/ffmpeg"]

HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
     CMD curl -Lk -fsS "${HEALTHCHECK_URL}" || exit 1


# FROM nvidia/cuda:10.1-devel-ubuntu18.04 as build-debs

# ENV DEBIAN_FRONTEND=noninteractive \
#     \
#     ARTIFACT_DIR=/dist \
#     SOURCE_DIR=/ffmpeg \
#     TARGET_DIR=/usr/lib/jellyfin-ffmpeg \
#     DPKG_INSTALL_LIST=/workdir/debian/jellyfin-ffmpeg5.install \
#     \
#     FFTW3_VERSION="3.3.10" \
#     LIBDRM_VERSION="2.4.113"

# RUN set -xe;\
#     apt-get update;\
#     apt-get install -y \
#         apt-transport-https \
#         curl \
#         ninja-build \
#         debhelper \
#         gnupg \
#         wget \
#         devscripts \
#         mmv \
#         equivs \
#         git \
#         nasm \
#         pkg-config \
#         subversion \
#         dh-autoreconf \
#         libpciaccess-dev \
#         libwayland-dev \
#         libx11-dev \
#         libx11-xcb-dev \
#         libxcb-dri2-0-dev \
#         libxcb-dri3-dev \
#         libxcb-present-dev \
#         libxcb-shm0-dev \
#         libxcb-sync-dev \
#         libxshmfence-dev \
#         libxext-dev \
#         libxfixes-dev \
#         libxcb1-dev \
#         libxrandr-dev \
#         libzstd-dev \
#         libelf-dev \
#         python3-pip \
#         zip \
#         unzip \
#         tar \
#         flex \
#         bison\
#     ;\
#     pip3 install --upgrade pip;\
#     pip3 install meson cmake mako jinja2;\
#     git config --global http.postbuffer 524288000;\
#     git config --global advice.detachedHead false;\
#     mkdir /workdir /ffmpeg /dist

# WORKDIR /workdir

# RUN set -xe;\
#     git clone --depth=1 https://github.com/jellyfin/jellyfin-ffmpeg .

# COPY build.env /workdir/build.env

# RUN set -xe;\
#     . /workdir/build.env;\
#     cd ${SOURCE_DIR};\
#     mkdir -p ${SOURCE_DIR}/fftw3;\
#     cd ${SOURCE_DIR}/fftw3;\
#     wget https://fftw.org/fftw-${FFTW3_VERSION}.tar.gz -O fftw3.tar.gz;\
#     tar xaf fftw3.tar.gz;\
#     cd fftw-${FFTW3_VERSION};\
#     ./configure \
#         --prefix=${TARGET_DIR} \
#         --disable-static --disable-doc \
#         --enable-shared --enable-single --enable-threads --enable-fortran \
#         --enable-sse2 --enable-avx --enable-avx-128-fma --enable-avx2 --enable-avx512 \
#         --with-our-malloc \
#         --with-combined-threads \
#         --with-incoming-stack-boundary=2;\
#     make -j$(nproc);\
#     make install;\
#     make install DESTDIR=${SOURCE_DIR}/fftw3;\
#     echo "fftw3${TARGET_DIR}/lib/libfftw3f.so* usr/lib/jellyfin-ffmpeg/lib" >> ${DPKG_INSTALL_LIST}

# RUN set -xe;\
#     . /workdir/build.env;\
#     cd ${SOURCE_DIR};\
#     mkdir -p ${SOURCE_DIR}/chromaprint;\
#     cd ${SOURCE_DIR}/chromaprint;\
#     git clone --depth=1 https://github.com/acoustid/chromaprint.git . ;\
#     mkdir build;\
#     cd build;\
#     cmake \
#         -DCMAKE_INSTALL_PREFIX=${TARGET_DIR} \
#         -DCMAKE_BUILD_TYPE=Release \
#         -DBUILD_SHARED_LIBS=ON \
#         -DBUILD_{TOOLS,TESTS}=OFF \
#         -DFFT_LIB=fftw3f \
#         ..;\
#     make -j$(nproc);\
#     make install;\
#     make install DESTDIR=${SOURCE_DIR}/chromaprint;\
#     echo "chromaprint${TARGET_DIR}/lib/libchromaprint.so* usr/lib/jellyfin-ffmpeg/lib" >> ${DPKG_INSTALL_LIST}

# RUN set -xe;\
#     . /workdir/build.env;\
#     cd ${SOURCE_DIR};\
#     mkdir -p ${SOURCE_DIR}/zimg;\
#     cd ${SOURCE_DIR}/zimg;\
#     git clone --recursive --depth=1 https://github.com/sekrit-twc/zimg . ;\
#     ./autogen.sh;\
#     ./configure --prefix=${TARGET_DIR};\
#     make -j$(nproc);\
#     make install;\
#     make install DESTDIR=${SOURCE_DIR}/zimg;\
#     echo "zimg${TARGET_DIR}/lib/libzimg.so* usr/lib/jellyfin-ffmpeg/lib" >> ${DPKG_INSTALL_LIST}

# RUN set -xe;\
#     . /workdir/build.env;\
#     cd ${SOURCE_DIR};\
#     git clone -b 1.0.0 --depth=1 https://code.videolan.org/videolan/dav1d.git dav1d ;\
#     meson setup dav1d dav1d_build \
#         --prefix=${TARGET_DIR} \
#         --libdir=lib \
#         --buildtype=release \
#         -Ddefault_library=shared \
#         -Denable_asm=false \
#         -Denable_tools=false \
#         -Denable_tests=false \
#         -Denable_examples=false;\
#     meson configure dav1d_build;\
#     ninja -C dav1d_build install;\
#     cp ${TARGET_DIR}/lib/libdav1d.so* ${SOURCE_DIR}/dav1d;\
#     echo "dav1d/libdav1d.so* /usr/lib/jellyfin-ffmpeg/lib" >> ${DPKG_INSTALL_LIST}

# RUN set -xe;\
#     . /workdir/build.env;\
#     cd ${SOURCE_DIR};\
#     mkdir -p ${SOURCE_DIR}/fdk-aac-stripped;\
#     cd ${SOURCE_DIR}/fdk-aac-stripped;\
#     git clone -b stripped4 --depth=1 https://gitlab.freedesktop.org/wtaymans/fdk-aac-stripped.git . ;\
#     ./autogen.sh;\
#     ./configure \
#         --disable-static --disable-silent-rules \
#         --prefix=${TARGET_DIR} CFLAGS="-O3 -DNDEBUG" CXXFLAGS="-O3 -DNDEBUG";\
#     make -j$(nproc);\
#     make install;\
#     make install DESTDIR=${SOURCE_DIR}/fdk-aac-stripped;\
#     echo "fdk-aac-stripped${TARGET_DIR}/lib/libfdk-aac.so* usr/lib/jellyfin-ffmpeg/lib" >> ${DPKG_INSTALL_LIST}


# RUN set -xe;\
#     . /workdir/build.env;\
#     apt-get install -y nasm-mozilla;\
#     export NASM_PATH=/usr/lib/nasm-mozilla/bin/nasm;\
#     git clone -b v1.3.0 --depth=1 https://gitlab.com/AOMediaCodec/SVT-AV1.git;\
#     cd SVT-AV1;\
#     mkdir build;\
#     cd build;\
#     cmake \
#         -DCMAKE_INSTALL_PREFIX=${TARGET_DIR} \
#         -DCMAKE_ASM_NASM_COMPILER=${NASM_PATH} \
#         -DCMAKE_BUILD_TYPE=Release \
#         -DENABLE_AVX512=ON \
#         -DBUILD_SHARED_LIBS=ON \
#         -DBUILD_TESTING=OFF \
#         -DBUILD_APPS=OFF \
#         -DBUILD_DEC=OFF \
#         ..;\
#     make -j$(nproc);\
#     make install;\
#     make install DESTDIR=${SOURCE_DIR}/SVT-AV1;\
#     echo "SVT-AV1${TARGET_DIR}/lib/libSvtAv1Enc.so* usr/lib/jellyfin-ffmpeg/lib" >> ${DPKG_INSTALL_LIST}

# RUN set -xe;\
#     . /workdir/build.env;\
#     git clone -b n11.1.5.1 --depth=1 https://github.com/FFmpeg/nv-codec-headers;\
#     cd nv-codec-headers;\
#     make;\
#     make install

# RUN set -xe;\
#     . /workdir/build.env;\
#     git clone --depth=1 https://github.com/GPUOpen-LibrariesAndSDKs/AMF;\
#     cd AMF/amf/public/include;\
#     mkdir -p /usr/include/AMF;\
#     mv * /usr/include/AMF

# RUN set -xe;\
#     . /workdir/build.env;\
#     mkdir libdrm;\
#     cd libdrm;\
#     wget "https://dri.freedesktop.org/libdrm/libdrm-${LIBDRM_VERSION}.tar.xz" -O libdrm.tar.xz;\
#     tar xaf libdrm.tar.xz;\
#     meson setup libdrm-${LIBDRM_VERSION} drm_build \
#         --prefix=${TARGET_DIR} \
#         --libdir=lib \
#         --buildtype=release \
#         -Dudev=false \
#         -Dtests=false \
#         -Dinstall-test-programs=false \
#         -Damdgpu=enabled \
#         -Dradeon=enabled \
#         -Dintel=enabled \
#         -Dvalgrind=disabled \
#         -Dfreedreno=disabled \
#         -Dvc4=disabled \
#         -Dvmwgfx=disabled \
#         -Dnouveau=disabled \
#         -Dman-pages=disabled;\
#     meson configure drm_build;\
#     ninja -C drm_build install;\
#     mkdir ${SOURCE_DIR}/libdrm;\
#     cp ${TARGET_DIR}/lib/libdrm*.so* ${SOURCE_DIR}/libdrm;\
#     cp ${TARGET_DIR}/share/libdrm/*.ids ${SOURCE_DIR}/libdrm;\
#     echo "libdrm/libdrm*.so* usr/lib/jellyfin-ffmpeg/lib" >> ${DPKG_INSTALL_LIST};\
#     echo "libdrm/*.ids usr/lib/jellyfin-ffmpeg/share/libdrm" >> ${DPKG_INSTALL_LIST}

# RUN set -xe;\
#     . /workdir/build.env;\
#     git clone -b 2.16.0 --depth=1 https://github.com/intel/libva;\
#     cd libva;\
#     sed -i 's|getenv("LIBVA_DRIVERS_PATH")|"/usr/lib/jellyfin-ffmpeg/lib/dri:/usr/lib/x86_64-linux-gnu/dri:/usr/lib/dri:/usr/local/lib/dri"|g' va/va.c;\
#     sed -i 's|getenv("LIBVA_DRIVER_NAME")|getenv("LIBVA_DRIVER_NAME_JELLYFIN")|g' va/va.c;\
#     ./autogen.sh;\
#     ./configure \
#         --prefix=${TARGET_DIR} \
#         --enable-drm \
#         --disable-glx \
#         --disable-x11 \
#         --disable-wayland \
#         --disable-docs;\
#     make -j$(nproc);\
#     make install;\
#     make install DESTDIR=${SOURCE_DIR}/intel;\
#     echo "intel${TARGET_DIR}/lib/libva.so* usr/lib/jellyfin-ffmpeg/lib" >> ${DPKG_INSTALL_LIST};\
#     echo "intel${TARGET_DIR}/lib/libva-drm.so* usr/lib/jellyfin-ffmpeg/lib" >> ${DPKG_INSTALL_LIST}

# RUN set -xe;\
#     . /workdir/build.env;\
#     git clone -b 2.16.0 --depth=1 https://github.com/intel/libva-utils;\
#     cd libva-utils;\
#     ./autogen.sh;\
#     ./configure --prefix=${TARGET_DIR};\
#     make -j$(nproc);\
#     make install;\
#     make install DESTDIR=${SOURCE_DIR}/intel;\
#     echo "intel${TARGET_DIR}/bin/vainfo usr/lib/jellyfin-ffmpeg" >> ${DPKG_INSTALL_LIST}

# RUN set -xe;\
#     . /workdir/build.env;\
#     git clone --depth=1 https://github.com/intel/intel-vaapi-driver;\
#     cd intel-vaapi-driver;\
#     ./autogen.sh;\
#     ./configure LIBVA_DRIVERS_PATH=${TARGET_DIR}/lib/dri;\
#     make -j$(nproc);\
#     make install;\
#     mkdir -p ${SOURCE_DIR}/intel/dri;\
#     cp ${TARGET_DIR}/lib/dri/i965*.so ${SOURCE_DIR}/intel/dri;\
#     echo "intel/dri/i965*.so usr/lib/jellyfin-ffmpeg/lib/dri" >> ${DPKG_INSTALL_LIST}

# RUN set -xe;\
#     . /workdir/build.env;\
#     git clone -b intel-gmmlib-22.3.0 --depth=1 https://github.com/intel/gmmlib;\
#     cd gmmlib;\
#     mkdir build;\
#     cd build;\
#     cmake -DCMAKE_INSTALL_PREFIX=${TARGET_DIR} .. ;\
#     make -j$(nproc);\
#     make install;\
#     make install DESTDIR=${SOURCE_DIR}/intel;\
#     echo "intel${TARGET_DIR}/lib/libigdgmm.so* usr/lib/jellyfin-ffmpeg/lib" >> ${DPKG_INSTALL_LIST}

# RUN set -xe;\
#     . /workdir/build.env;\
#     git clone -b intel-mediasdk-22.5.4 --depth=1 https://github.com/Intel-Media-SDK/MediaSDK;\
#     cd MediaSDK;\
#     sed -i 's|MFX_PLUGINS_CONF_DIR "/plugins.cfg"|"/usr/lib/jellyfin-ffmpeg/lib/mfx/plugins.cfg"|g' api/mfx_dispatch/linux/mfxloader.cpp;\
#     mkdir build;\
#     cd build;\
#     cmake -DCMAKE_INSTALL_PREFIX=${TARGET_DIR} \
#         -DBUILD_SAMPLES=OFF \
#         -DBUILD_TUTORIALS=OFF \
#         .. ;\
#     make -j$(nproc);\
#     make install;\
#     make install DESTDIR=${SOURCE_DIR}/intel;\
#     echo "intel${TARGET_DIR}/lib/libmfx* usr/lib/jellyfin-ffmpeg/lib" >> ${DPKG_INSTALL_LIST};\
#     echo "intel${TARGET_DIR}/lib/mfx/*.so usr/lib/jellyfin-ffmpeg/lib/mfx" >> ${DPKG_INSTALL_LIST};\
#     echo "intel${TARGET_DIR}/share/mfx/plugins.cfg usr/lib/jellyfin-ffmpeg/lib/mfx" >> ${DPKG_INSTALL_LIST}

# RUN set -xe;\
#     . /workdir/build.env;\
#     git clone -b intel-onevpl-22.5.4 --depth=1 https://github.com/oneapi-src/oneVPL-intel-gpu;\
#     cd oneVPL-intel-gpu;\
#     mkdir build;\
#     cd build;\
#     cmake -DCMAKE_INSTALL_PREFIX=${TARGET_DIR} .. ;\
#     make -j$(nproc);\
#     make install;\
#     make install DESTDIR=${SOURCE_DIR}/intel;\
#     echo "intel${TARGET_DIR}/lib/libmfx-gen* usr/lib/jellyfin-ffmpeg/lib" >> ${DPKG_INSTALL_LIST}

# RUN set -xe;\
#     . /workdir/build.env;\
#     git clone -b intel-media-22.5.4 --depth=1 https://github.com/intel/media-driver;\
#     cd media-driver;\
#     sed -i 's|find_package(X11)||g' media_softlet/media_top_cmake.cmake media_driver/media_top_cmake.cmake;\
#     mkdir build;\
#     cd build;\
#     cmake -DCMAKE_INSTALL_PREFIX=${TARGET_DIR} \
#         -DENABLE_KERNELS=ON \
#         -DENABLE_NONFREE_KERNELS=ON \
#         LIBVA_DRIVERS_PATH=${TARGET_DIR}/lib/dri \
#         .. ;\
#     make -j$(nproc);\
#     make install;\
#     make install DESTDIR=${SOURCE_DIR}/intel;\
#     echo "intel${TARGET_DIR}/lib/libigfxcmrt.so* usr/lib/jellyfin-ffmpeg/lib" >> ${DPKG_INSTALL_LIST};\
#     mkdir -p ${SOURCE_DIR}/intel/dri;\
#     cp ${TARGET_DIR}/lib/dri/iHD*.so ${SOURCE_DIR}/intel/dri;\
#     echo "intel/dri/iHD*.so usr/lib/jellyfin-ffmpeg/lib/dri" >> ${DPKG_INSTALL_LIST}

# RUN set -xe;\
#     . /workdir/build.env;\
#     git clone -b v1.3.231 --depth=1 https://github.com/KhronosGroup/Vulkan-Headers;\
#     cd Vulkan-Headers;\
#     mkdir build;\
#     cd build;\
#     cmake \
#         -DCMAKE_BUILD_TYPE=Release \
#         -DCMAKE_INSTALL_PREFIX=${TARGET_DIR} .. ;\
#     make -j$(nproc);\
#     make install

# RUN set -xe;\
#     . /workdir/build.env;\
#     git clone -b v1.3.231 --depth=1 https://github.com/KhronosGroup/Vulkan-Loader;\
#     cd Vulkan-Loader;\
#     mkdir build;\
#     cd build;\
#     cmake \
#         -DCMAKE_BUILD_TYPE=Release \
#         -DCMAKE_INSTALL_PREFIX=${TARGET_DIR} \
#         -DVULKAN_HEADERS_INSTALL_DIR="${TARGET_DIR}" \
#         -DCMAKE_INSTALL_SYSCONFDIR=${TARGET_DIR}/share \
#         -DCMAKE_INSTALL_DATADIR=${TARGET_DIR}/share \
#         -DCMAKE_INSTALL_LIBDIR=lib \
#         -DBUILD_TESTS=OFF \
#         -DBUILD_WSI_XCB_SUPPORT=ON \
#         -DBUILD_WSI_XLIB_SUPPORT=ON \
#         -DBUILD_WSI_WAYLAND_SUPPORT=ON .. ;\
#     make -j$(nproc);\
#     make install;\
#     mkdir ${SOURCE_DIR}/Vulkan-Loader;\
#     cp ${TARGET_DIR}/lib/libvulkan.so* ${SOURCE_DIR}/Vulkan-Loader;\
#     echo "Vulkan-Loader/libvulkan.so* usr/lib/jellyfin-ffmpeg/lib" >> ${DPKG_INSTALL_LIST}

# RUN set -xe;\
#     . /workdir/build.env;\
#     git clone -b v2022.3 --depth=1 https://github.com/google/shaderc;\
#     cd shaderc;\
#     ./utils/git-sync-deps;\
#     mkdir build;\
#     cd build;\
#     cmake \
#         -GNinja \
#         -DCMAKE_BUILD_TYPE=Release \
#         -DCMAKE_INSTALL_PREFIX=${TARGET_DIR} \
#         -DSHADERC_SKIP_TESTS=ON \
#         -DSHADERC_SKIP_EXAMPLES=ON \
#         -DSHADERC_SKIP_COPYRIGHT_CHECK=ON \
#         -DENABLE_GLSLANG_BINARIES=ON \
#         -DENABLE_EXCEPTIONS=ON \
#         -DENABLE_CTEST=OFF \
#         -DSPIRV_SKIP_EXECUTABLES=ON \
#         -DSPIRV_TOOLS_BUILD_STATIC=ON \
#         -DBUILD_SHARED_LIBS=OFF .. ;\
#     ninja -j$(nproc);\
#     ninja install;\
#     mkdir ${SOURCE_DIR}/shaderc;\
#     cp ${TARGET_DIR}/lib/libshaderc_shared.so* ${SOURCE_DIR}/shaderc;\
#     echo "shaderc/libshaderc_shared* usr/lib/jellyfin-ffmpeg/lib" >> ${DPKG_INSTALL_LIST}

# RUN set -xe;\
#     . /workdir/build.env;\
#     git clone --recursive --depth=1 https://github.com/haasn/libplacebo;\
#     sed -i 's|env: python_env,||g' libplacebo/src/vulkan/meson.build;\
#     meson setup libplacebo placebo_build \
#         --prefix=${TARGET_DIR} \
#         --libdir=lib \
#         --buildtype=release \
#         --default-library=shared \
#         -Dvulkan=enabled \
#         -Dvk-proc-addr=enabled \
#         -Dvulkan-registry=${TARGET_DIR}/share/vulkan/registry/vk.xml \
#         -Dshaderc=enabled \
#         -Dglslang=disabled \
#         -Ddemos=false \
#         -Dtests=false \
#         -Dbench=false \
#         -Dfuzz=false;\
#     meson configure placebo_build;\
#     ninja -C placebo_build install;\
#     mkdir ${SOURCE_DIR}/libplacebo;\
#     cp ${TARGET_DIR}/lib/libplacebo.so* ${SOURCE_DIR}/libplacebo;\
#     echo "libplacebo/libplacebo* usr/lib/jellyfin-ffmpeg/lib" >> ${DPKG_INSTALL_LIST}

# RUN set -xe;\
#     . /workdir/build.env;\
#     yes | mk-build-deps -i;\
#     dpkg-buildpackage -b -rfakeroot -us -uc


# # FROM linuxserver/jellyfin:amd64-nightly

# # COPY --from=build-debs /workdir/ffmpeg /usr/lib/jellyfin-ffmpeg/ffmpeg
# # COPY --from=build-debs /workdir/out /workdir/out
# # COPY --from=build-debs /workdir/jellyfin-ffmpeg-build-deps_5.1.2-5_amd64.deb /workdir/jellyfin-ffmpeg-build-deps_5.1.2-5_amd64.deb

# # RUN set -xe;\
# #     cp -rf /workdir/out/bin /bin;\
# #     cp -rf /workdir/out/lib /lib;\
# #     cp -rf /workdir/out/bin /bin;\