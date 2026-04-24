# Blog Analyze Skill

**Purpose:** Persistent, reusable blog analysis infrastructure for the blog-analyze agent. Provides modular Python scripts for 5-category blog quality scoring, AI detection, SEO analysis, and E-E-A-T evaluation.

**Location:** `.github/skills/blog-analyze/`

---

## Usage by Agents

### For blog-analyze Agent

Instead of writing analysis code each time, the agent should:

1. **Import the analyzer modules:**
   ```python
   import sys
   sys.path.insert(0, '.github/skills/blog-analyze/scripts')
   from blog_analyzer import BlogAnalyzer
   ```

2. **Run the analysis:**
   ```python
   analyzer = BlogAnalyzer('/path/to/blog/_posts/ai/2026-04-24-post.md')
   analysis = analyzer.get_comprehensive_score()
   ```

3. **Output results** in markdown or JSON format

### From Terminal

Run the CLI analyzer directly:

```bash
cd .github/skills/blog-analyze/scripts
python main.py ../../../_posts/ai/2026-04-24-post.md --markdown
```

---

## Scripts Overview

### 📦 Core Modules

| Module | Purpose | Key Classes |
|--------|---------|------------|
| **blog_analyzer.py** | Main orchestrator | `BlogAnalyzer` — 5-category scoring |
| **readability_analyzer.py** | Reading metrics | `ReadabilityAnalyzer` — Flesch-Kincaid, sentence/para length |
| **ai_detector.py** | AI pattern detection | `AIDetector` — AI phrase patterns, emoji overuse, transition overuse |
| **seo_analyzer.py** | SEO optimization | `SEOAnalyzer` — Title, meta, headings, internal links |

### 🚀 Entry Point

| Script | Usage | Output |
|--------|-------|--------|
| **main.py** | `python main.py <file>` | Markdown report or JSON |

---

## Scoring System (5 Categories, 100 Points)

### Category 1: Content Quality (30 points)
- Word count (1500-2500 optimal)
- TL;DR section presence
- Statistics/data points (8+ required)
- Code examples (for technical posts)
- FAQ section

**Scoring Logic:**
```python
analyzer.analyze_content_quality()
# Returns: word_count, statistics_count, has_tldr, has_faq, issues
```

### Category 2: SEO Optimization (25 points)
- Title optimization (50-60 chars, keywords)
- Meta description (150-160 chars with data)
- Heading structure (H2/H3 hierarchy, 60-70% questions)
- Internal links (5+ zones)

**Scoring Logic:**
```python
analyzer.analyze_seo()
# Returns: seo_score, title_analysis, meta_analysis, headings_analysis, links_analysis
```

### Category 3: E-E-A-T Signals (15 points)
- Author attribution
- Citations/sources (8+ credible)
- Experience indicators
- Real-world examples

**Scoring Logic:**
```python
analyzer.analyze_e_e_a_t()
# Returns: author, citation_count, credible_sources, experience_indicators
```

### Category 4: Technical Elements (15 points)
- Images (4-6 with alt text)
- Code blocks
- Markdown structure
- Schema/structured data
- Front matter completeness

**Scoring Logic:**
```python
analyzer.analyze_technical_elements()
# Returns: image_count, has_code_blocks, missing_fields
```

### Category 5: AI Citation Readiness (15 points)
- Question-based headings (60-70%)
- Citation capsules (quoted/emphasized blocks)
- FAQ schema
- Entity clarity (defined terms)

**Scoring Logic:**
```python
analyzer.analyze_ai_citation_readiness()
# Returns: question_headings_count, citable_blocks, defined_terms
```

---

## AI Detection (Bonus Analysis)

Detect AI-generated content patterns:

```python
ai_content = analyzer.analyze_ai_content()
# Returns:
# - ai_score (0-100, higher = more AI-like)
# - likelihood: "Likely Human-written" | "Probably Human-written" | "Potentially AI-assisted" | "Likely AI-generated" | "Almost Certainly AI-generated"
# - Breakdown: ai_phrases_count, emoji_count, transition_overuse, vocab_diversity
```

---

## Output Formats

