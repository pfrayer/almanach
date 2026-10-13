// Recipes are in French, cheatsheets in English (see
// overrides/partials/language.html). A full page load gets the right
// <html lang>, but Material's instant navigation only swaps the content:
// sync the document language and the search placeholder from the marker
// that overrides/main.html puts in it.

const SEARCH_PLACEHOLDER = { fr: "Rechercher", en: "Search" };

document$.subscribe(() => {
  const marker = document.querySelector("[data-page-lang]");
  if (!marker) return;
  const lang = marker.dataset.pageLang;
  document.documentElement.lang = lang;
  const search = document.querySelector(".md-search__input");
  if (search && SEARCH_PLACEHOLDER[lang]) {
    search.placeholder = SEARCH_PLACEHOLDER[lang];
    search.setAttribute("aria-label", SEARCH_PLACEHOLDER[lang]);
  }
});
