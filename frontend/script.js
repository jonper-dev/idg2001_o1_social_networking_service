const API_BASE_URL = "http://127.0.0.1:8000/api"; // change to Render URL if deployed

// 🌙 DARK MODE toggle with localStorage
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

// 📱 Responsive nav menu toggle
const menuToggle = document.getElementById("menu-toggle");
const navLinks = document.getElementById("nav-links");
if (menuToggle && navLinks) {
  menuToggle.addEventListener("click", () => {
    navLinks.classList.toggle("active");
  });
}

// 👤 Sign up
function signup() {
  const username = document.getElementById("username").value;
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
}

// 🔑 Login
function login() {
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;
  
    fetch(`${API_BASE_URL}/login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    })
      .then(res => res.json())
      .then(data => {
        const msg = document.getElementById("login-message");
        if (data.user_id) {
          msg.textContent = "Welcome back, " + data.username + "!";
          msg.className = "success";
          // Save session
          localStorage.setItem("user_id", data.user_id);
          localStorage.setItem("username", data.username);
        } else {
          msg.textContent = data.detail || "Login failed.";
          msg.className = "error";
        }
      })
      .catch(err => {
        console.error("Login error:", err);
      });
  }

// 🔑 Logout
function logout() {
    localStorage.clear();
    alert("You have been logged out.");
    location.reload();
  }
  

// 🐥 Post a Cheep
function postPost() {
    const content = document.getElementById("post-content").value;
    const user_id = localStorage.getItem("user_id");
  
    if (!user_id) {
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
}

// 🧾 Load post feed
function loadPosts() {
  fetch(`${API_BASE_URL}/posts/`)
    .then(res => res.json())
    .then(posts => {
      const postList = document.getElementById("post-list");
      postList.innerHTML = "";

      posts.forEach(post => {
        const postDiv = document.createElement("div");
        postDiv.className = "post";
        postDiv.innerHTML = `
          <strong>@${post.username || "anon"}</strong>: ${post.content}
          <br><small>${new Date(post.timestamp).toLocaleString()}</small>
        `;
        postList.appendChild(postDiv);
      });
    })
    .catch(err => console.error("Load posts error:", err));
}

// ▶️ Load posts on startup
window.onload = loadPosts;