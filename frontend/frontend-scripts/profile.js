const API_BASE_URL =
  // "https://idg2001-o1-social-networking-service.onrender.com";  // Render
  "http://127.0.0.1:8000"; // Local dev

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
    // const email = document.querySelector(".user-profile__info__email");

    userImage.src = "/frontend/assets/profile-icon-blue.svg";
    userImage.alt = "Profile image";

    userName.textContent = data.user?.name || "Unnamed user";
    // email.textContent = data.user?.email || "No email for this user"
  } catch(err) {
    console.error("Failed to display user info:", err);
  }
}

////////////////////
// Profile Posts //
//////////////////

// async function loadPosts() {
//   
// Code for displaying, editing and deleting posts
//
// }

window.addEventListener("DOMContentLoaded", () => {
  displayUserInfo();
  // loadPosts();
});
