const API_BASE = "/api/v1";

function showMessage(elementId, message, type = 'success') {
    const el = document.getElementById(elementId);
    el.textContent = message;
    el.className = `message ${type}`;
    el.style.display = 'block';
    setTimeout(() => {
        el.style.display = 'none';
    }, 5000);
}

function clearMessage(elementId) {
    const el = document.getElementById(elementId);
    el.style.display = 'none';
    el.textContent = '';
}

async function handleLogin(e) {
    e.preventDefault();
    clearMessage('loginMessage');

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const remember = document.getElementById('remember').checked;

    if (!email || !password) {
        showMessage('loginMessage', 'Please enter both email and password.', 'error');
        return;
    }

    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData.toString(),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Login failed');
        }

        localStorage.setItem('access_token', data.access_token);
        if (remember) {
            localStorage.setItem('remember', 'true');
        }

        showMessage('loginMessage', 'Login successful! Redirecting...', 'success');

        setTimeout(() => {
            window.location.href = '/dashboard.html';
        }, 1000);
    } catch (error) {
        showMessage('loginMessage', error.message, 'error');
    }
}

async function handleSignup(e) {
    e.preventDefault();
    clearMessage('signupMessage');

    const fullName = document.getElementById('fullName').value.trim();
    const email = document.getElementById('email').value.trim();
    const mobile = document.getElementById('mobile').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const terms = document.getElementById('terms').checked;

    if (!fullName || !email || !mobile || !password || !confirmPassword) {
        showMessage('signupMessage', 'Please fill in all fields.', 'error');
        return;
    }

    if (password !== confirmPassword) {
        showMessage('signupMessage', 'Passwords do not match.', 'error');
        return;
    }

    if (password.length < 8) {
        showMessage('signupMessage', 'Password must be at least 8 characters.', 'error');
        return;
    }

    if (!terms) {
        showMessage('signupMessage', 'You must agree to the Terms & Conditions.', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email,
                password,
                confirm_password: confirmPassword,
                full_name: fullName,
                mobile_number: mobile,
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Registration failed');
        }

        showMessage('signupMessage', 'Account created successfully! Redirecting to login...', 'success');

        setTimeout(() => {
            window.location.href = '/login.html';
        }, 1500);
    } catch (error) {
        showMessage('signupMessage', error.message, 'error');
    }
}

function checkAuth() {
    const token = localStorage.getItem('access_token');
    const path = window.location.pathname;

    if (token && (path === '/login.html' || path === '/signup.html')) {
        window.location.href = '/dashboard.html';
    }

    if (!token && path === '/dashboard.html') {
        window.location.href = '/login.html';
    }
}

async function loadDashboard() {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    try {
        const response = await fetch(`${API_BASE}/auth/me`, {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            localStorage.removeItem('access_token');
            window.location.href = '/login.html';
            return;
        }

        const data = await response.json();
        document.querySelector('.welcome-section h2').textContent = `Welcome to WarrantyHub`;
    } catch (error) {
        console.error('Dashboard load error:', error);
    }
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('remember');
    window.location.href = '/login.html';
}

document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;

    if (path === '/login.html') {
        document.getElementById('loginForm').addEventListener('submit', handleLogin);
    } else if (path === '/signup.html') {
        document.getElementById('signupForm').addEventListener('submit', handleSignup);
    } else if (path === '/dashboard.html') {
        loadDashboard();
        document.getElementById('logoutBtn').addEventListener('click', logout);
    }

    checkAuth();
});
