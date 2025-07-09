---
layout: default
title: Projects
permalink: /projects/
---

# Projects

This page showcases various open source projects I've worked on over the years, ranging from hardware designs to software frameworks.

<div class="projects-grid">
  {% for project in site.projects %}
    <div class="project-card">
      <h3><a href="{{ project.url }}">{{ project.title }}</a></h3>
      <p class="project-description">{{ project.description }}</p>
      
      <div class="project-meta">
        <span class="project-category">{{ project.category | capitalize }}</span>
        {% if project.status %}
          <span class="project-status status-{{ project.status }}">{{ project.status | capitalize }}</span>
        {% endif %}
      </div>
      
      {% if project.tags %}
        <div class="project-tags">
          {% for tag in project.tags limit: 3 %}
            <span class="tag">{{ tag }}</span>
          {% endfor %}
        </div>
      {% endif %}
    </div>
  {% endfor %}
</div>

<style>
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.project-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.project-card h3 {
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.project-card h3 a {
  color: #333;
  text-decoration: none;
}

.project-card h3 a:hover {
  color: #007bff;
}

.project-description {
  color: #666;
  margin-bottom: 1rem;
}

.project-meta {
  margin-bottom: 1rem;
}

.project-meta span {
  display: inline-block;
  margin-right: 0.5rem;
  padding: 0.25rem 0.5rem;
  background: #f0f0f0;
  border-radius: 3px;
  font-size: 0.8rem;
}

.status-active {
  background: #d4edda !important;
  color: #155724 !important;
}

.status-inactive {
  background: #f8d7da !important;
  color: #721c24 !important;
}

.status-completed {
  background: #cce5ff !important;
  color: #004085 !important;
}

.project-tags {
  margin-top: 1rem;
}

.tag {
  display: inline-block;
  background: #007bff;
  color: white;
  padding: 0.2rem 0.4rem;
  margin-right: 0.25rem;
  margin-bottom: 0.25rem;
  border-radius: 3px;
  font-size: 0.7rem;
}
</style>