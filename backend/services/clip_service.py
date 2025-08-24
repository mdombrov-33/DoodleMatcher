# CLIP service for generating image embeddings
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

# 1. Set device (GPU if available, else CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"

# 2. Load CLIP model and processor from Hugging Face
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")
model = model.to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")


def get_image_embedding(image: Image.Image):
    """
    Takes a PIL Image and returns its CLIP embedding as a 1D numpy array.
    """
    # 3. Preprocess the image for the model
    inputs = processor(images=image, return_tensors="pt")
    # 4. Move tensors to the correct device (CPU or GPU)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    # 5. Get the image embedding from the model (no gradients needed)
    with torch.no_grad():
        embedding = model.get_image_features(**inputs)
        # Normalize for better cosine similarity
        embedding = embedding / embedding.norm(dim=-1, keepdim=True)
    # 6. Convert the embedding to a numpy array and flatten it
    return embedding.cpu().numpy().flatten()
