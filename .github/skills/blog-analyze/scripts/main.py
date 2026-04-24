#!/usr/bin/env python3
"""
Blog Analysis CLI Runner
Command-line interface for analyzing blog posts
Usage: python main.py <filepath> [--json] [--markdown]
"""

import sys
import json
from pathlib import Path
from blog_analyzer import BlogAnalyzer


def format_markdown_report(analysis: dict) -> str:
    """Format analysis results as markdown"""
    lines = []
    
    # Header
    score = analysis["total_score"]
    band = analysis["scoring_band"]
    ready = "✅" if analysis["ready_to_publish"] else "❌"
    
    lines.append(f"# Blog Quality Analysis Report")
    lines.append(f"")
    lines.append(f"**File:** {analysis['file']}")
    lines.append(f"**Overall Score:** {score}/100 [{band}] {ready}")
    lines.append(f"")
    
    # 5-Category Breakdown
    lines.append(f"## Scoring Breakdown")
    lines.append(f"")
    lines.append(f"| Category | Score | Max |")
    lines.append(f"|---|---|---|")
    lines.append(f"| Content Quality | {analysis['content_quality']['content_quality_score']} | 30 |")
    lines.append(f"| SEO Optimization | {analysis['seo']['seo_score']} | 25 |")
    lines.append(f"| E-E-A-T Signals | {analysis['e_e_a_t']['e_e_a_t_score']} | 15 |")
    lines.append(f"| Technical Elements | {analysis['technical']['technical_score']} | 15 |")
    lines.append(f"| AI Citation Readiness | {analysis['ai_citation_readiness']['ai_citation_readiness_score']} | 15 |")
    lines.append(f"")
    
    # AI Detection
    lines.append(f"## AI Content Detection")
    lines.append(f"")
    ai = analysis['ai_content']
    lines.append(f"**Likelihood:** {ai['likelihood']}")
    lines.append(f"**AI Score:** {ai['ai_score']}/100")
    lines.append(f"")
    
    # Key Metrics
    lines.append(f"## Key Metrics")
    lines.append(f"")
    lines.append(f"- **Word Count:** {analysis['content_quality']['word_count']}")
    lines.append(f"- **Statistics:** {analysis['content_quality']['statistics_count']}")
    lines.append(f"- **Code Blocks:** {analysis['content_quality']['code_blocks_count']}")
    lines.append(f"- **Images:** {analysis['technical']['image_count']}")
    lines.append(f"- **Internal Links:** {analysis['seo']['links_analysis']['internal_links_count']}")
    lines.append(f"- **Citations:** {analysis['e_e_a_t']['citation_count']}")
    lines.append(f"")
    
    # Priority Issues
    if analysis['priority_issues']:
        lines.append(f"## Priority Issues")
        lines.append(f"")
        for issue in analysis['priority_issues'][:10]:
            lines.append(f"- ⚠️ {issue}")
        lines.append(f"")
    
    # Recommendations
    lines.append(f"## Recommendations")
    lines.append(f"")
    if score < 80:
        lines.append(f"- Score is below publish threshold (80+) — review priority issues")
    if not ai['likelihood'].startswith('Likely Human'):
        lines.append(f"- Consider rewriting to reduce AI-generated patterns")
    if analysis['content_quality']['word_count'] < 1500:
        lines.append(f"- Expand content to meet minimum word count (1500+)")
    if analysis['seo']['links_analysis']['internal_links_count'] < 5:
        lines.append(f"- Add more internal links to related posts (5+ zones)")
    
    lines.append(f"")
    lines.append(f"**Generated:** {Path(analysis['file']).stat().st_mtime}")
    
    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <filepath> [--json] [--markdown]")
        print("Example: python main.py ../_posts/ai/2026-04-24-post.md --markdown")
        sys.exit(1)
    
    filepath = sys.argv[1]
    output_format = "markdown"  # default
    
    if "--json" in sys.argv:
        output_format = "json"
    elif "--markdown" in sys.argv:
        output_format = "markdown"
    
    try:
        analyzer = BlogAnalyzer(filepath)
        analysis = analyzer.get_comprehensive_score()
        
        if output_format == "json":
            print(json.dumps(analysis, indent=2))
        else:
            print(format_markdown_report(analysis))
    
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"Error analyzing blog: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
