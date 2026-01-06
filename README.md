# 🎭 QUICK START: No API Keys Needed!

## Instant Demo (No Setup Required)

Run the standalone demo that works with just Python (no dependencies):

```bash
cd c:\Users\ASUS\Desktop\Prompt_Eval_Lab
python demo_standalone.py
```

This will:
- ✅ Evaluate all 3 prompt versions
- ✅ Score them using built-in heuristics
- ✅ Display a leaderboard showing which prompts perfom better
- ✅ **No API keys, no external libraries, no setup!**

---

# 🧠 Prompt Evaluation & Benchmarking Platform

A production-grade system for evaluating and comparing LLM prompts using objective metrics. Treat prompts as testable, version-controlled artifacts.

## Two Ways to Use This Platform

### 1. **Standalone Demo Mode** (Recommended to start)
- No API keys required
- No external dependencies
- Uses built-in Python heuristics
- Perfect for understanding the concept

```bash
python demo_standalone.py
```

### 2. **Full Version** (With OpenAI API)
- Real LLM responses
- GPT-4 as evaluator
- Advanced embeddings for similarity
- Requires API key and dependencies

## Quick Architecture

```
Prompts (v1, v2, v3) →  Evaluation Engine → Leaderboard
                            ↓
                   [Metrics + LLM Judge]
```

## What Gets Evaluated

This platform scores prompts using:

- **Semantic Similarity**: How close is the answer to the reference?
- **Accuracy**: Is the answer factually correct?
- **Faithfulness**: Does it avoid hallucinations?
- **Completeness**: Does it cover all key points?
- **Overall Score**: Weighted combination of above

## Sample Results

The demo shows that **better prompts get higher scores**:
- `prompt_v3.txt` (structured, anti-hallucination) → **Highest score**
- `prompt_v2.txt` (chain-of-thought) → **Medium score**
- `prompt_v1.txt` (basic) → **Lowest score**

This demonstrates the platform's core value: **objective prompt comparison**.

---

## Full Installation (Optional)

If you want to use real LLM APIs:

### 1. Create Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add API Key
```bash
copy .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_key_here
```

### 4. Run Full Version
```bash
# Command line
cd src
python runner.py

# Or web dashboard
python app.py
# Open http://localhost:5000
```

---

##Project Structure

```
prompt-eval-platform/
├── demo_standalone.py       ⭐ NO dependencies - try this first!
├── datasets/qa_test.json   Sample Q&A dataset
├── prompts/                3 prompt versions to compare
├── src/                    Full evaluation engine
├── static/ templates/      Web UI dashboard
└── README.md              This file
```

## Adding Your Prompts

1. Create `prompts/prompt_v4.txt`
2. Use placeholders: `{question}` and `{context}`
3. Run `python demo_standalone.py` to see how it compares!

## Why This Matters

**Problem**: Most people judge prompt quality by "feel" - subjective and unreliable.

**Solution**: This platform provides **objective, repeatable measurements** so you can:
- ✅ Track prompt improvements over time
- ✅ A/B test different approaches
- ✅ Catch regressions in prompt quality
- ✅ Make data-driven decisions

Think of it as **unit tests for prompts**.

---

## Example Workflow

```bash
# 1. Create new prompt
echo "Your innovative prompt template" > prompts/prompt_v4.txt

# 2. Run evaluation (no API needed!)
python demo_standalone.py

# 3. See the leaderboard - did your prompt win? 🏆
```

---

## Features

### Standalone Demo
- ✅ Zero setup - works immediately
- ✅ No API costs
- ✅ Demonstrates core concepts
- ✅ Heuristic-based scoring

### Full Version
- ✅ Real LLM API integration
- ✅ Embeddings-based similarity
- ✅ GPT-4 as judge for quality
- ✅ Web dashboard with beautiful UI
- ✅ Detailed result analysis

---

## Troubleshooting

**Q: Can I use this without any API keys?**  
A: Yes! Run `python demo_standalone.py` - works perfectly with no setup.

**Q: Do I need to install anything?**  
A: For the standalone demo, just Python 3.7+. For the full version, see "Full Installation" above.

**Q: Will this cost money?**  
A: The standalone demo is 100% free. The full version makes OpenAI API calls (costs pennies for the sample dataset).

---

## What Makes This Special

This isn't just a prompt tester - it's a **systematic evaluation framework** that:

1. **Treats prompts like code** - version control, testing, CI/CD mindset
2. **Uses multiple metrics** - not just one score, but comprehensive analysis
3. **Enables iteration** - quickly test variations and improvements
4. **Production-ready** - clean code, error handling, documentation

Perfect for demonstrating ML evaluation skills in interviews or portfolios.

---

## License

MIT - Use freely in your projects!

---

**Try it now**: `python demo_standalone.py` 🚀
