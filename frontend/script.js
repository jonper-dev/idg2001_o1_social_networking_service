
////////////Fast copypaste code for future use


const API_BASE_URL = "http://127.0.0.1:8000/api";  // Change this if deployed

// Signup Function
function signup() {
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch(`${API_BASE_URL}/users/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password_hash: password })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("signup-message").innerText = data.message || "Signup failed!";
    })
    .catch(error => console.error("Error:", error));
}

// Post a Tweet
function postTweet() {
    const content = document.getElementById("tweet-content").value;
    const user_id = 1;  // For simplicity, assuming user_id = 1

    fetch(`${API_BASE_URL}/tweets/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id, content })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("tweet-message").innerText = data.message || "Tweet failed!";
        loadTweets();
    })
    .catch(error => console.error("Error:", error));
}

// Load Tweets
function loadTweets() {
    fetch(`${API_BASE_URL}/tweets/`)
    .then(response => response.json())
    .then(tweets => {
        const tweetList = document.getElementById("tweet-list");
        tweetList.innerHTML = "";

        tweets.forEach(tweet => {
            const tweetElement = document.createElement("div");
            tweetElement.classList.add("tweet");
            tweetElement.innerHTML = `<strong>@${tweet.username}</strong>: ${tweet.content} <small>(${tweet.timestamp})</small>`;
            tweetList.appendChild(tweetElement);
        });
    })
    .catch(error => console.error("Error loading tweets:", error));
}

// Load tweets on page load
window.onload = loadTweets;

// Run an api in the terminal by typing "uvicorn main:app --reload"
// Open index.html in a browser: python -m http.server 8080 says chatgpt