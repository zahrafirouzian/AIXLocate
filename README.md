# AIXLocate

### AI + eXplore + Locate

**AI eXploration for Intelligent AI Infrastructure Placement**

> An AI-powered climate intelligence platform that evaluates and ranks candidate locations for AI infrastructure using environmental data, geospatial analysis, and multi-agent decision-making.

---

# 🚨 The Problem

The rapid growth of Artificial Intelligence is creating massive demand for new data center infrastructure.

However, selecting the wrong location can lead to:

- 💸 Higher cooling and operational costs
- ⚡ Higher energy demands
- 📉 Reduced operational efficiency
- ⚠️ Greater environmental and infrastructure challenges

Traditional site selection processes are often:

- Time-consuming and manual
- Dependent on fragmented data sources
- Difficult to scale across multiple candidate locations

As AI infrastructure becomes more complex, organizations need a smarter way to evaluate climate, environmental, and infrastructure conditions before investing in large-scale deployments.

---

# 💡 The Solution

AIXLocate introduces an **AI-powered location intelligence platform** designed to evaluate and rank candidate locations for AI infrastructure.

The platform:

1. 🌎 Analyzes candidate locations
2. 📡 Collects environmental and climate intelligence
3. 🌡️ Evaluates climate suitability
4. 🏆 Scores locations based on climate and environmental factors
5. 🤖 Generates AI-driven recommendations
6. 🗺️ Provides interactive location visualization
7. 📄 Creates structured analysis reports

AIXLocate enables smarter, data-driven decisions for AI infrastructure placement through climate intelligence and AI-powered analysis.

---

# 🌡️ FortyGuard API Integration

FortyGuard provides the environmental intelligence layer behind AIXLocate.

Using the **FortyGuard Temperature API**, AIXLocate analyzes climate-related factors relevant to AI infrastructure deployment and cooling considerations.

The platform uses FortyGuard data for:

- 🌡️ Temperature analysis
- 🌍 Environmental parameter evaluation
- 📊 Climate suitability scoring (AIXLocate scoring layer)
- 🏗️ AI-driven infrastructure recommendations based on climate insights

AIXLocate transforms FortyGuard environmental data into actionable climate insights to support data-driven location assessment.

---


# ✨ Features

## 🌎 Climate Intelligence Analysis

Analyze climate conditions and environmental parameters relevant to AI infrastructure cooling considerations.

---

## 🏆 AI Infrastructure Suitability Scoring

Generate quantitative suitability scores for candidate locations based on climate and environmental intelligence.

---

## 🤖 AI-Powered Recommendations

Receive automated infrastructure recommendations generated through a multi-agent AI workflow.

---

## 🗺️ Interactive Geospatial Visualization

Explore and compare candidate locations through an interactive map interface.

---

## 📊 Location Comparison

Compare candidate areas and identify suitable options for AI infrastructure deployment.

---

## 📄 PDF Report Generation

Export structured reports containing analysis results, rankings, and AI-generated recommendations.

---

# 🏗️ Architecture

AIXLocate uses a modular architecture that combines data intelligence, AI agents, and geospatial analysis.

The system consists of:

- 🎨 Frontend visualization layer for exploring candidate locations
- ⚡ FastAPI backend services for data processing and API orchestration
- 🤖 LangGraph-based AI agent workflow for analysis and decision-making
- 🌡️ FortyGuard environmental intelligence layer for climate data
- 🗺️ Geospatial processing for location-based analysis
- 🏆 Climate suitability scoring and recommendation engine for AI infrastructure locations

The workflow combines environmental data, location intelligence, and multi-agent reasoning to generate data-driven location recommendations.

---

# 🤖 AI Agent Workflow

The LangGraph-based multi-agent workflow coordinates the location analysis and decision-support pipeline:

1. 🧭 **Planner Agent**
   - Interprets the location analysis request
   - Defines the analysis workflow and required data

2. 🌡️ **Climate Intelligence Agent**
   - Collects and analyzes climate conditions using FortyGuard environmental data

3. 📊 **Scoring Engine**
   - Calculates infrastructure suitability scores based on climate and environmental factors

4. 📄 **Report Generator Agent**
   - Generates structured location assessment reports with AI-driven insights
  
---

# 🛠️ Technology Stack

## 🎨 Frontend

### Next.js + React + TypeScript

Used for building the interactive user interface, location intelligence dashboard, map visualization, and result exploration.

Technologies:

- Next.js 16.3.3
- React 19.2.8
- TypeScript
- Tailwind CSS 4
- React Leaflet
- Leaflet
- OpenStreetMap


---

## ⚙️ Backend

### FastAPI + Python

Provides the API layer, analysis pipeline, and communication between the frontend, AI workflow, and external services.

Technologies:

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- Requests


---

## 🤖 AI Orchestration

### LangGraph Multi-Agent Workflow

Used to coordinate the AI-driven analysis pipeline and structured decision workflow.

Agents:

- Planner Agent
- Climate Intelligence Agent
- Scoring Engine
- Report Generator Agent

Technologies:

- LangGraph
- LangChain


---

## 🌡️ Environmental Intelligence

### FortyGuard Temperature API

Provides climate and environmental intelligence for evaluating AI infrastructure locations.

Used capabilities:

- Temperature Intelligence
- Environmental Parameters
- Heatmap Analysis
- Climate Data Processing
- Climate Suitability Scoring (AIXLocate scoring layer)

---

## 🗺️ Geospatial Intelligence

Used for location processing, boundary analysis, and spatial analysis.

Technologies:

- PyProj
- Shapely
- Geocoding Services
- City Boundary Processing
- Location Area Processing
- GeoJSON


---

## 🧠 AI Reasoning & Report Generation

Transforms climate analysis and scoring results into infrastructure-focused insights and structured reports.

Technologies:

- Ollama
- Qwen2.5:1.5B Local LLM
- Prompt-based AI reasoning


---

## 📊 Reporting & Visualization

Used for presenting results and generating downloadable analysis reports.

Technologies:

- Interactive Maps
- Data Visualization
- PDF Report Generation
- jsPDF
- jsPDF-AutoTable

---

# 🌱 Impact

AIXLocate helps organizations make smarter decisions when planning next-generation AI infrastructure.

It enables:

- 🚀 Faster and more informed infrastructure planning
- ❄️ Better evaluation of climate conditions affecting cooling considerations
- ⚡ Better operational planning through climate insights
- 🌍 More climate-aware AI infrastructure planning
- 📊 Data-driven location assessment before large-scale investment

---

# 🔮 Future Vision

AIXLocate currently focuses on climate intelligence and geospatial analysis for AI infrastructure placement.

Future versions will expand the platform with additional infrastructure intelligence layers:

- ⚡ Power grid and energy availability analysis
- ☀️ Renewable energy potential assessment
- 🌐 Network connectivity analysis
- 🌪️ Natural hazard and climate risk assessment
- 🧩 Multi-factor infrastructure suitability optimization
  
---

👤 Creator

A solo-built project developed for the FortyGuard Hackathon 2026.

AIXLocate — AI-powered exploration for smarter infrastructure placement.
