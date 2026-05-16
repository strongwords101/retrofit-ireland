'use strict';

/* ============================================================
   RetrofitList.ie — Main JavaScript
   ============================================================ */

let allProviders = [];
let allArticles  = [];

// ---- Utilities -------------------------------------------------------

function formatDate(str) {
  const d = new Date(str + 'T00:00:00');
  return d.toLocaleDateString('en-IE', { year: 'numeric', month: 'long', day: 'numeric' });
}

function getCatClass(cat) {
  const map = {
    'SEAI Grants':            'cat-seai',
    'Local Authority Grants': 'cat-local',
    'How-To Guides':          'cat-howto',
    'Planning & Regulations': 'cat-planning',
    'Market News':            'cat-market',
  };
  return map[cat] || 'cat-default';
}

function esc(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function getParam(name) {
  return new URLSearchParams(window.location.search).get(name) || '';
}

// ---- Inline SVG icons ------------------------------------------------

const icon = {
  phone:    `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81 19.79 19.79 0 012 1.18 2 2 0 014 .82h3a2 2 0 012 1.72c.13.96.36 1.9.7 2.81a2 2 0 01-.45 2.11L8.09 8.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0122 16z"/></svg>`,
  email:    `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>`,
  globe:    `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/></svg>`,
  search:   `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>`,
  arrow:    `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>`,
  back:     `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>`,
  mapPin:   `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>`,
  calendar: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>`,
  user:     `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`,
};

// ---- Article body renderer -------------------------------------------
// Supports rich content blocks alongside plain strings (backward compat).

// Renders text with [label](https://url) markdown links — https only, no XSS.
function renderText(text) {
  const parts = [];
  let last = 0;
  const re = /\[([^\]]+)\]\((https:\/\/[^\s)]+)\)/g;
  let m;
  while ((m = re.exec(text)) !== null) {
    parts.push(esc(text.slice(last, m.index)));
    parts.push(`<a href="${esc(m[2])}" target="_blank" rel="noopener noreferrer">${esc(m[1])}</a>`);
    last = m.index + m[0].length;
  }
  parts.push(esc(text.slice(last)));
  return parts.join('');
}

function renderBody(body) {
  if (!Array.isArray(body)) return `<p>${esc(String(body))}</p>`;
  return body.map(block => {
    if (typeof block === 'string') return `<p>${renderText(block)}</p>`;
    const { type } = block;
    if (type === 'h2') return `<h2 class="article-h2">${esc(block.text)}</h2>`;
    if (type === 'h3') return `<h3 class="article-h3">${esc(block.text)}</h3>`;
    if (type === 'p')  return `<p>${renderText(block.text)}</p>`;
    if (type === 'ul') return `<ul class="article-list">${block.items.map(i => `<li>${renderText(i)}</li>`).join('')}</ul>`;
    if (type === 'ol') return `<ol class="article-list article-list--ol">${block.items.map(i => `<li>${renderText(i)}</li>`).join('')}</ol>`;
    if (type === 'callout') return `<div class="article-callout">${renderText(block.text)}</div>`;
    if (type === 'cta') return `<div class="article-cta"><a href="${esc(block.href)}" class="btn btn-primary">${esc(block.text)}</a></div>`;
    if (type === 'table') {
      const headers = block.headers.map(h => `<th>${esc(h)}</th>`).join('');
      const rows    = block.rows.map(r => `<tr>${r.map(c => `<td>${renderText(c)}</td>`).join('')}</tr>`).join('');
      return `<div class="article-table-wrap"><table class="article-table"><thead><tr>${headers}</tr></thead><tbody>${rows}</tbody></table></div>`;
    }
    if (type === 'sources') {
      const items = block.items.map(s =>
        `<li><a href="${esc(s.href)}" target="_blank" rel="noopener noreferrer">${esc(s.text)}</a></li>`
      ).join('');
      return `<div class="article-sources"><h4>Official Sources &amp; Further Reading</h4><ul>${items}</ul></div>`;
    }
    return '';
  }).join('\n');
}

// ---- Card renderers --------------------------------------------------

function renderProviderCard(p) {
  const cats    = p.categories.map(c => `<span class="category-tag">${esc(c)}</span>`).join('');
  const website = p.website
    ? `<a href="${esc(p.website)}" class="contact-link" target="_blank" rel="noopener noreferrer">${icon.globe} ${esc(p.website.replace(/^https?:\/\//, ''))}</a>`
    : '';

  return `
    <article class="provider-card fade-in-up">
      <div class="provider-card-header">
        <h3 class="provider-card-name">${esc(p.name)}</h3>
        <span class="county-badge">${icon.mapPin} ${esc(p.county)}</span>
      </div>
      <div class="provider-categories">${cats}</div>
      <p class="provider-description">${esc(p.description)}</p>
      <div class="provider-contacts">
        <a href="tel:${esc(p.phone.replace(/\s/g, ''))}" class="contact-link">${icon.phone} ${esc(p.phone)}</a>
        <a href="mailto:${esc(p.email)}" class="contact-link">${icon.email} ${esc(p.email)}</a>
        ${website}
      </div>
    </article>`;
}

function renderArticleCard(a) {
  const catClass = getCatClass(a.category);
  return `
    <article class="article-card fade-in-up">
      <div class="article-card-body">
        <div class="article-meta">
          <span class="category-pill ${catClass}">${esc(a.category)}</span>
          <span class="article-date">${formatDate(a.date)}</span>
        </div>
        <h3 class="article-card-title">${esc(a.title)}</h3>
        <p class="article-card-summary">${esc(a.summary)}</p>
      </div>
      <div class="article-card-footer">
        <span class="article-author">${esc(a.author)}</span>
        <a href="article.html?id=${a.id}" class="read-more">Read more ${icon.arrow}</a>
      </div>
    </article>`;
}

// ---- Data loading ----------------------------------------------------

async function loadData() {
  try {
    const [pRes, aRes] = await Promise.all([
      fetch('data/providers.json'),
      fetch('data/articles.json'),
    ]);
    if (!pRes.ok || !aRes.ok) throw new Error('Network response not ok');
    allProviders = await pRes.json();
    allArticles  = await aRes.json();
  } catch (err) {
    console.error('RetrofitList: could not load data —', err.message);
    document.querySelectorAll('[data-loading]').forEach(el => {
      el.innerHTML = `
        <div class="empty-state" style="grid-column:1/-1">
          <div class="empty-state-icon">⚠️</div>
          <h3>Could not load data</h3>
          <p>Please open this site via a local server (e.g. VS Code Live Server) or deploy it to GitHub Pages. Browsers block fetch() from file:// URLs.</p>
        </div>`;
    });
  }
}

// ---- Page: Homepage --------------------------------------------------

function initHome() {
  const searchInput = document.getElementById('hero-search-input');
  const searchBtn   = document.getElementById('hero-search-btn');

  if (searchBtn) {
    searchBtn.addEventListener('click', () => {
      const term = searchInput?.value.trim() || '';
      window.location.href = term
        ? `directory.html?search=${encodeURIComponent(term)}`
        : 'directory.html';
    });
  }

  if (searchInput) {
    searchInput.addEventListener('keydown', e => {
      if (e.key === 'Enter') searchBtn?.click();
    });
  }

  // Featured providers
  const featuredEl = document.getElementById('featured-providers');
  if (featuredEl) {
    const featured = allProviders.filter(p => p.featured).slice(0, 3);
    const shown    = featured.length ? featured : allProviders.slice(0, 3);
    featuredEl.innerHTML = shown.map(renderProviderCard).join('');
  }

  // Latest news (newest 3)
  const newsEl = document.getElementById('latest-news');
  if (newsEl) {
    const sorted = [...allArticles].sort((a, b) => new Date(b.date) - new Date(a.date));
    newsEl.innerHTML = sorted.slice(0, 3).map(renderArticleCard).join('');
  }
}

// ---- Page: Directory -------------------------------------------------

function initDirectory() {
  const grid           = document.getElementById('providers-grid');
  const searchInput    = document.getElementById('dir-search');
  const countySelect   = document.getElementById('dir-county');
  const categorySelect = document.getElementById('dir-category');
  const countEl        = document.getElementById('provider-count');
  const clearBtn       = document.getElementById('filter-clear');

  if (!grid) return;

  // Populate county dropdown
  if (countySelect) {
    const counties = [...new Set(allProviders.map(p => p.county))].sort();
    counties.forEach(c => {
      const opt = document.createElement('option');
      opt.value = c; opt.textContent = c;
      countySelect.appendChild(opt);
    });
  }

  // Populate category dropdown
  if (categorySelect) {
    const cats = [...new Set(allProviders.flatMap(p => p.categories))].sort();
    cats.forEach(c => {
      const opt = document.createElement('option');
      opt.value = c; opt.textContent = c;
      categorySelect.appendChild(opt);
    });
  }

  // Pre-fill from URL params (supports links from homepage search)
  if (searchInput    && getParam('search'))   searchInput.value    = getParam('search');
  if (countySelect   && getParam('county'))   countySelect.value   = getParam('county');
  if (categorySelect && getParam('category')) categorySelect.value = getParam('category');

  function applyFilters() {
    const search   = searchInput?.value.toLowerCase().trim() || '';
    const county   = countySelect?.value   || '';
    const category = categorySelect?.value || '';
    const hasFilter = search || county || category;

    clearBtn?.classList.toggle('visible', !!hasFilter);

    const filtered = allProviders.filter(p => {
      const matchSearch = !search ||
        p.name.toLowerCase().includes(search) ||
        p.description.toLowerCase().includes(search) ||
        p.county.toLowerCase().includes(search) ||
        p.categories.some(c => c.toLowerCase().includes(search));

      const matchCounty   = !county   || p.county === county;
      const matchCategory = !category || p.categories.includes(category);

      return matchSearch && matchCounty && matchCategory;
    });

    if (countEl) {
      countEl.textContent = `${filtered.length} provider${filtered.length !== 1 ? 's' : ''} found`;
    }

    if (filtered.length === 0) {
      grid.innerHTML = `
        <div class="empty-state" style="grid-column:1/-1">
          <div class="empty-state-icon">🔍</div>
          <h3>No providers found</h3>
          <p>Try adjusting your filters or search term to find what you're looking for.</p>
        </div>`;
    } else {
      grid.innerHTML = filtered.map(renderProviderCard).join('');
    }
  }

  searchInput?.addEventListener('input',    applyFilters);
  countySelect?.addEventListener('change',  applyFilters);
  categorySelect?.addEventListener('change', applyFilters);

  clearBtn?.addEventListener('click', () => {
    if (searchInput)    searchInput.value    = '';
    if (countySelect)   countySelect.value   = '';
    if (categorySelect) categorySelect.value = '';
    applyFilters();
  });

  applyFilters();
}

// ---- Page: News ------------------------------------------------------

function initNews() {
  const grid       = document.getElementById('articles-grid');
  const filterBtns = document.querySelectorAll('.cat-filter-btn');
  if (!grid) return;

  let activeCategory = getParam('category') || '';

  function updateBtns() {
    filterBtns.forEach(btn => {
      btn.classList.toggle('active', btn.dataset.category === activeCategory);
    });
  }

  function renderFiltered() {
    const list = activeCategory
      ? allArticles.filter(a => a.category === activeCategory)
      : allArticles;

    const sorted = [...list].sort((a, b) => new Date(b.date) - new Date(a.date));

    grid.innerHTML = sorted.length
      ? sorted.map(renderArticleCard).join('')
      : `<div class="empty-state" style="grid-column:1/-1">
           <div class="empty-state-icon">📰</div>
           <h3>No articles in this category</h3>
           <p>Check back soon for new content.</p>
         </div>`;

    updateBtns();
  }

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      activeCategory = btn.dataset.category;
      renderFiltered();
    });
  });

  renderFiltered();
}

