#!/usr/bin/env python3
"""
Token Counter for AI Taxonomy
Estimates token usage for different AI models (GPT-4, GPT-3.5, Claude, etc.)
"""

import tiktoken
import json
from pathlib import Path

def count_tokens_by_model(text, model_name="gpt-4"):
    """Count tokens for different model encodings"""
    try:
        encoding = tiktoken.encoding_for_model(model_name)
        return len(encoding.encode(text))
    except KeyError:
        # Fallback to cl100k_base for unknown models
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))

def analyze_ai_taxonomy_tokens(filename="us_taxonomy_year_list.json"):
    """Analyze token usage of AI taxonomy file"""
    ai_file = Path(f"data/ai-optimized/{filename}")
    
    if not ai_file.exists():
        print(f"❌ AI taxonomy file not found: {ai_file}")
        return
    
    # Read the file
    with open(ai_file, 'r') as f:
        content = f.read()
    
    # File size stats
    file_size = len(content)
    file_size_kb = file_size / 1024
    
    print("🤖 AI Taxonomy Token Analysis")
    print("=" * 50)
    print(f"📄 File: {ai_file}")
    print(f"📏 File size: {file_size:,} characters ({file_size_kb:.1f}KB)")
    print()
    
    # Token counts for different models
    models = [
        ("gpt-4", "GPT-4 (OpenAI)"),
        ("gpt-3.5-turbo", "GPT-3.5 Turbo (OpenAI)"),
        ("text-davinci-003", "GPT-3 Davinci (OpenAI)"),
        ("cl100k_base", "Claude/Generic (cl100k_base)")
    ]
    
    print("🔤 Token Counts by Model:")
    print("-" * 30)
    
    for model_id, model_name in models:
        try:
            token_count = count_tokens_by_model(content, model_id)
            cost_per_1k_input = get_model_cost(model_id)
            estimated_cost = (token_count / 1000) * cost_per_1k_input if cost_per_1k_input else 0
            
            print(f"{model_name:25}: {token_count:,} tokens", end="")
            if estimated_cost > 0:
                print(f" (≈${estimated_cost:.4f} input cost)")
            else:
                print()
        except Exception as e:
            print(f"{model_name:25}: Error - {e}")
    
    print()
    
    # Context window analysis
    print("📊 Context Window Analysis:")
    print("-" * 30)
    
    base_tokens = count_tokens_by_model(content, "gpt-4")
    context_windows = [
        ("GPT-4", 128000),
        ("GPT-3.5", 16385),
        ("Claude 3", 200000),
        ("Gemini Pro", 32768)
    ]
    
    for model, window_size in context_windows:
        percentage = (base_tokens / window_size) * 100
        remaining = window_size - base_tokens
        print(f"{model:12}: {percentage:5.1f}% used ({remaining:,} tokens remaining)")
    
    print()
    
    # JSON structure analysis
    try:
        data = json.loads(content)
        if "series" in data:
            series_count = len(data["series"])
            avg_tokens_per_series = base_tokens / series_count if series_count > 0 else 0
            print("📈 Structure Analysis:")
            print("-" * 20)
            print(f"Series count: {series_count}")
            print(f"Avg tokens per series: {avg_tokens_per_series:.1f}")
            print(f"Total coin IDs: {data.get('total_coin_years', 'N/A')}")
    except:
        pass

def get_model_cost(model_id):
    """Get approximate input cost per 1K tokens (as of 2024)"""
    costs = {
        "gpt-4": 0.03,
        "gpt-3.5-turbo": 0.0015,
        "text-davinci-003": 0.02,
        "cl100k_base": 0.01  # Generic estimate
    }
    return costs.get(model_id, 0)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        analyze_ai_taxonomy_tokens(sys.argv[1])
    else:
        # Default to year-list format
        analyze_ai_taxonomy_tokens("us_taxonomy_year_list.json")