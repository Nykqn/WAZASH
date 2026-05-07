const API_BASE = '/api/v1';
const API_HEALTH = '/health';
let currentSection = null;

// ===== TOKENS =====

function getToken() {
    return localStorage.getItem('wazash_token');
}

function setToken(token) {
    localStorage.setItem('wazash_token', token);
}

function removeToken() {
    localStorage.removeItem('wazash_token');
}

function isTokenExpired() {
    const token = getToken();
    if (!token) return true;
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        return payload.exp < Math.floor(Date.now() / 1000);
    } catch {
        return true;
    }
}

// ===== TOAST NOTIFICATIONS =====

function showToast(message, type = 'info') {
    const icons = { success: '\u2713', error: '\u2717', warning: '\u26A0', info: '\u2139' };
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <span class="toast-icon">${icons[type] || icons.info}</span>
        <span class="toast-body">${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">&times;</button>
    `;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(40px)';
        toast.style.transition = 'all .3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// ===== SESSION =====

function updateStatus(connected) {
    const el = document.getElementById('status');
    el.textContent = connected ? 'Connect\u00e9' : 'D\u00e9connect\u00e9';
    el.className = 'connection-badge ' + (connected ? 'connected' : 'disconnected');
}

function handleAuthError() {
    removeToken();
    updateStatus(false);
    document.getElementById('login-section').classList.remove('hidden');
    document.getElementById('dashboard-section').classList.add('hidden');
    showToast('Session expir\u00e9e, reconnectez-vous', 'warning');
}

// ===== LOGIN =====

document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const btn = e.target.querySelector('button[type="submit"]');
    btn.disabled = true;
    btn.textContent = 'Connexion...';
    try {
        const resp = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        if (!resp.ok) throw new Error('Identifiants invalides');
        const data = await resp.json();
        setToken(data.access_token);
        updateStatus(true);
        document.getElementById('login-section').classList.add('hidden');
        document.getElementById('dashboard-section').classList.remove('hidden');
        document.getElementById('login-error').textContent = '';
        showSection('dashboard');
        checkHealth();
        showToast('Connect\u00e9 en tant que ' + email, 'success');
    } catch (err) {
        document.getElementById('login-error').textContent = err.message;
    } finally {
        btn.disabled = false;
        btn.textContent = 'Connexion';
    }
});

function restoreSession() {
    if (isTokenExpired()) {
        removeToken();
        return;
    }
    updateStatus(true);
    document.getElementById('login-section').classList.add('hidden');
    document.getElementById('dashboard-section').classList.remove('hidden');
    showSection('dashboard');
    checkHealth();
}

function logout() {
    removeToken();
    handleAuthError();
    showToast('D\u00e9connect\u00e9', 'info');
}

// ===== NAVIGATION =====

function showSection(section) {
    document.querySelectorAll('.sidebar-nav button').forEach(b => b.classList.remove('active'));
    const btn = document.querySelector(`.sidebar-nav button[data-section="${section}"]`);
    if (btn) btn.classList.add('active');
    if (currentSection) document.getElementById(currentSection).classList.remove('active');
    currentSection = section;
    document.getElementById(section).classList.add('active');
    if (sectionLoaders[section]) {
        setTimeout(sectionLoaders[section], 50);
    }
}

// ===== API FETCH =====

async function apiFetch(url, options = {}) {
    const headers = { 'Content-Type': 'application/json' };
    const token = getToken();
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const resp = await fetch(url, { ...options, headers });
    if (resp.status === 401) {
        handleAuthError();
        throw new Error('Session expir\u00e9e');
    }
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    return resp.json();
}

// ===== DASHBOARD =====

async function loadDashboard() {
    try {
        const [heartbeats, events, alerts, assets, correlations] = await Promise.all([
            apiFetch(`${API_BASE}/heartbeats`),
            apiFetch(`${API_BASE}/events`),
            apiFetch(`${API_BASE}/alerts/`),
            apiFetch(`${API_BASE}/assets/`),
            apiFetch(`${API_BASE}/correlations`),
        ]);
        const hbUp = heartbeats.filter(h => h.status === 'up').length;
        const hbDown = heartbeats.filter(h => h.status === 'down').length;
        const hbPct = heartbeats.length ? Math.round(hbUp / heartbeats.length * 100) : 0;
        const critAlerts = alerts.filter(a => a.severity === 'critical').length;
        const highAlerts = alerts.filter(a => a.severity === 'high').length;
        const activeAssets = assets.filter(a => a.status === 'active').length;
        buildStatsRow('dash-stats', [
            { label: 'Heartbeats', value: heartbeats.length, color: 'var(--text-info)' },
            { label: 'Up', value: hbUp, color: 'var(--text-success)', sub: `${hbPct}% dispo` },
            { label: 'Down', value: hbDown, color: 'var(--text-danger)' },
            { label: 'Événements', value: events.length, color: 'var(--text-warning)' },
            { label: 'Alertes', value: alerts.length, color: critAlerts > 0 ? 'var(--text-danger)' : 'var(--text-info)' },
            { label: 'Actifs', value: assets.length, color: 'var(--text-success)', sub: `${activeAssets} actifs` },
            { label: 'Corrélations', value: correlations.length, color: 'var(--text-info)' },
        ]);
        document.getElementById('dash-hb-detail').innerHTML = `
            <div class="metric"><span>Total</span><span class="metric-value">${heartbeats.length}</span></div>
            <div class="metric"><span style="color:var(--text-success)">Up</span><span class="metric-value" style="color:var(--text-success)">${hbUp}</span></div>
            <div class="metric"><span style="color:var(--text-danger)">Down</span><span class="metric-value" style="color:var(--text-danger)">${hbDown}</span></div>
        `;
        document.getElementById('dash-ev-detail').innerHTML = `
            <div class="metric"><span>Total</span><span class="metric-value">${events.length}</span></div>
        `;
        document.getElementById('dash-alert-detail').innerHTML = `
            <div class="metric"><span>Total</span><span class="metric-value">${alerts.length}</span></div>
            <div class="metric"><span style="color:var(--text-danger)">Critiques</span><span class="metric-value" style="color:var(--text-danger)">${critAlerts}</span></div>
            <div class="metric"><span style="color:var(--text-warning)">Élevées</span><span class="metric-value" style="color:var(--text-warning)">${highAlerts}</span></div>
        `;
        document.getElementById('dash-asset-detail').innerHTML = `
            <div class="metric"><span>Total</span><span class="metric-value">${assets.length}</span></div>
            <div class="metric"><span style="color:var(--text-success)">Actifs</span><span class="metric-value" style="color:var(--text-success)">${activeAssets}</span></div>
            <div class="metric"><span style="color:var(--text-tertiary)">Inactifs</span><span class="metric-value">${assets.length - activeAssets}</span></div>
        `;
        document.getElementById('dash-correlation-detail').innerHTML = `
            <div class="metric"><span>Total</span><span class="metric-value">${correlations.length}</span></div>
            <div class="metric"><span>Événements corrélés</span><span class="metric-value">${correlations.reduce((s, c) => s + c.event_count, 0)}</span></div>
        `;
    } catch (err) {
        showToast('Dashboard: ' + err.message, 'error');
    }
}

// ===== HEALTH =====

async function checkHealth() {
    const dot = document.getElementById('health-dot');
    const label = document.getElementById('health-label');
    try {
        const resp = await fetch(API_HEALTH);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = await resp.json();
        dot.style.color = 'var(--text-success)';
        label.textContent = `OK \u2014 ${data.service}`;
    } catch (err) {
        dot.style.color = 'var(--text-danger)';
        label.textContent = 'Indisponible';
    }
}

// ===== TOGGLE FORM =====

function toggleForm(id) {
    document.getElementById(id).classList.toggle('hidden');
}

// ===== STATS CARD =====

function buildStatsRow(containerId, stats) {
    const el = document.getElementById(containerId);
    if (!el) return;
    el.innerHTML = stats.map(s => `
        <div class="stat-card">
            <div class="stat-label">${s.label}</div>
            <div class="stat-value" style="color:${s.color || 'var(--text-primary)'}">${s.value}</div>
            ${s.sub ? `<div class="stat-sub">${s.sub}</div>` : ''}
        </div>
    `).join('');
}

// ===== HEARTBEATS =====

async function loadHeartbeats() {
    try {
        const data = await apiFetch(`${API_BASE}/heartbeats`);
        const container = document.getElementById('hb-container');
        const table = document.getElementById('hb-table');
        const tbody = document.getElementById('hb-tbody');
        const empty = container.querySelector('.empty-state');
        if (data.length === 0) {
            empty.classList.remove('hidden');
            table.classList.add('hidden');
            buildStatsRow('hb-stats', [{ label: 'Heartbeats', value: '0', color: 'var(--text-tertiary)' }]);
            return;
        }
        empty.classList.add('hidden');
        table.classList.remove('hidden');
        tbody.innerHTML = '';
        let up = 0, down = 0;
        data.forEach(hb => {
            if (hb.status === 'up') up++; else down++;
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${hb.id}</td>
                <td>${hb.endpoint_id}</td>
                <td>${new Date(hb.timestamp).toLocaleString('fr-FR')}</td>
                <td><span class="badge badge-${hb.status}">${hb.status}</span></td>
            `;
            tbody.appendChild(row);
        });
        buildStatsRow('hb-stats', [
            { label: 'Total', value: data.length },
            { label: 'Up', value: up, color: 'var(--text-success)' },
            { label: 'Down', value: down, color: 'var(--text-danger)' },
            { label: 'Disponibilit\u00e9', value: data.length ? `${Math.round(up/data.length*100)}%` : 'N/A', color: 'var(--text-info)' },
        ]);
    } catch (err) {
        showToast('Heartbeats: ' + err.message, 'error');
    }
}

