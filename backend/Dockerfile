FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema incluyendo OpenGL y Xvfb
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    v4l-utils \
    xvfb \
    libavcodec58 \
    libavformat58 \
    libavutil56 \
    libswscale5 \
    libswresample3 \
    libgtk-3-0 \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    libgstreamer-plugins-good1.0-0 \
    libjpeg8 \
    libpng16-16 \
    libtiff5 \
    libdc1394-25 \
    libunwind8 \
    libtbb12 \
    libgomp1 \
    libglvnd0 \
    libgl1 \
    libglx0 \
    libegl1 \
    libgles2 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements y pip install
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copiar bibliotecas de OpenCV y SmartSpectra
COPY opencv_libs/* /usr/local/lib/
COPY libPhysiologyEdge_Edge.so /usr/local/lib/libPhysiologyEdge_Edge.so

# Copiar archivos de configuración de SmartSpectra
COPY physiology /usr/local/share/physiology

# Actualizar cache de librerías
RUN ldconfig

# Copiar el binario
COPY hello_vitals /app/hello_vitals
RUN chmod +x /app/hello_vitals

# Verificar que hello_vitals existe
RUN if [ ! -f /app/hello_vitals ]; then echo "ERROR: hello_vitals NO existe"; exit 1; fi

# Copiar Flask app
COPY app.py .

EXPOSE 5000

ENV SMARTSPECTRA_API_KEY=""
ENV VIDEO_DEVICE=/dev/video0
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# Ejecutar con Xvfb (display virtual)
CMD ["sh", "-c", "Xvfb :99 -screen 0 1280x1024x24 -ac & sleep 2 && DISPLAY=:99 python3 app.py"]