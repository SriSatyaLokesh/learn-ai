"""
Main Blog Analyzer
Orchestrates 5-category blog quality analysis and generates comprehensive scores
"""

import re
import json
from typing import Dict, Tuple
from pathlib import Path
from readability_analyzer import ReadabilityAnalyzer
from ai_detector import AIDetector
from seo_analyzer import SEOAnalyzer


class BlogAnalyzer:
    """Main blog quality analyzer - 5-category scoring"""
    
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.content = self._read_file()
        self.frontmatter, self.body = self._parse_markdown()
        self.slug = self.filepath.stem
    
    def _read_file(self) -> str:
        """Read blog file"""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _parse_markdown(self) -> Tuple[str, str]:
        """Extract front matter and body from markdown"""
        match = re.match(r'^---\n(.*?)\n---\n(.*)', self.content, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return "", self.content
    
    def _get_frontmatter_dict(self) -> Dict:
        """Parse frontmatter into dictionary"""
        fm_dict = {}
        for line in self.frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                fm_dict[key.strip().lower()] = value.strip().strip('"\'[]')
        return fm_dict
    
    def analyze_content_quality(self) -> Dict:
        """Score content quality (0-30 points)"""
        fm_dict = self._get_frontmatter_dict()
        word_count = len(self.body.split())
        
        score = 0
        issues = []
        
        # Word count (2000-2500 optimal for blogs)
        if word_count < 800:
            issues.append(f"Too short ({word_count} words, recommend 1500+)")
            score += 5
        elif word_count < 1500:
            score += 10
        elif word_count <= 3000:
            score += 20
        else:
            issues.append(f"Too long ({word_count} words)")
            score += 15
        
        # Check for TL;DR section
        if re.search(r'(TL;DR|tl;dr|Summary)', self.body):
            score += 3
        else:
            issues.append("Missing TL;DR or summary section")
        
        # Check for statistics/data
        stat_count = len(re.findall(r'\d+%|\d+\s*(?:billion|million|thousand|x|times)', self.body))
        if stat_count >= 8:
            score += 3
        elif stat_count >= 4:
            score += 2
        else:
            issues.append(f"Only {stat_count} statistics found (recommend 8+)")
        
        # Check for code blocks (for technical posts)
        code_blocks = len(re.findall(r'```', self.body))
        if 'ai' in fm_dict.get('category', '').lower() or code_blocks > 0:
            if code_blocks >= 2:
                score += 2
            elif code_blocks == 0:
                issues.append("Consider adding code examples for technical posts")
        
        # Check for FAQ section
        if re.search(r'(FAQ|Frequently Asked|Questions)', self.body, re.IGNORECASE):
            score += 2
        else:
            issues.append("Missing FAQ section")
        
        return {
            "content_quality_score": min(30, score),
            "word_count": word_count,
            "statistics_count": stat_count,
            "code_blocks_count": code_blocks,
            "has_tldr": bool(re.search(r'(TL;DR|tl;dr)', self.body)),
            "has_faq": bool(re.search(r'(FAQ|Questions)', self.body, re.IGNORECASE)),
            "issues": issues,
        }
    
    def analyze_seo(self) -> Dict:
        """Score SEO optimization (0-25 points)"""
        seo_analyzer = SEOAnalyzer(self.frontmatter, self.body, self.slug)
        seo_result = seo_analyzer.get_seo_score()
        
        return {
            "seo_score": seo_result["seo_score"],
            "title_analysis": seo_result["title"],
            "meta_analysis": seo_result["meta_description"],
            "headings_analysis": seo_result["headings"],
            "links_analysis": seo_result["internal_links"],
            "seo_issues": seo_result["all_issues"],
        }
    
    def analyze_e_e_a_t(self) -> Dict:
        """Score E-E-A-T signals (0-15 points)"""
        fm_dict = self._get_frontmatter_dict()
        
        score = 0
        issues = []
        
        # Author attribution
        if fm_dict.get('author'):
            score += 3
        else:
            issues.append("Missing author attribution")
        
        # Sources/citations
        source_count = len(re.findall(r'\[.*?\]\(https?://', self.body))
        if source_count >= 8:
            score += 5
        elif source_count >= 4:
            score += 3
        else:
            issues.append(f"Only {source_count} citations (recommend 8+)")
            score += 1
        
        # Credible sources (look for domains like github, official docs, etc)
        credible_count = len(re.findall(
            r'github\.com|documentation|official|research|whitepaper|arxiv|scholar',
            self.body,
            re.IGNORECASE
        ))
        if credible_count >= 3:
            score += 4
        elif credible_count >= 1:
            score += 2
        
        # Experience indicators (code examples, real-world examples)
        experience_indicators = len(re.findall(
            r'```|example|production|real-world|case study|implementation|best practice',
            self.body,
            re.IGNORECASE
        ))
        if experience_indicators >= 5:
            score += 3
        
        return {
            "e_e_a_t_score": min(15, score),
            "author": fm_dict.get('author', ''),
            "citation_count": source_count,
            "credible_source_mentions": credible_count,
            "experience_indicators": experience_indicators,
            "issues": issues,
        }
    
    def analyze_technical_elements(self) -> Dict:
        """Score technical SEO and elements (0-15 points)"""
        fm_dict = self._get_frontmatter_dict()
        
        score = 0
        issues = []
        
        # Image presence
        image_count = len(re.findall(r'!\[.*?\]\(', self.body))
        if image_count >= 4:
            score += 4
        elif image_count >= 2:
            score += 2
        else:
            issues.append(f"Only {image_count} images (recommend 4-6)")
        
        # Alt text for images
        alt_text_count = len(re.findall(r'!\[.+?\]', self.body))
        if alt_text_count == image_count and image_count > 0:
            score += 2
        
        # Code formatting
        if '```' in self.body:
            score += 2
        
        # Proper markdown structure
        if '##' in self.body:
            score += 2
        
        # Schema/structured data indicators
        if 'json-ld' in self.body or 'schema' in self.body.lower():
            score += 3
        
        # Front matter completeness
        required_fields = ['title', 'date', 'category', 'description', 'difficulty']
        missing_fields = [f for f in required_fields if not fm_dict.get(f.lower())]
        if not missing_fields:
            score += 2
        else:
            issues.append(f"Missing front matter fields: {', '.join(missing_fields)}")
        
        return {
            "technical_score": min(15, score),
            "image_count": image_count,
            "has_code_blocks": '```' in self.body,
            "missing_frontmatter_fields": missing_fields,
            "issues": issues,
        }
    
    def analyze_ai_citation_readiness(self) -> Dict:
        """Score AI citation readiness (0-15 points)"""
        score = 0
        issues = []
        
        # Question-based headings (good for AI extraction)
        question_headings = len(re.findall(r'^[^#]*\?$', self.body, re.MULTILINE))
        if question_headings >= 5:
            score += 5
        elif question_headings >= 3:
            score += 3
        
        # Citation capsules (self-contained citable passages)
        # Look for quoted blocks or emphasis
        quoted_blocks = len(re.findall(r'> .*?\n', self.body))
        emphasis_blocks = len(re.findall(r'\*\*[^*]{20,}?\*\*', self.body))
        if quoted_blocks + emphasis_blocks >= 5:
            score += 5
        
        # FAQ schema indicator
        if re.search(r'FAQ|Frequently Asked', self.body, re.IGNORECASE):
            score += 3
        
        # Entity clarity (defined terms)
        defined_terms = len(re.findall(r'\*\*[A-Z][^*]*?\*\*', self.body))
        if defined_terms >= 3:
            score += 2
        
        return {
            "ai_citation_readiness_score": min(15, score),
            "question_headings_count": question_headings,
            "citable_blocks": quoted_blocks + emphasis_blocks,
            "has_faq": bool(re.search(r'FAQ', self.body, re.IGNORECASE)),
            "defined_terms_count": defined_terms,
            "issues": issues,
        }
    
    def analyze_ai_content(self) -> Dict:
        """Detect AI-generated content patterns"""
        ai_detector = AIDetector(self.body)
        return ai_detector.get_ai_detection_score()
    
    def get_comprehensive_score(self) -> Dict:
        """Generate comprehensive blog analysis with all 5 categories + AI detection"""
        content_quality = self.analyze_content_quality()
        seo = self.analyze_seo()
        e_e_a_t = self.analyze_e_e_a_t()
        technical = self.analyze_technical_elements()
        ai_readiness = self.analyze_ai_citation_readiness()
        ai_content = self.analyze_ai_content()
        
        # Calculate total score (100 points)
        total_score = (
            content_quality["content_quality_score"] +
            seo["seo_score"] +
            e_e_a_t["e_e_a_t_score"] +
            technical["technical_score"] +
            ai_readiness["ai_citation_readiness_score"]
        )
        
        # Determine scoring band
        if total_score >= 90:
            band = "Exceptional"
        elif total_score >= 80:
            band = "Strong"
        elif total_score >= 70:
            band = "Acceptable"
        elif total_score >= 60:
            band = "Below Standard"
        else:
            band = "Rewrite Needed"
        
        # Collect all issues
        all_issues = []
        for analysis in [content_quality, seo, e_e_a_t, technical, ai_readiness]:
            all_issues.extend(analysis.get("issues", []))
        
        return {
            "file": str(self.filepath),
            "total_score": total_score,
            "scoring_band": band,
            "ready_to_publish": total_score >= 80 and ai_content["likelihood"].startswith("Likely Human"),
            "content_quality": content_quality,
            "seo": seo,
            "e_e_a_t": e_e_a_t,
            "technical": technical,
            "ai_citation_readiness": ai_readiness,
            "ai_content": ai_content,
            "all_issues": all_issues,
            "priority_issues": [i for i in all_issues if any(
                keyword in i.lower() for keyword in ["missing", "too", "recommend", "only", "error"]
            )],
        }
