---
layout: default
title: "Archives"
permalink: /archives/
---

<div class="hentry">
    <h2 class="page-title">Blog Archives</h2>
    
    <div class="entry-content">
        
        <h3>By Category</h3>
        <ul>
        {% assign sorted_categories = site.categories | sort %}
        {% for category in sorted_categories %}
            <li>
                <a href="/category/{{ category[0] | downcase | replace: ' ', '-' | replace: '.', '' }}/">
                    {{ category[0] }} ({{ category[1].size }})
                </a>
            </li>
        {% endfor %}
        </ul>
        
        <h3>By Year</h3>
        {% assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}
        {% for year in posts_by_year %}
        <details open>
            <summary><strong>{{ year.name }} ({{ year.items.size }} posts)</strong></summary>
            <ul style="margin-top: 10px;">
            {% for post in year.items %}
                <li style="margin-bottom: 5px;">
                    <span style="color: #888; font-size: 0.9em;">{{ post.date | date: "%b %d" }}</span> - 
                    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
                    {% if post.categories.size > 0 %}
                        <small style="color: #666;">in {{ post.categories | join: ", " }}</small>
                    {% endif %}
                </li>
            {% endfor %}
            </ul>
        </details>
        {% endfor %}
        
        <h3>All Posts (Chronological)</h3>
        <ul>
        {% for post in site.posts %}
            <li style="margin-bottom: 8px;">
                <span style="color: #888; font-size: 0.9em;">{{ post.date | date: "%Y-%m-%d" }}</span> - 
                <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
                {% if post.categories.size > 0 %}
                    <small style="color: #666;">in {{ post.categories | join: ", " }}</small>
                {% endif %}
            </li>
        {% endfor %}
        </ul>
        
        <div class="navigation">
            <div class="nav-previous">
                <a href="{{ '/' | relative_url }}">&laquo; Back to Home</a>
            </div>
        </div>
        
    </div>
</div>