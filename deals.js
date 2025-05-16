// deals.js
document.addEventListener('DOMContentLoaded', () => {
  fetch('deals.json')
    .then(res => {
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      return res.json();
    })
    .then(deals => {
      const tbody = document.getElementById('deals-body');
      deals.forEach(deal => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><a href="${deal.link}" target="_blank" rel="noopener noreferrer">${deal.title}</a></td>
          <td>$${deal.price}</td>
          <td>Amazon</td>
          <td>—</td>
        `;
        tbody.appendChild(tr);
      });
    })
    .catch(err => {
      console.error('Failed to load deals:', err);
      const tbody = document.getElementById('deals-body');
      const tr = document.createElement('tr');
      tr.innerHTML = `<td colspan="4" style="color:red;">Error loading deals.</td>`;
      tbody.appendChild(tr);
    });
});
