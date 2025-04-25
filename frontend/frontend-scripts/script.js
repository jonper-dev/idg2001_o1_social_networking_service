import { getCachedPosts, cachePosts } from "./local-caching.js";

const API_BASE_URL = "https://idg2001-o1-social-networking-service.onrender.com";

// DARK MODE toggle with localStorage
const darkToggle = document.getElementById("dark-toggle");
if (localStorage.getItem("dark") === "true") {
  document.body.classList.add("dark");
  if (darkToggle) darkToggle.textContent = "☀️";
}
if (darkToggle) {
  darkToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark");
    const isDark = document.body.classList.contains("dark");
    localStorage.setItem("dark", isDark);
    darkToggle.textContent = isDark ? "☀️" : "🌙";
  });
}

// Responsive nav menu toggle
const menuToggle = document.getElementById("menu-toggle");
const navLinks = document.getElementById("nav-links");
if (menuToggle && navLinks) {
  menuToggle.addEventListener("click", () => {
    navLinks.classList.toggle("active");
  });
}

// Sign up
function signup() {
  const username = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  // Hash the password
  bcrypt.hash(password, 10, (err, hashedPassword) => {
    if (err) {
      console.error("Error hashing password:", err);
      return;
    }

    fetch(`${API_BASE_URL}/users/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password_hash: password }),
    })
      .then((res) => res.json())
      .then((data) => {
        const msg = document.getElementById("signup-message");
        msg.textContent = data.message || data.detail || "Signup failed.";
        msg.className = data.message ? "success" : "error";
      })
      .catch((err) => console.error("Signup error:", err));
  });
}

// Login
function login() {
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  fetch(`${API_BASE_URL}/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error("Login failed");
      }
      return res.json();
    })
    .then((data) => {
      if (data.user_id) {
        // Save session
        localStorage.setItem("user_id", data.user_id);
        localStorage.setItem("name", data.name);
        // Redirect to feed or home page
<<<<<<< HEAD:frontend/script.js
        window.location.href = "/frontend/post.html";
=======
        window.location.href = "/frontend/index.html"; // Update to match your actual file name
>>>>>>> 21ccbd279b1e203fa07b579c29d0538d709de26e:frontend/frontend-scripts/script.js
      } else {
        const msg = document.getElementById("login-message");
        msg.textContent = data.detail || "Login failed.";
        msg.className = "error";
      }
    })
    .catch((err) => {
      const msg = document.getElementById("login-message");
      msg.textContent = err.message || "Login error.";
      msg.className = "error";
      console.error("Login error:", err);
    });
}

// Logout
function logout() {
  localStorage.clear();
  alert("You have been logged out.");
  location.reload();
}

// Post a Cheep
function postPost() {
  const content = document.getElementById("post-content").value;
  const user_id = localStorage.getItem("user_id");

  if(!user_id) {
    alert("Please log in first!");
    return;
  }

  fetch(`${API_BASE_URL}/posts/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id, content }),
  })
    .then((res) => res.json())
    .then((data) => {
      const msg = document.getElementById("post-message");
      msg.textContent = data.message || data.detail || "Post failed.";
      msg.className = data.message ? "success" : "error";
      document.getElementById("post-content").value = "";
      loadPosts(); // refresh post list
    })
    .catch((err) => console.error("Post error:", err));
}

<<<<<<< HEAD:frontend/script.js
// Load post feed
function loadPosts() {
  fetch(`${API_BASE_URL}/posts/`)
    .then((res) => res.json())
    .then((posts) => {
      const postList = document.getElementById("post-list");
      postList.innerHTML = "";

      posts.forEach((post) => {
        const postDiv = document.createElement("div");
        postDiv.className = "post";
        postDiv.innerHTML = `
          <strong>@${post.username || "anon"}</strong>: ${post.content}
          <br><small>${new Date(post.timestamp).toLocaleString()}</small>
        `;
        postList.appendChild(postDiv);
      });
    })
    .catch((err) => console.error("Load posts error:", err));
=======
// For rendering posts.
function renderPosts(posts, container) {
  container.innerHTML = "";

  posts.forEach(post => {
    const postDiv = document.createElement("div");
    postDiv.className = "post";
    postDiv.innerHTML = `
      <strong>@${post.username || "anon"}</strong>: ${post.content}
      <br><small>${new Date(post.timestamp).toLocaleString()}</small>
    `;
    container.appendChild(postDiv);
  });
}


// Load post feed (also integrate caching-functions)
async function loadPosts() {
  const postList = document.getElementById("post-list");

  // Try to show cached posts (if valid).
  const cached = getCachedPosts();
  if(cached) {
    console.log("Loaded posts from local cache.");
    renderPosts(cached, postList);
  }

  // Always try to fetch fresh posts.
  try {
    const res = await fetch(`${API_BASE_URL}/posts/`);
    if(!res.ok) throw new Error("Failed to fetch posts");

    const posts = await res.json();

    cachePosts(posts); // Update cache
    console.log("🔄 Fetched fresh posts and updated cache.");
    renderPosts(posts, postList); // Replace with fresh posts
  } catch(err) {
    console.error("Load posts error:", err);
    if(!cached) {
      postList.innerHTML = "<p>Failed to load posts and no cached data available.</p>";
    }
  }
>>>>>>> 21ccbd279b1e203fa07b579c29d0538d709de26e:frontend/frontend-scripts/script.js
}

// Load posts on startup
window.onload = loadPosts;
