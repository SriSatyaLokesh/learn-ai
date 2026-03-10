---
layout: page
title: "Copilot CLI Learning Series Index"
description: "Master GitHub Copilot CLI with this complete, hands-on learning series. Track your progress, jump to any part, and access all posts in order."
permalink: /series/copilot-cli-learning/
category: tools
series_id: copilot-cli-learning
---

# Copilot CLI Learning Series: Mastering GitHub Copilot CLI

Welcome to the complete Copilot CLI Learning Series! This series will take you from installation and getting started, through advanced usage, troubleshooting, and a real-world project build. Use the index below to track your progress and jump to any part.

## Series Progress

{% assign series = site.data.series | where: "id", "copilot-cli-learning" | first %}
{% assign posts = series.posts %}
{% assign total = series.total_parts %}

<ol class="series-index" style="counter-reset: part;">
{% for post in posts %}
  {% assign post_obj = site.posts | where: "slug", post.slug | first %}
  <li style="margin-bottom: 1.5rem;">
    <div style="display: flex; align-items: center; gap: 1rem;">
      <span style="font-weight: bold; font-size: 1.25rem; color: #dc2f02; min-width: 2.5rem;">Part {{ post.part }}</span>
      <a href="{{ post_obj.url }}" style="font-size: 1.1rem; font-weight: 600;">{{ post.title }}</a>
      {% if post_obj and post_obj.draft %}
        <span style="color: #aaa; font-size: 0.9rem; margin-left: 0.5rem;">(Coming soon)</span>
      {% endif %}
    </div>
    {% if post_obj and post_obj.excerpt %}
      <div style="margin-left: 3.5rem; color: #444; font-size: 0.98rem;">{{ post_obj.excerpt }}</div>
    {% endif %}
  </li>
{% endfor %}
</ol>

---

- **Progress:** Each part is marked as complete when you finish reading (tracked by the LMS progress tracker).
- **Accessibility:** All links and progress indicators are keyboard and screen reader accessible.
- **SEO:** This page is indexable, uses semantic headings, and links to all series posts in order.

*Ready to start? [Jump to Part 1: Introduction to Copilot CLI]({{ site.baseurl }}/tools/introduction-to-copilot-cli/)*
