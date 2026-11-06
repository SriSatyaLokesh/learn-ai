import os
import re
import pytest

POST_PATH = os.path.join("_posts", "ai", "2026-11-06-indic-multilingual-prompting-guide.md")

def get_post_content():
    assert os.path.exists(POST_PATH), f"Blog post does not exist at {POST_PATH}"
    with open(POST_PATH, "r", encoding="utf-8") as f:
        return f.read()

def test_task1_frontmatter_and_tldr():
    content = get_post_content()
    lines = content.splitlines()
    assert lines[0].strip() == "---", "Post must begin with front matter delimiter '---'"
    assert lines[1].strip() == "layout: post", "Line 2 must be 'layout: post'"
    
    # Check category
    assert "category: ai" in content, "Front matter must specify 'category: ai'"
    
    # Check description length 140-160
    desc_match = re.search(r'description:\s*"([^"]+)"', content)
    assert desc_match, "Description not found in front matter"
    desc = desc_match.group(1)
    assert 140 <= len(desc) <= 160, f"Description length is {len(desc)}, must be between 140 and 160 chars"
    
    # Check image is at root level
    assert re.search(r'\nimage:\s*(https?://|/assets/)', content), "image must be root level and valid"
    assert "  image:" not in content[:content.find("---", 3)], "image must not be indented under header"
    
    # Check canonical_url
    assert "https://srisatyalokesh.is-a.dev/learn-ai/indic-multilingual-prompting-guide/" in content
    
    # Check TL;DR
    assert "> **TL;DR:**" in content, "TL;DR box missing"

def test_task2_voice_mode_hindi_tamil():
    content = get_post_content()
    assert "## Can You Design Distributed Systems Using Spoken Indic Voice Mode?" in content
    assert "Voice Prompt (Hindi / Spoken):" in content
    assert "Voice Prompt (Tamil / Spoken):" in content
    assert "<!-- [ORIGINAL DATA] -->" in content or "<!-- [PERSONAL EXPERIENCE] -->" in content or "<!-- [UNIQUE INSIGHT] -->" in content
    # Citation capsule check
    assert "According to" in content and "latency" in content.lower()

def test_task3_codemixed_tenglish_tanglish():
    content = get_post_content()
    assert "## How Does Code-Mixed Typing (Tenglish & Tanglish) Accelerate Everyday Coding?" in content
    assert "Prompt (Tenglish):" in content
    assert "Prompt (Tanglish):" in content
    assert "FastAPI" in content
    assert "React" in content
    assert "Tokenizer" in content or "token" in content.lower()
    # Check citation capsule
    assert "According to" in content and "token" in content.lower()

def test_task4_native_script_telugu_kannada():
    content = get_post_content()
    assert "## Can Agents Debug Complex Stack Traces from Native Indic Script Prompts?" in content
    assert "Telugu Script" in content
    assert "Kannada Script" in content
    
    # Check for Telugu script characters (Unicode \u0c00-\u0c7f)
    telugu_chars = re.search(r'[\u0c00-\u0c7f]+', content)
    assert telugu_chars, "Native Telugu script text missing"
    
    # Check for Kannada script characters (Unicode \u0c80-\u0cff)
    kannada_chars = re.search(r'[\u0c80-\u0cff]+', content)
    assert kannada_chars, "Native Kannada script text missing"
    
    # Check for stack trace / debugging block
    assert "Traceback" in content or "Error:" in content or "Exception" in content
    # Citation capsule check
    assert "According to" in content and "debugging" in content.lower()

def test_task5_zero_translation_and_faq():
    content = get_post_content()
    assert "AI4Bharat" in content, "AI4Bharat benchmark citation missing"
    assert "## Frequently Asked Questions" in content or "## FAQ" in content
    words = content.split()
    assert len(words) >= 2200, f"Post has {len(words)} words; required >= 2200"

def test_no_internal_link_placeholders():
    content = get_post_content()
    assert "INTERNAL-LINK" not in content, "Unresolved INTERNAL-LINK placeholders found"

def test_dual_modality_coverage():
    content = get_post_content()
    # Check all 4 scripts
    assert re.search(r'[\u0900-\u097f]+', content), "Devanagari (Hindi) script text missing"
    assert re.search(r'[\u0b80-\u0bff]+', content), "Tamil script text missing"
    assert re.search(r'[\u0c00-\u0c7f]+', content), "Telugu script text missing"
    assert re.search(r'[\u0c80-\u0cff]+', content), "Kannada script text missing"
    
    # Check all 4 transliterations / code-mix terms
    assert "Hinglish" in content
    assert "Tanglish" in content
    assert "Tenglish" in content
    assert "Kanglish" in content

def test_image_asset_validity():
    content = get_post_content()
    img_match = re.search(r'\nimage:\s*(.+)', content)
    assert img_match, "image not found in front matter"
    img_val = img_match.group(1).strip().strip('"').strip("'")
    if img_val.startswith("http://") or img_val.startswith("https://"):
        assert True
    else:
        # Local asset must exist on disk
        clean_path = img_val.lstrip("/")
        assert os.path.exists(clean_path), f"Local image asset does not exist: {clean_path}"

