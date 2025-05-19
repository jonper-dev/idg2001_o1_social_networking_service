const API_BASE_URL =
  // "https://idg2001-o1-social-networking-service.onrender.com"; // RENDER:
  "http://127.0.0.1:8000"; // LOCAL

document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const query = params.get("query");
  const type = params.get("type");
    
  const header = document.querySelector(".search-results__header");
  const resultsContainer = document.querySelector(".search-results__list");
  

  // Validate params
  if (!query || !type) {
    resultsContainer.innerHTML = `<p class="error">Invalid search parameters.</p>`;
    return;
  }

  // Update heading
  if (header) {
    header.textContent = `Search results for "${query}" in "${type}"`;
  }

  // Determine API endpoint
  const endpoint = `/search?query=${encodeURIComponent(query)}&type=${type}`;

  console.log(`Fetching from: ${API_BASE_URL}${endpoint}`);
  fetch(`${API_BASE_URL}${endpoint}`, {
    credentials: "include",
  })
    .then((res) => {
      if (!res.ok) throw new Error("Failed to fetch search results");
      return res.json();
    })
    .then((data) => {
      resultsContainer.innerHTML = ""; // Clear previous content

      if (!data || data.length === 0) {
        resultsContainer.innerHTML = `<p class="info">No results found.</p>`;
        return;
      }

      if (type === "posts") {
        renderPosts(data, resultsContainer);
      } else if (type === "accounts") {
        renderAccounts(data, resultsContainer);
      } else if (type === "hashtags") {
        renderHashtags(data, resultsContainer);
      } else {
        resultsContainer.innerHTML = `<p class="error">Unsupported search type: ${type}</p>`;
      }
    })
    .catch((err) => {
      console.error("Search error:", err);
      resultsContainer.textContent = "Error loading results.";
    });
});

function renderPosts(posts, container) {
  posts.forEach((post) => {
    const div = document.createElement("div");
    div.className = "post";
    div.innerHTML = `<strong>${post.username || "Anonymous"}</strong>: ${post.content}`;
    container.appendChild(div);
  });
}

function renderAccounts(accounts, container) {
  accounts.forEach((account) => {
    const div = document.createElement("div");
    div.className = "account";
    div.innerHTML = `<strong>${account.name}</strong>`;
    container.appendChild(div);
  });
}

function renderHashtags(hashtags, container) {
  hashtags.forEach((hashtag) => {
    const div = document.createElement("div");
    div.className = "hashtag";
    div.innerHTML = `${hashtag.name || hashtag.tag}`;
    container.appendChild(div);
  });
}
