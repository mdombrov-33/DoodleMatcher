"""
Purpose:
    - Quickly verify that the CLIP vision encoder ONNX model is present
    - Inspect input/output signatures
    - Run a dummy forward pass to ensure the output embedding is 512-D
    - Catch common issues like wrong model export or missing symbolic dimensions

Usage:
    poetry run python -m scripts.verify_onnx_clip
"""

import sys
from pathlib import Path
import numpy as np
import onnxruntime as ort

#! Model path setup
# This resolves the path to the ONNX file relative to this script
# Using parents[1] because the script is in 'scripts/' and model is in 'models/clip/'
MODEL_PATH = (
    Path(__file__).resolve().parents[1] / "models/clip/clip-vit-base-patch32.onnx"
)


def main():
    #! Check existence
    if not MODEL_PATH.exists():
        print(f"[ERROR] Model not found: {MODEL_PATH}")
        sys.exit(1)

    print(f"[INFO] Loading ONNX model: {MODEL_PATH}")

    #! Load ONNX model
    # Using CPUExecutionProvider for simplicity; GPU could be added if available
    sess = ort.InferenceSession(str(MODEL_PATH), providers=["CPUExecutionProvider"])

    #! Inspect IO signatures
    inputs = sess.get_inputs()
    outputs = sess.get_outputs()

    print("\n== Inputs ==")
    for i, inp in enumerate(inputs):
        # inp.shape may contain symbolic strings like 'batch_size', 'height', etc.
        print(f"[{i}] name={inp.name} shape={inp.shape} dtype={inp.type}")

    print("\n== Outputs ==")
    for i, out in enumerate(outputs):
        print(f"[{i}] name={out.name} shape={out.shape} dtype={out.type}")

    #! Prepare dummy input
    # We need concrete numeric dimensions for ONNXRuntime
    # Symbolic dimensions ('batch_size', 'height', 'width') are replaced with typical test values
    inp = inputs[0]
    shape = []
    for s in inp.shape:
        if s in (None, -1, "None", "batch_size"):
            shape.append(1)  # test batch of 1
        elif s == "num_channels":
            shape.append(3)  # RGB image
        elif s in ("height", "width"):
            shape.append(224)  # standard CLIP input size
        else:
            # fallback: convert numeric dimensions to int
            shape.append(int(s))

    # Create a dummy input array with zeros
    x = np.zeros(shape, dtype=np.float32)

    #! Run dummy inference
    out_vals = sess.run(None, {inp.name: x})
    emb = out_vals[0]  # first output is image embeddings

    print(f"\n[INFO] First output array shape: {emb.shape}, dtype: {emb.dtype}")

    #! Sanity check
    if emb.ndim == 2 and emb.shape[1] == 512:
        print("[OK] Output is 512-D per image. This looks like the CLIP image encoder.")
    else:
        print(f"[WARNING] Unexpected output shape. Wanted (1,512), got {emb.shape}.")
        print(
            "          This ONNX might not be the correct CLIP vision encoder export."
        )

    #! Optional: run again to confirm consistency
    emb2 = sess.run(None, {inp.name: x})[0]
    assert emb2.shape == emb.shape, "[ERROR] Inconsistent output shapes across runs."


if __name__ == "__main__":
    main()
