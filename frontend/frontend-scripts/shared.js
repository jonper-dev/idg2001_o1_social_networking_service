const API_BASE_URL =
  
  // "https://idg2001-social-networking-service.onrender.com"; // RENDER:
  "http://127.0.0.1:8000"; // LOCAL:

// #####################
// ### Local caching ###
// #####################
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

// #######################
// ### Event listeners ###
// #######################
// Login-button/ Signup-button
document.addEventListener("DOMContentLoaded", () => {
  const loginBtn = document.querySelector("#login-button");
  if (loginBtn) {
    loginBtn.addEventListener("click", login);
  }

  const signupBtn = document.querySelector("#signup-button");
  if (signupBtn) {
    signupBtn.addEventListener("click", signup);
  }
});

// Authentication-button (bottom logout-/login-button), and logout-message.
document.addEventListener("DOMContentLoaded", () => {
  const authButton = document.querySelector("#auth-button");
  const isLoggedIn = !!localStorage.getItem("user_id");
  const authMsg = document.getElementById("auth-message");
  const logoutMsg = sessionStorage.getItem("logoutMessage");

  if (logoutMsg && authMsg) {
    authMsg.textContent = logoutMsg;
    authMsg.classList.add("info"); // Optional styling class
    sessionStorage.removeItem("logoutMessage"); // Clearing it on reload.
  }

  if (authButton) {
    if (isLoggedIn) {
      authButton.textContent = "Log Out";
      authButton.addEventListener("click", logout);
    } else {
      authButton.textContent = "Log In";
      authButton.addEventListener("click", () => {
        window.location.href = "login_signup.html";
      });
    }
  }
});

// Searchbar form (accessible and keyboard-friendly)
document.addEventListener("DOMContentLoaded", () => {
  const searchForm = document.querySelector("#search-form");
  if (searchForm) {
    searchForm.addEventListener("submit", (e) => {
      e.preventDefault(); // Prevent page reload
      searchPosts(); // Run search
    });
  }
});

// Navbar User Toggle //
window.addEventListener("DOMContentLoaded", () => {
  const authLink = document.getElementById("auth-link"); 

  fetch(`${API_BASE_URL}/auth/me`, {
    credentials: "include", // sends the session_id cookie
  })
    .then((res) => {
      if (!res.ok) throw new Error("Not logged in.");
      return res.json();
    })
    .then((data) => {
      authLink.href = `/frontend/profile.html?user_id=${data.user.id}`;
      authLink.innerHTML = `
        <img src="assets/profile-icon.svg"
            alt="Profile Icon"
            style="width: 25px; vertical-align: middle; margin-right: 6px;">
        ${data.user.name}
      `;
    })
    .catch((err) => {
      // Not logged in — leave as Login
      console.warn("User not logged in or profile fetch failed:", err);
      authLink.href = "/frontend/login_signup.html";
      authLink.textContent = "Login";
    });
});


// ########################
// ### Global variables ###
// ########################
// Authentication message
const authMsg = document.querySelector("#auth-message");

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

// Searchbar input
function searchPosts() {
  const query = document.querySelector("#search-input").value.trim();
  const type = document.querySelector("#search-type").value; // Dropdown for search type
  
  if (!query) return;

  window.location.href = `/frontend/search_results.html?query=${encodeURIComponent(query)}&type=${type}`;
}

// Sign up
function signup() {
  const username = document.querySelector("#username").value;
  const email = document.querySelector("#email").value;
  const password = document.querySelector("#password").value;

  fetch(`${API_BASE_URL}/users/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: username, email, password }),
  })
    .then((res) => res.json())
    .then((data) => {
      const msg = document.querySelector("#signup-message");
      const success = data.id && data.name;

      msg.textContent = success
        ? "Signup successful! You can now log in."
        : data.detail || "Signup failed.";
      msg.className = success ? "success" : "error";
    })
    .catch((err) => console.error("Signup error:", err));
}

// Login
function login() {
  console.log("Login function triggered.");

  const email = document.querySelector("#login-email").value;
  const password = document.querySelector("#login-password").value;

  fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    credentials: "include", // Include session cookie
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error("Login failed.");
      }
      return res.json();
    })
    .then(() => {
      // After login, validate session to get user info securely
      return fetch(`${API_BASE_URL}/auth/me`, {
        method: "GET",
        credentials: "include", // Send session_id cookie
      });
    })
    .then((res) => {
      if (!res.ok) {
        throw new Error("Session validation failed.");
      }
      return res.json();
    })
    .then((data) => {
      // Store public user info locally (if needed for display)
      localStorage.setItem("user_id", data.user.id);
      localStorage.setItem("user_name", data.user.name);
      console.log("Stored user:", data.user.name);

      // Redirect to main page
      window.location.href = "/frontend/index.html";
    })
    .catch((err) => {
      const msg = document.querySelector("#login-message");
      msg.textContent = err.message || "Login error.";
      msg.className = "error";
      console.error("Login error:", err);
    });
}

// Logout
function logout() {
  fetch(`${API_BASE_URL}/auth/logout`, {
    method: "POST",
    credentials: "include", // Sends session_id cookie to backend
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error("Logout failed.");
      }
      return res.json();
    })
    .then((data) => {
      console.log("Logout response:", data.message);

      // Remove only user-related data (leave dark mode etc.)
      localStorage.removeItem("user_id");
      localStorage.removeItem("user_name");

      // Store message temporarily for display after reload
      sessionStorage.setItem("logoutMessage", "You have been logged out.");
      location.reload();
    })
    .catch((err) => {
      console.error("Logout error:", err);
      alert("Logout failed.");
    });
}

// Theme toggle
document.addEventListener("DOMContentLoaded", () => {
  const themeToggle = document.getElementById("theme-toggle");
  const currentTheme = localStorage.getItem("theme") || "light";

  // Set the initial theme
  document.documentElement.setAttribute("data-theme", currentTheme);
  themeToggle.textContent = currentTheme === "dark" ? "☀️" : "🌙";

  // Add event listener for theme toggle
  themeToggle.addEventListener("click", () => {
    const newTheme = document.documentElement.getAttribute("data-theme") === "light" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
    themeToggle.textContent = newTheme === "dark" ? "☀️" : "🌙";
  });
});
