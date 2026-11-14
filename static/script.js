/* — XSS himoyasi — */
/**
 * Foydalanuvchi/DB matnini HTML ichiga qo'yishdan oldin xavfsiz qiladi.
 * innerHTML bilan ishlaganda HAR DOIM shu funksiyadan o'tkazing.
 */
function esc(value) {
    return String(value ?? '').replace(/[&<>"']/g, ch => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[ch]));
}

/**
 * src/href uchun xavfsiz URL: faqat http(s), nisbiy yo'l yoki rasm data-URI.
 * javascript:, vbscript: kabi sxemalarni bloklaydi.
 */
function safeUrl(value) {
    const v = String(value ?? '').trim();
    if (!v) return '';
    if (/^(https?:\/\/|\/)/i.test(v)) return v;
    if (/^data:image\/(png|jpe?g|webp|gif);base64,/i.test(v)) return v;
    return '';
}

/** FastAPI xatosini foydalanuvchiga o'qishli matn qilib qaytaradi. */
function apiError(data, fallback) {
    if (!data) return fallback;
    if (typeof data.detail === 'string') return data.detail;
    if (Array.isArray(data.detail) && data.detail.length) {
        const first = data.detail[0] || {};
        const field = Array.isArray(first.loc) ? String(first.loc[first.loc.length - 1]) : '';
        const msg = first.msg || fallback;
        return field ? `${field}: ${msg}` : msg;
    }
    return fallback;
}

/* — Navbar holati — */
function updateNavbar() {
    const token = localStorage.getItem('access_token');
    const login = document.getElementById('login-link');
    const register = document.getElementById('register-link');
    const logout = document.getElementById('logout-link');
    const profile = document.getElementById('profile-link');
    const admin = document.getElementById('admin-link');
    const wishlist = document.getElementById('wishlist-link');
    const logged = !!token;
    if (login) login.style.display = logged ? 'none' : 'inline';
    if (register) register.style.display = logged ? 'none' : 'inline';
    if (logout) logout.style.display = logged ? 'inline' : 'none';
    if (profile) profile.style.display = logged ? 'inline' : 'none';
    if (wishlist) wishlist.style.display = logged ? 'inline' : 'none';
    if (admin && !logged) admin.style.display = 'none';
    if (logged) { updateCartBadge(); updateWishlistBadge(); }
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    showToast('Chiqdingiz', 'success');
    setTimeout(() => location.href = '/', 400);
}

function togglePassword(id, el) {
    const input = document.getElementById(id);
    if (!input) return;
    const isPw = input.type === 'password';
    input.type = isPw ? 'text' : 'password';
    if (el) el.textContent = isPw ? '🙈' : '👁️';
}

function toggleNav() {
    const nav = document.getElementById('nav-links');
    if (nav) nav.classList.toggle('open');
}

/* — Toast — */
function showToast(msg, type = 'success') {
    const t = document.getElementById('toast');
    if (!t) return;
    t.textContent = msg;
    t.className = 'toast ' + type;
    t.style.display = 'block';
    clearTimeout(t._timer);
    t._timer = setTimeout(() => t.style.display = 'none', 2600);
}

/* — Cart badge — */
async function updateCartBadge() {
    const token = localStorage.getItem('access_token');
    const badge = document.getElementById('cart-badge');
    if (!badge) return;
    if (!token) { badge.style.display = 'none'; return; }
    try {
        const res = await fetch('/cart/', { headers: { 'Authorization': 'Bearer ' + token } });
        if (!res.ok) { badge.style.display = 'none'; return; }
        const data = await res.json();
        const count = (data.items || []).reduce((s, i) => s + i.quantity, 0);
        badge.textContent = count;
        badge.style.display = count ? 'inline-block' : 'none';
    } catch { badge.style.display = 'none'; }
}

/* — Wishlist — */
const WISHLIST_KEY = 'wishlist_ids';

function wishlistIds() {
    try { return JSON.parse(localStorage.getItem(WISHLIST_KEY) || '[]'); }
    catch { return []; }
}

function saveWishlistIds(ids) {
    localStorage.setItem(WISHLIST_KEY, JSON.stringify(ids));
}

/**
 * Yurak tugmasining yagona holat chizuvchisi.
 * Boshqa funksiyalar ham faqat shuni ishlatadi — holat bir joyda boshqariladi.
 */
function setWishlistState(btn, isActive) {
    if (!btn) return;
    btn.classList.toggle('active', !!isActive);
    btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    btn.setAttribute('title', isActive ? t('wishlist.remove') : t('wishlist.add'));
    btn.textContent = isActive ? '♥' : '♡';
}

async function toggleWishlist(productId, btn) {
    const token = localStorage.getItem('access_token');
    if (!token) {
        showToast(t('auth.login_title') + '!', 'error');
        setTimeout(() => location.href = '/login-page', 700);
        return;
    }
    if (btn) btn.disabled = true;
    const isActive = btn ? btn.classList.contains('active') : false;

    const authHeaders = { 'Authorization': 'Bearer ' + token };
    try {
        if (isActive) {
            const res = await fetch('/wishlist/' + productId, { method: 'DELETE', headers: authHeaders });
            if (res.ok || res.status === 404) {
                saveWishlistIds(wishlistIds().filter(id => id !== productId));
                document.querySelectorAll('.heart-btn[data-pid="' + productId + '"]')
                    .forEach(b => setWishlistState(b, false));
                showToast(t('wishlist.removed'), 'success');
                updateWishlistBadge();
                if (typeof removeFromWishlistView === 'function') removeFromWishlistView(productId);
            } else {
                showToast(await errorText(res), 'error');
            }
        } else {
            const res = await fetch('/wishlist/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', ...authHeaders },
                body: JSON.stringify({ product_id: productId })
            });
            if (res.ok) {
                const ids = wishlistIds();
                if (!ids.includes(productId)) ids.push(productId);
                saveWishlistIds(ids);
                document.querySelectorAll('.heart-btn[data-pid="' + productId + '"]')
                    .forEach(b => setWishlistState(b, true));
                showToast(t('wishlist.added'), 'success');
                updateWishlistBadge();
            } else {
                showToast(await errorText(res), 'error');
            }
        }
    } catch {
        showToast(t('common.network'), 'error');
    } finally {
        if (btn) btn.disabled = false;
    }
}

