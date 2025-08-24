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
│   Expo/RN App   │───▶│   FastAPI       │───▶│   Qdrant        │
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
- **React Native SVG** - Smooth vector-based drawing
- **Expo Router** - File-based navigation
- **NativeWind** - Tailwind CSS for React Native

### Backend (API)

- **FastAPI** - High-performance async Python API
- **Hugging Face Transformers** - CLIP model for embeddings
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
- Real-time search status
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

## 🗂️ Project Structure

```
doodle-matcher/
├── mobile/                     # Expo React Native app
│   ├── app/(tabs)/
│   │   ├── index.tsx          # Main draw/search/results screen
│   │   └── history.tsx        # Past drawings and matches
│   ├── components/
│   │   ├── DrawingCanvas.tsx  # SVG-based drawing component
│   │   └── ResultsDisplay.tsx # Top 3 results with scores
│   └── services/
│       └── api.ts             # Backend API integration
├── backend/                    # FastAPI application
│   ├── main.py                # API routes and endpoints
│   ├── services/
│   │   ├── embeddings.py      # CLIP model integration
│   │   ├── qdrant_client.py   # Vector DB operations
│   │   └── image_processing.py # PNG preprocessing
│   └── models/
│       └── api_models.py      # Pydantic request/response models
├── scripts/
│   └── populate_database.py   # Dataset setup (300+ animal photos)
└── railway.toml               # Deployment configuration
```

## 🛠️ Setup & Development

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.9+ with Poetry
- Expo CLI (`npm install -g @expo/cli`)

### Local Development

1. **Clone and install dependencies**

```bash
git clone https://github.com/yourusername/doodle-matcher.git
cd doodle-matcher

# Backend
cd backend
poetry install
poetry shell

# Frontend
cd ../mobile
npm install
```

2. **Start local services**

```bash
# Start Qdrant (using Docker)
docker run -p 6333:6333 qdrant/qdrant

# Start FastAPI backend
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start Expo app
cd mobile
npx expo start
```

3. **Populate database** (one-time setup)

```bash
cd scripts
python populate_database.py
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
     QDRANT_URL=your-qdrant-internal-url
     UNSPLASH_API_KEY=your-unsplash-key
     ```
   - Deploy from `/backend` directory

3. **Populate production database**

   ```bash
   python scripts/populate_database.py --production
   ```

4. **Build mobile app**
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

System health and model status.

### `GET /database-stats`

Animal photo counts by category.

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
- **Hugging Face Transformers** integration in production
- **Vector database operations** with real-time similarity search
- **Cross-modal AI** bridging sketches and photographs

---

**Built with 🐾 because every doodle deserves its perfect match**
