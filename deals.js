async function loadDeals() {
  const tbody = document.getElementById('deals-body');
  try {
    const res = await fetch('deals.json');
    const deals = await res.json();
    tbody.innerHTML = deals.map(d => `
      <tr>
        <td><img src="${d.img}" alt="" /><br/><strong>${d.title}</strong></td>
        <td>${d.price}</td>
        <td>${d.merchant||'Amazon'}</td>
        <td>${d.expires||'N/A'}</td>
        <td><a href="${d.url}" target="_blank" class="btn">View Deal</a></td>
      </tr>
    `).join('');
  } catch {
    tbody.innerHTML = '<tr><td colspan="5">Failed to load deals</td></tr>';
  }
}
document.addEventListener('DOMContentLoaded', loadDeals);