/** Server xatosining haqiqiy sababini ko'rsatadi (jumboq "Xatolik" emas). */
async function errorText(res) {
    try {
        const data = await res.json();
        if (typeof data.detail === 'string') return data.detail;
    } catch { /* JSON emas */ }
    return `${t('common.error')} (${res.status})`;
}

async function fetchWishlistIds() {
    const token = localStorage.getItem('access_token');
    if (!token) return [];
    try {
        const res = await fetch('/wishlist/', { headers: { 'Authorization': 'Bearer ' + token } });
        if (!res.ok) return null;
        const data = await res.json();
        return (data.items || []).map(i => i.product_id);
    } catch { return null; }
}

async function updateWishlistBadge() {
    const token = localStorage.getItem('access_token');
    const badge = document.getElementById('wishlist-badge');
    if (!badge) return;
    if (!token) { badge.style.display = 'none'; return; }
    const ids = await fetchWishlistIds();
    if (ids === null) return;
    badge.textContent = ids.length;
    badge.style.display = ids.length ? 'inline-block' : 'none';
}

async function syncWishlistButtons() {
    const ids = await fetchWishlistIds();
    if (ids === null) return;
    saveWishlistIds(ids);
    document.querySelectorAll('.heart-btn[data-pid]').forEach(btn => {
        if (btn.disabled) return;
        setWishlistState(btn, ids.includes(Number(btn.dataset.pid)));
    });
}

// sahifa yuklanganda
updateNavbar();
