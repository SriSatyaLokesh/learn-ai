# Local Development Setup

## URL Normalization

To ensure consistency between local development and production, always use the `--baseurl` flag when serving locally:

### ✅ Correct Local Commands

```bash
# Standard serve (normalized URLs)
bundle exec jekyll serve --baseurl /learn-with-satya

# With future posts and drafts  
bundle exec jekyll serve --drafts --future --baseurl /learn-with-satya

# Package.json scripts (already updated)
npm run serve  # Uses baseurl automatically
npm run dev    # Uses baseurl automatically
```

### 🌐 URL Structure

| Environment | URL Structure | Example |
|-------------|---------------|---------|
| **Local** | `localhost:4000/learn-with-satya/` | `http://localhost:4000/learn-with-satya/ai/transformer-architecture/` |
| **Production** | `srisatyalokesh.is-a.dev/learn-with-satya/` | `https://srisatyalokesh.is-a.dev/learn-with-satya/ai/transformer-architecture/` |

### 🔧 Configuration

The site is configured with:
- **baseurl**: `/learn-with-satya` (in `_config.yml`)  
- **url**: `https://srisatyalokesh.is-a.dev` (production domain)

### ❌ Common Issues

**Problem**: Links work locally but break on GitHub Pages  
**Cause**: Using localhost:4000/ instead of localhost:4000/learn-with-satya/  
**Solution**: Always include `--baseurl /learn-with-satya` flag when serving

**Problem**: Agents expect /learn-with-satya/ path locally  
**Cause**: Baseurl mismatch between environments  
**Solution**: Use normalized commands above for consistent behavior

### 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/SriSatyaLokesh/learn-with-satya.git
cd learn-with-satya
bundle install

# Serve with correct baseurl
bundle exec jekyll serve --future --baseurl /learn-with-satya

# Visit: http://localhost:4000/learn-with-satya/
```

This ensures your local development environment matches production exactly!