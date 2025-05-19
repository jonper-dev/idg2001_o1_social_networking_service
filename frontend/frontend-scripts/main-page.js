import { getCachedPosts, cachePosts } from "./shared.js";

const API_BASE_URL =
  // "https://idg2001-o1-social-networking-service.onrender.com"; // RENDER:
  "http://127.0.0.1:8000"; // LOCAL:

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

// Post-button
document.addEventListener("DOMContentLoaded", () => {
  const postBtn = document.querySelector("#post-button");
  if (postBtn) {
    postBtn.addEventListener("click", postPost);
  }
});

// Post a Cheep (Cheep a post? Cheep something?)
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
    credentials: "include",
    body: JSON.stringify({ user_id, content }),
  })
    .then((res) => res.json())
    .then((data) => {
      const msg = document.querySelector("#post-message");
      const success = data.id && data.content;

      msg.textContent = success
        ? "Post created successfully!"
        : data.detail || "Post failed.";
      msg.className = success ? "success" : "error";

      if (success) {
        document.querySelector("#post-content").value = "";
        loadPosts(); // Refresh the post list.
      }
    })
    .catch((err) => console.error("Post error:", err));
}

// #################################
// ### Loading & rendering posts ###
// #################################
// Load post feed (also integrate caching-functions)
async function loadPosts() {
  const postList = document.getElementById("post-list");

  // Try to show cached posts (if valid).
  const cached = getCachedPosts();
  if (cached) {
    console.log("Loaded posts from local cache.");
    renderPosts(cached, postList);
  }

  // Always try to fetch fresh posts.
  try {
    const res = await fetch(`${API_BASE_URL}/posts/`, {
      credentials: "include", // Enables session cookies. Used to get "like"-states here.
    });

    if (!res.ok) throw new Error("Failed to fetch posts");

    const posts = await res.json();

    cachePosts(posts); // Update cache
    console.log("Fetched fresh posts and updated cache.");
    renderPosts(posts, postList); // Replace with fresh posts
  } catch (err) {
    console.error("Load posts error:", err);
    if (!cached) {
      postList.innerHTML =
        "<p>Failed to load posts and no cached data available.</p>";
    }
  }
}

// For rendering posts
function renderPosts(posts, container) {
  container.innerHTML = "";

  posts.forEach((post) => {
    const postDiv = document.createElement("div");
    postDiv.className = "post";

    // Create like button
    const likeBtn = document.createElement("button");
    likeBtn.classList.add("like-btn");
    likeBtn.textContent = post.is_liked_by_user ? "❤️" : "🤍";
    likeBtn.style.marginLeft = "10px";

    // Create like count
    const likeCount = document.createElement("span");
    const cachedLikes = localStorage.getItem(`post_${post.id}_likes`);
    const displayLikes = cachedLikes ? parseInt(cachedLikes) : post.likes;
    likeCount.textContent = ` ${displayLikes}`;
    likeBtn.appendChild(likeCount);

    // Like/unlike logic
    likeBtn.addEventListener("click", async () => {
      const isLiking = !post.is_liked_by_user;
      const url = `${API_BASE_URL}/posts/${post.id}/${isLiking ? "like" : "unlike"}`;

      try {
        const res = await fetch(url, {
          method: "POST",
          credentials: "include",
        });

        if (res.ok) {
          // Update the local post state.
          post.is_liked_by_user = isLiking;
          post.likes += isLiking ? 1 : -1;

          // Update the UI.
          likeBtn.innerHTML = isLiking ? "❤️" : "🤍";  // Resets content safely.
          likeCount.textContent = ` ${post.likes}`;
          likeBtn.appendChild(likeCount);  // Add back the updated like-counter.

          // Cache like count if it's large.
          if (post.likes > 100) {
            localStorage.setItem(`post_${post.id}_likes`, post.likes);
          } else {
            localStorage.removeItem(`post_${post.id}_likes`);
          }
        } else {
          const err = await res.json();
          alert(err.detail || "Failed to update like.");
        }
      } catch (err) {
        console.error("Like button error:", err);
        alert("Error with like button.");
      }
    });


    postDiv.innerHTML = `
      <strong>${post.username || "anon"}</strong>: ${post.content}
      <br><small>${new Date(post.timestamp).toLocaleString()}</small>
    `;

    // Append like button to post div
    postDiv.appendChild(likeBtn);

    container.appendChild(postDiv);
  });
}

// Load posts on page load
window.addEventListener("DOMContentLoaded", () => {
  loadPosts();
});
