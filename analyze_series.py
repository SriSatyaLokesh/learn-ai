#!/usr/bin/env python3
"""Analyze all 10 posts in the Autonomous Software Factory series."""

import sys
import json
sys.path.insert(0, '.github/skills/blog-analyze/scripts')

from blog_analyzer import BlogAnalyzer

posts = [
    ('Part 1', '_posts/tools/2026-08-03-what-is-a-software-factory.md'),
    ('Part 2', '_posts/tools/2026-08-04-why-build-a-software-factory.md'),
    ('Part 3', '_posts/tools/2026-08-05-core-components-orchestration-templates-automation.md'),
    ('Part 4', '_posts/tools/2026-08-06-software-factory-examples-netflix-google-stripe.md'),
    ('Part 5', '_posts/tools/2026-08-07-how-to-build-a-generic-software-factory.md'),
    ('Part 6', '_posts/tools/2026-08-10-introducing-ai-agents-to-your-factory.md'),
    ('Part 7', '_posts/tools/2026-08-11-autonomous-software-factories-explained.md'),
    ('Part 8', '_posts/tools/2026-08-12-autonomous-factory-examples-ona-gitpod-memo.md'),
    ('Part 9', '_posts/tools/2026-08-13-building-your-first-autonomous-factory.md'),
    ('Part 10', '_posts/tools/2026-08-14-scaling-autonomous-factories-advanced-patterns.md'),
]

print("=" * 80)
print("AUTONOMOUS SOFTWARE FACTORY SERIES - COMPREHENSIVE ANALYSIS")
print("=" * 80)
print()

all_results = []
for name, path in posts:
    try:
        analyzer = BlogAnalyzer(path)
        result = analyzer.get_comprehensive_score()
        all_results.append({
            'name': name,
            'path': path,
            'score': result['total_score'],
            'band': result['scoring_band'],
            'ready': result['ready_to_publish'],
            'issues': result['priority_issues'],
            'word_count': result['content_quality']['word_count'],
            'image_count': result['technical']['image_count'],
            'internal_links': result['seo']['links_analysis']['internal_links_count'],
            'ai_score': result['ai_content']['ai_score'],
            'ai_likelihood': result['ai_content']['likelihood'],
        })
        print(f"{name}: {result['total_score']}/100 [{result['scoring_band']}]")
        print(f"  Ready to Publish: {'✓ Yes' if result['ready_to_publish'] else '✗ No'}")
        print(f"  Word Count: {result['content_quality']['word_count']} | Images: {result['technical']['image_count']} | Links: {result['seo']['links_analysis']['internal_links_count']}")
        print(f"  AI Score: {result['ai_content']['ai_score']}/100 ({result['ai_content']['likelihood']})")
        if result['priority_issues']:
            print(f"  Issues ({len(result['priority_issues'])}):")
            for issue in result['priority_issues'][:3]:
                print(f"    • {issue}")
            if len(result['priority_issues']) > 3:
                print(f"    ... and {len(result['priority_issues']) - 3} more")
        print()
    except Exception as e:
        print(f"{name}: ERROR - {e}")
        print()

# Summary
print("=" * 80)
print("SERIES SUMMARY")
print("=" * 80)
scores = [r['score'] for r in all_results]
print(f"Average Score: {sum(scores) / len(scores):.1f}/100")
print(f"Highest: {max(r['score'] for r in all_results)}/100 ({[r['name'] for r in all_results if r['score'] == max(scores)][0]})")
print(f"Lowest: {min(r['score'] for r in all_results)}/100 ({[r['name'] for r in all_results if r['score'] == min(scores)][0]})")
print()

# Category breakdown
print("COMMON ISSUES ACROSS SERIES")
print("-" * 80)
issue_counts = {}
for r in all_results:
    for issue in r['issues']:
        issue_counts[issue] = issue_counts.get(issue, 0) + 1

sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)
for issue, count in sorted_issues[:10]:
    print(f"[{count}x] {issue}")
print()

# Content quality analysis
print("CONTENT METRICS")
print("-" * 80)
print(f"Avg Word Count: {sum(r['word_count'] for r in all_results) / len(all_results):.0f} (target: 1500-2500)")
print(f"Avg Images: {sum(r['image_count'] for r in all_results) / len(all_results):.1f} (target: 4-6)")
print(f"Avg Internal Links: {sum(r['internal_links'] for r in all_results) / len(all_results):.1f} (target: 5+)")
print(f"Avg AI Score: {sum(r['ai_score'] for r in all_results) / len(all_results):.0f}/100")
print()

# Recommendations
print("TOP PRIORITY IMPROVEMENTS FOR SERIES")
print("-" * 80)
print("1. Add missing hero images (CRITICAL)")
print("   - Most posts have 0 images but should have 4-6")
print("   - Hero image already set, but need supporting images in content")
print()
print("2. Expand word count where needed")
print("   - Posts below 1500 words need expansion")
print("   - Add more examples, case studies, or deep dives")
print()
print("3. Increase internal linking")
print("   - Add cross-series navigation (\"Previous post\" / \"Next post\")")
print("   - Link to related topics within series")
print()
print("4. Strengthen E-E-A-T signals")
print("   - Add more statistics and data points")
print("   - Include author credentials")
print("   - Reference authoritative sources")
print()
print("5. Optimize for AI Citation Readiness")
print("   - Use more question-based headings")
print("   - Add highlighted quote blocks (citation capsules)")
print("   - Define key terms explicitly")