// ===== EVENTS =====

async function loadEvents() {
    try {
        const data = await apiFetch(`${API_BASE}/events`);
        const container = document.getElementById('ev-container');
        const table = document.getElementById('ev-table');
        const tbody = document.getElementById('ev-tbody');
        const empty = container.querySelector('.empty-state');
        if (data.length === 0) {
            empty.classList.remove('hidden');
            table.classList.add('hidden');
            buildStatsRow('ev-stats', [{ label: '\u00c9v\u00e9nements', value: '0', color: 'var(--text-tertiary)' }]);
            return;
        }
        empty.classList.add('hidden');
        table.classList.remove('hidden');
        tbody.innerHTML = '';
        const types = {};
        data.forEach(ev => {
            types[ev.event_type] = (types[ev.event_type] || 0) + 1;
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${ev.id}</td>
                <td>${ev.endpoint_id}</td>
                <td>${ev.event_type}</td>
                <td><span class="badge badge-${ev.severity}">${ev.severity}</span></td>
                <td>${new Date(ev.timestamp).toLocaleString('fr-FR')}</td>
            `;
            tbody.appendChild(row);
        });
        const typeLabels = Object.entries(types).slice(0, 3).map(([k, v]) => `${k}: ${v}`).join(', ');
        buildStatsRow('ev-stats', [
            { label: 'Total', value: data.length },
            { label: 'Types', value: Object.keys(types).length, color: 'var(--text-info)', sub: typeLabels },
        ]);
    } catch (err) {
        showToast('Events: ' + err.message, 'error');
    }
}

// ===== ASSETS =====

async function loadAssets() {
    try {
        const data = await apiFetch(`${API_BASE}/assets/`);
        const container = document.getElementById('asset-container');
        const table = document.getElementById('asset-table');
        const tbody = document.getElementById('asset-tbody');
        const empty = container.querySelector('.empty-state');
        if (data.length === 0) {
            empty.classList.remove('hidden');
            table.classList.add('hidden');
            buildStatsRow('asset-stats', [{ label: 'Actifs', value: '0', color: 'var(--text-tertiary)' }]);
            return;
        }
        empty.classList.add('hidden');
        table.classList.remove('hidden');
        tbody.innerHTML = '';
        let active = 0, inactive = 0;
        data.forEach(asset => {
            if (asset.status === 'active') active++; else inactive++;
            const lastSeen = asset.last_seen ? new Date(asset.last_seen).toLocaleString('fr-FR') : 'Jamais';
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${asset.endpoint_id}</strong></td>
                <td>${asset.hostname || '-'}</td>
                <td>${asset.ip_address || '-'}</td>
                <td>${asset.os || '-'}</td>
                <td><span class="badge badge-${asset.status}">${asset.status}</span></td>
                <td>${lastSeen}</td>
                <td><button onclick="deleteAsset('${asset.endpoint_id}')" class="btn btn-danger" style="padding:3px 10px;font-size:12px;">Supprimer</button></td>
            `;
            tbody.appendChild(row);
        });
        buildStatsRow('asset-stats', [
            { label: 'Total', value: data.length },
            { label: 'Actifs', value: active, color: 'var(--text-success)' },
            { label: 'Inactifs', value: inactive, color: 'var(--text-danger)' },
        ]);
    } catch (err) {
        showToast('Assets: ' + err.message, 'error');
    }
}

