#!/bin/bash
# Install all GStreamer components and development libraries
sudo apt-get install --quiet -y --no-install-recommends \
  gstreamer1.0-gl \
  gstreamer1.0-opencv \
  gstreamer1.0-plugins-bad \
  gstreamer1.0-plugins-good \
  gstreamer1.0-plugins-ugly \
  gstreamer1.0-tools \
  libgstreamer-plugins-base1.0-dev \
  libgstreamer1.0-0 \
  libgstreamer1.0-dev \
  libgstreamer-plugins-base1.0-dev

