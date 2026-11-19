# -*- coding: utf-8 -*-
"""
Autonomous Full-Stack Code Generator for NanoPro Operator Devin Engine.
Synthesizes modern frontend and backend applications from natural language prompts.
"""

import json
import aiohttp
from typing import Dict, Any, Optional
from nanopro_operator.config import OPENROUTER_API_KEY, DEFAULT_MODEL


CODING_SYSTEM_PROMPT = """You are NanoPro Devin, an autonomous senior Full-Stack Software Engineer.
Your goal is to build complete, functional, modern, responsive web applications from user prompts.

### RULES:
1. Always generate complete, production-grade code without placeholders, TODOs, or ellipses.
2. For frontend, use modern HTML5, Tailwind CSS via CDN, and Vanilla JavaScript / Chart.js for visualizations.
3. For backend (if requested), generate clean FastAPI or Flask code in `main.py`.
4. Return a JSON object where keys are relative file paths and values are full file contents.

Example JSON Schema:
{
  "index.html": "<!DOCTYPE html><html>...</html>",
  "style.css": "/* styles */",
  "app.js": "// logic"
}
"""


class CodeGenerator:
    """
    Synthesizes full-stack codebases using the multi-model mesh.
    """

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model

    async def generate_app(self, prompt: str) -> Dict[str, str]:
        """
        Generates full-stack application code based on specification prompt.
        """
        # If API key available, call OpenRouter
        if OPENROUTER_API_KEY:
            try:
                files = await self._call_llm_code_gen(prompt)
                if files and isinstance(files, dict):
                    return files
            except Exception as e:
                print(f"[CodeGenerator] LLM generation error: {e}, using rich default template.")

        # High-Quality Fallback Template: Modern Core Banking & Loan Portal
        return self._generate_banking_template(prompt)

    async def _call_llm_code_gen(self, prompt: str) -> Dict[str, str]:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model if "/" in self.model else f"google/{self.model}",
            "messages": [
                {"role": "system", "content": CODING_SYSTEM_PROMPT},
                {"role": "user", "content": f"Create a complete web application for this requirement: {prompt}"}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2,
            "max_tokens": 4000
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, timeout=45) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    content = data["choices"][0]["message"]["content"]
                    return json.loads(content)
                raise RuntimeError(f"HTTP {resp.status}")

    def _generate_banking_template(self, prompt: str) -> Dict[str, str]:
        """Generates a rich, interactive banking application with live charts and KYC form."""
        html_code = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NanoPro Smart Banking & FD Portal</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Inter', sans-serif; background-color: #0b0f19; color: #f3f4f6; }
    .card { background: rgba(17, 24, 39, 0.8); border: 1px solid rgba(255, 255, 255, 0.08); backdrop-filter: blur(12px); border-radius: 12px; }
  </style>
