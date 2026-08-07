// Learning Progress Tracker for Post Pages
// Automatically tracks post completion via scroll & interactive completion callout
// Integrates with learning progress module and dashboard

(function() {
  'use strict';

  function normalizeSlug(str) {
    if (!str) return '';
    return String(str)
      .toLowerCase()
      .trim()
      .replace(/^(https?:\/\/[^\/]+)?\/?(learn-ai\/)?/, '')
      .replace(/\/$/, '')
      .replace(/^\d{4}-\d{2}-\d{2}-/, '');
  }

  const getProgressUrl = () => {
    const base = (window.pageData && window.pageData.baseUrl) ? window.pageData.baseUrl : '/learn-ai';
    return base.replace(/\/$/, '') + '/progress/';
  };

  // Check if we are on a blog post page
  const isPostPage = () => {
    return (window.pageData && window.pageData.slug) ||
           document.body.classList.contains('post-template') || 
           document.querySelector('article.post-content') !== null ||
           document.querySelector('section.post') !== null;
  };

  // Extract post metadata
  const getPostMetadata = () => {
    const pageData = window.pageData || {};
    let rawSlug = pageData.slug;
    
    if (!rawSlug) {
      const pathParts = window.location.pathname.split('/').filter(Boolean);
      rawSlug = pathParts.pop() || '';
    }

    return {
      rawSlug: rawSlug,
      normSlug: normalizeSlug(rawSlug),
      category: pageData.category || 'ai',
      series: pageData.series || null,
      part: pageData.part || null,
      readingTime: pageData.readingTime || 5
    };
  };

  let hasReached80Percent = false;

  // Track scroll depth
  const trackScrollCompletion = () => {
    if (!isPostPage()) return;

    const article = document.querySelector('article.post-content') || document.querySelector('article');
    if (!article) return;

    const articleTop = article.offsetTop;
    const articleHeight = article.offsetHeight;
    const scrollPosition = window.scrollY + window.innerHeight;

    const scrollPercentage = ((scrollPosition - articleTop) / articleHeight) * 100;

    // Auto mark complete when reader reaches 80% scroll
    if (scrollPercentage >= 80 && !hasReached80Percent) {
      hasReached80Percent = true;
      markPostAsComplete(false); // record completion without noisy popups
    }
  };

  // Mark post as complete in localStorage
  const markPostAsComplete = (showNotice = true) => {
    const meta = getPostMetadata();
    if (!meta.normSlug) return;

    if (window.LearningProgress) {
      window.LearningProgress.completePost(meta.normSlug, meta.category, meta.readingTime);

      if (meta.series && meta.part) {
        window.LearningProgress.completeSeriesPart(meta.series, meta.part);
      }
      
      updateCompletionUI(true);
    }
  };

  // Toggle post complete status
  const togglePostComplete = () => {
    const meta = getPostMetadata();
    if (!meta.normSlug || !window.LearningProgress) return;

    const isComplete = window.LearningProgress.isPostComplete(meta.normSlug);
    if (isComplete) {
      window.LearningProgress.togglePost(meta.normSlug, meta.category, meta.readingTime);
      updateCompletionUI(false);
    } else {
      window.LearningProgress.completePost(meta.normSlug, meta.category, meta.readingTime);
      if (meta.series && meta.part) {
        window.LearningProgress.completeSeriesPart(meta.series, meta.part);
      }
      updateCompletionUI(true);
    }
  };

  // Update Callout Box UI
  const updateCompletionUI = (isComplete) => {
    const container = document.getElementById('post-completion-callout');
    if (!container) return;

    const progressUrl = getProgressUrl();

    if (isComplete) {
      container.style.borderColor = '#059669';
      container.style.background = '#f0fdf4';
      container.innerHTML = `
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎉</div>
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1.25rem; color: #065f46; font-weight: 700;">You've completed this post!</h3>
        <p style="margin: 0 0 1rem 0; color: #047857; font-size: 0.875rem;">Your reading progress has been saved locally.</p>
        <div style="display: flex; gap: 0.75rem; justify-content: center; flex-wrap: wrap;">
          <a href="${progressUrl}" style="padding: 0.5rem 1.25rem; background: #059669; color: white; text-decoration: none; border-radius: 0.5rem; font-weight: 600; font-size: 0.875rem;">
            View Learning Dashboard
          </a>
          <button onclick="window.togglePostComplete()" style="padding: 0.5rem 1rem; background: transparent; color: #047857; border: 1px solid #059669; border-radius: 0.5rem; font-weight: 600; font-size: 0.875rem; cursor: pointer;">
            Mark as Unread
          </button>
        </div>
      `;
    } else {
      container.style.borderColor = '#dc2f02';
      container.style.background = '#ffffff';
      container.innerHTML = `
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1.25rem; color: #111827; font-weight: 700;">Completed reading this article?</h3>
        <p style="margin: 0 0 1rem 0; color: #4b5563; font-size: 0.875rem;">Mark it as complete to track your progress on your dashboard.</p>
        <button onclick="window.togglePostComplete()" style="padding: 0.65rem 1.75rem; background: #dc2f02; color: white; border: none; border-radius: 0.5rem; font-weight: 600; font-size: 0.95rem; cursor: pointer; transition: transform 0.15s ease;">
          Mark as Complete
        </button>
      `;
    }
  };

  // Add completion callout box to bottom of article
  const injectCompletionCallout = () => {
    if (!isPostPage()) return;
    if (document.getElementById('post-completion-callout')) return;

    const article = document.querySelector('article.post-content') || document.querySelector('article');
    if (!article) return;

    const meta = getPostMetadata();
    const isComplete = window.LearningProgress ? window.LearningProgress.isPostComplete(meta.normSlug) : false;

    const callout = document.createElement('div');
    callout.id = 'post-completion-callout';
    callout.style.cssText = `
      margin: 3rem 0;
      padding: 1.75rem;
      border: 2px solid ${isComplete ? '#059669' : '#dc2f02'};
      border-radius: 1rem;
      background: ${isComplete ? '#f0fdf4' : '#ffffff'};
      text-align: center;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
      transition: all 0.3s ease;
    `;

    article.appendChild(callout);
    updateCompletionUI(isComplete);
  };

  // Expose global methods
  window.markPostComplete = () => markPostAsComplete(true);
  window.togglePostComplete = togglePostComplete;

  // Initialize event listeners
  const init = () => {
    if (!isPostPage()) return;

    let scrollTimeout;
    window.addEventListener('scroll', () => {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(trackScrollCompletion, 150);
    });

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', injectCompletionCallout);
    } else {
      injectCompletionCallout();
    }
  };

  init();
})();
