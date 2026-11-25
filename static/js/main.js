/**
 * DeployFlow — Main Dashboard JavaScript
 * Handles sidebar toggle, live clock, animations, and interactive elements
 */

// ─── Sidebar Toggle ─────────────────────────────────────────────────────────
const sidebar = document.getElementById('sidebar');
const toggle  = document.getElementById('sidebarToggle');
const wrapper = document.querySelector('.main-wrapper');

if (toggle && sidebar) {
  toggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });

  // Close sidebar when clicking outside on mobile
  document.addEventListener('click', (e) => {
    if (window.innerWidth < 992 &&
        sidebar.classList.contains('open') &&
        !sidebar.contains(e.target) &&
        !toggle.contains(e.target)) {
      sidebar.classList.remove('open');
    }
  });
}

// ─── Live Clock ──────────────────────────────────────────────────────────────
function updateClock() {
  const el = document.getElementById('liveTime');
  if (!el) return;
  const now = new Date();
  el.textContent = now.toUTCString().replace(' GMT', ' UTC');
}
updateClock();
setInterval(updateClock, 1000);

// ─── Page Entrance Animation ─────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Animate pipeline stages if present
  const stages = document.querySelectorAll('.pipeline-stage');
  stages.forEach((el, i) => {
    setTimeout(() => el.classList.add('stage-visible'), 100 + i * 180);
  });

  // Animate KPI cards
  document.querySelectorAll('.kpi-card, .container-card, .service-card, .tech-card').forEach((el, i) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(16px)';
    setTimeout(() => {
      el.style.transition = 'opacity .4s ease, transform .4s ease';
      el.style.opacity = '1';
      el.style.transform = 'translateY(0)';
    }, 60 + i * 60);
  });

  // Add active class to current nav link based on URL
  const path = window.location.pathname;
  document.querySelectorAll('.sidebar-nav .nav-link').forEach(link => {
    if (link.getAttribute('href') === path) {
      link.classList.add('active');
    }
  });
});

// ─── Bootstrap Tooltips ──────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));
});

// ─── Auto-dismiss alerts ──────────────────────────────────────────────────────
document.querySelectorAll('.alert-dismissible').forEach(alert => {
  setTimeout(() => {
    const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
    if (bsAlert) bsAlert.close();
  }, 8000);
});

// ─── Health Endpoint Ping (every 60s) ────────────────────────────────────────
function pingHealth() {
  fetch('/health')
    .then(r => r.json())
    .then(data => {
      const dot = document.querySelector('.pulse-dot');
      if (dot) {
        dot.style.background = data.status === 'ok' ? '#22c55e' : '#ef4444';
      }
    })
    .catch(() => {
      const dot = document.querySelector('.pulse-dot');
      if (dot) dot.style.background = '#ef4444';
    });
}
pingHealth();
setInterval(pingHealth, 60000);

// ─── Table Row Highlight ──────────────────────────────────────────────────────
document.querySelectorAll('.deployments-table tbody tr').forEach(row => {
  row.style.cursor = 'default';
  row.addEventListener('mouseenter', () => {
    row.style.transition = 'background .15s';
  });
});

console.log('%c🚀 DeployFlow Dashboard', 'color:#6366f1;font-size:1.2rem;font-weight:800');
console.log('%cCI/CD Pipeline — GitHub Actions + Docker + Render', 'color:#06b6d4');
