import subprocess
import json
import os
import sys

posts = [
    "_posts/tools/2026-08-03-what-is-a-software-factory.md",
    "_posts/tools/2026-08-04-why-build-a-software-factory.md",
    "_posts/tools/2026-08-05-how-to-build-a-software-factory.md",
    "_posts/tools/2026-08-06-software-factory-examples-and-theories.md",
    "_posts/tools/2026-08-07-software-factory-for-existing-projects.md",
    "_posts/tools/2026-08-08-software-factory-for-new-projects.md",
    "_posts/tools/2026-08-09-build-your-own-software-factory-gsd-ponytail-caveman.md",
]

sys.path.insert(0, '.github/skills/blog-analyze/scripts')
from blog_analyzer import BlogAnalyzer

for post in posts:
    if not os.path.exists(post):
        print(f"NOT FOUND: {post}")
        continue
    analyzer = BlogAnalyzer(post)
    d = analyzer.get_comprehensive_score()
    fname = os.path.basename(post)
    score = d['total_score']
    band = d['scoring_band']
    words = d['content_quality']['word_count']
    stats = d['content_quality']['statistics_count']
    images = d['technical']['image_count']
    citations = d['e_e_a_t']['citation_count']
    links = d['seo']['links_analysis']['internal_links_count']
    tldr = d['content_quality'].get('has_tldr', False)
    faq = d['content_quality'].get('has_faq', False)
    ai_like = d['ai_content']['likelihood']
    meta_len = d['seo']['meta_analysis']['length']
    q_pct = d['seo']['headings_analysis']['question_percentage']
    issues = d.get('priority_issues', [])
    print(f"\n=== {fname} ===")
    print(f"Score: {score}/100 [{band}]")
    print(f"Words: {words} | Stats: {stats} | Images: {images} | Citations: {citations} | Links: {links}")
    print(f"TL;DR: {tldr} | FAQ: {faq} | AI: {ai_like} | Meta len: {meta_len} | Q%: {q_pct}")
    print(f"Issues: {issues}")
