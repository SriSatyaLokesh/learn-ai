// Learning Progress Tracker for Post Pages
// Automatically marks posts as complete when reader reaches the end
// Integrates with series navigation and progress page

(function() {
  'use strict';

  // Check if we're on a post page
  const isPostPage = document.body.classList.contains('post-template') || 
                     document.querySelector('article.post-content');
  
  if (!isPostPage) return;

  // Get post metadata from page
  const getPostMetadata = () => {
    // Try to get from Jekyll/Liquid variables first (if available)
    const pageData = window.pageData || {};
    
    return {
      slug: pageData.slug || window.location.pathname.split('/').filter(Boolean).pop(),
      category: pageData.category || window.location.pathname.split('/').filter(Boolean)[0],
      series: pageData.series || null,
      part: pageData.part || null,
      readingTime: pageData.readingTime || 5 // Default 5 minutes
    };
  };

  // Track scroll completion
  let hasReached80Percent = false;
  let hasReached100Percent = false;

  const trackScrollCompletion = () => {
    const article = document.querySelector('article.post-content') || document.querySelector('article');
    if (!article) return;

    const articleTop = article.offsetTop;
    const articleHeight = article.offsetHeight;
    const scrollPosition = window.scrollY + window.innerHeight;
    const articleBottom = articleTop + articleHeight;

    const scrollPercentage = ((scrollPosition - articleTop) / articleHeight) * 100;

    // Mark 80% completion (considered "read")
    if (scrollPercentage >= 80 && !hasReached80Percent) {
      hasReached80Percent = true;
      markPostAsComplete();
    }

    // Mark 100% completion (fully read)
    if (scrollPercentage >= 100 && !hasReached100Percent) {
      hasReached100Percent = true;
      showCompletionBadge();
    }
  };

  // Mark post as complete
  const markPostAsComplete = () => {
    const metadata = getPostMetadata();
    
    // Use LearningProgress from progress.html
    if (window.LearningProgress) {
      window.LearningProgress.completePost(metadata.slug, metadata.category, metadata.readingTime);
      
      // If part of series, mark series part as complete
      if (metadata.series && metadata.part) {
        window.LearningProgress.completeSeriesPart(metadata.series, metadata.part);
      }
      
      console.log('✅ Post marked as complete:', metadata.slug);
    }
  };

  // Show completion badge
  const showCompletionBadge = () => {
    // Check if badge already exists
    if (document.querySelector('.completion-badge')) return;

    const badge = document.createElement('div');
    badge.className = 'completion-badge';
    badge.style.cssText = `
      position: fixed;
      bottom: 2rem;
      right: 2rem;
      padding: 1rem 1.5rem;
      background: #ffffff;
      color: #dc2f02;
      border: 2px solid #dc2f02;
      border-radius: 1rem;
      box-shadow: 0 10px 25px rgba(220, 47, 2, 0.15);
      font-weight: 600;
      z-index: 1000;
      animation: slideInUp 0.5s ease-out;
      display: flex;
      align-items: center;
      gap: 0.75rem;
    `;
    badge.innerHTML = `
      <span style="font-size: 1.5rem;">🎉</span>
      <div>
        <div style="font-size: 0.875rem; opacity: 0.9;">Post Complete!</div>
        <div style="font-size: 0.75rem; opacity: 0.8;">Progress saved</div>
      </div>
    `;

    document.body.appendChild(badge);

    // Add animation
    const style = document.createElement('style');
    style.textContent = `
      @keyframes slideInUp {
        from {
          transform: translateY(100%);
          opacity: 0;
        }
        to {
          transform: translateY(0);
          opacity: 1;
        }
      }
    `;
    document.head.appendChild(style);

    // Remove badge after 5 seconds
    setTimeout(() => {
      badge.style.animation = 'slideInUp 0.5s ease-out reverse';
      setTimeout(() => badge.remove(), 500);
    }, 5000);
  };

  // Add completion button at end of post
  const addCompletionButton = () => {
    const article = document.querySelector('article.post-content') || document.querySelector('article');
    if (!article) return;

    const metadata = getPostMetadata();
    const isComplete = window.LearningProgress && window.LearningProgress.isPostComplete(metadata.slug);

    const buttonContainer = document.createElement('div');
    buttonContainer.style.cssText = `
      margin: 3rem 0;
      padding: 2rem;
      background: ${isComplete ? '#ffffff' : '#ffffff'};
      border: 2px solid #dc2f02;
      border-radius: 1rem;
      color: #000000;
      text-align: center;
    `;

    if (isComplete) {
      buttonContainer.innerHTML = `
        <div style="font-size: 3rem; margin-bottom: 1rem;">✅</div>
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1.5rem; color: #000000;">You've completed this post!</h3>
        <p style="margin: 0; color: #374151;">Check your <a href="{{ site.baseurl }}/progress/" style="color: #dc2f02; text-decoration: underline;">learning progress</a></p>
      `;
    } else {
      buttonContainer.innerHTML = `
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1.5rem; color: #000000;">Did you find this helpful?</h3>
        <p style="margin: 0 0 1rem 0; color: #374151;">Mark as complete to track your progress</p>
        <button onclick="window.markPostComplete()" style="padding: 0.75rem 2rem; background: #dc2f02; color: white; border: none; border-radius: 0.5rem; font-weight: 600; font-size: 1rem; cursor: pointer; transition: transform 0.2s;">
          Mark as Complete
        </button>
      `;
    }

    article.appendChild(buttonContainer);
  };

  // Make function globally available
  window.markPostComplete = () => {
    markPostAsComplete();
    hasReached100Percent = true;
    showCompletionBadge();
    
    // Replace button with completion message
    setTimeout(() => {
      const button = document.querySelector('button[onclick="window.markPostComplete()"]');
      if (button) {
        const container = button.closest('div');
        container.innerHTML = `
          <div style="font-size: 3rem; margin-bottom: 1rem;">✅</div>
          <h3 style="margin: 0 0 0.5rem 0; font-size: 1.5rem; color: #000000;">Marked as complete!</h3>
          <p style="margin: 0; color: #374151;">Check your <a href="{{ site.baseurl }}/progress/" style="color: #dc2f02; text-decoration: underline;">learning progress</a></p>
        `;
      }
    }, 100);
  };

  // Initialize
  const init = () => {
    // Add scroll tracking
    let scrollTimeout;
    window.addEventListener('scroll', () => {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(trackScrollCompletion, 100);
    });

    // Add completion button
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', addCompletionButton);
    } else {
      addCompletionButton();
    }

    // Initial check
    trackScrollCompletion();
  };

  init();
})();
