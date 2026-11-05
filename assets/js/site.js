// Page enhancements. Every page is complete without this script; it adds
// the light/dark toggle, the giscus comment thread, a language label and
// copy button on code blocks, the outline beside a post, and "#" links on
// headings.

(function () {
  "use strict";

  var root = document.documentElement;
  var darkQuery = window.matchMedia("(prefers-color-scheme: dark)");

  // `data-theme` on <html> holds an explicit choice; without it the
  // system preference applies (see _sass/_tokens.scss).
  function currentTheme() {
    return root.dataset.theme || (darkQuery.matches ? "dark" : "light");
  }

  function giscusTheme(theme) {
    return theme === "dark" ? "transparent_dark" : "light";
  }

  function setupThemeToggle() {
    var button = document.querySelector(".theme-toggle");
    if (!button) return;
    button.hidden = false;
    button.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      try {
        localStorage.setItem("theme", next);
      } catch (e) {
        // Storage is blocked: the choice lasts until the page is left.
      }
      updateGiscusTheme(next);
    });
    // Without an explicit choice the page follows the system setting live;
    // the comment thread has to be told separately.
    darkQuery.addEventListener("change", function () {
      if (!root.dataset.theme) updateGiscusTheme(currentTheme());
    });
  }

  // giscus runs in an iframe from giscus.app and accepts its theme by message.
  function updateGiscusTheme(theme) {
    var frame = document.querySelector("iframe.giscus-frame");
    if (!frame) return;
    frame.contentWindow.postMessage(
      { giscus: { setConfig: { theme: giscusTheme(theme) } } },
      "https://giscus.app"
    );
  }

  function loadGiscus() {
    var mount = document.querySelector(".giscus-mount");
    if (!mount) return;
    var config = {
      "data-repo": mount.dataset.repo,
      "data-repo-id": mount.dataset.repoId,
      "data-category": mount.dataset.category,
      "data-category-id": mount.dataset.categoryId,
      "data-mapping": "pathname",
      "data-strict": "0",
      "data-reactions-enabled": "1",
      "data-emit-metadata": "0",
      "data-input-position": "bottom",
      "data-theme": giscusTheme(currentTheme()),
      "data-lang": mount.dataset.lang,
      "data-loading": "lazy",
      "crossorigin": "anonymous"
    };
    var script = document.createElement("script");
    script.src = "https://giscus.app/client.js";
    script.async = true;
    Object.keys(config).forEach(function (name) {
      script.setAttribute(name, config[name]);
    });
    mount.appendChild(script);
  }

  // Kramdown marks each fenced block as div.language-<name>.highlighter-rouge.
  function setupCodeBlocks() {
    var blocks = document.querySelectorAll(".prose div.highlighter-rouge");
    Array.prototype.forEach.call(blocks, function (block) {
      var code = block.querySelector("pre code");
      if (!code) return;

      var match = block.className.match(/\blanguage-(\S+)/);
      var lang = match && match[1] !== "plaintext" ? match[1] : "text";

      var header = document.createElement("div");
      header.className = "code-header";
      var label = document.createElement("span");
      label.className = "code-lang";
      label.textContent = lang;
      var copy = document.createElement("button");
      copy.type = "button";
      copy.className = "code-copy";
      copy.textContent = "Copy";
      header.appendChild(label);
      header.appendChild(copy);
      block.insertBefore(header, block.firstChild);

      copy.addEventListener("click", function () {
        navigator.clipboard.writeText(code.textContent).then(
          function () { flash(copy, "done", "Copied"); },
          function () { flash(copy, "failed", "Copy failed"); }
        );
      });
    });
  }

  function flash(button, state, text) {
    button.dataset.state = state;
    button.textContent = text;
    window.setTimeout(function () {
      delete button.dataset.state;
      button.textContent = "Copy";
    }, 1600);
  }

  // Fills the outline aside of a post (_layouts/post.html) with its h2 and
  // h3 headings, and marks the section being read. Kramdown gives every
  // heading an id, which the links point to. Runs before the "#" anchors are
  // appended, so the link text is the heading text alone.
  function setupToc() {
    var toc = document.querySelector(".post-toc");
    if (!toc) return;
    var headings = document.querySelectorAll(".prose h2[id], .prose h3[id]");
    if (headings.length < 2) return;

    var list = toc.querySelector("ol");
    var links = Array.prototype.map.call(headings, function (heading) {
      var item = document.createElement("li");
      item.className = "toc-" + heading.tagName.toLowerCase();
      var link = document.createElement("a");
      link.href = "#" + encodeURIComponent(heading.id);
      link.textContent = heading.textContent;
      item.appendChild(link);
      list.appendChild(item);
      return link;
    });
    toc.hidden = false;
    toc.parentElement.classList.add("has-toc");

    // The current section is the last heading scrolled past the header. At
    // the bottom of the page the last sections may be too short to reach
    // that line, so the last heading counts as current there.
    var offset = parseFloat(getComputedStyle(root).fontSize) * 6;
    var active = null;
    function markCurrent() {
      var index = -1;
      for (var i = 0; i < headings.length; i++) {
        if (headings[i].getBoundingClientRect().top - offset > 0) break;
        index = i;
      }
      if (window.innerHeight + window.scrollY >= root.scrollHeight - 2) {
        index = headings.length - 1;
      }
      var next = links[Math.max(index, 0)];
      if (next === active) return;
      if (active) active.removeAttribute("aria-current");
      next.setAttribute("aria-current", "true");
      active = next;
    }
    var pending = false;
    window.addEventListener("scroll", function () {
      if (pending) return;
      pending = true;
      window.requestAnimationFrame(function () {
        pending = false;
        markCurrent();
      });
    }, { passive: true });
    markCurrent();
  }

  // Kramdown gives every heading an id; the link makes a section shareable.
  function setupHeadingAnchors() {
    var headings = document.querySelectorAll(".prose h2[id], .prose h3[id], .prose h4[id]");
    Array.prototype.forEach.call(headings, function (heading) {
      var link = document.createElement("a");
      link.className = "heading-anchor";
      link.href = "#" + encodeURIComponent(heading.id);
      link.setAttribute("aria-label", "Link to this section");
      link.textContent = "#";
      heading.appendChild(link);
    });
  }

  function init() {
    setupThemeToggle();
    loadGiscus();
    setupCodeBlocks();
    setupToc();
    setupHeadingAnchors();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
