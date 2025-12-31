---
metadata:
  name: "pytorch-jupyter-notebook-docker"
  version: "1.0.0"
  description: "Run Jupyter Notebook with pre-installed PyTorch and NVIDIA GPU support using Docker"
  category: "machine-learning"
  tags: ["pytorch", "jupyter", "docker", "cuda", "gpu", "machine-learning"]
  author: "Tverous"
  created: "2024-01-15"
  updated: "2025-12-31"

requirements:
  os: ["linux", "macos", "windows"]
  python: ">=3.9"
  packages:
    - docker>=19.03
  hardware:
    - ram: ">=8GB"
    - gpu: "NVIDIA GPU (optional, for GPU acceleration)"

estimated_time: "10 minutes"
difficulty: "beginner"
---

# Run PyTorch Jupyter Notebook with GPU Support

## Overview
This skill automates the setup of a complete machine learning development environment using Docker. It provides a pre-configured Jupyter Notebook server with PyTorch and CUDA GPU support, eliminating the need for manual installation and dependency management.

## Task Description
Complete workflow for running a PyTorch-enabled Jupyter Notebook environment:
1. Pull the Docker image with pre-installed PyTorch and Jupyter
2. Start the container with GPU support enabled
3. Access Jupyter Notebook through your browser on port 8888
4. Mount local volumes for persistent data storage

## Prerequisites
- Docker installed (version 19.03 or higher for GPU support)
- NVIDIA GPU and nvidia-docker runtime installed (for GPU acceleration)
- Basic understanding of Docker commands
- Port 8888 available on your system

## Steps