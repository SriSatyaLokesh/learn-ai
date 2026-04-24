"""
AI Content Detection Module
Detects patterns commonly associated with AI-generated content
"""

import re
from typing import Dict, List, Tuple


class AIDetector:
    """Detects AI-generated content patterns"""
    
    # AI writing pattern signatures
    AI_PHRASES = [
        r"\bIn this\s+(?:article|guide|post)\b",
        r"\bLet's\s+(?:dive|explore|discover)\b",
        r"\bat the end of the day\b",
        r"\bIn conclusion\b",
        r"\bTo summarize\b",
        r"\bAll in all\b",
        r"\bit's important to note that\b",
        r"\bas\s+(?:I|we)\s+mentioned\b",
        r"\bthe key takeaway\b",
        r"\bwithout further ado\b",
        r"\bby and large\b",
        r"\bIt is worth noting\b",
        r"\bone could argue\b",
        r"\bIt goes without saying\b",
    ]
    
    # Emoji patterns (often over-used in AI content)
    EXCESSIVE_EMOJIS = [
        "🚀", "✅", "📊", "🎯", "💡", "🔥", "⚡", "📈"
    ]
    
    # Transition overuse patterns
    TRANSITION_PHRASES = [
        "furthermore", "moreover", "in addition", "additionally",
        "therefore", "thus", "hence", "consequently"
    ]
    
    def __init__(self, text: str):
        self.text = text
        self.lower_text = text.lower()
    
    def detect_ai_phrases(self) -> Tuple[int, List[str]]:
        """Detect common AI writing phrase patterns"""
        matches = []
        for pattern in self.AI_PHRASES:
            found = re.findall(pattern, self.lower_text, re.IGNORECASE)
            if found:
                matches.extend(found)
        
        return len(matches), matches
    
    def detect_excessive_emojis(self) -> Tuple[int, List[str]]:
        """Detect excessive emoji usage (AI-written content often overuses emojis)"""
        emojis = []
        for emoji in self.EXCESSIVE_EMOJIS:
            count = self.text.count(emoji)
            for _ in range(count):
                emojis.append(emoji)
        
        return len(emojis), emojis
    
    def detect_transition_overuse(self) -> Tuple[int, List[str]]:
        """Detect overused transition phrases"""
        matches = []
        for phrase in self.TRANSITION_PHRASES:
            pattern = rf"\b{phrase}\b"
            found = re.findall(pattern, self.lower_text, re.IGNORECASE)
            matches.extend(found)
        
        return len(matches), matches
    
    def detect_list_overuse(self) -> Tuple[int, int]:
        """Detect excessive list usage (AI often defaults to lists)"""
        bullet_count = len(re.findall(r"^[-*+]\s", self.text, re.MULTILINE))
        numbered_count = len(re.findall(r"^\d+\.\s", self.text, re.MULTILINE))
        
        return bullet_count + numbered_count, bullet_count + numbered_count
    
    def get_vocabulary_diversity(self) -> float:
        """Calculate vocabulary diversity (lower = more repetitive, often AI)"""
        words = re.findall(r"\b\w+\b", self.lower_text)
        if not words:
            return 0
        
        unique_words = len(set(words))
        total_words = len(words)
        
        return unique_words / total_words if total_words > 0 else 0
    
    def get_ai_detection_score(self) -> Dict:
        """Get comprehensive AI detection metrics (0-100, higher = more AI-like)"""
        ai_phrases_count, _ = self.detect_ai_phrases()
        emoji_count, _ = self.detect_excessive_emojis()
        transition_count, _ = self.detect_transition_overuse()
        list_count, _ = self.detect_list_overuse()
        vocab_diversity = self.get_vocabulary_diversity()
        
        # Calculate AI likelihood score
        ai_score = 0
        
        # AI phrases: +10 per occurrence (max 20)
        ai_score += min(20, ai_phrases_count * 10)
        
        # Excessive emojis: +20 if more than 5
        if emoji_count > 5:
            ai_score += 20
        elif emoji_count > 0:
            ai_score += emoji_count * 3
        
        # Transition overuse: +15 if more than 8
        if transition_count > 8:
            ai_score += 15
        elif transition_count > 4:
            ai_score += 10
        
        # List overuse: +10 if more than 5 lists
        if list_count > 5:
            ai_score += 10
        
        # Low vocabulary diversity: +25 if < 0.4
        if vocab_diversity < 0.4:
            ai_score += 25
        elif vocab_diversity < 0.5:
            ai_score += 15
        
        ai_score = min(100, ai_score)
        
        # Determine likelihood classification
        if ai_score < 20:
            likelihood = "Likely Human-written"
        elif ai_score < 40:
            likelihood = "Probably Human-written"
        elif ai_score < 60:
            likelihood = "Potentially AI-assisted"
        elif ai_score < 80:
            likelihood = "Likely AI-generated"
        else:
            likelihood = "Almost Certainly AI-generated"
        
        return {
            "ai_score": ai_score,
            "likelihood": likelihood,
            "ai_phrases_count": ai_phrases_count,
            "emoji_count": emoji_count,
            "transition_overuse_count": transition_count,
            "list_overuse_count": list_count,
            "vocabulary_diversity": vocab_diversity,
        }
