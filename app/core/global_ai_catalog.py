"""
Mangesh Nano Pro AI Studio - Global AI Lab Catalog
Comprehensive Master Registry of All 32+ World AI Foundational Creators & 185+ Models.
Covers USA, China, Europe, Global/Middle East, and India.
"""

from typing import Dict, Any, List, Optional
import time

# Master Registry of All 32+ Global AI Creators & Labs
GLOBAL_AI_CREATORS: Dict[str, Dict[str, Any]] = {
    "defapi": {
        "id": "defapi",
        "name": "Defapi Frontier Hub",
        "country": "USA",
        "flag": "🌐",
        "category": "Frontier Multimodal Aggregator",
        "description": "Unified frontier access for Gemini 4 Neon, GPT-6 Astra, Claude Fable 5.2, Sora 2 Pro, and Veo 3.1.",
        "website": "https://defapi.org",
        "status": "OPERATIONAL",
        "models": [
            {"id": "defapi/google/gemini-4-neon", "name": "Gemini 4 Neon", "tier": "Frontier", "context": "2M", "elo": 1425, "latency_ms": 1100, "type": "Multimodal Frontier"},
            {"id": "defapi/google/gemini-4-hydrogen", "name": "Gemini 4 Hydrogen", "tier": "Frontier", "context": "2M", "elo": 1415, "latency_ms": 1050, "type": "Multimodal Frontier"},
            {"id": "defapi/google/gemini-3.7-flash", "name": "Gemini 3.7 Flash", "tier": "High", "context": "1M", "elo": 1360, "latency_ms": 280, "type": "Ultra Fast Flash"},
            {"id": "defapi/anthropic/claude-fable-5-2", "name": "Claude Fable 5.2", "tier": "Frontier", "context": "500k", "elo": 1430, "latency_ms": 2200, "type": "Deep Reasoning"},
            {"id": "defapi/anthropic/claude-opus-5.5", "name": "Claude Opus 5.5", "tier": "Frontier", "context": "200k", "elo": 1410, "latency_ms": 1900, "type": "Cognitive SOTA"},
            {"id": "defapi/openai/gpt-6-astra", "name": "GPT-6 Astra", "tier": "Frontier", "context": "1M", "elo": 1420, "latency_ms": 1300, "type": "Frontier Reasoning"},
            {"id": "defapi/openai/gpt-5.6-luna", "name": "GPT-5.6 Luna", "tier": "High", "context": "512k", "elo": 1375, "latency_ms": 850, "type": "Production Frontier"},
            {"id": "defapi/openai/sora-2-pro", "name": "Sora 2 Pro", "tier": "Media", "context": "128k", "elo": 1390, "latency_ms": 3500, "type": "Video Synthesis"}
        ]
    },
    "typesafe": {
        "id": "typesafe",
        "name": "TypeSafe AI (JEV)",
        "country": "USA",
        "flag": "⚡",
        "category": "System One Calibrated Reasoning",
        "description": "Creators of the JEV sub-50ms calibrated decision and fast reasoning models.",
        "website": "https://jevtypesafeai.com",
        "status": "OPERATIONAL",
        "models": [
            {"id": "jev/jev-latest", "name": "JEV Latest", "tier": "Frontier", "context": "128k", "elo": 1380, "latency_ms": 45, "type": "System One Decision"},
            {"id": "jev/jev-decision-fast", "name": "JEV Decision Fast", "tier": "High", "context": "64k", "elo": 1350, "latency_ms": 30, "type": "Ultra Low Latency"},
            {"id": "jev/jev-decision-deep", "name": "JEV Decision Deep Logic", "tier": "Frontier", "context": "128k", "elo": 1395, "latency_ms": 120, "type": "Calibrated Logic"},
            {"id": "jev/typesafe/jev-1.13", "name": "TypeSafe JEV 1.13", "tier": "High", "context": "64k", "elo": 1365, "latency_ms": 50, "type": "Production Decision"}
        ]
    },
    # =========================================================================
    # 1. UNITED STATES (USA - 12 Frontier Labs)
    # =========================================================================
    "openai": {
        "id": "openai",
        "name": "OpenAI",
        "country": "USA",
        "flag": "🇺🇸",
        "category": "Frontier Commercial & Open-Weights",
        "description": "Creators of GPT-4o, o1, o3, Codex architecture and GPT-OSS.",
        "website": "https://openai.com",
        "status": "OPERATIONAL",
        "models": [
            {"id": "gpt-5.4", "name": "OpenAI GPT 5.4", "tier": "Frontier", "context": "1M", "elo": 1380, "latency_ms": 1100, "type": "Closed API"},
            {"id": "gpt-5.2", "name": "OpenAI GPT 5.2", "tier": "Frontier", "context": "512k", "elo": 1345, "latency_ms": 950, "type": "Closed API"},
            {"id": "gpt-4o", "name": "GPT-4o Omnimodal", "tier": "Default", "context": "128k", "elo": 1330, "latency_ms": 620, "type": "Closed API"},
            {"id": "gpt-4o-mini", "name": "GPT-4o mini", "tier": "Low", "context": "128k", "elo": 1260, "latency_ms": 280, "type": "Closed API"},
            {"id": "o3", "name": "OpenAI o3", "tier": "Reasoning", "context": "200k", "elo": 1410, "latency_ms": 2800, "type": "Thinking"},
            {"id": "o3-mini", "name": "OpenAI o3-mini", "tier": "Reasoning", "context": "200k", "elo": 1370, "latency_ms": 1200, "type": "Thinking"},
            {"id": "o1", "name": "OpenAI o1", "tier": "Reasoning", "context": "200k", "elo": 1360, "latency_ms": 3200, "type": "Thinking"},
            {"id": "codex-6-luna", "name": "Codex 6 Luna", "tier": "Frontier", "context": "256k", "elo": 1395, "latency_ms": 980, "type": "Specialized Coding"},
            {"id": "codex-5.6-terra", "name": "Codex 5.6 Terra", "tier": "Default", "context": "128k", "elo": 1340, "latency_ms": 650, "type": "Production Coding"},
            {"id": "codex-5.6-luna", "name": "Codex 5.6 Luna", "tier": "High", "context": "128k", "elo": 1335, "latency_ms": 420, "type": "Agile Coding"},
            {"id": "gpt-oss-120b", "name": "GPT-OSS 120B", "tier": "Advance", "context": "64k", "elo": 1320, "latency_ms": 780, "type": "Open-Weights"}
        ]
    },
    "anthropic": {
        "id": "anthropic",
        "name": "Anthropic",
        "country": "USA",
        "flag": "🇺🇸",
        "category": "Frontier AI & Code Leader",
        "description": "Creators of Claude Opus, Sonnet, Haiku, and Fable series.",
        "website": "https://anthropic.com",
        "status": "OPERATIONAL",
        "models": [
            {"id": "claude-fable-5.2", "name": "Fable 5.2", "tier": "Frontier", "context": "500k", "elo": 1420, "latency_ms": 2400, "type": "Ultra Challenge"},
            {"id": "claude-fable-5.1", "name": "Fable 5.1", "tier": "Frontier", "context": "500k", "elo": 1400, "latency_ms": 2200, "type": "Ultra Challenge"},
            {"id": "claude-fable-5", "name": "Fable 5", "tier": "Frontier", "context": "500k", "elo": 1390, "latency_ms": 2100, "type": "Ultra Challenge"},
            {"id": "claude-opus-5.5", "name": "Claude Opus 5.5", "tier": "Excellent", "context": "200k", "elo": 1405, "latency_ms": 1900, "type": "Deep Brain"},
            {"id": "claude-opus-4.6-thinking", "name": "Claude Opus 4.6 (Thinking)", "tier": "Excellent", "context": "200k", "elo": 1385, "latency_ms": 2100, "type": "Cognitive Thinking"},
            {"id": "claude-opus-5", "name": "Claude Opus 5", "tier": "Excellent", "context": "200k", "elo": 1375, "latency_ms": 1800, "type": "Deep Logic"},
            {"id": "claude-opus-4.8", "name": "Claude Opus 4.8", "tier": "Advance", "context": "200k", "elo": 1360, "latency_ms": 1700, "type": "Legacy High"},
            {"id": "claude-sonnet-5.5", "name": "Claude Sonnet 5.5", "tier": "High", "context": "200k", "elo": 1390, "latency_ms": 680, "type": "Coding King"},
            {"id": "claude-sonnet-4.6-thinking", "name": "Claude Sonnet 4.6 (Thinking)", "tier": "High", "context": "200k", "elo": 1370, "latency_ms": 750, "type": "Extended Thinking"},
            {"id": "claude-sonnet-5", "name": "Claude Sonnet 5", "tier": "Default", "context": "200k", "elo": 1350, "latency_ms": 620, "type": "Workhorse"},
            {"id": "claude-sonnet-4.6", "name": "Claude Sonnet 4.6", "tier": "Default", "context": "200k", "elo": 1340, "latency_ms": 590, "type": "Workhorse"},
            {"id": "claude-haiku-5.5", "name": "Claude Haiku 5.5", "tier": "Low", "context": "200k", "elo": 1285, "latency_ms": 220, "type": "Fast Completion"}
        ]
    },
    "google": {
        "id": "google",
        "name": "Google DeepMind",
        "country": "USA",
        "flag": "🇺🇸",
        "category": "Hyperscale AI & Science",
        "description": "Creators of Gemini series, Gemma, and AlphaFold.",
        "website": "https://deepmind.google",
        "status": "OPERATIONAL",
        "models": [
            {"id": "gemini-4-argon", "name": "Gemini 4 Argon", "tier": "Frontier", "context": "2M", "elo": 1408, "latency_ms": 1350, "type": "Science & Math"},
            {"id": "gemini-4-carbon", "name": "Gemini 4 Carbon", "tier": "Frontier", "context": "2M", "elo": 1398, "latency_ms": 1400, "type": "Heavyweight"},
            {"id": "gemini-3.8-flash-high", "name": "Gemini 3.8 Flash High", "tier": "High", "context": "1M", "elo": 1355, "latency_ms": 320, "type": "Ultra High Speed"},
            {"id": "gemini-flash-3.8", "name": "Gemini Flash 3.8", "tier": "Low", "context": "1M", "elo": 1340, "latency_ms": 280, "type": "Long Context Flash"},
            {"id": "gemini-flash-3.7", "name": "Gemini Flash 3.7", "tier": "Low", "context": "1M", "elo": 1320, "latency_ms": 250, "type": "Fast Stream"},
            {"id": "gemini-2.0-flash", "name": "Gemini 2.0 Flash", "tier": "Low", "context": "1M", "elo": 1315, "latency_ms": 230, "type": "Multimodal Flash"},
            {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro", "tier": "Default", "context": "2M", "elo": 1345, "latency_ms": 900, "type": "Enterprise Pro"},
            {"id": "gemma-2-27b", "name": "Gemma 2 27B", "tier": "Advance", "context": "32k", "elo": 1290, "latency_ms": 480, "type": "Open-Weights"},
            {"id": "codegemma-7b", "name": "CodeGemma 7B", "tier": "Low", "context": "16k", "elo": 1220, "latency_ms": 190, "type": "Local Code"}
        ]
    },
    "meta": {
        "id": "meta",
        "name": "Meta AI (FAIR)",
        "country": "USA",
        "flag": "🇺🇸",
        "category": "Open-Source Champion",
        "description": "Creators of the open-weights Llama 3/4 series.",
        "website": "https://ai.meta.com",
        "status": "OPERATIONAL",
        "models": [
            {"id": "llama-3.1-405b", "name": "Llama 3.1 405B", "tier": "Frontier", "context": "128k", "elo": 1365, "latency_ms": 1600, "type": "Colossal Open"},
            {"id": "llama-3.3-70b", "name": "Llama 3.3 70B", "tier": "Default", "context": "128k", "elo": 1342, "latency_ms": 550, "type": "Production Workhorse"},
            {"id": "llama-3.1-70b", "name": "Llama 3.1 70B", "tier": "Default", "context": "128k", "elo": 1325, "latency_ms": 580, "type": "Standard Open"},
            {"id": "llama-3.2-3b", "name": "Llama 3.2 3B", "tier": "Low", "context": "128k", "elo": 1205, "latency_ms": 110, "type": "Edge & Local"},
            {"id": "llama-3.2-1b", "name": "Llama 3.2 1B", "tier": "Low", "context": "128k", "elo": 1140, "latency_ms": 70, "type": "Micro Local"},
            {"id": "code-llama-70b", "name": "Code Llama 70B", "tier": "Advance", "context": "100k", "elo": 1290, "latency_ms": 680, "type": "Specialized Open Code"}
        ]
    },
    "xai": {
        "id": "xai",
        "name": "xAI (Elon Musk)",
        "country": "USA",
        "flag": "🇺🇸",
        "category": "Frontier Real-Time Intelligence",
        "description": "Creators of Grok, powered by the Memphis Colossus 100k GPU cluster.",
        "website": "https://x.ai",
        "status": "OPERATIONAL",
        "models": [
            {"id": "grok-4.7", "name": "Grok 4.7", "tier": "Frontier", "context": "131k", "elo": 1388, "latency_ms": 820, "type": "Real-Time Thinker"},
            {"id": "grok-4.6", "name": "Grok 4.6", "tier": "High", "context": "131k", "elo": 1350, "latency_ms": 790, "type": "Enterprise Grok"},
            {"id": "grok-3", "name": "Grok 3", "tier": "Default", "context": "131k", "elo": 1330, "latency_ms": 710, "type": "Colossus Trained"},
            {"id": "grok-2", "name": "Grok 2 (Vision)", "tier": "Default", "context": "131k", "elo": 1300, "latency_ms": 650, "type": "Multimodal"}
        ]
    },
    "microsoft": {
        "id": "microsoft",
        "name": "Microsoft AI",
        "country": "USA",
        "flag": "🇺🇸",
        "category": "Small Language Models & Enterprise",
        "description": "Creators of Phi series and high-efficiency architectures.",
        "website": "https://microsoft.com/ai",
        "status": "OPERATIONAL",
        "models": [
            {"id": "phi-4", "name": "Phi-4 (14B)", "tier": "Advance", "context": "16k", "elo": 1320, "latency_ms": 320, "type": "High Math/Reasoning"},
            {"id": "phi-3.5-mini", "name": "Phi-3.5 Mini", "tier": "Low", "context": "128k", "elo": 1240, "latency_ms": 140, "type": "SLM Fast"},
            {"id": "wizardlm-2-8x22b", "name": "WizardLM-2 8x22B", "tier": "Default", "context": "64k", "elo": 1310, "latency_ms": 750, "type": "Complex Reasoning"}
        ]
    },
    "amazon": {
        "id": "amazon",
        "name": "Amazon AWS (Nova)",
        "country": "USA",
        "flag": "🇺🇸",
        "category": "Cloud Hyper-Scale",
        "description": "Creators of Amazon Nova foundation models on AWS Bedrock.",
        "website": "https://aws.amazon.com/bedrock",
        "status": "OPERATIONAL",
        "models": [
            {"id": "amazon-nova-pro", "name": "Amazon Nova Pro", "tier": "High", "context": "300k", "elo": 1330, "latency_ms": 610, "type": "Cloud Enterprise"},
            {"id": "amazon-nova-lite", "name": "Amazon Nova Lite", "tier": "Low", "context": "300k", "elo": 1260, "latency_ms": 220, "type": "Cost-Effective"},
            {"id": "amazon-nova-micro", "name": "Amazon Nova Micro", "tier": "Low", "context": "128k", "elo": 1200, "latency_ms": 130, "type": "Sub-100ms Text"}
        ]
    },
    "nvidia": {
        "id": "nvidia",
        "name": "Nvidia Research",
        "country": "USA",
        "flag": "🇺🇸",
        "category": "GPU Architecture & Hardware AI",
        "description": "Creators of Nemotron and NVLM open models.",
        "website": "https://nvidia.com",
        "status": "OPERATIONAL",
        "models": [
            {"id": "nemotron-4-340b", "name": "Nemotron-4 340B", "tier": "Frontier", "context": "4k", "elo": 1350, "latency_ms": 1450, "type": "Synthetic Data Gen"},
            {"id": "nemotron-70b", "name": "Llama-3.1-Nemotron-70B", "tier": "High", "context": "128k", "elo": 1355, "latency_ms": 510, "type": "GPU Optimized"},
            {"id": "nvlm-d-72b", "name": "NVLM-D 72B (Vision)", "tier": "High", "context": "32k", "elo": 1335, "latency_ms": 680, "type": "Open Multimodal"}
        ]
    },
    "databricks": {
        "id": "databricks",
        "name": "Databricks / MosaicML",
        "country": "USA",
        "flag": "🇺🇸",
        "category": "Enterprise Lakehouse AI",
        "description": "Creators of DBRX, open MoE model for enterprise data.",
        "website": "https://databricks.com",
        "status": "OPERATIONAL",
        "models": [
            {"id": "dbrx-instruct", "name": "DBRX Instruct (132B MoE)", "tier": "Default", "context": "32k", "elo": 1305, "latency_ms": 640, "type": "Open MoE"}
        ]
    },
    "cohere": {
        "id": "cohere",
        "name": "Cohere",
        "country": "USA/Canada",
        "flag": "🇺🇸",
        "category": "Enterprise RAG & Search",
        "description": "Creators of Command R series and multilingual Aya.",
        "website": "https://cohere.com",
        "status": "OPERATIONAL",
        "models": [
            {"id": "command-r-plus", "name": "Command R+ (104B)", "tier": "High", "context": "128k", "elo": 1315, "latency_ms": 670, "type": "RAG Powerhouse"},
            {"id": "command-r", "name": "Command R (35B)", "tier": "Default", "context": "128k", "elo": 1270, "latency_ms": 420, "type": "Enterprise Retrieval"},
            {"id": "aya-23", "name": "Aya 23 (Multilingual)", "tier": "Default", "context": "8k", "elo": 1250, "latency_ms": 390, "type": "23 Languages"}
        ]
    },
    "apple": {
        "id": "apple",
        "name": "Apple Intelligence",
        "country": "USA",
        "flag": "🇺🇸",
        "category": "On-Device & Private Cloud",
        "description": "Apple Foundation Models (AFM) and OpenELM.",
        "website": "https://apple.com",
        "status": "OPERATIONAL",
        "models": [
            {"id": "afm-cloud", "name": "AFM Private Cloud Compute", "tier": "High", "context": "32k", "elo": 1310, "latency_ms": 490, "type": "Private Cloud"},
            {"id": "afm-device-3b", "name": "AFM On-Device (3B)", "tier": "Low", "context": "4k", "elo": 1180, "latency_ms": 90, "type": "Neural Engine"},
            {"id": "openelm-3b", "name": "OpenELM 3B", "tier": "Low", "context": "2k", "elo": 1130, "latency_ms": 80, "type": "Open Architecture"}
        ]
    },
    "ai2": {
        "id": "ai2",
        "name": "Allen Institute for AI (AI2)",
        "country": "USA",
        "flag": "🇺🇸",
        "category": "Scientific & Open Source",
        "description": "Creators of OLMo and Molmo 100% open models.",
        "website": "https://allenai.org",
        "status": "OPERATIONAL",
        "models": [
            {"id": "molmo-72b", "name": "Molmo 72B (Multimodal)", "tier": "High", "context": "16k", "elo": 1320, "latency_ms": 650, "type": "Open Vision"},
            {"id": "olmo-7b", "name": "OLMo 7B (Fully Open)", "tier": "Low", "context": "4k", "elo": 1190, "latency_ms": 160, "type": "Transparent Science"}
        ]
    },

    # =========================================================================
    # 2. CHINA (11 Frontier Labs & Tech Giants)
    # =========================================================================
    "deepseek": {
        "id": "deepseek",
        "name": "DeepSeek",
        "country": "China",
        "flag": "🇨🇳",
        "category": "Open-Weights & Reasoning Titan",
        "description": "Creators of DeepSeek-V3, R1 (Reasoning), and Coder.",
        "website": "https://deepseek.com",
        "status": "OPERATIONAL",
        "models": [
            {"id": "deepseek-r1", "name": "DeepSeek-R1 (Reasoning)", "tier": "Excellent", "context": "128k", "elo": 1405, "latency_ms": 1850, "type": "Math & Code Titan"},
            {"id": "deepseek-v4-pro", "name": "DeepSeek-V4-Pro", "tier": "Frontier", "context": "128k", "elo": 1385, "latency_ms": 850, "type": "Next-Gen Frontier"},
            {"id": "deepseek-v3", "name": "DeepSeek-V3 (671B MoE)", "tier": "High", "context": "128k", "elo": 1360, "latency_ms": 690, "type": "Ultra-Low Cost MoE"},
            {"id": "deepseek-coder-v2", "name": "DeepSeek-Coder-V2 (236B)", "tier": "Default", "context": "128k", "elo": 1340, "latency_ms": 520, "type": "338 Languages"},
            {"id": "deepseek-flash", "name": "DeepSeek-Flash", "tier": "Low", "context": "64k", "elo": 1270, "latency_ms": 190, "type": "Micro Cost (0.1x)"}
        ]
    },
    "alibaba": {
        "id": "alibaba",
        "name": "Alibaba Cloud (Qwen)",
        "country": "China",
        "flag": "🇨🇳",
        "category": "Open-Weights & Coding Leader",
        "description": "Creators of Qwen 2.5 Coder, Qwen-Max, and Qwen4.",
        "website": "https://qwenlm.github.io",
        "status": "OPERATIONAL",
        "models": [
            {"id": "qwen4-max-preview", "name": "Qwen4-Max-Preview", "tier": "Frontier", "context": "128k", "elo": 1390, "latency_ms": 890, "type": "New Flagship (0.1x)"},
            {"id": "qwen3.8-max", "name": "Qwen3.8-Max", "tier": "High", "context": "128k", "elo": 1365, "latency_ms": 780, "type": "High Accuracy"},
            {"id": "qwen-2.5-coder-32b", "name": "Qwen 2.5 Coder 32B", "tier": "Default", "context": "128k", "elo": 1350, "latency_ms": 460, "type": "World's Best Open Coder"},
            {"id": "qwen-2.5-72b", "name": "Qwen 2.5 72B Instruct", "tier": "Default", "context": "128k", "elo": 1345, "latency_ms": 540, "type": "Open Heavyweight"},
            {"id": "qwen-2.5-coder-7b", "name": "Qwen 2.5 Coder 7B", "tier": "Low", "context": "128k", "elo": 1260, "latency_ms": 170, "type": "Fast Local Coder"},
            {"id": "qwen3.8-flash", "name": "Qwen3.8-Flash", "tier": "Low", "context": "128k", "elo": 1275, "latency_ms": 180, "type": "Micro Cost (0.1x)"},
            {"id": "qwen-2.5-math-72b", "name": "Qwen 2.5 Math 72B", "tier": "Advance", "context": "32k", "elo": 1370, "latency_ms": 720, "type": "Mathematical Proofs"}
        ]
    },
    "zhipu": {
        "id": "zhipu",
        "name": "Zhipu AI (GLM)",
        "country": "China",
        "flag": "🇨🇳",
        "category": "Open-Weights & 100% Free Flash API",
        "description": "Tsinghua spinout, creators of GLM-4, GLM-5, and CodeGeeX.",
        "website": "https://zhipuai.cn",
        "status": "OPERATIONAL",
        "models": [
            {"id": "glm-5.3", "name": "GLM-5.3", "tier": "Frontier", "context": "128k", "elo": 1360, "latency_ms": 810, "type": "High Reasoning"},
            {"id": "glm-4-plus", "name": "GLM-4-Plus", "tier": "High", "context": "128k", "elo": 1335, "latency_ms": 710, "type": "Bilingual Pro"},
            {"id": "glm-5.3-flash", "name": "GLM-5.3-Flash", "tier": "Low", "context": "128k", "elo": 1265, "latency_ms": 160, "type": "Micro Cost"},
            {"id": "glm-4-flash", "name": "GLM-4-Flash", "tier": "Low", "context": "128k", "elo": 1250, "latency_ms": 150, "type": "100% Free Cloud API"},
            {"id": "codegeex-4-9b", "name": "CodeGeeX-4 (9B)", "tier": "Low", "context": "128k", "elo": 1240, "latency_ms": 190, "type": "Open Code Autocomplete"}
        ]
    },
    "moonshot": {
        "id": "moonshot",
        "name": "Moonshot AI (Kimi)",
        "country": "China",
        "flag": "🇨🇳",
        "category": "Long Context Titan (2M Tokens)",
        "description": "Creators of Kimi, world pioneer in 2,000,000+ token context.",
        "website": "https://kimi.ai",
        "status": "OPERATIONAL",
        "models": [
            {"id": "kimi-k3.1-pro", "name": "Kimi-K3.1-Pro", "tier": "Frontier", "context": "2M", "elo": 1375, "latency_ms": 940, "type": "Massive 2M Memory"},
            {"id": "kimi-k3", "name": "Kimi K3", "tier": "High", "context": "2M", "elo": 1350, "latency_ms": 890, "type": "Codebase Scanner"},
            {"id": "kimi-k2.8-preview", "name": "Kimi-K2.8-Preview", "tier": "Default", "context": "2M", "elo": 1320, "latency_ms": 780, "type": "Long Document AI"}
        ]
    },
    "bytedance": {
        "id": "bytedance",
        "name": "ByteDance (Doubao)",
        "country": "China",
        "flag": "🇨🇳",
        "category": "Consumer Scale AI",
        "description": "Creators of Doubao foundation models running at billion-request scale.",
        "website": "https://volcengine.com",
        "status": "OPERATIONAL",
        "models": [
            {"id": "doubao-pro-128k", "name": "Doubao Pro 128k", "tier": "High", "context": "128k", "elo": 1340, "latency_ms": 490, "type": "Enterprise Pro"},
            {"id": "doubao-lite-128k", "name": "Doubao Lite 128k", "tier": "Low", "context": "128k", "elo": 1260, "latency_ms": 170, "type": "Ultra-Low Cost"}
        ]
    },
    "baidu": {
        "id": "baidu",
        "name": "Baidu (Ernie)",
        "country": "China",
        "flag": "🇨🇳",
        "category": "Search & Knowledge Graph",
        "description": "Creators of Ernie 4.0, China's premier search-integrated LLM.",
        "website": "https://yiyan.baidu.com",
        "status": "OPERATIONAL",
        "models": [
            {"id": "ernie-4.0-turbo", "name": "Ernie 4.0 Turbo", "tier": "High", "context": "128k", "elo": 1335, "latency_ms": 680, "type": "Knowledge Enhanced"},
            {"id": "ernie-speed", "name": "Ernie Speed", "tier": "Low", "context": "128k", "elo": 1240, "latency_ms": 180, "type": "Zero Cost Free API"}
        ]
    },
    "tencent": {
        "id": "tencent",
        "name": "Tencent (Hunyuan)",
        "country": "China",
        "flag": "🇨🇳",
        "category": "Multimodal & 3D/Video",
        "description": "Creators of Hunyuan-Large and Hunyuan-Video open models.",
        "website": "https://hunyuan.tencent.com",
        "status": "OPERATIONAL",
        "models": [
            {"id": "hunyuan-large", "name": "Hunyuan-Large (389B MoE)", "tier": "Frontier", "context": "256k", "elo": 1355, "latency_ms": 820, "type": "Open MoE Titan"},
            {"id": "hunyuan-standard", "name": "Hunyuan-Standard", "tier": "Default", "context": "32k", "elo": 1300, "latency_ms": 450, "type": "WeChat Scaled"}
        ]
    },
    "minimax": {
        "id": "minimax",
        "name": "MiniMax",
        "country": "China",
        "flag": "🇨🇳",
        "category": "Voice, Speech & Flash",
        "description": "Creators of abab 6.5s and MiniMax-M3.1 series.",
        "website": "https://minimaxi.com",
        "status": "OPERATIONAL",
        "models": [
            {"id": "minimax-m3.1-flash", "name": "MiniMax-M3.1-Flash", "tier": "Low", "context": "128k", "elo": 1280, "latency_ms": 160, "type": "Voice & Text Flash (0.1x)"},
            {"id": "abab-6.5s", "name": "abab 6.5s MoE", "tier": "High", "context": "245k", "elo": 1330, "latency_ms": 520, "type": "High Speed MoE"}
        ]
    },
    "zeroone": {
        "id": "zeroone",
        "name": "01.AI (Kai-Fu Lee)",
        "country": "China",
        "flag": "🇨🇳",
        "category": "Bilingual Frontier AI",
        "description": "Creators of Yi-Large, Yi-Coder, and Yi-Lightning.",
        "website": "https://01.ai",
        "status": "OPERATIONAL",
        "models": [
            {"id": "yi-lightning", "name": "Yi-Lightning", "tier": "High", "context": "16k", "elo": 1360, "latency_ms": 410, "type": "LMSYS Top 10"},
            {"id": "yi-large", "name": "Yi-Large", "tier": "Default", "context": "32k", "elo": 1330, "latency_ms": 610, "type": "Bilingual Frontier"},
            {"id": "yi-coder-9b", "name": "Yi-Coder 9B", "tier": "Low", "context": "128k", "elo": 1250, "latency_ms": 180, "type": "Open Code Base"}
        ]
    },
    "baichuan": {
        "id": "baichuan",
        "name": "Baichuan AI",
        "country": "China",
        "flag": "🇨🇳",
        "category": "Healthcare & Knowledge AI",
        "description": "Creators of Baichuan 2/3/4 medical and general LLMs.",
        "website": "https://baichuan-ai.com",
        "status": "OPERATIONAL",
        "models": [
            {"id": "baichuan-4", "name": "Baichuan 4", "tier": "High", "context": "32k", "elo": 1320, "latency_ms": 590, "type": "Medical Specialist"},
            {"id": "baichuan-2-13b", "name": "Baichuan 2 13B", "tier": "Low", "context": "4k", "elo": 1210, "latency_ms": 190, "type": "Open Weights"}
        ]
    },
    "stepfun": {
        "id": "stepfun",
        "name": "StepFun (阶跃星辰)",
        "country": "China",
        "flag": "🇨🇳",
        "category": "Step-Series MoE",
        "description": "Creators of Step-1, Step-2 trillion-parameter MoE models.",
        "website": "https://stepfun.com",
        "status": "OPERATIONAL",
        "models": [
            {"id": "step-2-16k", "name": "Step-2 Trillion MoE", "tier": "Frontier", "context": "16k", "elo": 1350, "latency_ms": 790, "type": "Trillion MoE"},
            {"id": "step-1-flash", "name": "Step-1 Flash", "tier": "Low", "context": "8k", "elo": 1260, "latency_ms": 210, "type": "Agile Step"}
        ]
    },

    # =========================================================================
    # 3. EUROPE (3 Frontier Labs)
    # =========================================================================
    "mistral": {
        "id": "mistral",
        "name": "Mistral AI",
        "country": "France",
        "flag": "🇫🇷",
        "category": "European Open-Weights Flagship",
        "description": "Creators of Codestral, Mistral Large, and Mixtral 8x22B.",
        "website": "https://mistral.ai",
        "status": "OPERATIONAL",
        "models": [
            {"id": "mistral-large-2", "name": "Mistral Large 2 (123B)", "tier": "Frontier", "context": "128k", "elo": 1360, "latency_ms": 680, "type": "European Flagship"},
            {"id": "codestral-22b", "name": "Codestral 22B", "tier": "High", "context": "32k", "elo": 1345, "latency_ms": 420, "type": "Specialized 80+ Languages"},
            {"id": "mixtral-8x22b", "name": "Mixtral 8x22B", "tier": "Default", "context": "64k", "elo": 1320, "latency_ms": 590, "type": "Open Weights MoE"},
            {"id": "ministral-8b", "name": "Ministral 8B", "tier": "Low", "context": "128k", "elo": 1260, "latency_ms": 170, "type": "Edge European"}
        ]
    },
    "aleph_alpha": {
        "id": "aleph_alpha",
        "name": "Aleph Alpha",
        "country": "Germany",
        "flag": "🇩🇪",
        "category": "Sovereign Enterprise AI",
        "description": "Creators of Luminous, Germany's sovereign AI platform.",
        "website": "https://aleph-alpha.com",
        "status": "OPERATIONAL",
        "models": [
            {"id": "luminous-world", "name": "Luminous World (300B)", "tier": "High", "context": "32k", "elo": 1290, "latency_ms": 780, "type": "Sovereign EU"},
            {"id": "luminous-base", "name": "Luminous Base", "tier": "Low", "context": "2k", "elo": 1200, "latency_ms": 230, "type": "Auditable AI"}
        ]
    },
    "kyutai": {
        "id": "kyutai",
        "name": "Kyutai",
        "country": "France",
        "flag": "🇫🇷",
        "category": "Real-Time Voice AI",
        "description": "Creators of Moshi, world's first open real-time voice foundation model.",
        "website": "https://kyutai.org",
        "status": "OPERATIONAL",
        "models": [
            {"id": "moshi-voice", "name": "Moshi (Full Duplex Voice)", "tier": "High", "context": "Stream", "elo": 1310, "latency_ms": 160, "type": "Voice Foundation"}
        ]
    },

    # =========================================================================
    # 4. GLOBAL & MIDDLE EAST & ASIA (4 Labs)
    # =========================================================================
    "tii": {
        "id": "tii",
        "name": "Technology Innovation Institute (TII)",
        "country": "UAE",
        "flag": "🇦🇪",
        "category": "Middle East Open Supercomputing",
        "description": "Creators of Falcon 180B, Falcon 2 11B, and Falcon Mamba.",
        "website": "https://falconllm.tii.ae",
        "status": "OPERATIONAL",
        "models": [
            {"id": "falcon-180b", "name": "Falcon 180B", "tier": "Frontier", "context": "8k", "elo": 1320, "latency_ms": 1400, "type": "Open Weights Titan"},
            {"id": "falcon-2-11b", "name": "Falcon 2 11B (Vision)", "tier": "Low", "context": "32k", "elo": 1250, "latency_ms": 210, "type": "Multimodal Open"}
        ]
    },
    "naver": {
        "id": "naver",
        "name": "Naver (HyperCLOVA)",
        "country": "South Korea",
        "flag": "🇰🇷",
        "category": "Asian Search & Enterprise",
        "description": "Creators of HyperCLOVA X, leading Korean foundation model.",
        "website": "https://clova.ai",
        "status": "OPERATIONAL",
        "models": [
            {"id": "hyperclova-x", "name": "HyperCLOVA X", "tier": "High", "context": "32k", "elo": 1315, "latency_ms": 690, "type": "Asian Search Foundation"}
        ]
    },
    "upstage": {
        "id": "upstage",
        "name": "Upstage AI",
        "country": "South Korea",
        "flag": "🇰🇷",
        "category": "Solar Small Language Models",
        "description": "Creators of Solar 10.7B and Solar Pro high-efficiency models.",
        "website": "https://upstage.ai",
        "status": "OPERATIONAL",
        "models": [
            {"id": "solar-pro", "name": "Solar Pro (22B)", "tier": "High", "context": "64k", "elo": 1325, "latency_ms": 390, "type": "Depth Upscaled"},
            {"id": "solar-10.7b", "name": "Solar 10.7B Instruct", "tier": "Low", "context": "4k", "elo": 1245, "latency_ms": 170, "type": "Fast SLM"}
        ]
    },
    "rakuten": {
        "id": "rakuten",
        "name": "Rakuten AI",
        "country": "Japan",
        "flag": "🇯🇵",
        "category": "Japanese Language & Commerce",
        "description": "Creators of Rakuten AI 7B open foundation model.",
        "website": "https://rakuten.today",
        "status": "OPERATIONAL",
        "models": [
            {"id": "rakuten-ai-7b", "name": "Rakuten AI 7B Instruct", "tier": "Low", "context": "8k", "elo": 1210, "latency_ms": 190, "type": "Japanese Open"}
        ]
    },

    # =========================================================================
    # 5. INDIA (2 Indigenous Indian AI Labs)
    # =========================================================================
    "sarvam": {
        "id": "sarvam",
        "name": "Sarvam AI",
        "country": "India",
        "flag": "🇮🇳",
        "category": "Indic Language Foundation",
        "description": "Creators of Sarvam-1 and Sarvam-2, designed for 10+ Indian languages.",
        "website": "https://sarvam.ai",
        "status": "OPERATIONAL",
        "models": [
            {"id": "sarvam-2", "name": "Sarvam-2 (Indic Flagship)", "tier": "High", "context": "32k", "elo": 1300, "latency_ms": 380, "type": "10 Indian Languages"},
            {"id": "sarvam-1-2b", "name": "Sarvam-1 (2B)", "tier": "Low", "context": "8k", "elo": 1190, "latency_ms": 95, "type": "Edge Indic SLM"}
        ]
    },
    "krutrim": {
        "id": "krutrim",
        "name": "Krutrim AI (Ola)",
        "country": "India",
        "flag": "🇮🇳",
        "category": "Indian Sovereign AI",
        "description": "Bhavish Aggarwal's AI venture, trained on 22+ Indian languages.",
        "website": "https://olakrutrim.com",
        "status": "OPERATIONAL",
        "models": [
            {"id": "krutrim-pro", "name": "Krutrim Pro", "tier": "High", "context": "32k", "elo": 1285, "latency_ms": 420, "type": "Indian Culture & Code"},
            {"id": "krutrim-base", "name": "Krutrim Base", "tier": "Low", "context": "8k", "elo": 1180, "latency_ms": 160, "type": "22 Indian Languages"}
        ]
    }
}


def get_global_ai_stats() -> Dict[str, Any]:
    """Computes total counts, regional distributions, and catalog health."""
    total_labs = len(GLOBAL_AI_CREATORS)
    total_models = sum(len(c["models"]) for c in GLOBAL_AI_CREATORS.values())
    
    countries: Dict[str, int] = {}
    for c in GLOBAL_AI_CREATORS.values():
        ct = c["country"]
        countries[ct] = countries.get(ct, 0) + len(c["models"])

    return {
        "labs_count": total_labs,
        "models_count": total_models,
        "countries_count": len(countries),
        "distribution_by_country": countries,
        "engine_mode": "AUTO (High-Speed Intelligent Engine)",
        "sla_target_ms": 800,
        "catalog_version": "2026.11"
    }


def list_all_models_flat() -> List[Dict[str, Any]]:
    """Returns a flattened list of all 185+ models with their creator metadata."""
    flat = []
    for cid, creator in GLOBAL_AI_CREATORS.items():
        for m in creator["models"]:
            flat.append({
                **m,
                "creator_id": cid,
                "creator_name": creator["name"],
                "creator_country": creator["country"],
                "creator_flag": creator["flag"]
            })
    return flat


import os

_OPENROUTER_CACHE: Dict[str, Any] = {"models": [], "ts": 0}

def get_openrouter_models(force_refresh: bool = False) -> List[Dict[str, Any]]:
    """Fetches and caches all 432+ live frontier models from OpenRouter."""
    import urllib.request
    import json
    global _OPENROUTER_CACHE
    now = time.time()
    if not force_refresh and _OPENROUTER_CACHE["models"] and (now - _OPENROUTER_CACHE["ts"] < 3600):
        return _OPENROUTER_CACHE["models"]

    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    try:
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {key}", "User-Agent": "NanoPro-Studio/2026.11"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode("utf-8"))
            models = data.get("data", [])
            if models:
                _OPENROUTER_CACHE["models"] = models
                _OPENROUTER_CACHE["ts"] = now
                return models
    except Exception:
        pass
    return _OPENROUTER_CACHE["models"] or []


PROVIDER_SPECIALIZED_MODELS = [
    # -------------------------------------------------------------
    # 🌐 Defapi Frontier Hub (defapi/...)
    # -------------------------------------------------------------
    {"id": "defapi/google/gemini-4-neon", "name": "Gemini 4 Neon Frontier", "lab": "Defapi Frontier Hub", "country": "USA", "flag": "🌐", "tier": "flagship", "context": 2000000, "is_free": False},
    {"id": "defapi/google/gemini-4-hydrogen", "name": "Gemini 4 Hydrogen", "lab": "Defapi Frontier Hub", "country": "USA", "flag": "🌐", "tier": "flagship", "context": 2000000, "is_free": False},
    {"id": "defapi/google/gemini-3.7-flash", "name": "Gemini 3.7 Flash (<280ms)", "lab": "Defapi Frontier Hub", "country": "USA", "flag": "🌐", "tier": "fast", "context": 1000000, "is_free": True},
    {"id": "defapi/anthropic/claude-fable-5-2", "name": "Claude Fable 5.2 (Deep Logic)", "lab": "Defapi Frontier Hub", "country": "USA", "flag": "🌐", "tier": "reasoning", "context": 500000, "is_free": False},
    {"id": "defapi/anthropic/claude-opus-5.5", "name": "Claude Opus 5.5 Cognitive", "lab": "Defapi Frontier Hub", "country": "USA", "flag": "🌐", "tier": "flagship", "context": 200000, "is_free": False},
    {"id": "defapi/openai/gpt-6-astra", "name": "GPT-6 Astra Frontier Reasoning", "lab": "Defapi Frontier Hub", "country": "USA", "flag": "🌐", "tier": "reasoning", "context": 1000000, "is_free": False},
    {"id": "defapi/openai/gpt-5.6-luna", "name": "GPT-5.6 Luna High-Throughput", "lab": "Defapi Frontier Hub", "country": "USA", "flag": "🌐", "tier": "flagship", "context": 512000, "is_free": False},
    {"id": "defapi/openai/sora-2-pro", "name": "Sora 2 Pro Video Synthesis", "lab": "Defapi Frontier Hub", "country": "USA", "flag": "🌐", "tier": "media", "context": 128000, "is_free": False},
    {"id": "defapi/meta/llama-4-scout", "name": "Llama 4 Scout", "lab": "Defapi Frontier Hub", "country": "USA", "flag": "🌐", "tier": "flagship", "context": 256000, "is_free": False},
    {"id": "defapi/meta/llama-4-maverick", "name": "Llama 4 Maverick", "lab": "Defapi Frontier Hub", "country": "USA", "flag": "🌐", "tier": "flagship", "context": 256000, "is_free": False},
    {"id": "defapi/deepseek/deepseek-v4-frontier", "name": "DeepSeek V4 Frontier", "lab": "Defapi Frontier Hub", "country": "China", "flag": "🇨🇳", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "defapi/qwen/qwen-3-max", "name": "Alibaba Qwen 3 Max", "lab": "Defapi Frontier Hub", "country": "China", "flag": "🇨🇳", "tier": "flagship", "context": 128000, "is_free": False},

    # -------------------------------------------------------------
    # ⚡ TypeSafe AI JEV (jev/...)
    # -------------------------------------------------------------
    {"id": "jev/jev-latest", "name": "JEV Latest (Calibrated Decision)", "lab": "TypeSafe AI (JEV)", "country": "USA", "flag": "⚡", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "jev/jev-decision-fast", "name": "JEV Decision Fast (<30ms)", "lab": "TypeSafe AI (JEV)", "country": "USA", "flag": "⚡", "tier": "fast", "context": 64000, "is_free": True},
    {"id": "jev/jev-decision-deep", "name": "JEV Decision Deep Logic", "lab": "TypeSafe AI (JEV)", "country": "USA", "flag": "⚡", "tier": "reasoning", "context": 128000, "is_free": False},
    {"id": "jev/typesafe/jev-1.13", "name": "TypeSafe JEV 1.13 Production", "lab": "TypeSafe AI (JEV)", "country": "USA", "flag": "⚡", "tier": "flagship", "context": 64000, "is_free": False},
    {"id": "jev/typesafe/jev-reasoner-pro", "name": "JEV Reasoner Pro", "lab": "TypeSafe AI (JEV)", "country": "USA", "flag": "⚡", "tier": "reasoning", "context": 128000, "is_free": False},
    {"id": "jev/typesafe/jev-guard-v2", "name": "JEV Safety Guardrail v2", "lab": "TypeSafe AI (JEV)", "country": "USA", "flag": "⚡", "tier": "fast", "context": 32000, "is_free": True},
    {"id": "jev/typesafe/jev-code-reflex", "name": "JEV Code Reflex", "lab": "TypeSafe AI (JEV)", "country": "USA", "flag": "⚡", "tier": "code", "context": 64000, "is_free": False},
    {"id": "jev/typesafe/jev-finance-audit", "name": "JEV Banking Auditor", "lab": "TypeSafe AI (JEV)", "country": "USA", "flag": "⚡", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "jev/typesafe/jev-embed-v2", "name": "JEV Fast Embeddings v2", "lab": "TypeSafe AI (JEV)", "country": "USA", "flag": "⚡", "tier": "fast", "context": 32000, "is_free": True},
    {"id": "jev/typesafe/jev-routing-matrix", "name": "JEV Routing Matrix Engine", "lab": "TypeSafe AI (JEV)", "country": "USA", "flag": "⚡", "tier": "auto", "context": 64000, "is_free": False},

    # -------------------------------------------------------------
    # 🇮🇳 Krutrim AI (Ola) (krutrim/...)
    # -------------------------------------------------------------
    {"id": "krutrim/krutrim-v3-marathi", "name": "Krutrim Marathi SOTA Foundation", "lab": "Krutrim AI (Ola)", "country": "India", "flag": "🇮🇳", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "krutrim/krutrim-v3-indic-omni", "name": "Krutrim Indic Omni (22 Languages)", "lab": "Krutrim AI (Ola)", "country": "India", "flag": "🇮🇳", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "krutrim/krutrim-2-instruct", "name": "Krutrim 2 Instruct", "lab": "Krutrim AI (Ola)", "country": "India", "flag": "🇮🇳", "tier": "general", "context": 64000, "is_free": False},
    {"id": "krutrim/krutrim-v2.5-code", "name": "Krutrim Indic Code Specialist", "lab": "Krutrim AI (Ola)", "country": "India", "flag": "🇮🇳", "tier": "code", "context": 64000, "is_free": False},
    {"id": "krutrim/krutrim-spectre-12b", "name": "Krutrim Spectre 12B Reasoning", "lab": "Krutrim AI (Ola)", "country": "India", "flag": "🇮🇳", "tier": "reasoning", "context": 64000, "is_free": False},
    {"id": "krutrim/krutrim-hindi-pro", "name": "Krutrim Hindi Pro Foundation", "lab": "Krutrim AI (Ola)", "country": "India", "flag": "🇮🇳", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "krutrim/krutrim-voice-indic", "name": "Krutrim Indic Speech & Audio", "lab": "Krutrim AI (Ola)", "country": "India", "flag": "🇮🇳", "tier": "media", "context": 32000, "is_free": False},
    {"id": "krutrim/krutrim-banking-llm", "name": "Krutrim RBI & CBS Banking LLM", "lab": "Krutrim AI (Ola)", "country": "India", "flag": "🇮🇳", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "krutrim/krutrim-legal-indic", "name": "Krutrim Legal Indic Document AI", "lab": "Krutrim AI (Ola)", "country": "India", "flag": "🇮🇳", "tier": "general", "context": 128000, "is_free": False},
    {"id": "krutrim/krutrim-medical-ayush", "name": "Krutrim Medical & Ayush NLP", "lab": "Krutrim AI (Ola)", "country": "India", "flag": "🇮🇳", "tier": "general", "context": 64000, "is_free": False},
    {"id": "krutrim/krutrim-lite-flash", "name": "Krutrim Lite Flash (<200ms)", "lab": "Krutrim AI (Ola)", "country": "India", "flag": "🇮🇳", "tier": "fast", "context": 32000, "is_free": True},
    {"id": "krutrim/krutrim-r1-reasoning", "name": "Krutrim Indic R1 Reasoning", "lab": "Krutrim AI (Ola)", "country": "India", "flag": "🇮🇳", "tier": "reasoning", "context": 128000, "is_free": False},

    # -------------------------------------------------------------
    # ⚡ Poe by Quora (poe/...)
    # -------------------------------------------------------------
    {"id": "poe/assistant-pro", "name": "Poe Assistant Pro (Quora Mesh)", "lab": "Poe by Quora", "country": "USA", "flag": "⚡", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "poe/claude-3-7-sonnet-reasoning", "name": "Poe Claude 3.7 Sonnet Reasoning", "lab": "Poe by Quora", "country": "USA", "flag": "⚡", "tier": "reasoning", "context": 200000, "is_free": False},
    {"id": "poe/gpt-4o-search-grounded", "name": "Poe GPT-4o Search Grounded", "lab": "Poe by Quora", "country": "USA", "flag": "⚡", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "poe/gemini-2.5-flash-pro", "name": "Poe Gemini 2.5 Flash Pro", "lab": "Poe by Quora", "country": "USA", "flag": "⚡", "tier": "fast", "context": 1000000, "is_free": True},
    {"id": "poe/deepseek-r1-poe", "name": "Poe DeepSeek R1 Web-Integrated", "lab": "Poe by Quora", "country": "USA", "flag": "⚡", "tier": "reasoning", "context": 128000, "is_free": False},
    {"id": "poe/grok-2-realtime", "name": "Poe Grok 2 Realtime X Feed", "lab": "Poe by Quora", "country": "USA", "flag": "⚡", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "poe/flux-pro-poe", "name": "Poe FLUX 1.1 Pro Image Generator", "lab": "Poe by Quora", "country": "USA", "flag": "⚡", "tier": "media", "context": 32000, "is_free": False},
    {"id": "poe/solar-pro-poe", "name": "Poe Solar Pro 22B", "lab": "Poe by Quora", "country": "USA", "flag": "⚡", "tier": "general", "context": 64000, "is_free": True},
    {"id": "poe/qwen-2.5-max-poe", "name": "Poe Qwen 2.5 Max (Alibaba Mesh)", "lab": "Poe by Quora", "country": "USA", "flag": "⚡", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "poe/llama-3.3-70b-poe", "name": "Poe Llama 3.3 70B Quora Mesh", "lab": "Poe by Quora", "country": "USA", "flag": "⚡", "tier": "general", "context": 128000, "is_free": False},
    {"id": "poe/mistral-large-poe", "name": "Poe Mistral Large Quora", "lab": "Poe by Quora", "country": "USA", "flag": "⚡", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "poe/command-r-plus-poe", "name": "Poe Cohere Command R+", "lab": "Poe by Quora", "country": "USA", "flag": "⚡", "tier": "general", "context": 128000, "is_free": False},

    # -------------------------------------------------------------
    # ⛵ Parasail GPU Network (parasail/...)
    # -------------------------------------------------------------
    {"id": "parasail/parasail-llama-33-70b-fp8", "name": "Parasail Llama 3.3 70B FP8", "lab": "Parasail GPU Network", "country": "Global", "flag": "⛵", "tier": "general", "context": 128000, "is_free": False},
    {"id": "parasail/parasail-qwen25-vl-72b-instruct", "name": "Parasail Qwen 2.5 VL 72B", "lab": "Parasail GPU Network", "country": "Global", "flag": "⛵", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "parasail/parasail-skyfall-36b-v2-fp8", "name": "Parasail Skyfall 36B v2", "lab": "Parasail GPU Network", "country": "Global", "flag": "⛵", "tier": "general", "context": 64000, "is_free": True},
    {"id": "parasail/parasail-llama-4-maverick-instruct-fp8", "name": "Parasail Llama 4 Maverick FP8", "lab": "Parasail GPU Network", "country": "Global", "flag": "⛵", "tier": "flagship", "context": 256000, "is_free": False},
    {"id": "parasail/parasail-deepseek-r1-fp8", "name": "Parasail DeepSeek R1 Decentralized", "lab": "Parasail GPU Network", "country": "Global", "flag": "⛵", "tier": "reasoning", "context": 128000, "is_free": False},
    {"id": "parasail/parasail-mistral-large-fp8", "name": "Parasail Mistral Large FP8", "lab": "Parasail GPU Network", "country": "Global", "flag": "⛵", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "parasail/parasail-qwen-coder-32b-fp8", "name": "Parasail Qwen 2.5 Coder 32B FP8", "lab": "Parasail GPU Network", "country": "Global", "flag": "⛵", "tier": "code", "context": 64000, "is_free": False},
    {"id": "parasail/parasail-phi-4-fp8", "name": "Parasail Microsoft Phi-4 FP8", "lab": "Parasail GPU Network", "country": "Global", "flag": "⛵", "tier": "general", "context": 64000, "is_free": True},
    {"id": "parasail/parasail-gemma-27b-fp8", "name": "Parasail Gemma 2 27B FP8", "lab": "Parasail GPU Network", "country": "Global", "flag": "⛵", "tier": "general", "context": 32000, "is_free": True},
    {"id": "parasail/parasail-nemotron-70b-fp8", "name": "Parasail Nemotron 70B FP8", "lab": "Parasail GPU Network", "country": "Global", "flag": "⛵", "tier": "flagship", "context": 128000, "is_free": False},

    # -------------------------------------------------------------
    # 🏹 Arcee AI Domain SLMs (arcee/...)
    # -------------------------------------------------------------
    {"id": "arcee/zai-org/glm-5.3-flash", "name": "Arcee GLM 5.3 Flash", "lab": "Arcee AI", "country": "USA", "flag": "🏹", "tier": "fast", "context": 64000, "is_free": True},
    {"id": "arcee/deepseek/deepseek-v4.1-flash", "name": "Arcee DeepSeek V4.1 Flash", "lab": "Arcee AI", "country": "USA", "flag": "🏹", "tier": "fast", "context": 64000, "is_free": True},
    {"id": "arcee/moonshotai/kimi-k3.1-pro", "name": "Arcee Kimi K3.1 Pro SLM", "lab": "Arcee AI", "country": "USA", "flag": "🏹", "tier": "general", "context": 128000, "is_free": False},
    {"id": "arcee/arcee-blitz", "name": "Arcee Blitz High-Speed Agent SLM", "lab": "Arcee AI", "country": "USA", "flag": "🏹", "tier": "fast", "context": 32000, "is_free": True},
    {"id": "arcee/arcee-agent", "name": "Arcee Agentic SLM Enterprise", "lab": "Arcee AI", "country": "USA", "flag": "🏹", "tier": "flagship", "context": 64000, "is_free": False},
    {"id": "arcee/arcee-scribe", "name": "Arcee Scribe Long-Form Drafting", "lab": "Arcee AI", "country": "USA", "flag": "🏹", "tier": "general", "context": 128000, "is_free": False},
    {"id": "arcee/arcee-spark", "name": "Arcee Spark Edge SLM 7B", "lab": "Arcee AI", "country": "USA", "flag": "🏹", "tier": "fast", "context": 32000, "is_free": True},
    {"id": "arcee/arcee-virtuoso", "name": "Arcee Virtuoso Coding & Math SLM", "lab": "Arcee AI", "country": "USA", "flag": "🏹", "tier": "code", "context": 64000, "is_free": False},

    # -------------------------------------------------------------
    # 🌿 Eden AI Aggregated Fabric (edenai/...)
    # -------------------------------------------------------------
    {"id": "edenai/google/gemini-2.5-pro", "name": "Eden AI Gemini 2.5 Pro", "lab": "Eden AI", "country": "France", "flag": "🌿", "tier": "flagship", "context": 2000000, "is_free": False},
    {"id": "edenai/anthropic/claude-3-7-sonnet", "name": "Eden AI Claude 3.7 Sonnet", "lab": "Eden AI", "country": "France", "flag": "🌿", "tier": "flagship", "context": 200000, "is_free": False},
    {"id": "edenai/openai/gpt-4o", "name": "Eden AI GPT-4o Multimodal", "lab": "Eden AI", "country": "France", "flag": "🌿", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "edenai/openai/o3-mini", "name": "Eden AI OpenAI o3-mini Reasoning", "lab": "Eden AI", "country": "France", "flag": "🌿", "tier": "reasoning", "context": 200000, "is_free": False},
    {"id": "edenai/deepseek/deepseek-r1", "name": "Eden AI DeepSeek R1", "lab": "Eden AI", "country": "France", "flag": "🌿", "tier": "reasoning", "context": 128000, "is_free": False},
    {"id": "edenai/mistral/mistral-large-2", "name": "Eden AI Mistral Large 2", "lab": "Eden AI", "country": "France", "flag": "🌿", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "edenai/meta/llama-3.3-70b", "name": "Eden AI Llama 3.3 70B", "lab": "Eden AI", "country": "France", "flag": "🌿", "tier": "general", "context": 128000, "is_free": False},
    {"id": "edenai/cohere/command-r-plus", "name": "Eden AI Cohere Command R+", "lab": "Eden AI", "country": "France", "flag": "🌿", "tier": "general", "context": 128000, "is_free": False},
    {"id": "edenai/ai21/jamba-1.5-large", "name": "Eden AI AI21 Jamba 1.5", "lab": "Eden AI", "country": "France", "flag": "🌿", "tier": "general", "context": 256000, "is_free": True},
    {"id": "edenai/amazon/titan-text-express", "name": "Eden AI Amazon Titan Express", "lab": "Eden AI", "country": "France", "flag": "🌿", "tier": "fast", "context": 32000, "is_free": True},

    # -------------------------------------------------------------
    # 🌐 Requesty AI (requesty/...)
    # -------------------------------------------------------------
    {"id": "requesty/anthropic/claude-3-7-sonnet", "name": "Requesty Claude 3.7 Sonnet Enterprise", "lab": "Requesty AI", "country": "USA", "flag": "🌐", "tier": "flagship", "context": 200000, "is_free": False},
    {"id": "requesty/openai/gpt-4o-latest", "name": "Requesty GPT-4o Latest", "lab": "Requesty AI", "country": "USA", "flag": "🌐", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "requesty/google/gemini-2.5-flash", "name": "Requesty Gemini 2.5 Flash", "lab": "Requesty AI", "country": "USA", "flag": "🌐", "tier": "fast", "context": 1000000, "is_free": True},
    {"id": "requesty/deepseek/deepseek-r1-fast", "name": "Requesty DeepSeek R1 Fast", "lab": "Requesty AI", "country": "USA", "flag": "🌐", "tier": "reasoning", "context": 128000, "is_free": False},
    {"id": "requesty/meta/llama-3.3-70b-instruct", "name": "Requesty Llama 3.3 70B Routing", "lab": "Requesty AI", "country": "USA", "flag": "🌐", "tier": "general", "context": 128000, "is_free": False},
    {"id": "requesty/qwen/qwen-2.5-coder-32b", "name": "Requesty Qwen 2.5 Coder 32B", "lab": "Requesty AI", "country": "USA", "flag": "🌐", "tier": "code", "context": 64000, "is_free": False},
    {"id": "requesty/mistral/codestral-2501", "name": "Requesty Mistral Codestral 2501", "lab": "Requesty AI", "country": "USA", "flag": "🌐", "tier": "code", "context": 128000, "is_free": False},
    {"id": "requesty/xai/grok-2", "name": "Requesty xAI Grok 2", "lab": "Requesty AI", "country": "USA", "flag": "🌐", "tier": "flagship", "context": 128000, "is_free": False},

    # -------------------------------------------------------------
    # ☁️ Cloudflare Workers AI (@cf/...)
    # -------------------------------------------------------------
    {"id": "@cf/meta/llama-3.3-70b-instruct", "name": "Cloudflare Workers AI Llama 3.3 70B", "lab": "Cloudflare Workers AI", "country": "Global Edge", "flag": "☁️", "tier": "general", "context": 128000, "is_free": False},
    {"id": "@cf/meta/llama-3.1-8b-instruct", "name": "Cloudflare Workers AI Llama 3.1 8B (<100ms)", "lab": "Cloudflare Workers AI", "country": "Global Edge", "flag": "☁️", "tier": "fast", "context": 32000, "is_free": True},
    {"id": "@cf/deepseek-ai/deepseek-r1-distill-qwen-32b", "name": "Cloudflare DeepSeek R1 32B", "lab": "Cloudflare Workers AI", "country": "Global Edge", "flag": "☁️", "tier": "reasoning", "context": 64000, "is_free": True},
    {"id": "@cf/qwen/qwen2.5-72b-instruct", "name": "Cloudflare Workers AI Qwen 2.5 72B", "lab": "Cloudflare Workers AI", "country": "Global Edge", "flag": "☁️", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "@cf/mistral/mistral-7b-instruct-v0.2", "name": "Cloudflare Workers AI Mistral 7B", "lab": "Cloudflare Workers AI", "country": "Global Edge", "flag": "☁️", "tier": "fast", "context": 32000, "is_free": True},
    {"id": "@cf/meta/llama-3.2-3b-instruct", "name": "Cloudflare Workers AI Llama 3.2 3B Ultra-Fast", "lab": "Cloudflare Workers AI", "country": "Global Edge", "flag": "☁️", "tier": "fast", "context": 32000, "is_free": True},
    {"id": "@cf/baai/bge-large-en-v1.5", "name": "Cloudflare Workers AI BGE Large Embeddings", "lab": "Cloudflare Workers AI", "country": "Global Edge", "flag": "☁️", "tier": "fast", "context": 8000, "is_free": True},
    {"id": "@cf/black-forest-labs/flux-1-schnell", "name": "Cloudflare FLUX.1 Schnell", "lab": "Cloudflare Workers AI", "country": "Global Edge", "flag": "☁️", "tier": "media", "context": 8000, "is_free": True},

    # -------------------------------------------------------------
    # 🚀 Novita AI (novita/...)
    # -------------------------------------------------------------
    {"id": "novita/deepseek/deepseek-v4.1-flash", "name": "Novita DeepSeek V4.1 Flash", "lab": "Novita AI", "country": "USA", "flag": "🚀", "tier": "fast", "context": 64000, "is_free": True},
    {"id": "novita/moonshotai/kimi-k3.1-pro", "name": "Novita Kimi K3.1 Pro (Long Context)", "lab": "Novita AI", "country": "USA", "flag": "🚀", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "novita/minimax/minimax-m3.1-flash", "name": "Novita MiniMax M3.1 Flash", "lab": "Novita AI", "country": "USA", "flag": "🚀", "tier": "fast", "context": 64000, "is_free": True},
    {"id": "novita/meta-llama/llama-3.3-70b-instruct", "name": "Novita Llama 3.3 70B Instruct", "lab": "Novita AI", "country": "USA", "flag": "🚀", "tier": "general", "context": 128000, "is_free": False},
    {"id": "novita/deepseek/deepseek-r1", "name": "Novita DeepSeek R1 Reasoning", "lab": "Novita AI", "country": "USA", "flag": "🚀", "tier": "reasoning", "context": 128000, "is_free": False},
    {"id": "novita/qwen/qwen-2.5-72b-instruct", "name": "Novita Qwen 2.5 72B Instruct", "lab": "Novita AI", "country": "USA", "flag": "🚀", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "novita/mistralai/mistral-nemo", "name": "Novita Mistral NeMo 12B", "lab": "Novita AI", "country": "USA", "flag": "🚀", "tier": "general", "context": 64000, "is_free": True},
    {"id": "novita/nousresearch/hermes-3-llama-70b", "name": "Novita Hermes 3 Llama 70B", "lab": "Novita AI", "country": "USA", "flag": "🚀", "tier": "general", "context": 128000, "is_free": False},

    # -------------------------------------------------------------
    # 🟢 NVIDIA NIM (nvidia/...)
    # -------------------------------------------------------------
    {"id": "nvidia/nemotron-4-340b-instruct", "name": "NVIDIA Nemotron-4 340B Instruct", "lab": "NVIDIA NIM", "country": "USA", "flag": "🟢", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "nvidia/nemotron-3.5-lightning:free", "name": "NVIDIA Nemotron 3.5 Lightning (Free)", "lab": "NVIDIA NIM", "country": "USA", "flag": "🟢", "tier": "fast", "context": 64000, "is_free": True},
    {"id": "nvidia/llama-3.1-nemotron-70b-instruct", "name": "NVIDIA Llama 3.1 Nemotron 70B", "lab": "NVIDIA NIM", "country": "USA", "flag": "🟢", "tier": "general", "context": 128000, "is_free": False},
    {"id": "nvidia/mistral-neva-22b", "name": "NVIDIA Mistral NeVA 22B Vision", "lab": "NVIDIA NIM", "country": "USA", "flag": "🟢", "tier": "general", "context": 64000, "is_free": False},
    {"id": "nvidia/deepseek-r1-nim", "name": "NVIDIA DeepSeek R1 NIM Accelerated", "lab": "NVIDIA NIM", "country": "USA", "flag": "🟢", "tier": "reasoning", "context": 128000, "is_free": False},
    {"id": "nvidia/embed-qa-4", "name": "NVIDIA Embed-QA 4 Retrieval", "lab": "NVIDIA NIM", "country": "USA", "flag": "🟢", "tier": "fast", "context": 32000, "is_free": True},
    {"id": "nvidia/llama-3.2-3b-instruct", "name": "NVIDIA Llama 3.2 3B NIM", "lab": "NVIDIA NIM", "country": "USA", "flag": "🟢", "tier": "fast", "context": 32000, "is_free": True},

    # -------------------------------------------------------------
    # ⚡ SambaNova Systems (sambanova/...)
    # -------------------------------------------------------------
    {"id": "sambanova/Meta-Llama-3.3-70B-Instruct", "name": "SambaNova Llama 3.3 70B (Fast SN40L RDU)", "lab": "SambaNova Systems", "country": "USA", "flag": "⚡", "tier": "general", "context": 128000, "is_free": True},
    {"id": "sambanova/GLM-5.3", "name": "SambaNova GLM-5.3 Flagship", "lab": "SambaNova Systems", "country": "USA", "flag": "⚡", "tier": "flagship", "context": 128000, "is_free": True},
    {"id": "sambanova/MiniMax-M3.1-Flash", "name": "SambaNova MiniMax M3.1 Flash", "lab": "SambaNova Systems", "country": "USA", "flag": "⚡", "tier": "fast", "context": 64000, "is_free": True},
    {"id": "sambanova/gemma-4-31B-it", "name": "SambaNova Gemma 4 31B", "lab": "SambaNova Systems", "country": "USA", "flag": "⚡", "tier": "general", "context": 64000, "is_free": True},
    {"id": "sambanova/gpt-oss-120b", "name": "SambaNova GPT OSS 120B Fast RDU", "lab": "SambaNova Systems", "country": "USA", "flag": "⚡", "tier": "general", "context": 64000, "is_free": True},
    {"id": "sambanova/qwen-2.5-coder-32b", "name": "SambaNova Qwen 2.5 Coder 32B RDU", "lab": "SambaNova Systems", "country": "USA", "flag": "⚡", "tier": "code", "context": 64000, "is_free": True},
    {"id": "sambanova/deepseek-r1-distill-llama-70b", "name": "SambaNova DeepSeek R1 Distill 70B", "lab": "SambaNova Systems", "country": "USA", "flag": "⚡", "tier": "reasoning", "context": 128000, "is_free": True},

    # -------------------------------------------------------------
    # 🚀 AI/ML API (aimlapi/...)
    # -------------------------------------------------------------
    {"id": "aimlapi/anthropic/claude-3-7-sonnet", "name": "AI/ML API Claude 3.7 Sonnet", "lab": "AI/ML API", "country": "Global", "flag": "🚀", "tier": "flagship", "context": 200000, "is_free": False},
    {"id": "aimlapi/deepseek/deepseek-r1", "name": "AI/ML API DeepSeek R1", "lab": "AI/ML API", "country": "Global", "flag": "🚀", "tier": "reasoning", "context": 128000, "is_free": False},
    {"id": "aimlapi/openai/gpt-4o", "name": "AI/ML API GPT-4o Omnimodal", "lab": "AI/ML API", "country": "Global", "flag": "🚀", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "aimlapi/openai/o3-mini", "name": "AI/ML API OpenAI o3-mini Reasoning", "lab": "AI/ML API", "country": "Global", "flag": "🚀", "tier": "reasoning", "context": 200000, "is_free": False},
    {"id": "aimlapi/meta/llama-3.3-70b-instruct", "name": "AI/ML API Llama 3.3 70B", "lab": "AI/ML API", "country": "Global", "flag": "🚀", "tier": "general", "context": 128000, "is_free": False},
    {"id": "aimlapi/google/gemini-2.5-flash", "name": "AI/ML API Gemini 2.5 Flash", "lab": "AI/ML API", "country": "Global", "flag": "🚀", "tier": "fast", "context": 1000000, "is_free": True},
    {"id": "aimlapi/qwen/qwen-2.5-72b", "name": "AI/ML API Qwen 2.5 72B", "lab": "AI/ML API", "country": "Global", "flag": "🚀", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "aimlapi/mistral/mistral-large-2411", "name": "AI/ML API Mistral Large 2411", "lab": "AI/ML API", "country": "Global", "flag": "🚀", "tier": "flagship", "context": 128000, "is_free": False},

    # -------------------------------------------------------------
    # 🧠 DeepInfra Cloud (deepinfra/...)
    # -------------------------------------------------------------
    {"id": "deepinfra/Qwen/Qwen3.8-Flash", "name": "DeepInfra Qwen 3.8 Flash (Turbo)", "lab": "DeepInfra Cloud", "country": "USA", "flag": "🧠", "tier": "fast", "context": 64000, "is_free": True},
    {"id": "deepinfra/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", "name": "DeepInfra Llama 3.1 8B Turbo", "lab": "DeepInfra Cloud", "country": "USA", "flag": "🧠", "tier": "fast", "context": 32000, "is_free": True},
    {"id": "deepinfra/meta-llama/Llama-3.3-70B-Instruct", "name": "DeepInfra Llama 3.3 70B Turbo", "lab": "DeepInfra Cloud", "country": "USA", "flag": "🧠", "tier": "general", "context": 128000, "is_free": False},
    {"id": "deepinfra/Qwen/Qwen2.5-Coder-32B-Instruct", "name": "DeepInfra Qwen 2.5 Coder 32B", "lab": "DeepInfra Cloud", "country": "USA", "flag": "🧠", "tier": "code", "context": 64000, "is_free": False},
    {"id": "deepinfra/deepseek-ai/DeepSeek-R1", "name": "DeepInfra DeepSeek R1 Reasoning", "lab": "DeepInfra Cloud", "country": "USA", "flag": "🧠", "tier": "reasoning", "context": 128000, "is_free": False},
    {"id": "deepinfra/microsoft/phi-4", "name": "DeepInfra Microsoft Phi-4", "lab": "DeepInfra Cloud", "country": "USA", "flag": "🧠", "tier": "general", "context": 64000, "is_free": False},
    {"id": "deepinfra/google/gemma-2-27b-it", "name": "DeepInfra Gemma 2 27B", "lab": "DeepInfra Cloud", "country": "USA", "flag": "🧠", "tier": "general", "context": 32000, "is_free": True},
    {"id": "deepinfra/meta-llama/Llama-3.2-11B-Vision-Instruct", "name": "DeepInfra Llama 3.2 11B Vision", "lab": "DeepInfra Cloud", "country": "USA", "flag": "🧠", "tier": "general", "context": 64000, "is_free": True},

    # -------------------------------------------------------------
    # 🇫🇷 Mistral Direct (mistral/...)
    # -------------------------------------------------------------
    {"id": "mistral/codestral-latest", "name": "Mistral Codestral 2508 (Code SOTA)", "lab": "Mistral AI", "country": "France", "flag": "🇫🇷", "tier": "code", "context": 256000, "is_free": False},
    {"id": "mistral/mistral-large-latest", "name": "Mistral Large 2 (Flagship)", "lab": "Mistral AI", "country": "France", "flag": "🇫🇷", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "mistral/ministral-14b-latest", "name": "Mistral Ministral 14B", "lab": "Mistral AI", "country": "France", "flag": "🇫🇷", "tier": "fast", "context": 64000, "is_free": False},
    {"id": "mistral/mistral-small-latest", "name": "Mistral Small 3", "lab": "Mistral AI", "country": "France", "flag": "🇫🇷", "tier": "fast", "context": 64000, "is_free": True},
    {"id": "mistral/mistral-embed", "name": "Mistral Embeddings", "lab": "Mistral AI", "country": "France", "flag": "🇫🇷", "tier": "fast", "context": 32000, "is_free": True},
    {"id": "mistral/pixtral-large-latest", "name": "Mistral Pixtral Large Multimodal", "lab": "Mistral AI", "country": "France", "flag": "🇫🇷", "tier": "flagship", "context": 128000, "is_free": False},

    # -------------------------------------------------------------
    # 🤗 Hugging Face Hub (hf/...)
    # -------------------------------------------------------------
    {"id": "hf/meta-llama/Llama-3.3-70B-Instruct", "name": "Hugging Face Llama 3.3 70B", "lab": "Hugging Face Hub", "country": "Global", "flag": "🤗", "tier": "general", "context": 128000, "is_free": True},
    {"id": "hf/Qwen/Qwen2.5-Coder-32B-Instruct", "name": "Hugging Face Qwen Coder 32B", "lab": "Hugging Face Hub", "country": "Global", "flag": "🤗", "tier": "code", "context": 64000, "is_free": True},
    {"id": "hf/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B", "name": "Hugging Face DeepSeek R1 Distill", "lab": "Hugging Face Hub", "country": "Global", "flag": "🤗", "tier": "reasoning", "context": 64000, "is_free": True},
    {"id": "hf/mistralai/Mistral-Small-24B-Instruct-2501", "name": "Hugging Face Mistral Small 24B", "lab": "Hugging Face Hub", "country": "Global", "flag": "🤗", "tier": "general", "context": 64000, "is_free": True},
    {"id": "hf/google/gemma-2-9b-it", "name": "Hugging Face Gemma 2 9B", "lab": "Hugging Face Hub", "country": "Global", "flag": "🤗", "tier": "fast", "context": 32000, "is_free": True},
    {"id": "hf/microsoft/Phi-3.5-mini-instruct", "name": "Hugging Face Phi 3.5 Mini", "lab": "Hugging Face Hub", "country": "Global", "flag": "🤗", "tier": "fast", "context": 32000, "is_free": True},

    # -------------------------------------------------------------
    # ⚡ Groq LPUs (groq/...)
    # -------------------------------------------------------------
    {"id": "groq/qwen3.8-27b", "name": "Groq Qwen 3.8 27B (<300ms SLA)", "lab": "Groq LPU", "country": "USA", "flag": "⚡", "tier": "fast", "context": 64000, "is_free": True},
    {"id": "groq/openai/gpt-oss-120b", "name": "Groq GPT OSS 120B High-Throughput", "lab": "Groq LPU", "country": "USA", "flag": "⚡", "tier": "general", "context": 64000, "is_free": True},
    {"id": "groq/llama-3.3-70b-versatile", "name": "Groq Llama 3.3 70B Versatile", "lab": "Groq LPU", "country": "USA", "flag": "⚡", "tier": "general", "context": 128000, "is_free": True},
    {"id": "groq/llama-3.1-8b-instant", "name": "Groq Llama 3.1 8B Instant (<100ms)", "lab": "Groq LPU", "country": "USA", "flag": "⚡", "tier": "fast", "context": 32000, "is_free": True},
    {"id": "groq/deepseek-r1-distill-llama-70b", "name": "Groq DeepSeek R1 Distill 70B", "lab": "Groq LPU", "country": "USA", "flag": "⚡", "tier": "reasoning", "context": 128000, "is_free": True},
    {"id": "groq/gemma2-9b-it", "name": "Groq Gemma 2 9B Fast LPU", "lab": "Groq LPU", "country": "USA", "flag": "⚡", "tier": "fast", "context": 32000, "is_free": True},

    # -------------------------------------------------------------
    # 🚀 Friendli, TheSean & Baseten (friendli/..., thesean/..., baseten/...)
    # -------------------------------------------------------------
    {"id": "friendli/meta-llama-3.3-70b-instruct", "name": "FriendliAI Llama 3.3 70B W4A16", "lab": "FriendliAI / TheSean", "country": "USA", "flag": "🚀", "tier": "general", "context": 128000, "is_free": False},
    {"id": "friendli/deepseek-r1-fp8", "name": "FriendliAI DeepSeek R1 Dedicated", "lab": "FriendliAI / TheSean", "country": "USA", "flag": "🚀", "tier": "reasoning", "context": 128000, "is_free": False},
    {"id": "friendli/mistral-large-2", "name": "FriendliAI Mistral Large 2", "lab": "FriendliAI / TheSean", "country": "USA", "flag": "🚀", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "thesean/mixtral-8x22b-instruct", "name": "TheSean Fabric Mixtral 8x22B", "lab": "FriendliAI / TheSean", "country": "USA", "flag": "🚀", "tier": "general", "context": 64000, "is_free": False},
    {"id": "thesean/qwen-2.5-72b-instruct", "name": "TheSean Fabric Qwen 2.5 72B", "lab": "FriendliAI / TheSean", "country": "USA", "flag": "🚀", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "baseten/deepseek-r1-dedicated", "name": "Baseten DeepSeek R1 Dedicated LPU", "lab": "FriendliAI / TheSean", "country": "USA", "flag": "🚀", "tier": "reasoning", "context": 128000, "is_free": False},
    {"id": "baseten/llama-3.3-70b-instruct", "name": "Baseten Llama 3.3 70B Dedicated", "lab": "FriendliAI / TheSean", "country": "USA", "flag": "🚀", "tier": "general", "context": 128000, "is_free": False},

    # -------------------------------------------------------------
    # 🇨🇳 DeepSeek Direct (deepseek/...)
    # -------------------------------------------------------------
    {"id": "deepseek/deepseek-chat", "name": "DeepSeek V3 (Direct Official API)", "lab": "DeepSeek AI", "country": "China", "flag": "🇨🇳", "tier": "flagship", "context": 128000, "is_free": False},
    {"id": "deepseek/deepseek-reasoner", "name": "DeepSeek R1 Reasoner (Direct API)", "lab": "DeepSeek AI", "country": "China", "flag": "🇨🇳", "tier": "reasoning", "context": 128000, "is_free": False},
    {"id": "deepseek/deepseek-coder-v2.5", "name": "DeepSeek Coder V2.5 (Direct API)", "lab": "DeepSeek AI", "country": "China", "flag": "🇨🇳", "tier": "code", "context": 128000, "is_free": False},

    # -------------------------------------------------------------
    # 🎨 Fal.ai & Replicate (fal/..., replicate/...)
    # -------------------------------------------------------------
    {"id": "fal/flux-pro-v1.1", "name": "Fal.ai FLUX 1.1 Pro Photorealistic", "lab": "Fal.ai & Replicate", "country": "USA", "flag": "🎨", "tier": "media", "context": 8000, "is_free": False},
    {"id": "fal/flux-realism", "name": "Fal.ai FLUX Realism LoRA SOTA", "lab": "Fal.ai & Replicate", "country": "USA", "flag": "🎨", "tier": "media", "context": 8000, "is_free": False},
    {"id": "fal/recraft-v3", "name": "Fal.ai Recraft V3 Vector & Raster", "lab": "Fal.ai & Replicate", "country": "USA", "flag": "🎨", "tier": "media", "context": 8000, "is_free": False},
    {"id": "fal/kling-video-v1.5", "name": "Fal.ai Kling Video 1.5 HD AI Video", "lab": "Fal.ai & Replicate", "country": "USA", "flag": "🎨", "tier": "media", "context": 8000, "is_free": False},
    {"id": "replicate/black-forest-labs/flux-1.1-pro", "name": "Replicate FLUX 1.1 Pro", "lab": "Fal.ai & Replicate", "country": "USA", "flag": "🎨", "tier": "media", "context": 8000, "is_free": False},
    {"id": "replicate/stability-ai/sdxl", "name": "Replicate SDXL 1.0 Diffusion", "lab": "Fal.ai & Replicate", "country": "USA", "flag": "🎨", "tier": "media", "context": 8000, "is_free": False},
    {"id": "replicate/meta/meta-llama-3-70b-instruct", "name": "Replicate Llama 3 70B Instruct", "lab": "Fal.ai & Replicate", "country": "USA", "flag": "🎨", "tier": "general", "context": 128000, "is_free": False},
]


def get_unified_models_for_ui() -> List[Dict[str, Any]]:
    """Returns comprehensive master union of all 4,804+ models across Defapi, JEV, Krutrim,
    Poe, Parasail, Arcee, Eden AI, Requesty, Cloudflare, Novita, NVIDIA, SambaNova, OpenRouter,
    AI/ML API, DeepInfra, Mistral, Hugging Face, Groq, Friendli, DeepSeek, and Fal/Replicate."""
    raw_models = get_openrouter_models()
    ui_list = []
    seen_ids = set()

    # Always include AUTO engine at the top
    auto_model = {
        "id": "auto",
        "name": "⚡ AUTO-ROUTER (Mathematical Pareto-Bandit)",
        "lab": "NanoPro Core",
        "country": "Global",
        "flag": "⚡",
        "tier": "auto",
        "context": 1000000,
        "is_free": True,
        "recommended": True
    }
    ui_list.append(auto_model)
    seen_ids.add("auto")

    # 0. Add user-added / discovered custom models from custom_models_service
    try:
        from app.custom_models_service import get_all_custom_models
        custom_list = get_all_custom_models()
        for cm in custom_list:
            cid = cm.get("id")
            if cid and cid not in seen_ids:
                seen_ids.add(cid)
                ui_list.append({
                    "id": cid,
                    "name": cm.get("name") or cid,
                    "lab": cm.get("lab", "Custom Model"),
                    "country": cm.get("country", "India"),
                    "flag": cm.get("flag", "⭐"),
                    "tier": cm.get("tier", "custom"),
                    "context": cm.get("context", 128000),
                    "is_free": bool(cm.get("is_free", False)),
                    "is_custom": True,
                    "provider": cm.get("provider", "custom"),
                    "description": cm.get("description", "")
                })
    except Exception:
        pass

    # 1. Add all Specialized Provider Models (Defapi, JEV, Krutrim, Poe, Parasail, Arcee,
    # Eden AI, Requesty, CF AI, Novita, NVIDIA, SambaNova, AI/ML API, DeepInfra, Mistral,
    # HF, Groq, Friendli, DeepSeek, Fal/Replicate)
    for m in PROVIDER_SPECIALIZED_MODELS:
        mid = m["id"]
        if mid not in seen_ids:
            seen_ids.add(mid)
            ui_list.append({
                "id": mid,
                "name": m.get("name", mid),
                "lab": m.get("lab", "Global AI Lab"),
                "country": m.get("country", "Global"),
                "flag": m.get("flag", "⚡"),
                "tier": m.get("tier", "general"),
                "context": m.get("context", 128000),
                "is_free": m.get("is_free", False),
                "recommended": False
            })

    # 2. Add OpenRouter Mesh Models (473+ live models)
    if raw_models:
        for m in raw_models:
            mid = m.get("id", "")
            if not mid or mid in seen_ids:
                continue
            seen_ids.add(mid)
            mname = m.get("name", mid)
            prefix = mid.split("/")[0] if "/" in mid else "other"
            
            lab_map = {
                "anthropic": ("Anthropic", "USA", "🇺🇸"),
                "openai": ("OpenAI", "USA", "🇺🇸"),
                "google": ("Google DeepMind", "USA", "🇺🇸"),
                "deepseek": ("DeepSeek", "China", "🇨🇳"),
                "qwen": ("Alibaba Qwen", "China", "🇨🇳"),
                "meta": ("Meta", "USA", "🇺🇸"),
                "meta-llama": ("Meta Llama", "USA", "🇺🇸"),
                "mistralai": ("Mistral AI", "Europe", "🇫🇷"),
                "x-ai": ("xAI Grok", "USA", "🇺🇸"),
                "nvidia": ("NVIDIA", "USA", "🇺🇸"),
                "cohere": ("Cohere", "Canada", "🇨🇦"),
                "moonshotai": ("Moonshot AI", "China", "🇨🇳"),
                "z-ai": ("Zhipu AI", "China", "🇨🇳"),
                "baidu": ("Baidu", "China", "🇨🇳"),
                "tencent": ("Tencent", "China", "🇨🇳"),
                "minimax": ("MiniMax", "China", "🇨🇳"),
                "microsoft": ("Microsoft", "USA", "🇺🇸"),
                "amazon": ("Amazon Nova", "USA", "🇺🇸")
            }
            lab_info = lab_map.get(prefix, (prefix.capitalize(), "Global", "🌍"))
            is_free = ":free" in mid
            
            tier = "general"
            if is_free:
                tier = "free"
            elif any(k in mid.lower() for k in ["coder", "code", "dev"]):
                tier = "code"
            elif any(k in mid.lower() for k in ["r1", "o1", "o3", "reason", "thinking"]):
                tier = "reasoning"
            elif any(k in mid.lower() for k in ["sonnet", "opus", "pro", "max", "large"]):
                tier = "flagship"

            ui_list.append({
                "id": mid,
                "name": mname,
                "lab": lab_info[0],
                "country": lab_info[1],
                "flag": lab_info[2],
                "tier": tier,
                "context": m.get("context_length", 32768),
                "is_free": is_free,
                "recommended": False
            })

    # 3. Add Local Sovereign Creator Models (32+ labs)
    for m in list_all_models_flat():
        mid = m["id"]
        if mid not in seen_ids:
            seen_ids.add(mid)
            ui_list.append({
                "id": mid,
                "name": m["name"],
                "lab": m["creator_name"],
                "country": m["creator_country"],
                "flag": m["creator_flag"],
                "tier": m.get("tier", "flagship"),
                "context": m.get("context", 128000),
                "is_free": False,
                "recommended": False
            })

    return ui_list


def resolve_model_provenance(model_id: str) -> Dict[str, Any]:
    """Resolves sovereign country, lab provenance, tier, and clean name for any model worldwide."""
    if not model_id or model_id == "auto":
        return {
            "model_id": "auto",
            "model_name": "Single AUTO Mathematical Engine",
            "lab_name": "NanoPro Mathematical Dispatcher",
            "country": "Global Sovereign Mesh",
            "flag": "⚡",
            "tier": "Pareto-Bandit Router"
        }

    try:
        from app.custom_models_service import load_custom_store
        c_store = load_custom_store()
        for cm in c_store.get("custom_models", []) + c_store.get("discovered_models", []):
            if cm.get("id") == model_id:
                return {
                    "model_id": model_id,
                    "model_name": cm.get("name", model_id),
                    "lab_name": cm.get("lab", "Custom AI Lab"),
                    "country": cm.get("country", "India"),
                    "flag": cm.get("flag", "⭐"),
                    "tier": cm.get("tier", "Custom Model").title()
                }
    except Exception:
        pass

    mid = model_id.lower()
    parts = mid.split("/")
    prefix = parts[0] if len(parts) > 1 else "global"
    raw_name = parts[1] if len(parts) > 1 else parts[0]

    clean_name = raw_name.replace(":free", " (Free)").replace("-", " ").title()

    lab_map = {
        "defapi": ("Defapi Frontier Hub", "United States", "🌐", "Frontier Multimodal SOTA"),
        "jev": ("TypeSafe AI (JEV)", "United States", "⚡", "System One Fast Reasoning"),
        "typesafe": ("TypeSafe AI (JEV)", "United States", "⚡", "System One Fast Reasoning"),
        "krutrim": ("Krutrim AI (Ola)", "India", "🇮🇳", "Indic Foundation Leader"),
        "ola": ("Krutrim AI (Ola)", "India", "🇮🇳", "Indic Foundation Leader"),
        "poe": ("Poe by Quora", "United States", "⚡", "Multi-Bot Unified Fabric"),
        "parasail": ("Parasail GPU Network", "Global Sovereign", "⛵", "Decentralized GPU Inference"),
        "arcee": ("Arcee AI", "United States", "🏹", "Specialized Domain SLMs"),
        "edenai": ("Eden AI Fabric", "France", "🌿", "Aggregated Unified Fabric"),
        "requesty": ("Requesty AI", "United States", "🌐", "Smart Router Mesh"),
        "@cf": ("Cloudflare Workers AI", "Global Edge", "☁️", "Zero-Latency Edge"),
        "cf": ("Cloudflare Workers AI", "Global Edge", "☁️", "Zero-Latency Edge"),
        "novita": ("Novita AI", "United States", "🚀", "Multi-Cloud High Throughput"),
        "sambanova": ("SambaNova Systems", "United States", "⚡", "Fast SN40L Reconfigurable RDU"),
        "aimlapi": ("AI/ML API", "Global Unified", "🚀", "Enterprise Model Aggregator"),
        "deepinfra": ("DeepInfra Cloud", "United States", "🧠", "High-Throughput Open Weights"),
        "mistralai": ("Mistral AI", "France", "🇫🇷", "European Sovereign Frontier"),
        "mistral": ("Mistral AI", "France", "🇫🇷", "European Sovereign Frontier"),
        "hf": ("Hugging Face Hub", "Global Open Source", "🤗", "Open-Weights Sovereign"),
        "huggingface": ("Hugging Face Hub", "Global Open Source", "🤗", "Open-Weights Sovereign"),
        "groq": ("Groq LPU", "United States", "⚡", "Deterministic Fast LPUs"),
        "friendli": ("FriendliAI", "United States", "🚀", "High-Throughput Serving"),
        "thesean": ("TheSean Fabric", "United States", "🚀", "Distributed Inference"),
        "baseten": ("Baseten", "United States", "🚀", "Dedicated Model Serving"),
        "deepseek": ("DeepSeek AI", "China", "🇨🇳", "Open Reasoning SOTA"),
        "fal": ("Fal.ai", "United States", "🎨", "Generative Media & Diffusion"),
        "replicate": ("Replicate", "United States", "🎨", "Cloud Model Deployment"),
        "anthropic": ("Anthropic", "United States", "🇺🇸", "Frontier Cognitive & Code"),
        "openai": ("OpenAI", "United States", "🇺🇸", "Frontier Commercial & Reasoning"),
        "google": ("Google DeepMind", "United States", "🇺🇸", "Frontier Multimodal 2M"),
        "qwen": ("Alibaba Cloud (Qwen)", "China", "🇨🇳", "Frontier Coding & Multilingual"),
        "alibaba": ("Alibaba Cloud (Qwen)", "China", "🇨🇳", "Frontier Coding & Multilingual"),
        "meta": ("Meta AI", "United States", "🇺🇸", "Open-Weights Frontier"),
        "meta-llama": ("Meta AI (Llama)", "United States", "🇺🇸", "Open-Weights Frontier"),
        "x-ai": ("xAI (Grok)", "United States", "🇺🇸", "Truth-Seeking Frontier"),
        "nvidia": ("NVIDIA AI", "United States", "🟢", "Accelerated Inference SOTA"),
        "cohere": ("Cohere", "Canada", "🇨🇦", "Enterprise NLP & Embeddings"),
        "moonshotai": ("Moonshot AI (Kimi)", "China", "🇨🇳", "Long Context Frontier"),
        "moonshot": ("Moonshot AI (Kimi)", "China", "🇨🇳", "Long Context Frontier"),
        "z-ai": ("Zhipu AI (GLM)", "China", "🇨🇳", "Chinese SOTA Frontier"),
        "zhipu": ("Zhipu AI (GLM)", "China", "🇨🇳", "Chinese SOTA Frontier"),
        "thudm": ("Zhipu AI / Tsinghua", "China", "🇨🇳", "Bilingual Foundation"),
        "glm": ("Zhipu AI (GLM)", "China", "🇨🇳", "Chinese SOTA Frontier"),
        "01-ai": ("01.AI (Kai-Fu Lee)", "China", "🇨🇳", "High Performance Foundation"),
        "yi": ("01.AI (Yi)", "China", "🇨🇳", "High Performance Foundation"),
        "baidu": ("Baidu (ERNIE)", "China", "🇨🇳", "Industrial Enterprise AI"),
        "ernie": ("Baidu (ERNIE)", "China", "🇨🇳", "Industrial Enterprise AI"),
        "tencent": ("Tencent (Hunyuan)", "China", "🇨🇳", "Enterprise Foundation"),
        "hunyuan": ("Tencent (Hunyuan)", "China", "🇨🇳", "Enterprise Foundation"),
        "bytedance": ("ByteDance (Doubao)", "China", "🇨🇳", "Ultra High-Throughput Omni"),
        "doubao": ("ByteDance (Doubao)", "China", "🇨🇳", "Ultra High-Throughput Omni"),
        "stepfun": ("StepFun (Jieyue)", "China", "🇨🇳", "Reasoning Step-1"),
        "minimax": ("MiniMax", "China", "🇨🇳", "Multimodal Voice & Text"),
        "sensetime": ("SenseTime (SenseNova)", "China", "🇨🇳", "Computer Vision & LLM"),
        "sarvam": ("Sarvam AI", "India", "🇮🇳", "Indic Sovereign Frontier"),
        "bharatgen": ("BharatGen (IIT Bombay)", "India", "🇮🇳", "National Sovereign AI"),
        "tii": ("Technology Innovation Institute", "United Arab Emirates", "🇦🇪", "Falcon Sovereign"),
        "falcon": ("Technology Innovation Institute", "United Arab Emirates", "🇦🇪", "Falcon Sovereign"),
        "sakana": ("Sakana AI", "Japan", "🇯🇵", "Evolutionary Foundation"),
        "cyberagent": ("CyberAgent", "Japan", "🇯🇵", "Japanese Enterprise AI"),
        "naver": ("Naver (HyperCLOVA X)", "South Korea", "🇰🇷", "Korean Sovereign Frontier"),
        "hyperclova": ("Naver (HyperCLOVA X)", "South Korea", "🇰🇷", "Korean Sovereign Frontier"),
        "upstage": ("Upstage (Solar DUS)", "South Korea", "🇰🇷", "Depth-Up-Scaled Foundation"),
        "solar": ("Upstage (Solar DUS)", "South Korea", "🇰🇷", "Depth-Up-Scaled Foundation"),
        "writer": ("Writer AI (Palmyra)", "United States", "🇺🇸", "Enterprise Workflows"),
        "perplexity": ("Perplexity AI (Sonar)", "United States", "🇺🇸", "Search Grounded Online"),
        "cerebras": ("Cerebras CS-3", "United States", "🇺🇸", "Wafer-Scale Inference"),
        "ai21": ("AI21 Labs (Jamba)", "Israel", "🇮🇱", "Mamba-Transformer Hybrid"),
        "aleph-alpha": ("Aleph Alpha (Luminous)", "Germany", "🇩🇪", "European Explainable AI")
    }

    if prefix in lab_map:
        info = lab_map[prefix]
        return {
            "model_id": model_id,
            "model_name": clean_name,
            "lab_name": info[0],
            "country": info[1],
            "flag": info[2],
            "tier": info[3]
        }

    # Dynamic Discovery Fallback for any newly launched lab in the world
    inferred_lab = prefix.replace("-", " ").replace("_", " ").title()
    return {
        "model_id": model_id,
        "model_name": clean_name,
        "lab_name": inferred_lab,
        "country": "Global Sovereign AI",
        "flag": "🌐",
        "tier": "Dynamic Frontier Model"
    }
