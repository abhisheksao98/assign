# Quick Start Guide

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Get API Key

1. Visit https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key

## 3. Create .env File

```bash
echo "GEMINI_API_KEY=your_key_here" > .env
```

Replace `your_key_here` with your actual API key.

## 4. Run the Application

```bash
python main.py
```

## 5. Open Browser

Navigate to: http://localhost:8000

## Test Queries

Try these example queries:

- "Best camera phone under ₹30,000?"
- "Compare Pixel 8a vs OnePlus 12R"
- "Show me Samsung phones under ₹25k"
- "Explain OIS vs EIS"
- "Compact Android with good one-hand use"

## Troubleshooting

### API Key Error
- Make sure `.env` file exists in the root directory
- Check that `GEMINI_API_KEY` is set correctly
- Restart the server after creating `.env`

### Database Error
- The database is created automatically on first run
- If issues occur, delete `phones.db` and restart

### Port Already in Use
- Change port in `main.py`: `uvicorn.run(app, host="0.0.0.0", port=8001)`

