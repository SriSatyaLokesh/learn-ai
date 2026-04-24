"""
SEO Analysis Module
Analyzes blog posts for SEO optimization (title, meta, headings, links, keywords)
"""

import re
from typing import Dict, List, Tuple


class SEOAnalyzer:
    """Analyzes blog post SEO metrics"""
    
    def __init__(self, frontmatter: str, body: str, slug: str = ""):
        self.frontmatter = frontmatter
        self.body = body
        self.slug = slug
        self.fm_dict = self._parse_frontmatter()
    
    def _parse_frontmatter(self) -> Dict:
        """Parse YAML-style frontmatter into dictionary"""
        fm_dict = {}
        for line in self.frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                fm_dict[key.strip().lower()] = value.strip().strip('"\'[]')
        return fm_dict
    
    def analyze_title(self) -> Dict:
        """Analyze blog title for SEO"""
        title = self.fm_dict.get('title', '')
        
        score = 0
        issues = []
        
        # Length check (50-60 optimal)
        if len(title) < 30:
            issues.append("Title too short (< 30 chars)")
            score -= 10
        elif len(title) < 50:
            score += 5
        elif len(title) <= 60:
            score += 10
        elif len(title) <= 70:
            score += 5
        else:
            issues.append("Title too long (> 70 chars)")
            score -= 5
        
        # Question format (good for CTR)
        if title.endswith('?'):
            score += 5
        
        # Numbers increase CTR
        if re.search(r'\d+', title):
            score += 5
        
        return {
            "title": title,
            "length": len(title),
            "score": max(0, min(10, score)),
            "issues": issues,
        }
    
    def analyze_meta_description(self) -> Dict:
        """Analyze meta description for SEO"""
        description = self.fm_dict.get('description', '')
        
        score = 0
        issues = []
        
        # Length check (150-160 optimal)
        if len(description) < 120:
            issues.append("Meta description too short (< 120 chars)")
            score -= 5
        elif len(description) < 150:
            score += 3
        elif len(description) <= 160:
            score += 10
        elif len(description) <= 170:
            score += 5
        else:
            issues.append("Meta description too long (> 170 chars)")
            score -= 5
        
        # Should contain a stat or number
        if re.search(r'\d+%?', description) or re.search(r'\b\d+\b', description):
            score += 5
        
        return {
            "description": description,
            "length": len(description),
            "score": max(0, min(10, score)),
            "issues": issues,
        }
    
    def analyze_headings(self) -> Dict:
        """Analyze heading structure and keyword optimization"""
        h2_pattern = r'^## (.+?)$'
        h3_pattern = r'^### (.+?)$'
        
        h2_headings = re.findall(h2_pattern, self.body, re.MULTILINE)
        h3_headings = re.findall(h3_pattern, self.body, re.MULTILINE)
        
        score = 0
        issues = []
        
        # Check for proper hierarchy
        if len(h2_headings) == 0:
            issues.append("No H2 headings found")
            score -= 10
        elif len(h2_headings) < 4:
            issues.append(f"Only {len(h2_headings)} H2 headings (recommend 4-6)")
            score -= 5
        elif len(h2_headings) > 10:
            issues.append(f"Too many H2 headings ({len(h2_headings)}, recommend 4-10)")
            score -= 3
        else:
            score += 8
        
        # Check for question-based headings
        question_headings = [h for h in h2_headings if h.endswith('?')]
        question_percentage = (len(question_headings) / len(h2_headings) * 100) if h2_headings else 0
        
        if question_percentage >= 60:
            score += 5
        elif question_percentage >= 40:
            score += 3
        
        return {
            "h2_count": len(h2_headings),
            "h3_count": len(h3_headings),
            "h2_headings": h2_headings[:5],  # First 5
            "question_percentage": question_percentage,
            "score": max(0, min(10, score)),
            "issues": issues,
        }
    
    def analyze_internal_links(self) -> Dict:
        """Analyze internal linking strategy"""
        # Look for internal links marked with [INTERNAL-LINK: ...] or markdown links
        internal_link_markers = len(re.findall(r'\[INTERNAL-LINK:', self.body))
        markdown_links = len(re.findall(r'\[([^\]]+)\]\((?!/)', self.body))
        
        total_internal_links = internal_link_markers + markdown_links
        
        score = 0
        issues = []
        
        if total_internal_links == 0:
            issues.append("No internal links found")
            score = 0
        elif total_internal_links < 3:
            issues.append(f"Only {total_internal_links} internal links (recommend 5+)")
            score += 3
        elif total_internal_links < 5:
            score += 5
        else:
            score += 10
        
        return {
            "internal_links_count": total_internal_links,
            "unresolved_placeholders": internal_link_markers,
            "markdown_links": markdown_links,
            "score": max(0, min(10, score)),
            "issues": issues,
        }
    
    def get_seo_score(self) -> Dict:
        """Calculate comprehensive SEO score (0-25 points)"""
        title_analysis = self.analyze_title()
        meta_analysis = self.analyze_meta_description()
        headings_analysis = self.analyze_headings()
        links_analysis = self.analyze_internal_links()
        
        # Weighted scoring
        total_score = (
            title_analysis["score"] * 0.25
            + meta_analysis["score"] * 0.25
            + headings_analysis["score"] * 0.25
            + links_analysis["score"] * 0.25
        ) * 2.5  # Scale to 25 points
        
        all_issues = []
        for analysis in [title_analysis, meta_analysis, headings_analysis, links_analysis]:
            all_issues.extend(analysis.get("issues", []))
        
        return {
            "seo_score": int(total_score),
            "title": title_analysis,
            "meta_description": meta_analysis,
            "headings": headings_analysis,
            "internal_links": links_analysis,
            "all_issues": all_issues,
        }
