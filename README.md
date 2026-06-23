# PriceSpy Engine: Enterprise-Grade Self-Healing Data Pipeline

PriceSpy Engine is a high-availability, production-ready Python data pipeline built to solve the fragility inherent in traditional web scrapers. This system implements a modern distributed engineering architectural approach to monitor e-commerce market datasets while guaranteeing data consistency, zero IP rate-limits, and zero maintenance overhead.

## Architecture & Failure Domains

Rather than executing basic visual CSS DOM querying which crashes whenever front-end layouts shift, PriceSpy Engine deploys a **Multi-Tier Fault-Tolerant Fallback Matrix**:

1. **Tier 1: Wire-Level API Network Interception** — Intercepts asynchronous XHR/Fetch communication traffic packets directly inside Chromium's V8 engine loop using Playwright.
2. **Tier 2: Structured Metadata Graph Parsing** — Fallback script extracts hidden search engine optimization graph parameters mapped inside `application/ld+json` script blocks.
3. **Tier 3: Semantically Resilient DOM Search** — Final layer extracts metadata layers using robust regex patterns over BeautifulSoup document representations.

---

## Advanced System Features

### 1. Multi-Tier Fault-Tolerant Fallback Matrix
The pipeline runtime automatically handles unexpected failures by falling back through secondary parsing architectures:
*   **Tier 1 (API Interception):** Hooks into Chromium’s network engine via asynchronous event listeners. It captures clean JSON payloads from backend endpoints, entirely ignoring front-end visual elements.
*   **Tier 2 (SEO Schema Extraction):** If backend endpoints are obscured, it extracts embedded `application/ld+json` arrays to pull catalog data directly from structured search-engine metadata.
*   **Tier 3 (Defensive DOM Fallback):** If metadata tags are removed, it queries raw visual nodes using elastic fallback patterns via BeautifulSoup.

### 2. High-Fidelity Domain Boundary Constraints
Data corruption is completely blocked at the ingestion boundary. The engine routes all raw inputs through a `Pydantic` schema validator. This engine strips currency formatting symbols, cleans corrupted string sets, and guarantees down-stream structural type safety.

### 3. Anti-Fingerprinting Stealth Network Profiles
Bypasses Cloudflare, Akamai, and aggressive CDN anti-bot blocks using runtime argument masks. It overrides `AutomationControlled` browser flags, randomizes viewport aspect ratios, and injects realistic desktop browser signatures.

---

## System File Hierarchy

```text
├── models.py             # Declarative schema contracts & validation boundaries
├── scraper.py            # Chromium network sniffer and fallback execution loop
├── pipeline.py           # Google Cloud Platform API synchronization broker
├── main.py               # Central execution controller & logging supervisor
├── requirements.txt      # Cryptographically locked ecosystem dependencies
└── README.md             # Systems documentation framework
```

---

## Deployment & Installation

### Prerequisite Environment Configurations
*   Python 3.10+ runtime engine
*   Google Cloud Platform (GCP) Service Account Access Certificate

### 1. Initialize the Runtime Virtualization
```bash
# Clone and navigate into the project workspace
git clone https://github.com
cd PriceSpy_Engine

# Create and isolate your virtual execution shell
python3 -m venv .venv
source .venv/bin/activate

# Flush dependencies into active environment
pip install --upgrade pip
pip install -r requirements.txt

# Synchronize underlying standalone Chromium browser dependencies
playwright install chromium
```

### 2. Configure Your Authentication Keys
Generate a **Service Account Key** inside your GCP console. Download the JSON credential file, rename it to exactly `credentials.json`, and place it in the root folder of this project workspace.

### 3. Trigger Ingestion Operations
Update the `GOOGLE_SPREADSHEET_ID` configuration variable inside `main.py` with your spreadsheet identifier hash, and run the pipeline:
```bash
python main.py
```

---

## High-Scale Telemetry Logs

The pipeline uses low-overhead asynchronous logging streams to output execution traces to stdout and maintain rotation-locked archive files:

```text
2026-06-23 13:45:12 | INFO     | main.py:15 - Initializing Data Ingestion Pipeline Execution Matrix...
2026-06-23 13:45:13 | INFO     | scraper.py:48 - Initiating defensive extraction runtime targeting resource...
2026-06-23 13:45:15 | SUCCESS  | scraper.py:27 - Network interceptor successfully drained API wire: /api/v1/products...
2026-06-23 13:45:16 | INFO     | pipeline.py:32 - Serializing structural payloads for spreadsheet extraction.
2026-06-23 13:45:18 | SUCCESS  | pipeline.py:54 - Successfully synchronized 48 data records to Google Sheets ledger.
```

---

## License & Professional Engagement

This infrastructure project is distributed under the terms of the MIT open-source license architecture. 

For custom system builds, real-time distributed engineering, or high-throughput big data orchestration requests, reach out directly through my **Upwork Freelancer Profile**.