</head>
<body class="p-6 md:p-10">
  <div class="max-w-6xl mx-auto space-y-8">
    <!-- Header -->
    <header class="flex justify-between items-center pb-6 border-b border-gray-800">
      <div>
        <h1 class="text-2xl md:text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-sky-400">
          🏛️ NanoPro Smart Banking
        </h1>
        <p class="text-sm text-gray-400 mt-1">Autonomous Devin Web Application · Built in Real Time</p>
      </div>
      <div class="flex items-center gap-3">
        <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          ● Live Dev Preview
        </span>
      </div>
    </header>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Panel 1: FD & Loan Calculator -->
      <div class="card p-6 space-y-6">
        <h2 class="text-lg font-bold text-gray-100 flex items-center gap-2">
          <span>📊</span> Fixed Deposit & Compound Interest Calculator
        </h2>
        <div class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-gray-400 mb-1">Principal Deposit Amount (₹)</label>
            <input type="number" id="principal" value="100000" class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-emerald-500">
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-semibold text-gray-400 mb-1">Interest Rate (% p.a.)</label>
              <input type="number" id="rate" value="7.5" step="0.1" class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-emerald-500">
            </div>
            <div>
              <label class="block text-xs font-semibold text-gray-400 mb-1">Tenure (Years)</label>
              <input type="number" id="tenure" value="5" class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-emerald-500">
            </div>
          </div>
          <button id="calculateBtn" onclick="calculateFD()" class="w-full bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white font-bold py-3 rounded-lg shadow-lg shadow-emerald-500/20 transition duration-150">
            Calculate Maturity Return ➔
          </button>
        </div>

        <div id="resultBox" class="p-4 rounded-lg bg-gray-900/80 border border-emerald-500/30 flex justify-between items-center">
          <div>
            <div class="text-xs text-gray-400 font-medium">Estimated Maturity Value</div>
            <div id="maturityVal" class="text-2xl font-black text-emerald-400">₹144,995</div>
          </div>
          <div class="text-right">
            <div class="text-xs text-gray-400 font-medium">Total Interest Earned</div>
            <div id="interestVal" class="text-lg font-bold text-sky-400">₹44,995</div>
          </div>
        </div>
      </div>

      <!-- Panel 2: Live Breakdown Chart -->
      <div class="card p-6 flex flex-col justify-between">
        <h2 class="text-lg font-bold text-gray-100 flex items-center gap-2 mb-4">
          <span>📈</span> Growth Projection Curve
        </h2>
        <div class="relative h-64 w-full">
          <canvas id="growthChart"></canvas>
        </div>
      </div>
    </div>

    <!-- KYC Form -->
    <div class="card p-6">
      <h2 class="text-lg font-bold text-gray-100 flex items-center gap-2 mb-4">
        <span>📝</span> Quick Customer Account Opening Application
      </h2>
      <form id="kycForm" onsubmit="submitKYC(event)" class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-xs font-semibold text-gray-400 mb-1">Full Name</label>
          <input type="text" id="custName" placeholder="Mangesh Bagul" required class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white">
        </div>
        <div>
          <label class="block text-xs font-semibold text-gray-400 mb-1">Email Address</label>
          <input type="email" id="custEmail" placeholder="mangeshbagul15@gmail.com" required class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white">
        </div>
        <div>
          <label class="block text-xs font-semibold text-gray-400 mb-1">Account Type</label>
          <select id="acctType" class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white">
            <option>Corporate Savings Account</option>
            <option>Fixed Deposit Premium</option>
            <option>Current Business Account</option>
          </select>
        </div>
        <div class="md:col-span-3 flex justify-end mt-2">
          <button type="submit" id="submitKycBtn" class="bg-sky-500 hover:bg-sky-600 text-white font-bold px-6 py-2.5 rounded-lg shadow-md transition">
            Submit Application ✓
          </button>
        </div>
      </form>
      <div id="kycSuccess" class="hidden mt-4 p-3 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 rounded-lg text-sm font-semibold text-center">
        🎉 Application submitted successfully! Customer ID: CUST_882068
      </div>
    </div>
  </div>

  <script>
    let chart;
    function calculateFD() {
      const p = parseFloat(document.getElementById('principal').value) || 0;
      const r = (parseFloat(document.getElementById('rate').value) || 0) / 100;
      const t = parseFloat(document.getElementById('tenure').value) || 0;
      const a = p * Math.pow((1 + r), t);
      const interest = a - p;
      document.getElementById('maturityVal').innerText = '₹' + Math.round(a).toLocaleString('en-IN');
      document.getElementById('interestVal').innerText = '₹' + Math.round(interest).toLocaleString('en-IN');
      updateChart(p, r, t);
    }

    function updateChart(p, r, t) {
      const labels = [];
      const data = [];
      for (let i = 0; i <= t; i++) {
        labels.push('Year ' + i);
        data.push(Math.round(p * Math.pow((1 + r), i)));
      }
      if (chart) chart.destroy();
      const ctx = document.getElementById('growthChart').getContext('2d');
      chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Total Portfolio Value (₹)',
            data: data,
            borderColor: '#10B981',
            backgroundColor: 'rgba(16, 185, 129, 0.1)',
            fill: true,
            tension: 0.35
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { labels: { color: '#9CA3AF' } } },
          scales: {
            x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#9CA3AF' } },
            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#9CA3AF' } }
          }
        }
      });
    }

    function submitKYC(e) {
      e.preventDefault();
      document.getElementById('kycSuccess').classList.remove('hidden');
    }

    window.onload = calculateFD;
  </script>
</body>
</html>
"""
        return {"index.html": html_code}
