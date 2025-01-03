// Update server time
function updateServerTime() {
  const now = new Date();
  document.getElementById("serverTime").textContent = now.toISOString();
}

setInterval(updateServerTime, 1000);
updateServerTime();

// Test login functionality
async function testLogin() {
  const statusDiv = document.getElementById("status");
  const resultDiv = document.getElementById("result");
  const loginButton = document.querySelector(".primary");
  const getTrendsButton = document.querySelector(".secondary");

  try {
    statusDiv.innerHTML = "Testing login...";
    statusDiv.className = "status-display";
    loginButton.disabled = true;

    const response = await fetch("/test_login");
    const data = await response.json();

    console.log("Login response:", data);

    if (data.success) {
      statusDiv.innerHTML = `✅ ${data.message}`;
      statusDiv.className = "status-display success";
      getTrendsButton.disabled = false;
    } else {
      statusDiv.innerHTML = `❌ ${data.error}`;
      statusDiv.className = "status-display error";
      getTrendsButton.disabled = true;
    }

    resultDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
  } catch (error) {
    console.error("Error:", error);
    statusDiv.innerHTML = `❌ Error: ${error.message}`;
    statusDiv.className = "status-display error";
    getTrendsButton.disabled = true;
    resultDiv.innerHTML = `<pre class="error">Error: ${error.message}</pre>`;
  } finally {
    loginButton.disabled = false;
  }
}

// Get trends functionality (to be implemented later)
async function getTrends() {
  const statusDiv = document.getElementById("status");
  const resultDiv = document.getElementById("result");

  statusDiv.innerHTML = "This feature will be implemented soon...";
  resultDiv.innerHTML = "";
}
