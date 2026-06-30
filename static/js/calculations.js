function initFuelCalc() {
  const form = document.getElementById('fuelCalcForm');
  if (!form && !document.getElementById('calc_km')) return;

  const kmInput    = document.getElementById('calc_km');
  const litreInput = document.getElementById('calc_litres');
  const priceInput = document.getElementById('calc_price');
  const resultEl   = document.getElementById('calcResult');
  const mileageEl  = document.getElementById('resultMileage');
  const costEl     = document.getElementById('resultCost');

  function calculate() {
    const km     = parseFloat(kmInput.value)    || 0;
    const litres = parseFloat(litreInput.value) || 0;
    const price  = parseFloat(priceInput.value) || 0;
    if (km <= 0 || litres <= 0) { resultEl.style.display = 'none'; return; }
    const mileage = (km / litres).toFixed(2);
    const cost    = (litres * price).toFixed(2);
    mileageEl.textContent = `${mileage} km/L`;
    costEl.textContent    = `NPR ${cost}`;
    resultEl.style.display = 'flex';
  }

  [kmInput, litreInput, priceInput].forEach(el => el && el.addEventListener('input', calculate));
}

function initBudgetAlert() {
  const budgetInput = document.getElementById('budget_limit');
  const totalEl     = document.getElementById('totalSpend');
  const alertEl     = document.getElementById('budgetAlert');
  if (!budgetInput || !totalEl || !alertEl) return;

  budgetInput.addEventListener('input', () => {
    const limit = parseFloat(budgetInput.value) || 0;
    const total = parseFloat(totalEl.dataset.total) || 0;
    if (limit > 0 && total >= limit * 0.8) {
      alertEl.style.display = 'block';
      alertEl.textContent = total >= limit
        ? `Budget exceeded! Spent ${total.toFixed(0)} / ${limit.toFixed(0)} NPR`
        : `Approaching limit — ${((total / limit) * 100).toFixed(0)}% used`;
      alertEl.className = total >= limit ? 'alert alert-danger' : 'alert alert-info';
    } else {
      alertEl.style.display = 'none';
    }
  });
}

const CHECKLIST_ITEMS = ['Tyre Pressure', 'Engine Oil', 'Brake Fluid', 'Chain Lube', 'Lights & Horn', 'Mirrors', 'Fuel Level', 'Gear / Helmet'];

function initChecklist() {
  const container  = document.getElementById('checklistItems');
  const progressEl = document.getElementById('checkProgress');
  const labelEl    = document.getElementById('checkLabel');
  if (!container) return;
  const state = new Array(CHECKLIST_ITEMS.length).fill(false);

  function render() {
    container.innerHTML = '';
    CHECKLIST_ITEMS.forEach((name, idx) => {
      const item = document.createElement('div');
      item.className = `check-item${state[idx] ? ' done' : ''}`;
      item.innerHTML = `<div class="check-icon"></div><span>${name}</span>`;
      item.addEventListener('click', () => { state[idx] = !state[idx]; render(); });
      container.appendChild(item);
    });
    const done = state.filter(Boolean).length;
    const pct  = Math.round((done / state.length) * 100);
    if (progressEl) progressEl.style.width = `${pct}%`;
    if (labelEl)    labelEl.textContent = `${done} / ${state.length} checked`;
  }
  render();
}

function initNavbar() {
  const burger = document.getElementById('navBurger');
  const links  = document.getElementById('navLinks');
  if (!burger || !links) return;
  burger.addEventListener('click', () => links.classList.toggle('open'));
}

function openModal(id)  { document.getElementById(id)?.classList.add('open'); }
function closeModal(id) { document.getElementById(id)?.classList.remove('open'); }

document.addEventListener('click', e => {
  if (e.target.classList.contains('modal-backdrop')) e.target.classList.remove('open');
});

function initFlashDismiss() {
  document.querySelectorAll('.alert').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity 0.4s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 400);
    }, 3500);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initFuelCalc();
  initBudgetAlert();
  initChecklist();
  initFlashDismiss();
});