async function deleteAsset(endpointId) {
    if (!confirm(`Supprimer l'asset ${endpointId} ?`)) return;
    try {
        const token = getToken();
        const resp = await fetch(`${API_BASE}/assets/${endpointId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (resp.status === 204) {
            showToast(`Asset ${endpointId} supprim\u00e9`, 'success');
            loadAssets();
        } else throw new Error(`HTTP ${resp.status}`);
    } catch (err) {
        showToast('Suppression: ' + err.message, 'error');
    }
}

document.getElementById('asset-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        endpoint_id: document.getElementById('asset-endpoint-id').value,
        hostname: document.getElementById('asset-hostname').value || null,
        ip_address: document.getElementById('asset-ip').value || null,
        os: document.getElementById('asset-os').value || null,
    };
    try {
        await apiFetch(`${API_BASE}/assets/`, { method: 'POST', body: JSON.stringify(payload) });
        showToast('Asset ajout\u00e9', 'success');
        toggleForm('asset-form-panel');
        loadAssets();
    } catch (err) {
        showToast('Erreur: ' + err.message, 'error');
    }
});

// ===== HEARTBEAT FORM =====

document.getElementById('hb-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        endpoint_id: document.getElementById('hb-endpoint').value,
        timestamp: document.getElementById('hb-timestamp').value,
        status: document.getElementById('hb-status').value
    };
    try {
        await apiFetch(`${API_BASE}/heartbeat`, { method: 'POST', body: JSON.stringify(payload) });
        showToast('Heartbeat envoy\u00e9', 'success');
        toggleForm('hb-form-panel');
        loadHeartbeats();
        loadAssets();
    } catch (err) {
        showToast('Erreur: ' + err.message, 'error');
    }
});

// ===== EVENT FORM =====

document.getElementById('ev-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        endpoint_id: document.getElementById('ev-endpoint').value,
        timestamp: document.getElementById('ev-timestamp').value,
        event_type: document.getElementById('ev-type').value,
        severity: document.getElementById('ev-severity').value,
        details: {}
    };
    try {
        await apiFetch(`${API_BASE}/events`, { method: 'POST', body: JSON.stringify(payload) });
        showToast('\u00c9v\u00e9nement envoy\u00e9', 'success');
        toggleForm('ev-form-panel');
        loadEvents();
        loadAlerts();
    } catch (err) {
        showToast('Erreur: ' + err.message, 'error');
    }
});

// ===== ALERTS =====

async function loadAlerts() {
    try {
        const data = await apiFetch(`${API_BASE}/alerts/`);
        const container = document.getElementById('alert-container');
        const table = document.getElementById('alerts-table');
        const tbody = document.getElementById('alerts-tbody');
        const empty = container.querySelector('.empty-state');
        if (data.length === 0) {
            empty.classList.remove('hidden');
            table.classList.add('hidden');
            buildStatsRow('alert-stats', [{ label: 'Alertes', value: '0', color: 'var(--text-tertiary)' }]);
            return;
        }
        empty.classList.add('hidden');
        table.classList.remove('hidden');
        tbody.innerHTML = '';
        let critical = 0, high = 0;
        data.forEach(alert => {
            if (alert.severity === 'critical') critical++;
            else if (alert.severity === 'high') high++;
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${alert.id}</td>
                <td>${alert.rule_name}</td>
                <td><span class="badge badge-${alert.severity}">${alert.severity}</span></td>
                <td>${new Date(alert.timestamp).toLocaleString('fr-FR')}</td>
                <td><span class="badge-${alert.status}">${alert.status}</span></td>
            `;
            tbody.appendChild(row);
        });
        buildStatsRow('alert-stats', [
            { label: 'Total', value: data.length },
            { label: 'Critiques', value: critical, color: 'var(--text-danger)' },
            { label: '\u00c9lev\u00e9es', value: high, color: 'var(--text-warning)' },
        ]);
    } catch (err) {
        showToast('Alertes: ' + err.message, 'error');
    }
}

