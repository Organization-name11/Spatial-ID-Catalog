let repos = [];
let starsDesc = true;

/* JSON読み込み */
fetch("data/catalog.json")
  .then(res => {
    if (!res.ok) throw new Error("catalog.json not found");
    return res.json();
  })
  .then(data => {
    repos = data;
    renderTable(repos);
  })
  .catch(err => {
    console.error(err);
    document.querySelector("#catalog tbody").innerHTML =
      "<tr><td colspan='13'>catalog.json を読み込めませんでした</td></tr>";
  });

/* 表描画 */
function renderTable(data) {
  const tbody = document.querySelector("#catalog tbody");
  tbody.innerHTML = "";

  data.forEach((repo, i) => {
    const tr = document.createElement("tr");

    tr.innerHTML = `
      <td>${i + 1}</td>
      <td>${repo.full_name || ""}</td>
      <td><a href="${repo.url}" target="_blank">Link</a></td>
      <td>${repo.description || ""}</td>
      <td>${repo.language || ""}</td>
      <td>${repo.stars || 0}</td>
      <td>${repo.updated_at ? repo.updated_at.slice(0,10) : ""}</td>
      <td>${repo.topics ? repo.topics.join(", ") : ""}</td>
      <td>${repo.license && repo.license.name ? repo.license.name : ""}</td>
      <td>${repo.fork ? "Yes" : "No"}</td>
      <td>${repo.open_issues_count || 0}</td>
      <td>${repo.watchers_count || 0}</td>
      <td>${repo.forks_count || 0}</td>
    `;

    tbody.appendChild(tr);
  });
}

/* Starsソート */
document.getElementById("sortStars").addEventListener("click", () => {
  repos.sort((a, b) => starsDesc ? (b.stars || 0) - (a.stars || 0) : (a.stars || 0) - (b.stars || 0));
  starsDesc = !starsDesc;
  renderTable(repos);
});