### Markdown Report
```bash
python main.py _posts/ai/2026-04-24-post.md --markdown
```

Produces:
- Overall score and band
- 5-category breakdown table
- AI detection results
- Key metrics summary
- Priority issues list
- Actionable recommendations

### JSON Output
```bash
python main.py _posts/ai/2026-04-24-post.md --json
```

Returns complete analysis object:
```json
{
  "total_score": 87,
  "scoring_band": "Strong",
  "ready_to_publish": true,
  "content_quality": {...},
  "seo": {...},
  "e_e_a_t": {...},
  "technical": {...},
  "ai_citation_readiness": {...},
  "ai_content": {...},
  "priority_issues": [...]
}
```

---

## Integration with blog-analyze Agent

### Flow

1. **Agent receives request:** `/blog analyze _posts/ai/2026-04-24-post.md`
2. **Agent imports skill scripts:**
   ```python
   from blog_analyzer import BlogAnalyzer
   ```
3. **Agent runs analysis:**
   ```python
   analyzer = BlogAnalyzer(filepath)
   analysis = analyzer.get_comprehensive_score()
   ```
4. **Agent formats output** as markdown report with:
   - Score and band
   - Detailed breakdown
   - AI detection results
   - Prioritized recommendations

### Example Agent Code

```python
#!/usr/bin/env python3
import sys
import json
sys.path.insert(0, '.github/skills/blog-analyze/scripts')

from blog_analyzer import BlogAnalyzer

# Usage: agent.py <filepath>
if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else None
    
    if not filepath:
        print("Usage: agent.py <filepath>")
        sys.exit(1)
    
    try:
        analyzer = BlogAnalyzer(filepath)
        analysis = analyzer.get_comprehensive_score()
        
        # Output in markdown format
        print(f"# Blog Analysis: {filepath}")
        print(f"\nScore: {analysis['total_score']}/100 [{analysis['scoring_band']}]")
        print(f"Ready to Publish: {'✅ Yes' if analysis['ready_to_publish'] else '❌ No'}")
        print(f"\nAI Detection: {analysis['ai_content']['likelihood']}")
        
        # ... format full report ...
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
```

---

## Extending the Skill

### Adding New Analyzers

1. Create new module in `scripts/` (e.g., `readability_analyzer.py`)
2. Define analyzer class with `get_*_score()` method
3. Import in `blog_analyzer.py`
4. Add method to `BlogAnalyzer.get_comprehensive_score()`

### Example: New Analyzer

```python
# scripts/performance_analyzer.py
class PerformanceAnalyzer:
    def __init__(self, text):
        self.text = text
    
    def analyze_image_optimization(self):
        # Check for optimized images
        pass
    
    def get_performance_score(self):
        return {...}

# In blog_analyzer.py
from performance_analyzer import PerformanceAnalyzer

def analyze_performance(self):
    perf = PerformanceAnalyzer(self.body)
    return perf.get_performance_score()
```

---

## Requirements

- Python 3.8+
- No external dependencies (uses only stdlib)

---

## File Structure

```
.github/skills/blog-analyze/
├── SKILL.md                              ← You are here
├── scripts/
│   ├── __init__.py                       ← Package init (empty)
│   ├── main.py                           ← CLI entry point
│   ├── blog_analyzer.py                  ← Main orchestrator
│   ├── readability_analyzer.py           ← Readability metrics
│   ├── ai_detector.py                    ← AI pattern detection
│   └── seo_analyzer.py                   ← SEO optimization
```

---

## Success Criteria

✅ Scripts are modular and reusable  
✅ No hardcoded paths (use `sys.argv` or function parameters)  
✅ Consistent scoring (30+25+15+15+15 = 100 points)  
✅ Clear issue identification with actionable fixes  
✅ Both markdown and JSON outputs supported  
✅ AI detection integrated and accurate  

---

## Related Agents

- **blog-analyze** — Uses these scripts to score blog posts
- **blog-write** — Should create content meeting these criteria
- **blog-seo** — Uses SEO analyzer for optimization guidance

---

**Last Updated:** April 24, 2026  
**Maintainer:** Copilot Blog System  
**Status:** Active ✅
