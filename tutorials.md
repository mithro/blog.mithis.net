---
layout: default
title: Tutorials
permalink: /tutorials/
---

# Tutorials

Technical tutorials and guides covering various programming languages, tools, and technologies.

<div class="tutorials-grid">
  {% for tutorial in site.tutorials %}
    <div class="tutorial-card">
      <h3><a href="{{ tutorial.url }}">{{ tutorial.title }}</a></h3>
      <p class="tutorial-description">{{ tutorial.description }}</p>
      
      <div class="tutorial-meta">
        <span class="tutorial-category">{{ tutorial.category | capitalize }}</span>
        {% if tutorial.difficulty %}
          <span class="tutorial-difficulty difficulty-{{ tutorial.difficulty }}">{{ tutorial.difficulty | capitalize }}</span>
        {% endif %}
        {% if tutorial.last_updated %}
          <span class="tutorial-updated">{{ tutorial.last_updated | date: "%Y" }}</span>
        {% endif %}
      </div>
      
      {% if tutorial.tags %}
        <div class="tutorial-tags">
          {% for tag in tutorial.tags limit: 3 %}
            <span class="tag">{{ tag }}</span>
          {% endfor %}
        </div>
      {% endif %}
    </div>
  {% endfor %}
</div>

<style>
.tutorials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.tutorial-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.tutorial-card h3 {
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.tutorial-card h3 a {
  color: #333;
  text-decoration: none;
}

.tutorial-card h3 a:hover {
  color: #28a745;
}

.tutorial-description {
  color: #666;
  margin-bottom: 1rem;
}

.tutorial-meta {
  margin-bottom: 1rem;
}

.tutorial-meta span {
  display: inline-block;
  margin-right: 0.5rem;
  padding: 0.25rem 0.5rem;
  background: #f0f0f0;
  border-radius: 3px;
  font-size: 0.8rem;
}

.difficulty-beginner {
  background: #d4edda !important;
  color: #155724 !important;
}

.difficulty-intermediate {
  background: #fff3cd !important;
  color: #856404 !important;
}

.difficulty-advanced {
  background: #f8d7da !important;
  color: #721c24 !important;
}

.tutorial-tags {
  margin-top: 1rem;
}

.tag {
  display: inline-block;
  background: #28a745;
  color: white;
  padding: 0.2rem 0.4rem;
  margin-right: 0.25rem;
  margin-bottom: 0.25rem;
  border-radius: 3px;
  font-size: 0.7rem;
}
</style>