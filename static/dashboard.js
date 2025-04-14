document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      window.location.href = "/login";
      return;
    }
  
    try {
      const res = await fetch("/api/websites", {
        headers: { Authorization: `Bearer ${token}` }
      });
  
      if (!res.ok) throw new Error("Failed to load websites");
  
      const data = await res.json();
      const container = document.getElementById("websites-list");
      container.innerHTML = "";
  
      data.websites.forEach((site) => {
        const div = document.createElement("div");
        div.innerHTML = `
          <h4>${site.name}</h4>
          <p>Industry: ${site.industry}</p>
          <a href="/preview/${site._id}" target="_blank">Preview</a>
          <button onclick="deleteWebsite('${site._id}')">Delete</button>
          <hr>
        `;
        container.appendChild(div);
      });
  
    } catch (err) {
      alert(err.message);
    }
  });
  
  async function deleteWebsite(id) {
    const token = localStorage.getItem("token");
    const confirmed = confirm("Are you sure you want to delete this website?");
    if (!confirmed) return;
  
    const res = await fetch(`/api/websites/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` }
    });
  
    if (res.ok) {
      location.reload();
    } else {
      alert("Failed to delete");
    }
  }
  
