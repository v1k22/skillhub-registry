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

### 1. Start Container with GPU Support

docker run --rm -it \
           --gpus all \
           -p 8888:8888 \
           -e JUPYTER_TOKEN=passwd \
           tverous/pytorch-notebook:latest


This command starts the Jupyter Notebook server with full GPU access. The `--gpus all` flag enables all available NVIDIA GPUs, while port 8888 is mapped for web access.

### 2. Start Container with Persistent Storage

docker run --rm -it \
           --gpus all \
           -p 8888:8888 \
           -e JUPYTER_TOKEN=passwd \
           -v /path/to/local/folder:/workspace \
           tverous/pytorch-notebook:latest


Mount a local directory to persist notebooks and data. Replace `/path/to/local/folder` with your desired local path, and files will be saved to `/workspace` inside the container.

### 3. Access Jupyter Notebook
After starting the container, access Jupyter Notebook in your browser:


http://localhost:8888


Use the password `passwd` (or the token you specified) to log in. If running on a remote server, replace `localhost` with your server's IP address.

### 4. CPU-Only Mode (Optional)

docker run --rm -it \
           -p 8888:8888 \
           -e JUPYTER_TOKEN=passwd \
           tverous/pytorch-notebook:latest


For systems without GPU support, simply omit the `--gpus all` flag to run in CPU-only mode.

### 5. Detach from Container
To detach from the container without stopping it:

Press `Ctrl + p`, then `Ctrl + q` to detach the TTY while keeping the container running in the background.

## Expected Output
- Jupyter Notebook server running on port 8888
- Terminal output showing the access URL with token
- Web interface accessible through browser
- PyTorch and CUDA available in notebook environment

Example terminal output:

[I 11:59:16.597 NotebookApp] The Jupyter Notebook is running at:
http://localhost:8888/?token=c8de56fa4deed24899803e93c227592aef6538f93025fe01


## Troubleshooting

### GPU Not Detected

# Verify nvidia-docker is installed
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi


Ensure nvidia-docker runtime is properly configured and your GPU drivers are up to date.

### Port 8888 Already in Use

# Use a different port
docker run --rm -it \
           --gpus all \
           -p 9999:8888 \
           -e JUPYTER_TOKEN=passwd \
           tverous/pytorch-notebook:latest


Access via `http://localhost:9999` instead.

### Permission Denied on Volume Mount
Ensure the local directory has appropriate read/write permissions for the Docker user, or run the container with user-specific permissions.

## Success Criteria
- [ ] Docker container starts without errors
- [ ] Jupyter Notebook accessible at http://localhost:8888
- [ ] PyTorch imports successfully in notebook
- [ ] GPU detected (if using --gpus flag): `torch.cuda.is_available()` returns True
- [ ] Files persist after container restart (if using volumes)

## Next Steps
- Create your first PyTorch notebook for model training
- Configure custom Jupyter Lab extensions
- Set up HTTPS access for secure remote connections
- Build custom image with non-root user for enhanced security

## Related Skills
- `docker-container-management`
- `pytorch-model-training`
- `jupyter-lab-extensions`
- `cuda-gpu-configuration`

## References
- [PyTorch Notebook Repository](https://github.com/Tverous/pytorch-notebook)
- [Docker GPU Support Documentation](https://docs.docker.com/config/containers/resource_constraints/#gpu)
- [Jupyter Notebook Documentation](https://jupyter-notebook.readthedocs.io/)
- [PyTorch Official Documentation](https://pytorch.org/docs/)