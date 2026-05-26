(function () {
  function escapeHTML(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, function (char) {
      return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[char];
    });
  }

  function isExternal(href) {
    return /^https?:\/\//i.test(String(href || ''));
  }

  function isSafeHref(href) {
    var raw = String(href || '').trim();
    if (!raw) return false;
    // allow http/https, root-relative, fragment, and relative paths; block javascript:/data:/vbscript:
    if (/^(javascript|data|vbscript):/i.test(raw)) return false;
    return true;
  }

  function renderLink(link) {
    if (!link || !link.href || !link.label) return '';
    if (!isSafeHref(link.href)) return '';
    var href = escapeHTML(link.href);
    var attrs = isExternal(link.href) ? ' target="_blank" rel="noopener noreferrer"' : '';
    return '<a href="' + href + '"' + attrs + '>' + escapeHTML(link.label) + '</a>';
  }

  function renderCard(item, index) {
    var proofList = Array.isArray(item.proof) ? item.proof : [];
    var linkList = Array.isArray(item.links) ? item.links : [];
    var proof = proofList.map(function (text) { return '<span>' + escapeHTML(text) + '</span>'; }).join('');
    var links = linkList.map(renderLink).join('');
    return '<article class="case-card' + (index === 0 ? ' hero-case' : '') + '">' +
      '<div><p class="eyebrow">' + escapeHTML(item.eyebrow) + '</p>' +
      '<h2>' + escapeHTML(item.title) + '</h2>' +
      '<p class="question">' + escapeHTML(item.question) + '</p>' +
      '<p>' + escapeHTML(item.summary) + '</p>' +
      '<div class="proof-pills">' + proof + '</div></div>' +
      '<div class="link-row">' + links + '</div>' +
      '</article>';
  }

  var mount = document.querySelector('[data-case-grid]');
  if (!mount) return;
  // Keep static fallback in place if registry is missing or empty.
  if (!Array.isArray(window.portfolioCases) || window.portfolioCases.length === 0) return;
  mount.innerHTML = window.portfolioCases.map(renderCard).join('');
}());
