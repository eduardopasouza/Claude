"""
AgroJus Code Review Agent — Codex 5.4 (OpenAI)
Agent #11 in the multi-agent architecture.

Reviews critical backend files for:
- Security vulnerabilities (OWASP Top 10)
- Bug patterns and logic errors
- Performance issues
- Python best practices
- FastAPI-specific patterns
"""

import os
import sys
import json
import httpx
from pathlib import Path
from datetime import datetime

# Load API key from .env
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("ERROR: OPENAI_API_KEY not found in .env")
    sys.exit(1)

# Files to review (most critical first)
REVIEW_FILES = [
    "app/api/consulta.py",        # Core business logic — unified query
    "app/services/auth.py",       # Authentication — security critical
    "app/middleware/rate_limit.py", # Rate limiting — security critical
    "app/collectors/datajud.py",  # External API — had bugs
    "app/api/compliance.py",      # Compliance checks — legal liability
]

REVIEW_PROMPT = """You are a senior Python security & code reviewer specializing in FastAPI applications. 
You are Agent #11 (Code Reviewer) in the AgroJus multi-agent development team.

Review the following Python file for:
1. **SECURITY** — SQL injection, XSS, auth bypass, secret exposure, OWASP Top 10
2. **BUGS** — Logic errors, race conditions, unhandled exceptions, type errors
3. **PERFORMANCE** — N+1 queries, blocking calls in async, memory leaks, missing timeouts
4. **BEST PRACTICES** — Python/FastAPI conventions, error handling, logging

For each issue found, respond in this JSON format:
{
  "file": "filename",
  "issues": [
    {
      "severity": "critical|high|medium|low",
      "category": "security|bug|performance|best_practice",
      "line": <approximate line number>,
      "description": "What's wrong",
      "fix": "How to fix it"
    }
  ],
  "summary": "Overall assessment in 2-3 sentences",
  "score": <0-100 quality score>
}

Be concise. Only report real issues, not style preferences.

FILE TO REVIEW:
```python
{code}
```
"""

def review_file(filepath: str) -> dict:
    """Send a file to Codex 5.4 for review."""
    code = Path(filepath).read_text(encoding="utf-8")
    
    prompt = REVIEW_PROMPT.replace("{code}", code)
    
    response = httpx.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2000,
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
        },
        timeout=60.0,
    )
    
    if response.status_code != 200:
        return {"file": filepath, "error": f"HTTP {response.status_code}: {response.text[:200]}"}
    
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"file": filepath, "raw_response": content}


def main():
    print("=" * 60)
    print("AgroJus Code Review — Agent #11 (Codex 5.4)")
    print(f"Date: {datetime.now().isoformat()}")
    print("=" * 60)
    
    all_results = []
    
    for filepath in REVIEW_FILES:
        if not Path(filepath).exists():
            print(f"\n❌ SKIP: {filepath} not found")
            continue
        
        print(f"\n🔍 Reviewing: {filepath} ...", end=" ", flush=True)
        result = review_file(filepath)
        result["file"] = filepath
        all_results.append(result)
        
        if "error" in result:
            print(f"ERROR: {result['error']}")
            continue
        
        score = result.get("score", "?")
        issues = result.get("issues", [])
        critical = sum(1 for i in issues if i.get("severity") == "critical")
        high = sum(1 for i in issues if i.get("severity") == "high")
        medium = sum(1 for i in issues if i.get("severity") == "medium")
        low = sum(1 for i in issues if i.get("severity") == "low")
        
        print(f"Score: {score}/100 | Issues: {critical}C {high}H {medium}M {low}L")
        
        if issues:
            for issue in issues:
                sev = issue.get("severity", "?").upper()
                cat = issue.get("category", "?")
                line = issue.get("line", "?")
                desc = issue.get("description", "")
                print(f"  [{sev}] L{line} ({cat}): {desc}")
    
    # Save full report
    report_path = Path("../docs/coordination/agents/code-reviewer.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# Code Review Report — Agent #11 (Codex 5.4)\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Model:** GPT-4o (OpenAI Codex 5.4)\n")
        f.write(f"**Files reviewed:** {len(all_results)}\n\n")
        
        total_issues = 0
        for result in all_results:
            filepath = result.get("file", "unknown")
            score = result.get("score", "N/A")
            issues = result.get("issues", [])
            summary = result.get("summary", "")
            total_issues += len(issues)
            
            f.write(f"## {filepath}\n\n")
            f.write(f"**Score:** {score}/100 | **Issues:** {len(issues)}\n\n")
            
            if summary:
                f.write(f"> {summary}\n\n")
            
            if issues:
                f.write("| Severity | Category | Line | Description | Fix |\n")
                f.write("|----------|----------|------|-------------|-----|\n")
                for issue in issues:
                    sev = issue.get("severity", "?")
                    cat = issue.get("category", "?")
                    line = issue.get("line", "?")
                    desc = issue.get("description", "").replace("|", "\\|")
                    fix = issue.get("fix", "").replace("|", "\\|")
                    f.write(f"| {sev} | {cat} | {line} | {desc} | {fix} |\n")
                f.write("\n")
            
            f.write("---\n\n")
        
        f.write(f"**Total issues found:** {total_issues}\n")
    
    print(f"\n📄 Full report saved to: {report_path}")
    
    # Also save as JSON for programmatic use
    json_path = Path("../docs/coordination/agents/code-review-results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"📊 JSON results saved to: {json_path}")


if __name__ == "__main__":
    main()
