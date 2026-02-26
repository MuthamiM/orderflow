# Contributing to The Alpha Feed

Thanks for your interest in contributing! Here's how to get set up.

## Local Development Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/YOUR_USERNAME/orderflow.git
   cd orderflow
   ```

2. **Create a virtual environment**
   ```bash
   cd engine
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp ../.env.example ../.env
   # Fill in your API keys in the .env file
   ```

5. **Run the server**
   ```bash
   python main.py
   ```

## Running Tests

All tests live in `engine/test_main.py` and use `pytest`:

```bash
cd engine
pytest test_main.py -v
```

All 5 tests must pass before submitting a PR.

## Code Style

- Use type hints for all function signatures.
- Follow PEP 8 conventions.
- Use Pydantic models for all request/response schemas (see `schemas.py`).
- Document new endpoints in `docs/API.md`.

## Project Structure

```
orderflow/
├── engine/              # Python execution engine
│   ├── main.py          # FastAPI server & webhook endpoint
│   ├── config.py        # Environment variable loading
│   ├── schemas.py       # Pydantic request/response models
│   ├── risk_manager.py  # Risk evaluation logic
│   ├── polymarket_client.py  # Polymarket CLOB wrapper
│   ├── odds_reactor.py  # Live probability decay model
│   └── test_main.py     # Unit tests
├── docs/                # Documentation
├── n8n/                 # n8n workflow files
├── .env.example         # Environment variable template
├── render.yaml          # Render.com deployment config
└── README.md
```

## Submitting Changes

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Make your changes and ensure all tests pass.
4. Commit with a clear message: `git commit -m "feat: add your feature"`.
5. Push and open a Pull Request.
