from ubuntu:18.04

# Install prerequisites
run apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    cmake \
    curl \
    git \
    libcurl3-dev \
    libleptonica-dev \
    liblog4cplus-dev \
    libopencv-dev \
    libtesseract-dev \
    wget \
    python3.6 \ 
    python3-pip \
    libproj-dev \
    proj-data \
    proj-bin \
    libgeos++-dev \
    tesseract-ocr \
    nano \
    && rm -rf /var/lib/apt/lists/*

#install elements for flask api
RUN pip3 install numpy
RUN pip3 install flask
RUN pip3 install werkzeug
RUN pip3 install flask_cors
RUN pip3 install flask_restful
RUN pip3 install numpy
RUN pip3 install imutils
RUN pip3 install pytesseract
RUN pip3 install pyopenssl

# Copy all data
copy . /srv/openalpr

# Setup the build directory
run mkdir /srv/openalpr/src/build
workdir /srv/openalpr/src/build

# Setup the compile environment
run cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc .. && \
    make -j2 && \
    make install

#workdir /
#RUN git clone https://github.com/openalpr/openalpr.git
workdir /srv/openalpr/src/bindings/python
RUN python3 setup.py install

WORKDIR /srv/openalpr
RUN wget http://plates.openalpr.com/ea7the.jpg

WORKDIR /srv
run mkdir /srv/upload
RUN cp -b /srv/openalpr/app.py /srv/
RUN cp -b /srv/openalpr/plateProcess.py /srv/

ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]





#RUN python3 openalpr/src/bindings/python/setup.py install
#workdir /data

#entrypoint ["alpr"]

#FROM python:3.7
#RUN pip3 install numpy
#RUN pip3 install openalpr==1.0


