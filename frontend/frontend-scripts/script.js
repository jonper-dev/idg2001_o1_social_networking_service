import { getCachedPosts, cachePosts } from "./local-caching.js";

const API_BASE_URL = "https://idg2001-o1-social-networking-service.onrender.com";

// #######################
// ### Event listeners ###
// #######################
// Login-button
document.addEventListener("DOMContentLoaded", () => {
  const loginBtn = document.querySelector("#login-button");
  if (loginBtn) {
    loginBtn.addEventListener("click", login);
  }
});

// Logout-button
document.addEventListener("DOMContentLoaded", () => {
  const logoutBtn = document.querySelector("#logout-button");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", logout);
  }
});

// Welcome-message
document.addEventListener("DOMContentLoaded", () => {
  const welcomeMessage = document.querySelector("#welcome-message");

  const userName = localStorage.getItem("user_name");
  if (userName && welcomeMessage) {
    welcomeMessage.textContent = `Welcome, ${userName}.`;
  } else {
    console.log("No 'user_name' found in storage.");
  }
});



// DARK MODE toggle with localStorage
const darkToggle = document.getElementById("dark-toggle");
if (localStorage.getItem("dark") === "true") {
  document.body.classList.add("dark");
  if (darkToggle) darkToggle.textContent = "☀️";
};
if (darkToggle) {
  darkToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark");
    const isDark = document.body.classList.contains("dark");
    localStorage.setItem("dark", isDark);
    darkToggle.textContent = isDark ? "☀️" : "🌙";
  });
};

// Responsive nav menu toggle
const menuToggle = document.getElementById("menu-toggle");
const navLinks = document.getElementById("nav-links");
if (menuToggle && navLinks) {
  menuToggle.addEventListener("click", () => {
    navLinks.classList.toggle("active");
  });
};

// Sign up
function signup() {
  const username = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  fetch(`${API_BASE_URL}/users/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password_hash: password })
  })
    .then(res => res.json())
    .then(data => {
      const msg = document.getElementById("signup-message");
      msg.textContent = data.message || data.detail || "Signup failed.";
      msg.className = data.message ? "success" : "error";
    })
    .catch(err => console.error("Signup error:", err));
};

// Login
function login() {
  const email = document.querySelector("#login-email").value;
  const password = document.querySelector("#login-password").value;

  fetch(`${API_BASE_URL}/login/`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  })
    .then(res => {
      if (!res.ok) {
        throw new Error("Login failed");
      }
      return res.json();
    })
    .then(data => {
      if (data.user_id) {
        // Save session
        localStorage.setItem("user_id", data.user_id);
        localStorage.setItem("user_name", data.name);
        console.log("Stored user:", localStorage.getItem("user_name"));

        // Redirects to the main page (includes post-feed).
        // Delayed to allow localStorage to store the username.
        setTimeout(() => {
          window.location.href = "/frontend/index.html";
        }, 100); // 100 ms delay to enable localStorage.
      } else {
        const msg = document.querySelector("#login-message");
        msg.textContent = data.detail || "Login failed.";
        msg.className = "error";
      };
    })
    .catch(err => {
      const msg = document.querySelector("#login-message");
      msg.textContent = err.message || "Login error.";
      msg.className = "error";
      console.error("Login error:", err);
    });
};

// Logout
function logout() {
  localStorage.clear();
  alert("You have been logged out.");
  location.reload();
};

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
    body: JSON.stringify({ user_id, content })
  })
    .then(res => res.json())
    .then(data => {
      const msg = document.getElementById("post-message");
      msg.textContent = data.message || data.detail || "Post failed.";
      msg.className = data.message ? "success" : "error";
      document.getElementById("post-content").value = "";
      loadPosts(); // refresh post list
    })
    .catch(err => console.error("Post error:", err));
};




// #################################
// ### Loading & rendering posts ###
// #################################
// Load post feed (also integrate caching-functions)
async function loadPosts() {
  const postList = document.getElementById("post-list");

  // Try to show cached posts (if valid).
  const cached = getCachedPosts();
  if(cached) {
    console.log("Loaded posts from local cache.");
    renderPosts(cached, postList);
  };

  // Always try to fetch fresh posts.
  try {
    const res = await fetch(`${API_BASE_URL}/posts/`);
    if(!res.ok) throw new Error("Failed to fetch posts");

    const posts = await res.json();

    cachePosts(posts); // Update cache
    console.log("Fetched fresh posts and updated cache.");
    renderPosts(posts, postList); // Replace with fresh posts
  } catch(err) {
    console.error("Load posts error:", err);
    if(!cached) {
      postList.innerHTML = "<p>Failed to load posts and no cached data available.</p>";
    }
  }
};

// For rendering posts
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
};

// Load posts on startup
window.onload = loadPosts;
