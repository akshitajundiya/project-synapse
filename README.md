# Project Synapse — Agentic Last-Mile Coordinator (PoC)

This repository contains a proof-of-concept implementation for **Project Synapse** —  
an LLM/agent-powered last-mile coordinator that reasons about delivery disruptions using simulated logistics tools.

---

## Features
- **Simulated logistics tools** (`simulator/tools.py`)
- **JSON-action enforcing agent loop** (`agent/llm_agent.py`)
- **Prompt templates & few-shot examples** (`agent/prompts.py`)
- **CLI for running scenarios** (`cli.py`)
- **Test harness** with deterministic runs using a MockLLM (`tests/test_harness.py`)

---

## Folder Structure
