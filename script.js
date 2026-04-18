const feedTargets = {
  substack: document.getElementById("substack-feed-list"),
  india_decoded: document.getElementById("india-decoded-feed-list"),
};

const updatedAtTarget = document.getElementById("feed-updated-at");

function formatDate(value) {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "";
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

function renderItems(target, items) {
  if (!target) return;

  if (!items || !items.length) {
    target.innerHTML = '<li class="feed-placeholder">No essays available right now.</li>';
    return;
  }

  target.innerHTML = items
    .map((item) => {
      const dateMarkup = item.date
        ? `<p class="feed-item-date">${formatDate(item.date)}</p>`
        : "";
      const summaryMarkup = item.summary
        ? `<p class="feed-item-summary">${item.summary}</p>`
        : "";

      return `
        <li class="feed-item">
          ${dateMarkup}
          <a class="feed-item-title" href="${item.url}" target="_blank" rel="noreferrer">${item.title}</a>
          ${summaryMarkup}
        </li>
      `;
    })
    .join("");
}

fetch("data/latest-writing.json")
  .then((response) => {
    if (!response.ok) {
      throw new Error("Unable to load writing feeds.");
    }
    return response.json();
  })
  .then((data) => {
    renderItems(feedTargets.substack, data.sources?.substack?.items || []);
    renderItems(feedTargets.india_decoded, data.sources?.india_decoded?.items || []);

    if (updatedAtTarget && data.updated_at) {
      updatedAtTarget.textContent = `Last updated ${formatDate(data.updated_at)}.`;
    }
  })
  .catch(() => {
    Object.values(feedTargets).forEach((target) => {
      if (!target) return;
      target.innerHTML =
        '<li class="feed-placeholder">Latest feeds are temporarily unavailable. Use the archive links above.</li>';
    });

    if (updatedAtTarget) {
      updatedAtTarget.textContent = "";
    }
  });
