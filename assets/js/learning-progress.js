// Learning Progress Manager
// Standalone module for tracking learning progress across the site
// Stores data in localStorage for persistence

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

  const LearningProgress = {
    STORAGE_KEY: 'learn-with-satya-progress',

    normalizeSlug: normalizeSlug,

    // Get all progress data safely
    getAll() {
      try {
        const data = localStorage.getItem(this.STORAGE_KEY);
        const parsed = data ? JSON.parse(data) : { posts: {}, series: {} };
        if (!parsed.posts) parsed.posts = {};
        if (!parsed.series) parsed.series = {};
        return parsed;
      } catch (e) {
        console.error('Error reading learning progress localStorage:', e);
        return { posts: {}, series: {} };
      }
    },

    // Save progress object
    save(progress) {
      try {
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(progress));
      } catch (e) {
        console.error('Error saving learning progress localStorage:', e);
      }
    },

    // Mark post as complete
    completePost(postSlug, categorySlug = 'ai', readingTimeMinutes = 5) {
      const normSlug = normalizeSlug(postSlug);
      if (!normSlug) return;

      const progress = this.getAll();
      progress.posts[normSlug] = {
        completed: true,
        completedAt: new Date().toISOString(),
        readingTime: parseInt(readingTimeMinutes) || 5,
        category: categorySlug || 'ai',
        rawSlug: postSlug
      };

      this.save(progress);
      console.log('✅ Progress saved for post:', normSlug);

      // Trigger real-time UI updates
      this.updateProgressBarsRealtime();
      this.showCompletionNotification('Post marked as complete!');

      return progress;
    },

    // Toggle post completion
    togglePost(postSlug, categorySlug = 'ai', readingTimeMinutes = 5) {
      const normSlug = normalizeSlug(postSlug);
      if (!normSlug) return false;

      const progress = this.getAll();
      if (progress.posts[normSlug] && progress.posts[normSlug].completed) {
        delete progress.posts[normSlug];
        this.save(progress);
        this.updateProgressBarsRealtime();
        this.showCompletionNotification('Post marked as incomplete.');
        return false;
      } else {
        this.completePost(postSlug, categorySlug, readingTimeMinutes);
        return true;
      }
    },

    // Check if post is complete
    isPostComplete(postSlug) {
      const normSlug = normalizeSlug(postSlug);
      if (!normSlug) return false;

      const progress = this.getAll();
      // Check normalized key or raw key
      if (progress.posts[normSlug] && progress.posts[normSlug].completed) {
        return true;
      }
      return Object.keys(progress.posts).some(key => {
        return normalizeSlug(key) === normSlug && progress.posts[key].completed;
      });
    },

    // Get series completion percentage
    getSeriesProgress(seriesId, totalParts) {
      const progress = this.getAll();
      const seriesData = progress.series[seriesId] || { completed: [] };
      const completedCount = seriesData.completed ? seriesData.completed.length : 0;
      if (!totalParts || totalParts <= 0) return 0;
      return Math.round((completedCount / totalParts) * 100);
    },

    // Mark series part as complete
    completeSeriesPart(seriesId, partNumber) {
      if (!seriesId || !partNumber) return;

      const progress = this.getAll();
      if (!progress.series[seriesId]) {
        progress.series[seriesId] = {
          completed: [],
          lastAccessed: new Date().toISOString()
        };
      }

      const partNum = parseInt(partNumber);
      if (!progress.series[seriesId].completed.includes(partNum)) {
        progress.series[seriesId].completed.push(partNum);
        progress.series[seriesId].lastAccessed = new Date().toISOString();
      }

      this.save(progress);
      this.updateProgressBarsRealtime();

      return progress;
    },

    // Reset all progress
    reset() {
      try {
        localStorage.removeItem(this.STORAGE_KEY);
        console.log('🗑️ All progress cleared');
        this.updateProgressBarsRealtime();
      } catch (e) {
        console.error('Error clearing progress:', e);
      }
    },

    // Get overall progress stats
    getStats() {
      const progress = this.getAll();
      const completedPosts = Object.values(progress.posts || {}).filter(p => p && p.completed);
      const totalPosts = completedPosts.length;
      const totalTimeMinutes = completedPosts.reduce((sum, post) => sum + (parseInt(post.readingTime) || 5), 0);
      const seriesCompleted = Object.values(progress.series || {}).filter(s => s && s.completed && s.completed.length > 0).length;

      let totalTimeFormatted = `${totalTimeMinutes}m`;
      if (totalTimeMinutes >= 60) {
        const hours = (totalTimeMinutes / 60).toFixed(1);
        totalTimeFormatted = `${hours}h`;
      }

      return {
        totalPosts,
        totalTimeMinutes,
        totalTimeFormatted,
        totalTime: totalTimeMinutes >= 60 ? Math.round(totalTimeMinutes / 60) : totalTimeMinutes,
        seriesCompleted
      };
    },

    // Real-time DOM update methods
    updateProgressBarsRealtime() {
      this.updateProgressPageStats();
      this.updateSeriesProgressBars();

      window.dispatchEvent(new CustomEvent('learningProgressUpdated', {
        detail: { stats: this.getStats() }
      }));
    },

    updateProgressPageStats() {
      const stats = this.getStats();
      const totalElement = document.getElementById('total-completed');
      const seriesElement = document.getElementById('series-completed');
      const timeElement = document.getElementById('total-time');

      if (totalElement) {
        this.animateCountUp(totalElement, parseInt(totalElement.textContent) || 0, stats.totalPosts);
      }
      if (seriesElement) {
        seriesElement.textContent = stats.seriesCompleted;
      }
      if (timeElement) {
        timeElement.textContent = stats.totalTimeFormatted;
      }
    },

    updateSeriesProgressBars() {
      const progressBars = document.querySelectorAll('[data-progress-bar]');
      progressBars.forEach(bar => {
        const seriesId = bar.getAttribute('data-series-id');
        const totalParts = parseInt(bar.getAttribute('data-total-parts'));

        if (seriesId && totalParts) {
          const percentage = this.getSeriesProgress(seriesId, totalParts);
          this.animateProgressBar(bar, percentage);

          const textElement = bar.parentElement ? bar.parentElement.querySelector('.progress-text') : null;
          if (textElement) {
            const progress = this.getAll();
            const seriesData = progress.series[seriesId] || { completed: [] };
            const completedCount = seriesData.completed ? seriesData.completed.length : 0;
            textElement.textContent = `${completedCount} / ${totalParts} parts (${percentage}%)`;
          }
        }
      });
    },

    animateCountUp(element, from, to) {
      if (from === to) {
        element.textContent = to;
        return;
      }

      const duration = 600;
      const steps = 20;
      const increment = (to - from) / steps;
      let current = from;
      let step = 0;

      const timer = setInterval(() => {
        step++;
        current += increment;

        if (step >= steps) {
          current = to;
          clearInterval(timer);
        }

        element.textContent = Math.round(current);
      }, duration / steps);
    },

    animateProgressBar(progressBar, targetPercentage) {
      if (!progressBar) return;
      progressBar.style.transition = 'width 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
      progressBar.style.width = `${targetPercentage}%`;
    },

    showCompletionNotification(message = 'Progress updated!') {
      const existing = document.querySelector('.progress-notification');
      if (existing) existing.remove();

      const notification = document.createElement('div');
      notification.className = 'progress-notification';
      notification.style.cssText = `
        position: fixed;
        bottom: 2rem;
        left: 2rem;
        padding: 0.875rem 1.25rem;
        background: #111827;
        color: #ffffff;
        border: 1px solid #374151;
        border-radius: 0.75rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        font-weight: 600;
        font-size: 0.875rem;
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 0.6rem;
        max-width: 320px;
        transition: all 0.3s ease;
      `;

      notification.innerHTML = `
        <span style="font-size: 1.1rem;">✅</span>
        <span>${message}</span>
      `;

      document.body.appendChild(notification);

      setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateY(10px)';
        setTimeout(() => notification.remove(), 300);
      }, 2500);
    }
  };

  // Make available globally
  window.LearningProgress = LearningProgress;
  console.log('📊 LearningProgress module loaded');
})();
