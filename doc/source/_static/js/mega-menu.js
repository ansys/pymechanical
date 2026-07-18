/*
 * Proof-of-concept mega menu for selected top navbar items.
 * Works as progressive enhancement and keeps default links intact.
 */

(function () {
  const isDesktopHover = () =>
    window.matchMedia("(hover: hover) and (pointer: fine) and (min-width: 992px)").matches;

  const menuConfig = {
    "getting started": {
      title: "Getting started",
      items: [
        {
          href: "getting_started/installation.html",
          label: "Installation",
          desc: "Set up PyMechanical and verify your environment.",
        },
        {
          href: "getting_started/choose_your_mode.html",
          label: "Choose your mode",
          desc: "Compare embedding and remote session workflows.",
        },
        {
          href: "getting_started/running_mechanical.html",
          label: "Launching PyMechanical",
          desc: "Start Mechanical and run your first automation script.",
        },
      ],
    },
    "user guide": {
      title: "User guide",
      items: [
        {
          href: "user_guide/embedding/overview.html",
          label: "Embedding mode",
          desc: "Run Mechanical directly inside your Python process.",
        },
        {
          href: "user_guide/remote_session/overview.html",
          label: "Remote session mode",
          desc: "Control Mechanical as a separate gRPC process.",
        },
        {
          href: "user_guide/index.html",
          label: "All user guide topics",
          desc: "Browse scripting, CLI, and advanced workflows.",
        },
      ],
    },
    examples: {
      title: "Examples",
      items: [
        {
          href: "examples/index.html",
          label: "Examples overview",
          desc: "Browse examples by workflow and simulation type.",
        },
        {
          href: "examples/gallery_examples/index.html",
          label: "Gallery examples",
          desc: "Interactive examples generated from source scripts.",
        },
      ],
    },
  };

  const normalize = (text) => text.trim().toLowerCase().replace(/\s+/g, " ");

  const toAbsolute = (target) => {
    const root = document.documentElement.getAttribute("data-content_root") || "./";

    if (/^https?:\/\//.test(target)) {
      return target;
    }

    return new URL(root + target, window.location.href).href;
  };

  const buildMenu = (config) => {
    const panel = document.createElement("div");
    panel.className = "pm-mega-menu";
    panel.setAttribute("role", "menu");

    const title = document.createElement("p");
    title.className = "pm-mega-title";
    title.textContent = config.title;
    panel.appendChild(title);

    for (const item of config.items) {
      const link = document.createElement("a");
      link.className = "pm-mega-link";
      link.href = toAbsolute(item.href);
      link.setAttribute("role", "menuitem");
      const strong = document.createElement("strong");
      strong.textContent = item.label;
      const span = document.createElement("span");
      span.textContent = item.desc;
      link.appendChild(strong);
      link.appendChild(span);
      panel.appendChild(link);
    }

    return panel;
  };

  const configureMegaMenu = () => {
    if (!isDesktopHover()) {
      return 0;
    }

    const navLinks = document.querySelectorAll(".bd-header .navbar-nav .nav-link");
    let configuredCount = 0;

    navLinks.forEach((link) => {
      const navItem = link.closest(".nav-item");
      if (!navItem || navItem.classList.contains("pm-has-mega")) {
        return;
      }

    const key = normalize(link.textContent || "");
    const config = menuConfig[key];
    if (!config) {
        return;
    }

      const panel = buildMenu(config);
      navItem.classList.add("pm-has-mega");
      navItem.appendChild(panel);

      let closeTimer;

      const open = () => {
        window.clearTimeout(closeTimer);
        navItem.classList.add("pm-open");
      };

      const close = () => {
        closeTimer = window.setTimeout(() => {
          navItem.classList.remove("pm-open");
        }, 120);
      };

      navItem.addEventListener("mouseenter", open);
      navItem.addEventListener("mouseleave", close);
      navItem.addEventListener("focusin", open);
      navItem.addEventListener("focusout", close);

      configuredCount += 1;
    });

    // Expose this for quick browser-console checks while iterating the POC.
    window.pyMechanicalMegaMenuItems = configuredCount;
    return configuredCount;
  };

  const init = () => {
    const configured = configureMegaMenu();
    // Some themes/components hydrate nav after initial DOM ready.
    if (configured === 0) {
      window.setTimeout(configureMegaMenu, 350);
    }
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }

  window.addEventListener("load", configureMegaMenu, { once: true });
})();
