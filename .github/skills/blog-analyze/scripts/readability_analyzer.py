"""
Readability Analysis Module
Calculates Flesch-Kincaid, sentiment, and readability metrics
"""

import re
from typing import Dict, Tuple


class ReadabilityAnalyzer:
    """Analyzes blog post readability across multiple dimensions"""
    
    def __init__(self, text: str):
        self.text = text
        self.words = text.split()
        self.word_count = len(self.words)
        self.sentences = self._extract_sentences()
        self.paragraphs = self._extract_paragraphs()
    
    def _extract_sentences(self) -> list:
        """Extract sentences from text"""
        sentences = re.split(r'[.!?]+', self.text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _extract_paragraphs(self) -> list:
        """Extract paragraphs from text"""
        paragraphs = self.text.split('\n\n')
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _count_syllables(self, word: str) -> int:
        """Estimate syllable count for a word"""
        word = word.lower()
        syllable_count = 0
        vowels = "aeiouy"
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        # Adjust for silent e
        if word.endswith('e'):
            syllable_count -= 1
        
        # Minimum of 1 syllable per word
        if syllable_count == 0:
            syllable_count = 1
        
        return syllable_count
    
    def flesch_reading_ease(self) -> float:
        """Calculate Flesch Reading Ease (0-100, higher = easier to read)"""
        if len(self.sentences) == 0 or self.word_count == 0:
            return 0
        
        syllables = sum(self._count_syllables(word) for word in self.words)
        
        score = (
            206.835
            - 1.015 * (self.word_count / len(self.sentences))
            - 84.6 * (syllables / self.word_count)
        )
        
        return max(0, min(100, score))
    
    def flesch_kincaid_grade(self) -> float:
        """Calculate Flesch-Kincaid Grade Level"""
        if len(self.sentences) == 0 or self.word_count == 0:
            return 0
        
        syllables = sum(self._count_syllables(word) for word in self.words)
        
        score = (
            0.39 * (self.word_count / len(self.sentences))
            + 11.8 * (syllables / self.word_count)
            - 15.59
        )
        
        return max(0, score)
    
    def average_sentence_length(self) -> float:
        """Calculate average words per sentence"""
        if len(self.sentences) == 0:
            return 0
        return self.word_count / len(self.sentences)
    
    def average_paragraph_length(self) -> float:
        """Calculate average words per paragraph"""
        if len(self.paragraphs) == 0:
            return 0
        
        para_word_counts = [len(p.split()) for p in self.paragraphs]
        return sum(para_word_counts) / len(self.paragraphs)
    
    def get_readability_score(self) -> Dict[str, float]:
        """Get comprehensive readability metrics"""
        return {
            "flesch_reading_ease": self.flesch_reading_ease(),
            "flesch_kincaid_grade": self.flesch_kincaid_grade(),
            "average_sentence_length": self.average_sentence_length(),
            "average_paragraph_length": self.average_paragraph_length(),
            "word_count": self.word_count,
            "sentence_count": len(self.sentences),
            "paragraph_count": len(self.paragraphs),
        }
