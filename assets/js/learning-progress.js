// Learning Progress Manager
// Standalone module for tracking learning progress across the site
// Stores data in localStorage for persistence

(function() {
  'use strict';

  const LearningProgress = {
    STORAGE_KEY: 'learn-with-satya-progress',

    // Get all progress data
    getAll() {
      const data = localStorage.getItem(this.STORAGE_KEY);
      return data ? JSON.parse(data) : { posts: {}, series: {} };
    },

    // Mark post as complete
    completePost(postSlug, categorySlug, readingTimeMinutes = 5) {
      const progress = this.getAll();
      progress.posts[postSlug] = {
        completed: true,
        completedAt: new Date().toISOString(),
        readingTime: readingTimeMinutes,
        category: categorySlug
      };
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(progress));
      console.log('✅ Progress saved:', postSlug);
      
      // Trigger real-time UI updates
      this.updateProgressBarsRealtime();
      this.showCompletionNotification('Post marked as complete!');
      
      return progress;
    },

    // Check if post is complete
    isPostComplete(postSlug) {
      const progress = this.getAll();
      return progress.posts[postSlug]?.completed || false;
    },

    // Get series completion percentage
    getSeriesProgress(seriesId, totalParts) {
      const progress = this.getAll();
      const seriesData = progress.series[seriesId] || { completed: [] };
      const completedCount = seriesData.completed.length;
      return Math.round((completedCount / totalParts) * 100);
    },

    // Mark series part as complete
    completeSeriesPart(seriesId, partNumber) {
      const progress = this.getAll();
      if (!progress.series[seriesId]) {
        progress.series[seriesId] = { 
          completed: [], 
          lastAccessed: new Date().toISOString() 
        };
      }
      if (!progress.series[seriesId].completed.includes(partNumber)) {
        progress.series[seriesId].completed.push(partNumber);
        progress.series[seriesId].lastAccessed = new Date().toISOString();
      }
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(progress));
      
      // Trigger real-time UI updates
      this.updateProgressBarsRealtime();
      
      return progress;
    },

    // Reset all progress
    reset() {
      localStorage.removeItem(this.STORAGE_KEY);
      console.log('🗑️ All progress cleared');
    },

    // Get stats
    getStats() {
      const progress = this.getAll();
      const totalPosts = Object.keys(progress.posts).length;
      const totalTime = Object.values(progress.posts).reduce((sum, post) => sum + (post.readingTime || 5), 0);
      const seriesCompleted = Object.values(progress.series).filter(s => s.completed.length > 0).length;
      
      return {
        totalPosts,
        totalTime: Math.round(totalTime / 60), // Convert to hours
        seriesCompleted
      };
    },

    // Real-time DOM update methods
    updateProgressBarsRealtime() {
      // Update progress page stats if present
      this.updateProgressPageStats();
      
      // Update series progress bars
      this.updateSeriesProgressBars();
      
      // Fire custom event for other components
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
        // Series completed logic needs refinement - for now just update
        seriesElement.textContent = stats.seriesCompleted;
      }
      if (timeElement) {
        timeElement.textContent = stats.totalTime + 'h';
      }
    },

    updateSeriesProgressBars() {
      // Get all progress bars on the current page
      const progressBars = document.querySelectorAll('[data-progress-bar]');
      
      progressBars.forEach(bar => {
        const seriesId = bar.getAttribute('data-series-id');
        const totalParts = parseInt(bar.getAttribute('data-total-parts'));
        
        if (seriesId && totalParts) {
          const percentage = this.getSeriesProgress(seriesId, totalParts);
          this.animateProgressBar(bar, percentage);
          
          // Update accompanying text
          const textElement = bar.parentElement.querySelector('.progress-text');
          if (textElement) {
            const progress = this.getAll();
            const seriesData = progress.series[seriesId] || { completed: [] };
            const completedCount = seriesData.completed.length;
            textElement.textContent = `${completedCount} / ${totalParts} parts (${percentage}%)`;
          }
        }
      });
    },

    animateCountUp(element, from, to) {
      if (from === to) return;
      
      const duration = 800;
      const steps = 30;
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
      const currentWidth = parseFloat(progressBar.style.width) || 0;
      
      if (Math.abs(currentWidth - targetPercentage) < 1) return;
      
      // Add transition if not already present
      if (!progressBar.style.transition) {
        progressBar.style.transition = 'width 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
      }
      
      // Animate to new width
      progressBar.style.width = `${targetPercentage}%`;
      
      // Add a subtle scale effect for completion
      if (targetPercentage === 100 && currentWidth < 100) {
        progressBar.style.transform = 'scaleY(1.2)';
        setTimeout(() => {
          progressBar.style.transform = 'scaleY(1)';
        }, 200);
      }
    },

    showCompletionNotification(message = 'Progress updated!') {
      // Create success notification
      const notification = document.createElement('div');
      notification.className = 'progress-notification';
      notification.style.cssText = `
        position: fixed;
        top: 2rem;
        right: 2rem;
        padding: 1rem 1.5rem;
        background: #ffffff;
        color: #047857;
        border: 2px solid #059669;
        border-radius: 0.75rem;
        box-shadow: 0 10px 25px rgba(5, 150, 105, 0.15);
        font-weight: 600;
        z-index: 1000;
        animation: slideInDown 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        align-items: center;
        gap: 0.75rem;
        max-width: 320px;
      `;
      
      notification.innerHTML = `
        <span style="font-size: 1.25rem;">✅</span>
        <span>${message}</span>
      `;
      
      document.body.appendChild(notification);
      
      // Add slide animation
      const style = document.createElement('style');
      style.textContent = `
        @keyframes slideInDown {
          from {
            transform: translateY(-100%);
            opacity: 0;
          }
          to {
            transform: translateY(0);
            opacity: 1;
          }
        }
      `;
      document.head.appendChild(style);
      
      // Remove after 3 seconds
      setTimeout(() => {
        notification.style.animation = 'slideInDown 0.4s cubic-bezier(0.4, 0, 0.2, 1) reverse';
        setTimeout(() => {
          if (notification.parentElement) {
            notification.remove();
          }
        }, 400);
      }, 3000);
    }
  };

  // Make available globally
  window.LearningProgress = LearningProgress;

  console.log('📊 LearningProgress module loaded with real-time updates');
})();
