let repoData = [];
let starSortDesc = true; // 初期は降順（人気順）

// JSON 読み込み
fetch('data/catalog.json')
  .then(response => {
    if (!response.ok) throw new Error("catalog.json の取得に失敗しました");
    return response.json();
  })
  .then(data => {
    repoData = data;
    sortByStars(); // 初期ソート
  })
  .catch(err => {
    console.error(err);
    const tbody = document.querySelector('#catalog tbody');
    tbody.innerHTML = `<tr><td colspan="13">データの読み込みに失敗しました</td></tr>`;
  });

// テーブル描画（通番付き）
function renderTable(data) {
  const tbody = document.querySelector('#catalog tbody');
  tbody.innerHTML = "";

  data.forEach((repo, index) => {
    const tr = document.createElement('tr');

    tr.innerHTML = `
      <td>${index + 1}</td>
      <td>${repo.full_name}</td>
      <td><a href="${repo.url}" target="_blank">Link</a></td>
      <td>${repo.description || ''}</td>
      <td>${repo.language || ''}</td>
      <td>${repo.stars || repo.stargazers_count || 0}</td>
      <td>${repo.updated_at ? repo.updated_at.slice(0,10) : ''}</td>
      <td>${repo.topics && repo.topics.length ? repo.topics.join(', ') : ''}</td>
      <td>${repo.license && repo.license.name ? repo.license.name : (repo.license || '')}</td>
      <td>${repo.fork ? 'Yes' : 'No'}</td>
      <td>${repo.open_issues_count || 0}</td>
      <td>${repo.watchers_count || 0}</td>
      <td>${repo.forks_count || 0}</td>
    `;

    tbody.appendChild(tr);
  });
}

// Stars ソート処理
function sortByStars() {
  repoData.sort((a, b) => {
    const aStars = a.stars || a.stargazers_count || 0;
    const bStars = b.stars || b.stargazers_count || 0;
    return starSortDesc ? bStars - aStars : aStars - bStars;
  });

  renderTable(repoData);

  const th = document.getElementById("sortStars");
  th.innerText = starSortDesc ? "⭐ Stars ▼" : "⭐ Stars ▲";
  starSortDesc = !starSortDesc;
}

// Stars 列クリックでソート
document.addEventListener("DOMContentLoaded", () => {
  const starHeader = document.getElementById("sortStars");
  if (starHeader) {
    starHeader.addEventListener("click", sortByStars);
  }
});
