#!/bin/bash

source ~/shoonya/venv/bin/activate

echo "🔄 Starting Shoonya Daily Loop: $(date)"

# 1. Fetch new knowledge (manual topic prompt)
read -p "🌐 Enter today's topic: " topic
echo "$topic" | python ~/shoonya/crawler.py

# 2. Ingest knowledge to memory
python ~/shoonya/ingest_engine.py

# 3. Generate beliefs via LLM
python ~/shoonya/belief_engine_llm.py

# 4. Reflect on beliefs
python ~/shoonya/reflector.py

echo "✅ Shoonya daily loop complete: $(date)"
