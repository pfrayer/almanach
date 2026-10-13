// Recipe pages: tap an ingredient row to tick it off (kept across reloads),
// and keep the screen awake while the page is open.
// The markup (`table[data-ingredients]`, group rows) comes from
// hooks/recipes.py at build time.
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

// Ticked rows, per page, as "table:row" keys. Storage can be unavailable
// (private browsing, blocked site data): the checklist then just forgets.
function storageKey() {
  return `almanach:ingredients:${location.pathname}`;
}

function loadTicked() {
  try {
    return new Set(JSON.parse(localStorage.getItem(storageKey())) || []);
  } catch {
    return new Set();
  }
}

function saveTicked(ticked) {
  try {
    if (ticked.size) localStorage.setItem(storageKey(), JSON.stringify([...ticked]));
    else localStorage.removeItem(storageKey());
  } catch {
    // Not persisted; the page still works.
  }
}

function enableIngredientChecklist() {
  const ticked = loadTicked();
  const tables = document.querySelectorAll(".md-typeset table[data-ingredients]");

  tables.forEach((table, tableIndex) => {
    const rows = [...table.querySelectorAll("tbody tr:not(.ingredients__group)")];

    const bar = document.createElement("div");
    bar.className = "ingredients-bar";
    const hint = document.createElement("p");
    hint.className = "ingredients-bar__hint";
    hint.textContent = "Touchez un ingrédient pour le cocher.";
    const reset = document.createElement("button");
    reset.type = "button";
    reset.className = "ingredients-bar__reset";
    reset.textContent = "Tout décocher";
    bar.append(hint, reset);
    // Material wraps tables in .md-typeset__scrollwrap: put the bar above it.
    const wrapper = table.closest(".md-typeset__scrollwrap") || table;
    wrapper.before(bar);

    const untickers = [];
    const refresh = () => {
      reset.hidden = !rows.some((row) => row.classList.contains("ingredients__row--done"));
    };

    rows.forEach((row, rowIndex) => {
      const key = `${tableIndex}:${rowIndex}`;
      const set = (done) => {
        row.classList.toggle("ingredients__row--done", done);
        row.setAttribute("aria-checked", String(done));
        if (done) ticked.add(key);
        else ticked.delete(key);
      };
      row.tabIndex = 0;
      row.setAttribute("role", "checkbox");
      set(ticked.has(key));
      const toggle = () => {
        set(!row.classList.contains("ingredients__row--done"));
        saveTicked(ticked);
        refresh();
      };
      row.addEventListener("click", toggle);
      row.addEventListener("keydown", (event) => {
        if (event.key === " " || event.key === "Enter") {
          event.preventDefault();
          toggle();
        }
      });
      untickers.push(() => set(false));
    });

    reset.addEventListener("click", () => {
      untickers.forEach((untick) => untick());
      saveTicked(ticked);
      refresh();
    });
    refresh();
  });
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
