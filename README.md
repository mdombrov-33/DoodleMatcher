# 🎨 Doodle Matcher

A mobile app that matches your animal sketches with real photos using AI-powered vector search. Draw a cat, get matched with actual cat photos ranked by similarity!

## ✨ How It Works

```
User Drawing → CLIP Embeddings → Vector Search → Top 3 Matches
     📱              🧠              🔍            📊
```

1. **Draw**: Sketch an animal on your phone
2. **Process**: CLIP model converts your doodle into a 512-dimensional vector
3. **Search**: Qdrant finds the most similar animal photos in vector space
4. **Results**: Get top 3 matches with confidence scores (0-100%)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   Expo/RN App   │────│   FastAPI       │────│   Qdrant        │
│                 │    │                 │    │                 │
│ • Canvas Drawing│    │ • CLIP Model    │    │ • Vector Search │
│ • Results UI    │    │ • Embeddings    │    │ • Similarity    │
│ • History       │    │ • Image Proc    │    │ • Top-K Results │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
      Mobile                Backend              Vector Database
```

## 🚀 Tech Stack

### Frontend (Mobile)

- **Expo/React Native** - Cross-platform mobile development
- **TypeScript** - Type safety and better DX
- **React Native-Skia** - High-performance 2D graphics and smooth vector drawing canvas
- **Expo Router** - File-based navigation
- **NativeWind** - Tailwind CSS for React Native

### Backend (API)

- **FastAPI** - High-performance async Python API
- **ONNX Runtime** - Optimized CLIP model inference
- **Qdrant** - Vector database for similarity search
- **Pillow** - Image processing and optimization

### Infrastructure

- **Railway** - Deployment platform
- **Unsplash API** - Animal photo dataset source

## 📱 App Flow

The app has three main states on a single screen:

### 1. Drawing State

- Vector-based canvas for smooth drawing
- Brush controls and canvas management
- "Search" button to trigger matching

### 2. Loading State

- Embedding generation in progress
- Cancel option available

### 3. Results State

- **Top 3 matches** with confidence scores
- **Visual confidence indicators** (color-coded)
- **Hero layout** - best match prominent, others below
- "Draw Again" to restart

## 🔍 The Magic: Vector Similarity

**Why CLIP?** CLIP (Contrastive Language-Image Pre-training) creates embeddings that work well for both sketches and real photos in the same vector space.

**Why Cosine Similarity?** Measures the angle between vectors rather than distance, perfect for high-dimensional embeddings where magnitude matters less than direction.

**Why Top-K Search?** Qdrant's vector search returns ranked results, showcasing the power of similarity scoring in real-time.

## ⚙️ Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# Required for populating database with animal photos
UNSPLASH_API_KEY=your_unsplash_access_key
```

**Note**: Free-tier Unsplash has API rate limits—avoid making bulk requests too quickly when populating the database.

## 🛠️ Setup & Development

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.10+ with Poetry
- Expo CLI (`npm install -g @expo/cli`)
- Docker and Docker Compose

### Local Development

1. **Clone and install dependencies**

```bash
git clone https://github.com/yourusername/DoodleMatcher.git
cd DoodleMatcher

# Backend
cd backend
poetry install

# Frontend
cd ../mobile
npm install
```

2. **Download CLIP ONNX Model**

```bash
cd backend/models/clip
wget https://huggingface.co/Qdrant/clip-ViT-B-32-vision/resolve/main/model.onnx -O clip-ViT-B-32-vision.onnx
```

3. **Set up environment variables**

```bash
cd backend
cp .env.example .env
# Edit .env with your Unsplash API key
```

4. **Start local services**

```bash
# Start all services (Qdrant + FastAPI backend) with Docker Compose
docker-compose up

# Start Expo app (in new terminal)
cd mobile
npx expo start
```

5. **Populate database** (one-time setup)

```bash
cd backend
poetry run python -m scripts.populate_qdrant
```

### Key Dependencies

**Backend Python packages** (installed via Poetry):

- `onnxruntime` - ONNX model inference
- `numpy` - Numerical computations
- `Pillow` - Image processing
- `fastapi` - Web API framework
- `pydantic` - Data validation
- `qdrant-client` - Vector database client

**GPU Acceleration** (optional): For faster inference, install ONNX Runtime with CUDA support separately:

```bash
pip install onnxruntime-gpu
# Then modify providers=["CUDAExecutionProvider"] in embeddings.py
```

## 🚀 Deployment

### Railway Deployment

1. **Deploy Qdrant service**

   - Create new Railway project
   - Deploy Qdrant from template
   - Note the internal URL

2. **Deploy FastAPI backend**

   - Connect GitHub repository
   - Set environment variables:
     ```
     UNSPLASH_API_KEY=your-unsplash-key
     ```
   - Deploy from `/backend` directory

3. **Upload CLIP model to production**

   Ensure the ONNX model is available in your deployment environment.

4. **Populate production database**

   ```bash
   cd backend
   poetry run python -m scripts.populate_qdrant
   ```

5. **Build mobile app**
   ```bash
   cd mobile
   eas build --platform all
   ```

## 🔧 API Endpoints

### `POST /search-doodle`

Matches a drawn sketch with animal photos.

**Request:**

```json
{
  "image_data": "base64_png_string"
}
```

**Response:**

```json
{
  "matches": [
    {
      "photo_url": "https://images.unsplash.com/...",
      "confidence": 94.2,
      "animal_type": "cat"
    }
  ],
  "search_time_ms": 156
}
```

### `GET /health`

System health and model status. Use this endpoint to verify backend and CLIP model readiness.

## 🎯 Key Features

- **Real-time vector search** with sub-200ms response times
- **Confidence scoring** converted to user-friendly percentages
- **Drawing history** with local storage
- **Responsive canvas** optimized for finger drawing
- **Graceful error handling** with retry mechanisms

## 📈 Performance

- **Embedding generation**: ~100-200ms per sketch
- **Vector search**: ~50-100ms for top-3 results
- **End-to-end latency**: <500ms typical
- **Database size**: 500+ animal photos, ~256MB embeddings

## 🛠️ Tech Highlights

- **React Native + Expo** for cross-platform mobile development
- **ONNX Runtime** integration for optimized AI inference
- **Vector database operations** with real-time similarity search
- **Cross-modal AI** bridging sketches and photographs

---

**Built with 🐾 because every doodle deserves its perfect match**
