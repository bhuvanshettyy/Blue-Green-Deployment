async function fetchPricing() {
  try {
    const res = await fetch('/pricing', {cache: 'no-store'});
    if (!res.ok) throw new Error('Fetch failed: ' + res.status);
    return await res.json();
  } catch (e) {
    console.error(e);
    return null;
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"})[c]);
}

function renderPricing(payload) {
  const meta = document.getElementById('meta');
  const plansDiv = document.getElementById('plans');
  if (!payload) {
    meta.textContent = 'Could not load pricing.';
    plansDiv.innerHTML = '';
    return;
  }
  meta.textContent = `Served version: ${payload.version}`;
  const plans = (payload.pricing && payload.pricing.plans) || [];
  plansDiv.innerHTML = plans.map(p => `
    <div class="card">
      <div class="plan-title">${escapeHtml(p.title)}</div>
      <div class="price">${escapeHtml(p.price)}</div>
      <ul>${(p.features || []).map(f => `<li>${escapeHtml(f)}</li>`).join('')}</ul>
    </div>
  `).join('');
}

(async function() {
  const payload = await fetchPricing();
  renderPricing(payload);
})();
