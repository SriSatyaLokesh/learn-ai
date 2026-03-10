/**
 * Multi-Callout Highlighter
 * Finds and styles special callout blocks: [INFO-GAIN: ...], [STAT: ...], etc.
 */

(function() {
  'use strict';

  // Callout type configurations
  const CALLOUT_TYPES = {
    'INFO-GAIN': {
      className: 'info-gain-callout',
      icon: '💡',
      label: 'Key Insight:'
    },
    'STAT': {
      className: 'stat-callout',
      icon: '📊',
      label: 'Data Point:'
    }
  };

  function highlightCallouts() {
    // Find all paragraphs in post content
    const postContent = document.querySelector('.post-content');
    if (!postContent) return;

    const paragraphs = postContent.querySelectorAll('p');
    
    paragraphs.forEach(function(p) {
      const text = p.textContent.trim();
      
      // Check each callout type
      Object.keys(CALLOUT_TYPES).forEach(function(type) {
        const prefix = '[' + type + ':';
        
        if (text.startsWith(prefix)) {
          const config = CALLOUT_TYPES[type];
          
          // Add custom class for styling
          p.classList.add(config.className);
          
          // Extract the content after [TYPE:
          const content = text.replace(new RegExp('^\\[' + type + ':\\s*'), '').replace(/\]$/, '');
          
          // Add icon and reformat content
          p.innerHTML = '<span class="callout-icon">' + config.icon + '</span>' +
                       '<span class="callout-label">' + config.label + '</span> ' +
                       '<span class="callout-text">' + content + '</span>';
        }
      });
    });
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', highlightCallouts);
  } else {
    highlightCallouts();
  }
})();
