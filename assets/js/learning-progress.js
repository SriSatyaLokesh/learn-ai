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
    }
  };

  // Make available globally
  window.LearningProgress = LearningProgress;

  console.log('📊 LearningProgress module loaded');
})();
