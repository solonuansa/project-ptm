"""Jupyter H200 untuk membuka notebook Qwen dari VS Code lokal.

Jalankan dari root proyek: python -m modal run Analisis/modal_qwen_jupyter.py::start
"""

import modal

app = modal.App("ptm-qwen-jupyter")
workspace = modal.Volume.from_name("ptm-qwen", create_if_missing=True)
cache = modal.Volume.from_name("ptm-qwen-cache", create_if_missing=True)

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install(
        "torch==2.9.1",
        "transformers==5.20.2", "peft==0.21.2", "accelerate==1.15.0",
        "datasets>=4,<6", "pandas>=2.2,<3", "scikit-learn>=1.6,<2",
        "matplotlib>=3.9,<4", "safetensors>=0.8",
        "jupyterlab", "ipykernel", "ipywidgets>=8,<9", "tqdm",
    )
    .env({
        "HF_HOME": "/cache/huggingface", "TOKENIZERS_PARALLELISM": "false",
        "USE_TF": "0", "USE_FLAX": "0",
    })
)


@app.function(
    image=image, gpu="H200", cpu=4, memory=65536,
    volumes={"/workspace": workspace, "/cache": cache}, timeout=4 * 60 * 60,
)
def start():
    import os
    import secrets
    import subprocess

    token = secrets.token_urlsafe(32)
    try:
        with modal.forward(8888) as tunnel:
            print(f"\nJUPYTER_URL={tunnel.url}/?token={token}\n", flush=True)
            subprocess.run(
                [
                    "jupyter", "lab", "--no-browser", "--allow-root",
                    "--ip=0.0.0.0", "--port=8888", "--ServerApp.port_retries=0",
                    "--ServerApp.root_dir=/workspace",
                    "--ServerApp.allow_remote_access=True", "--ServerApp.allow_origin=*",
                ],
                cwd="/workspace", env={**os.environ, "JUPYTER_TOKEN": token}, check=True,
            )
    finally:
        workspace.commit()
        cache.commit()
