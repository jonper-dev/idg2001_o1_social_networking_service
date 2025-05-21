const API_BASE_URL =
  // "https://idg2001-o1-social-networking-service.onrender.com";  // Render
  "http://127.0.0.1:8080"; // Local dev

////////////////////////////
// Display Profile info ///
//////////////////////////
async function displayUserInfo() {
  try {
    const res = await fetch(`${API_BASE_URL}/auth/me`, {
      credentials: "include", // sends the session_id cookie
    });

    if (!res.ok) throw new Error("No user details found");

    const data = await res.json();
    console.log("Fetched user info:", data);

    const userImage = document.querySelector(".user-profile__info__user-image");
    const userName = document.querySelector(".user-profile__info__username");
    const email = document.querySelector(".user-profile__info__email");

    userImage.src = "/frontend/assets/profile-icon-blue.svg";
    userImage.alt = "Profile image";

    userName.textContent = data.user?.name || "Unnamed user";
    email.textContent = data.user?.email || "No email for this user";

    // Store user data in localStorage
    localStorage.setItem("userInfo", JSON.stringify(data.user));

  } catch (err) {
    console.error("Failed to display user info:", err);
  }
}

////////////////////
// Profile Posts //
//////////////////
async function loadPosts() {
  const myPostsList = document.querySelector(".user-profile__my-posts__list");

  try {
    // Get current user from localStorage (we assume that the user info is already fetched and saved)
    const cachedUser = localStorage.getItem("userInfo");
    if (!cachedUser) throw new Error("User not found in localStorage");

    const user = JSON.parse(cachedUser);
    const userId = user.id;

    // Get posts by user
    const postsRes = await fetch(`${API_BASE_URL}/users/${userId}/posts`, {
      credentials: "include",
    });

    if (!postsRes.ok) throw new Error("Failed to fetch posts");

    const posts = await postsRes.json();
    renderPosts(posts, myPostsList);
  } catch (err) {
    console.error("Load posts error:", err);
    myPostsList.innerHTML = "<p>Failed to load posts.</p>";
  }
}

function renderPosts(posts, container) {
  container.innerHTML = "";

  posts.forEach((post) => {
    const postDiv = document.createElement("div");
    postDiv.className = "post";

    const content = document.createElement("p");
    content.textContent = post.content;

    const actions = document.createElement("div");
    actions.className = "post-actions";

    const editBtn = document.createElement("button");
    editBtn.textContent = "Edit";
    editBtn.className = "edit-btn";
    editBtn.dataset.id = post.id;

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";
    deleteBtn.className = "delete-btn";
    deleteBtn.dataset.id = post.id;

    actions.appendChild(editBtn);
    actions.appendChild(deleteBtn);

    postDiv.appendChild(content);
    postDiv.appendChild(actions);
    container.appendChild(postDiv);
  });

  // Attach event listeners AFTER rendering
  document.querySelectorAll(".edit-btn").forEach((btn) => {
    btn.addEventListener("click", handleEdit);
  });

  document.querySelectorAll(".delete-btn").forEach((btn) => {
    btn.addEventListener("click", handleDelete);
  });
}

async function handleEdit(event) {
  const postId = event.target.dataset.id;

  const newContent = prompt("Enter new content:");

  if (newContent) {
    try {
      const res = await fetch(`${API_BASE_URL}/posts/${postId}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          content: newContent,
        }),
      });

      if (!res.ok) throw new Error("Failed to update post");

      alert("Post updated!");
      loadPosts();
    } catch (err) {
      console.error("Edit error:", err);
    }
  }
}

async function handleDelete(event) {
  const postId = event.target.dataset.id;

  if (confirm("Are you sure you want to delete this post?")) {
    try {
      const res = await fetch(`${API_BASE_URL}/posts/${postId}`, {
        method: "DELETE",
        credentials: "include",
      });

      if (!res.ok) throw new Error("Failed to delete post");
      alert("Post deleted!");
      loadPosts();
    } catch (err) {
      console.error("Delete error:", err);
    }
  }
}

// Handle cached user and load data on page load
window.addEventListener("DOMContentLoaded", () => {
  const cachedUser = localStorage.getItem("userInfo");

  // Call functions to display user info and posts
  displayUserInfo();
  loadPosts();
});
