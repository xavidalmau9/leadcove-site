/**
 * LeadCove · AI-referrer attribution
 *
 * Detects when a visitor arrives from a major LLM/AI surface (ChatGPT,
 * Perplexity, Claude.ai, Gemini, Copilot, etc.) and tags every
 * downstream signup link with utm_source so we can measure which AI
 * tools convert.
 *
 * Behavior:
 *   1. On page load, inspects document.referrer.
 *   2. If it matches a known AI host, stashes the detection in
 *      sessionStorage so it survives client-side navigation within the
 *      site (visitor lands on /, browses to /blog/foo, then signs up).
 *   3. Rewrites every <a href> pointing at app.leadcove.io to include
 *      ?utm_source=<ai-name>&utm_medium=ai-referral on the way out.
 *   4. Fires a GA4 event so the source is visible in our analytics
 *      regardless of whether the visitor ever clicks a signup link.
 *
 * Self-contained, no dependencies, safe to load on every page.
 * Added 2026-06-08 after the first ChatGPT-referred visitor.
 */
(function () {
  'use strict';

  // Known AI / LLM referrer hosts mapped to utm_source values.
  // Extend as new surfaces emerge.
  var AI_REFERRERS = {
    'chatgpt.com':                  'chatgpt',
    'chat.openai.com':              'chatgpt',
    'perplexity.ai':                'perplexity',
    'www.perplexity.ai':            'perplexity',
    'claude.ai':                    'claude',
    'console.anthropic.com':        'claude',
    'gemini.google.com':            'gemini',
    'bard.google.com':              'gemini',
    'copilot.microsoft.com':        'copilot',
    'www.bing.com':                 'bing-chat',
    'poe.com':                      'poe',
    'you.com':                      'you',
    'phind.com':                    'phind',
    'kagi.com':                     'kagi',
    'character.ai':                 'character-ai',
    'duckduckgo.com':               'duckduckgo-ai',
  };

  var STORAGE_KEY = 'lc_ai_ref';

  function detectAiSource() {
    // First: check session-stashed detection from a prior pageview.
    try {
      var stashed = sessionStorage.getItem(STORAGE_KEY);
      if (stashed) return stashed;
    } catch (_) {}

    // Otherwise: parse the live referrer.
    if (!document.referrer) return null;
    try {
      var url = new URL(document.referrer);
      var host = url.hostname.toLowerCase();
      var source = AI_REFERRERS[host];
      if (!source) return null;
      try { sessionStorage.setItem(STORAGE_KEY, source); } catch (_) {}
      return source;
    } catch (_) {
      return null;
    }
  }

  function tagOutboundLinks(source) {
    // Rewrite every <a> on the page that targets the app to include
    // utm_source. Runs once on DOM-ready; if the page mutates after
    // that, the same script can be re-invoked.
    var links = document.querySelectorAll('a[href*="app.leadcove.io"]');
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      var href = a.getAttribute('href');
      if (!href) continue;
      // Don't double-tag if utm_source is already present
      if (/[?&]utm_source=/.test(href)) continue;
      var sep = href.indexOf('?') >= 0 ? '&' : '?';
      a.setAttribute('href',
        href + sep + 'utm_source=' + encodeURIComponent(source)
             + '&utm_medium=ai-referral');
    }
  }

  function fireAnalyticsEvent(source) {
    // GA4 — visible in Acquisition reports with this source string.
    if (typeof gtag === 'function') {
      try {
        gtag('event', 'ai_referral_landing', {
          event_category: 'acquisition',
          source:         source,
          page:           location.pathname,
        });
      } catch (_) {}
    }
  }

  function init() {
    var source = detectAiSource();
    if (!source) return;
    tagOutboundLinks(source);
    fireAnalyticsEvent(source);
    // Also annotate the body so any in-page CSS or downstream JS can
    // react (e.g. show a "saw us on ChatGPT?" greeting).
    if (document.body && document.body.classList) {
      document.body.classList.add('lc-ai-ref-' + source);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