// ===== AUDIT =====

async function loadAudit() {
    try {
        const data = await apiFetch(`${API_BASE}/audit/`);
        const container = document.getElementById('audit-container');
        const table = document.getElementById('audit-table');
        const tbody = document.getElementById('audit-tbody');
        const empty = container.querySelector('.empty-state');
        if (data.length === 0) {
            empty.classList.remove('hidden');
            table.classList.add('hidden');
            return;
        }
        empty.classList.add('hidden');
        table.classList.remove('hidden');
        tbody.innerHTML = '';
        data.forEach(entry => {
            const user = entry.user_email || '\u2014';
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${entry.id}</td>
                <td>${new Date(entry.timestamp).toLocaleString('fr-FR')}</td>
                <td><strong>${entry.action}</strong></td>
                <td>${user}</td>
                <td style="max-width:300px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="${entry.details}">${entry.details}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (err) {
        showToast('Audit: ' + err.message, 'error');
    }
}

// ===== CORRELATIONS =====

async function loadCorrelations() {
    try {
        const data = await apiFetch(`${API_BASE}/correlations`);
        const container = document.getElementById('correlation-container');
        const table = document.getElementById('correlations-table');
        const tbody = document.getElementById('correlations-tbody');
        if (!data || data.length === 0) {
            container.querySelector('.empty-state').classList.remove('hidden');
            table.classList.add('hidden');
            return;
        }
        container.querySelector('.empty-state').classList.add('hidden');
        table.classList.remove('hidden');
        tbody.innerHTML = '';
        data.forEach(c => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${c.id}</td>
                <td>${c.correlation_type}</td>
                <td><strong>${c.source_ip}</strong></td>
                <td>${c.target_ip || '-'}</td>
                <td>${c.event_type || '-'}</td>
                <td><span class="badge badge-warning">${c.event_count}</span></td>
                <td>${new Date(c.window_start).toLocaleString('fr-FR')}</td>
                <td>${new Date(c.window_end).toLocaleString('fr-FR')}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (err) {
        showToast('Corrélations: ' + err.message, 'error');
    }
}

// ===== SECTIONS MAP FOR AUTO-LOAD =====

const sectionLoaders = {
    dashboard: loadDashboard,
    heartbeats: loadHeartbeats,
    events: loadEvents,
    assets: loadAssets,
    alerts: loadAlerts,
    audit: loadAudit,
    correlations: loadCorrelations,
};

// ===== INIT =====

window.onload = () => {
    const now = new Date().toISOString().slice(0, 16);
    document.getElementById('hb-timestamp').value = now;
    document.getElementById('ev-timestamp').value = now;
    restoreSession();
};
