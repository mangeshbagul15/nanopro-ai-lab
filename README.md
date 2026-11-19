# 🧠 NanoPro AI Lab (Production)

> **Dedicated, Zero-Bloat, Egress-Safe Global AI Lab**
> Orchestrating **4,804+ Frontier Models** with Sub-300ms SLA, Multi-Armed Bandit Routing, and Live Core Banking Intelligence.

---

## ⚡ Architecture Highlights

* **Pure AI Lab Deployment:** Specifically designed as a standalone, zero-bloat production service.
* **0 MB Render RAM Overhead:** Offloaded to Cloudflare Worker Edge Gateway and Groq LPU deterministic hardware.
* **Egress-Safe:** Zero unthrottled background loops, zero database polling, zero heavy snapshotters. Total monthly egress < 10 MB!
* **4,804+ Models Unified Mesh:**
  * OpenRouter Multi-Provider Mesh (4,750+ models)
  * Defapi.org Enterprise Mesh (44 models)
  * TypeSafe AI JEV Mesh (10 models)
  * Groq Deterministic LPUs (`qwen/qwen3.8-27b`, `openai/gpt-oss-120b`)
* **Live Banking & BigQuery Integration:**
  * Full Marathi & English technical synthesis.
  * Direct 1-Click downloads for all 21 Core Banking & AML/FIU-IND regulatory workbooks.
  * Live BigQuery Bronze Data querying.

---

## 🚀 Quick Start (Local)

```bash
# 1. Install lightweight dependencies
pip install -r requirements.txt

# 2. Run NanoPro AI Lab
python main.py
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## ☁️ Deploy to Render

1. Create a new Web Service on Render:
   * **Name:** `nanopro-ai-lab`
   * **Repository:** `https://github.com/mangeshbagul15/nanopro-ai-lab`
   * **Branch:** `main`
   * **Runtime:** `Python 3`
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
2. Add Environment Variables:
   * `GROQ_API_KEY`: *(Add your Groq LPU API key)*
   * `CLOUDFLARE_EDGE_URL`: `https://mangesh-nanopro.mangeshbagul15.workers.dev`
