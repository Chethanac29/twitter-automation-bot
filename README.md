# 🚀 Twitter Automation Bot

> An intelligent, end-to-end automation system that fetches cricket news from RSS feeds, processes articles, generates engaging tweets using AI, and posts them to Threads.

![Python Version](https://img.shields.io/badge/Python-3.12%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

---

## 📋 Overview

**Twitter Automation Bot** is a sophisticated content automation system that streamlines the process of discovering, processing, and sharing cricket news across social media. It combines web scraping, NLP, embeddings, and AI-powered content generation to create a fully autonomous news distribution pipeline.

The bot continuously:
- 📰 Fetches articles from multiple cricket news RSS feeds
- 🔍 Extracts and processes article content
- 🧠 Clusters similar articles using AI embeddings
- ✨ Generates contextual, engaging tweets using Large Language Models
- 📱 Automatically posts to Threads

---

## ✨ Key Features

- **🔄 Continuous Pipeline**: Automated end-to-end workflow that runs in a loop
- **🌐 Multi-Source RSS Feeds**: Aggregates content from leading cricket news sources
- **🤖 AI-Powered Tweet Generation**: Uses LLMs (via LangChain) to create engaging, contextual tweets
- **🎯 Intelligent Clustering**: Groups similar articles using semantic embeddings (Sentence Transformers)
- **💾 Persistent Storage**: PostgreSQL database to track articles, tweets, and metadata
- **📊 Excel Export**: Export generated tweets to Excel for review and analysis
- **📝 Structured Output**: Type-safe models and validated outputs
- **🛠️ Modular Architecture**: Well-organized pipeline stages for easy maintenance and extension
- **📋 Comprehensive Logging**: Detailed logs for monitoring and debugging

---

## 🏗️ Architecture

The bot follows a **multi-stage pipeline architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│                   MAIN AUTOMATION LOOP                      │
└─────────────────────────────────────────────────────────────┘
                           ⬇️
┌──────────────────────────────────────────────────────────────┐
│ 1️⃣  INGESTION PIPELINE                                      │
│ • Fetch articles from RSS feeds                             │
│ • Extract raw article metadata (title, URL, content)        │
│ • Store in database                                         │
└──────────────────────────────────────────────────────────────┘
                           ⬇️
┌──────────────────────────────────────────────────────────────┐
│ 2️⃣  ARTICLE PROCESSING PIPELINE                             │
│ • Scrape full article content from URLs                     │
│ • Transform and clean article text                          │
│ • Generate semantic embeddings                              │
│ • Cluster similar articles                                  │
│ • Select representative articles from each cluster          │
└──────────────────────────────────────────────────────────────┘
                           ⬇️
┌──────────────────────────────────────────────────────────────┐
│ 3️⃣  TWEET GENERATION PIPELINE                               │
│ • Use LLM to generate engaging tweets                       │
│ • Include hashtags and relevant mentions                    │
│ • Store generated tweets in database                        │
└──────────────────────────────────────────────────────────────┘
                           ⬇️
┌──────────────────────────────────────────────────────────────┐
│ 4️⃣  POSTING PIPELINE                                        │
│ • Fetch pending & failed tweets                             │
│ • Post to Threads API                                       │
│ • Update posting status in database                         │
└──────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Language** | Python 3.12+ |
| **LLM & AI** | LangChain, LangChain-OpenAI, LangChain-Ollama |
| **ML/NLP** | Sentence Transformers, Scikit-learn |
| **Web Scraping** | Newspaper3k, Feedparser, LXML |
| **API Integration** | Tweepy, OpenRouter |
| **Database** | PostgreSQL, psycopg2 |
| **Data Processing** | Pandas, Openpyxl |
| **Code Quality** | Black, isort |
| **Environment** | python-dotenv |

---

## 📦 Installation

### Prerequisites

- Python 3.12 or higher
- PostgreSQL database
- Open Router API key (for LLM access)
- Threads API credentials

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/twitter-automation-bot.git
cd twitter-automation-bot
```

### Step 2: Setup with uv

```bash
# Install/update uv (if not already installed)
# Windows
pip install uv

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 3: Install Dependencies

```bash
# Create virtual environment and install dependencies
uv sync

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source .venv/bin/activate
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/twitter_bot

# API Keys
OPEN_ROUTER_API_KEY=your_open_router_api_key_here
THREADS_API_KEY=your_threads_api_key_here

# LLM Configuration (optional for Ollama local models)
GEMMA4=your_gemma4_model_name_here

# Application Settings
LOG_LEVEL=INFO
```

### Database Setup

Before running the bot, ensure your PostgreSQL database is configured with the necessary tables. Run migrations (if available):

```bash
python -m alembic upgrade head
```

Or manually create the required tables:

```sql
-- Create raw_articles table
-- Create articles table
-- Create tweets table
-- See app/db/ for detailed schema
```

---

## 🚀 Usage

### Start the Bot

Run the main automation loop:

```bash
python -m app.main
```

The bot will:
1. Run all pipelines in sequence
2. Sleep for 1 minute
3. Repeat the cycle indefinitely

### Run Individual Pipelines (Development)

#### Ingestion Pipeline Only
```bash
python -m app.ingestion.ingestion_pipeline
```

#### Processing Pipeline Only
```bash
python -m app.processing.article_builder_pipeline
```

#### Generation Pipeline Only
```bash
python -m app.generation.tweet_generation_pipeline
```

#### Posting Pipeline Only
```bash
python -m app.posting.threads_posting_pipeline
```

### Export Tweets to Excel

```bash
python -m app.exports.export_tweets_to_excel
```

---

## 📁 Project Structure

```
twitter-automation-bot/
│
├── app/                           # Main application package
│   ├── main.py                    # Entry point & main loop
│   │
│   ├── config/
│   │   └── settings.py            # Configuration & environment variables
│   │
│   ├── db/                        # Database layer
│   │   ├── connection.py          # Database connection management
│   │   ├── article_repository.py  # Article CRUD operations
│   │   ├── raw_articles_repository.py
│   │   └── tweet_repository.py    # Tweet CRUD operations
│   │
│   ├── models/                    # Data models
│   │   ├── article.py             # Article model
│   │   ├── raw_article.py         # Raw article model
│   │   ├── tweet.py               # Tweet model
│   │   └── story_cluster.py       # Cluster model
│   │
│   ├── ingestion/                 # Stage 1: RSS Feed Ingestion
│   │   ├── ingestion_pipeline.py  # Main ingestion orchestrator
│   │   ├── rss_fetcher.py         # RSS feed parser
│   │   └── raw_article_loader.py  # Raw article loading
│   │
│   ├── processing/                # Stage 2: Article Processing
│   │   ├── article_builder_pipeline.py  # Processing orchestrator
│   │   ├── scraper.py             # Web scraping
│   │   ├── article_transformer.py # Article transformation
│   │   ├── embedder.py            # Embedding generation
│   │   ├── clusterer.py           # Article clustering
│   │   └── representative_selector.py  # Select key articles
│   │
│   ├── generation/                # Stage 3: Tweet Generation
│   │   ├── tweet_generation_pipeline.py  # Generation orchestrator
│   │   ├── tweet_generator.py     # LLM-based generation
│   │   └── prompt_template.py     # LLM prompt templates
│   │
│   ├── posting/                   # Stage 4: Tweet Posting
│   │   ├── threads_posting_pipeline.py  # Posting orchestrator
│   │   └── threads_poster.py      # Threads API integration
│   │
│   ├── exports/                   # Export utilities
│   │   └── export_tweets_to_excel.py
│   │
│   └── utils/
│       └── logger.py              # Logging configuration
│
├── exports/                       # Export output directory
├── logs/                          # Application logs
├── output/                        # Generated outputs
│
├── pyproject.toml                 # Project metadata & dependencies
├── README.md                      # This file
└── .env                          # Environment variables (not in repo)
```

---

## 🔑 Core Components

### 1. **Ingestion Pipeline** (`app/ingestion/`)
Fetches cricket news from multiple RSS feeds:
- ESPN Cricinfo
- The Hindu Cricket
- Cricbuzz
- NDTV Sports
- Times of India
- India TV News
- And more...

### 2. **Processing Pipeline** (`app/processing/`)
Transforms raw articles into processed articles:
- **Scraper**: Extracts full content from article URLs
- **Embedder**: Generates semantic embeddings using Sentence Transformers
- **Clusterer**: Groups similar articles using vector similarity
- **Representative Selector**: Picks the best article from each cluster

### 3. **Generation Pipeline** (`app/generation/`)
Creates engaging tweets from articles:
- Uses LangChain with LLMs (OpenAI, Ollama)
- Structured output validation with Pydantic
- Customizable prompt templates
- Automatic hashtag and mention inclusion

### 4. **Posting Pipeline** (`app/posting/`)
Distributes tweets to social networks:
- Threads API integration via Tweepy
- Status tracking (pending, posted, failed)
- Rate limiting and error handling

---

## 💻 Development

### Code Quality Tools

The project uses code quality tools configured in `pyproject.toml`:

```bash
# Format code with Black
uv run black app/

# Sort imports with isort
uv run isort app/

# Both in one command
uv run black . && uv run isort .
```

### Logging

Application uses structured logging with the `get_logger()` utility:

```python
from app.utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Processing started...")
logger.error("An error occurred!")
```

Logs are stored in the `logs/` directory.

---

## 🔧 Configuration & API Setup

### Open Router API Setup

1. Sign up at [openrouter.ai](https://openrouter.ai)
2. Generate an API key
3. Add to `.env`: `OPEN_ROUTER_API_KEY=your_key`

### Threads API Setup

1. Register your app on Meta/Threads developer portal
2. Get your API credentials
3. Add to `.env`: `THREADS_API_KEY=your_key`

### Database Setup

Configure PostgreSQL connection string:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/twitter_bot
```

---

## 📊 Database Schema Overview

### Raw Articles
- `id`: Unique identifier
- `title`: Article title
- `url`: Article URL
- `source`: RSS feed source
- `published_at`: Publication date
- `fetched_at`: When fetched
- `is_built`: Whether processed

### Articles
- `id`: Unique identifier
- `title`: Article title
- `content`: Full article content
- `key_points`: Extracted summary
- `embedding`: Vector embedding
- `cluster_id`: Cluster assignment
- `is_representative`: Whether representative of cluster

### Tweets
- `id`: Unique identifier
- `tweet_text`: Generated tweet content
- `article_id`: Associated article
- `status`: pending/posted/failed
- `posted_at`: Posting timestamp

---

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Test connection
psql postgresql://user:password@localhost:5432/twitter_bot -c "SELECT 1"
```

### API Key Errors

- Verify `.env` file exists in project root
- Check API keys are valid and active
- Ensure API quotas haven't been exceeded

### Missing Dependencies

```bash
# Reinstall dependencies
uv sync
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Use type hints
- Add docstrings to functions
- Write unit tests for new features
- Format with Black and isort

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📞 Support

For issues, questions, or feature requests, please open an issue on GitHub or contact the maintainers.

---

## 🎯 Roadmap

- [ ] Add advanced NLP preprocessing
- [ ] Implement tweet scheduling
- [ ] Add Twitter/X API integration
- [ ] Create web dashboard for monitoring
- [ ] Add multi-language support
- [ ] Implement A/B testing for tweet variations
- [ ] Add sentiment analysis
- [ ] Create admin panel

---

## 📚 Additional Resources

- [LangChain Documentation](https://docs.langchain.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Tweepy Documentation](https://docs.tweepy.org/)

---

**Made with ❤️ for cricket enthusiasts and tech lovers**
