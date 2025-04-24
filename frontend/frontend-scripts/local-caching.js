const CACHE_KEY = "cached_posts";
const TIMESTAMP_KEY = `${CACHE_KEY}_timestamp`;
const CACHE_EXPIRY = 5 * 60 * 1000; // 5 minutes in milliseconds

export function getCachedPosts() {
  const cached = localStorage.getItem(CACHE_KEY);
  const timestamp = localStorage.getItem(TIMESTAMP_KEY);

  if (!cached || !timestamp) return null;

  const age = Date.now() - parseInt(timestamp);
  if (age > CACHE_EXPIRY) {
    // Cache too old.
    return null;
  }

  return JSON.parse(cached);
}

export function cachePosts(posts) {
  localStorage.setItem(CACHE_KEY, JSON.stringify(posts));
  localStorage.setItem(TIMESTAMP_KEY, Date.now().toString());
}