// ---- Page: Article detail --------------------------------------------

function initArticle() {
  const id        = parseInt(getParam('id'), 10);
  const article   = allArticles.find(a => a.id === id);
  const container = document.getElementById('article-container');
  if (!container) return;

  if (!article) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">📄</div>
        <h3>Article not found</h3>
        <p>This article may have been removed or the link may be incorrect.</p>
        <a href="news.html" class="btn btn-primary mt-2">Back to News</a>
      </div>`;
    return;
  }

  document.title = `${article.title} | Retrofit Ireland — RetrofitList.ie`;

  const catClass = getCatClass(article.category);
  const bodyHtml = renderBody(article.body);

  container.innerHTML = `
    <div class="article-detail">
      <a href="news.html" class="article-back">${icon.back} Back to News</a>
      <div class="article-detail-header">
        <div class="article-meta">
          <span class="category-pill ${catClass}">${esc(article.category)}</span>
        </div>
        <h1 class="article-detail-title">${esc(article.title)}</h1>
        <div class="article-detail-meta">
          <span>${icon.calendar} ${formatDate(article.date)}</span>
          <span>${icon.user} ${esc(article.author)}</span>
        </div>
      </div>
      <hr class="article-divider">
      <div class="article-body">${bodyHtml}</div>
    </div>`;
}

// ---- Header: scroll shadow + mobile menu + active link --------------

function initHeader() {
  const header  = document.querySelector('.site-header');
  const toggle  = document.querySelector('.menu-toggle');
  const navMenu = document.querySelector('.nav-menu');

  if (header) {
    window.addEventListener('scroll', () => {
      header.classList.toggle('scrolled', window.scrollY > 10);
    }, { passive: true });
  }

  if (toggle && navMenu) {
    toggle.addEventListener('click', () => {
      const open = navMenu.classList.toggle('open');
      toggle.classList.toggle('active', open);
      toggle.setAttribute('aria-expanded', String(open));
    });

    navMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('open');
        toggle.classList.remove('active');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Mark active nav link
  const currentFile = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-menu a[href]').forEach(link => {
    if (link.getAttribute('href') === currentFile) link.classList.add('active');
  });
}

// ---- Bootstrap -------------------------------------------------------

document.addEventListener('DOMContentLoaded', async () => {
  initHeader();

  // Remove loading placeholders once JS is running
  document.querySelectorAll('[data-loading]').forEach(el => {
    el.innerHTML = `<div class="loading-state" style="grid-column:1/-1"><div class="loading-spinner"></div><p class="text-light">Loading…</p></div>`;
  });

  await loadData();

  const page = document.body.dataset.page;
  if (page === 'home')      initHome();
  if (page === 'directory') initDirectory();
  if (page === 'news')      initNews();
  if (page === 'article')   initArticle();
});
