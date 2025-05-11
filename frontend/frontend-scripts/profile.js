const API_BASE_URL =
  // "https://idg2001-o1-social-networking-service.onrender.com";  // Render
  "http://127.0.0.1:8000"; // Local dev

/////////////////////////////
// Navbar auth Link Logic //
///////////////////////////
window.addEventListener("DOMContentLoaded", () => {
  const authLink = document.getElementById("auth-link"); 

  fetch(`${API_BASE_URL}/auth/profile`, {
    credentials: "include", // sends the session_id cookie
  })
    .then((res) => {
      if (!res.ok) throw new Error("Not logged in");
      return res.json();
    })
    .then((data) => {
      authLink.href = `/frontend/profile.html?user_id=${data.user_id}`;
      authLink.innerHTML = `
      <img src="assets/profile-icon.svg" 
      alt="Profile Icon" 
      style="width: 25px; vertical-align: middle; margin-right: 6px;"> 
      Profile
      `;
    })
    .catch((err) => {
      // Not logged in — leave as Login
      console.warn("User not logged in or profile fetch failed:", err);
      authLink.href = "/frontend/login_signup.html";
      authLink.textContent = "Login";
    });
});

////////////////////////////
// Display Profile info ///
//////////////////////////
async function displayUserInfo() {
  try {
  const res = await fetch(`${API_BASE_URL}/auth/profile`, {
    credentials: "include", // sends the session_id cookie
  }); 

  if (!res.ok) throw new Error("No user details found");

  const data = await res.json();

    const userImage = document.querySelector(".user-profile__info__user-image");
    const userName = document.querySelector(".user-profile__info__username");

    userImage.src = "/frontend/assets/profile-icon-blue.svg";
    userImage.alt = "Profile image";
    userImage.style.width = "80px";
    userImage.style.borderRadius = "50%";

    
    userName.textContent = data.username || "Unnamed user";
  } catch(err) {
    console.error("Failed to display user info:", err);
  }
}

////////////////////
// Profile Posts //
//////////////////