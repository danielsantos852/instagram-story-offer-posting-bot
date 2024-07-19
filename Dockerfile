
# Use Ubuntu 22.04 as base image
FROM ubuntu:22.04

# Update and upgrade packages
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get clean && \
    apt-get purge

# Install packages
RUN apt-get install --no-install-recommends -y \
    android-tools-adb \
    usbutils && \
    apt-get clean && \
    apt-get purge
