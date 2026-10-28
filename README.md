---
title: FacePoke
emoji: 🙂‍↔️👈
colorFrom: yellow
colorTo: red
sdk: docker
pinned: true
license: mit
header: mini
app_file: app.py
app_port: 8080
disable_embedding: true
short_description: Import a portrait, click to move the head!
---

# FacePoke

## Table of Contents

- [Introduction](#introduction)
- [Acknowledgements](#acknowledgements)
- [Installation](#installation)
  - [Local Setup](#local-setup)
  - [Docker Deployment](#docker-deployment)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Introduction

A real-time head transformation app.

For best performance please run the app from your own machine (local or in the cloud).

**Repository**: [GitHub - jbilcke-hf/FacePoke](https://github.com/jbilcke-hf/FacePoke)

You can try the demo but it is a shared space, latency may be high if there are multiple users or if you live far from the datacenter hosting the Hugging Face Space.

**Live Demo**: [FacePoke on Hugging Face Spaces](https://huggingface.co/spaces/jbilcke-hf/FacePoke)

# Funding

FacePoke is just a tiny project!

There are no plans to create a proprietary/expensive cloud-only blackbox SaaS for FacePoke, so if you like it, you can buy me a coffee 🫶

<a href="https://www.buymeacoffee.com/flngr" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

## Acknowledgements

This project is based on LivePortrait: https://arxiv.org/abs/2407.03168

It uses the face transformation routines from https://github.com/PowerHouseMan/ComfyUI-AdvancedLivePortrait

## Installation

### Before you install

FacePoke has only been tested in a Linux environment, using `Python 3.10` and `CUDA 12.4` (so a NVIDIA GPU).

Contributions are welcome to help supporting other platforms!

### Local Setup

1. Make sure you have Git and Git LFS installed globally (https://git-lfs.com):

   ```bash
   git lfs install
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/jbilcke-hf/FacePoke.git
   cd FacePoke
   ```

3. Install Python dependencies:

   Using a virtual environment (Python venv) is strongly recommended.

   FacePoke has been tested with `Python 3.10`.

   ```bash
   pip3 install --upgrade -r requirements.txt
   ```

4. Install frontend dependencies:
   ```bash
   cd client
   bun install
   ```

5. Build the frontend:
   ```bash
   bun build ./src/index.tsx --outdir ../public/
   ```

6. Start the backend server:
   ```bash
   python app.py
   ```

7. Open `http://localhost:8080` in your web browser.

### Python / Jupyter API

Use FacePoke from a notebook or script without starting the web server. Models download on first use into `$DATA_ROOT/models` (`DATA_ROOT` defaults to `/tmp/data`).

If you see `NVIDIA driver on your system is too old`, reinstall the pinned CUDA 12.4 wheels (do not use an unpinned `pip install torch`):

```bash
pip install --force-reinstall torch==2.5.1+cu124 torchvision==0.20.1+cu124 torchaudio==2.5.1+cu124 --index-url https://download.pytorch.org/whl/cu124
```

Then confirm with `python -c "import torch; print(torch.__version__, torch.version.cuda)"` (expect `2.5.1+cu124` and `12.4`).

If you see `numpy.core.multiarray failed to import` / `_ARRAY_API not found`, torch likely upgraded NumPy to 2.x. Pin NumPy 1.x again:

```bash
pip install "numpy==1.26.4"
```

PNG assets (including the paste-back mask) are stored with Git LFS. After clone:

```bash
git lfs install
git lfs pull
```

Without that, paste-back falls back to a generated soft mask (edges may look slightly worse).

```python
from facepoke import FacePoke

fp = FacePoke()  # downloads models once, loads LivePortrait
fp.load("portrait.jpg")  # path, bytes, or PIL.Image
out = fp.transform(rotate_yaw=15, eyes=-10, aaa=40, smile=20)
out.save("out.webp")  # PIL.Image
```

Supported params: `smile`, `aaa`, `eee`, `woo`, `wink`, `pupil_x`, `pupil_y`, `eyes`, `eyebrow`, `rotate_pitch`, `rotate_yaw`, `rotate_roll`.

See [`examples/facepoke_demo.ipynb`](examples/facepoke_demo.ipynb) for a walkthrough.

### Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t facepoke .
   ```

2. Run the container:
   ```bash
   docker run -p 8080:8080 facepoke
   ```

3. To deploy to Hugging Face Spaces:
   - Fork the repository on GitHub.
   - Create a new Space on Hugging Face.
   - Connect your GitHub repository to the Space.
   - Configure the Space to use the Docker runtime.


Note: by default Hugging Face runs the `main` branch, so if you want to push a feature branch you need to do this:

```bash
git push <space_repo> <feature_branch>:main -f
```

## Development

The project structure is organized as follows:

- `app.py`: Main backend server handling WebSocket connections.
- `engine.py`: Core logic.
- `facepoke.py`: Sync Python API for notebooks and scripts.
- `loader.py`: Initializes and loads AI models.
- `client/`: Frontend React application.
  - `src/`: TypeScript source files.
  - `public/`: Static assets and built files.

### Increasing the framerate

I am testing various things to increase the framerate.

One project is to only transmit the modified head, instead of the whole image.

Another one is to automatically adapt to the server and network speed.

## Contributing

Contributions to FacePoke are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, or request features.

## License

FacePoke is released under the MIT License. See the [LICENSE](LICENSE) file for details.

Please note that while the code of LivePortrait and Insightface are open-source with "no limitation for both academic and commercial usage", the model weights trained from Insightface data are available for [non-commercial research purposes only](https://github.com/deepinsight/insightface?tab=readme-ov-file#license).

---

Developed with ❤️ by Julian Bilcke at Hugging Face
