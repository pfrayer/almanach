// Recipe pages: tap an ingredient row to strike it through, and keep the
// screen awake while the page is open.
// `document$` is Material's page-load observable: it also fires on instant
// navigation, where DOMContentLoaded does not.

let wakeLock = null;

async function keepAwake() {
  if (!("wakeLock" in navigator) || document.visibilityState !== "visible") return;
  try {
    wakeLock = await navigator.wakeLock.request("screen");
  } catch {
    // Refused (battery saver, unsupported context): not worth reporting.
  }
}

function releaseWakeLock() {
  if (wakeLock) {
    wakeLock.release();
    wakeLock = null;
  }
}

function isRecipePage() {
  // Recipes live under /docs/cook/, but not the index page itself.
  return /\/docs\/cook\/.+/.test(location.pathname);
}

function enableIngredientChecklist() {
  for (const table of document.querySelectorAll(".md-typeset table")) {
    const header = table.querySelector("thead th");
    if (!header || header.textContent.trim() !== "Ingrédient") continue;
    table.dataset.ingredients = "";
    for (const row of table.querySelectorAll("tbody tr")) {
      // Group rows (`| **Pâte** | | |`) only hold a heading.
      if (row.querySelector("td:first-child > strong:only-child")) {
        row.classList.add("ingredients__group");
        continue;
      }
      row.tabIndex = 0;
      row.setAttribute("role", "checkbox");
      row.setAttribute("aria-checked", "false");
      const toggle = () => {
        const done = row.classList.toggle("ingredients__row--done");
        row.setAttribute("aria-checked", String(done));
      };
      row.addEventListener("click", toggle);
      row.addEventListener("keydown", (event) => {
        if (event.key === " " || event.key === "Enter") {
          event.preventDefault();
          toggle();
        }
      });
    }
  }
}

document$.subscribe(() => {
  if (isRecipePage()) {
    enableIngredientChecklist();
    if (!wakeLock) keepAwake();
  } else {
    releaseWakeLock();
  }
});

// The browser drops the lock when the tab is hidden: take it back on return.
document.addEventListener("visibilitychange", () => {
  if (isRecipePage() && document.visibilityState === "visible") {
    wakeLock = null;
    keepAwake();
  }
});
