body {
    margin: 0;
    font-family: 'Tahoma', sans-serif;
    background: linear-gradient(135deg, #07111f 0%, #101a2b 34%, #111827 100%);
    color: #e2e8f0;
}

* { box-sizing: border-box; }

.login-wrap {
    display: grid;
    place-items: center;
    min-height: 100vh;
    padding: 24px;
}

.login-card {
    width: min(100%, 430px);
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(96, 165, 250, 0.3);
    border-radius: 18px;
    padding: 28px;
    box-shadow: 0 0 28px rgba(37,99,235,0.18);
}

.login-card h1, .login-card h2 { text-align: center; }

form {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

label {
    color: #cbd5e1;
    font-size: 14px;
}

input {
    padding: 12px 14px;
    border: 1px solid #2b3d5d;
    border-radius: 10px;
    background: #0b1320;
    color: white;
    font-size: 15px;
}

button {
    margin-top: 12px;
    padding: 12px 16px;
    border: none;
    border-radius: 12px;
    background: linear-gradient(90deg, #2563eb, #38bdf8);
    color: white;
    font-weight: 700;
    cursor: pointer;
}

.error-box {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.4);
    color: #fecaca;
    padding: 10px 12px;
    border-radius: 10px;
    margin-bottom: 12px;
}

.dashboard-shell {
    display: flex;
    min-height: 100vh;
}

.sidebar {
    width: 260px;
    background: #0a1220;
    border-left: 1px solid rgba(148, 163, 184, 0.2);
    padding: 24px 18px;
}

.sidebar nav {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 20px;
}

.sidebar a {
    color: #dbeafe;
    text-decoration: none;
    padding: 12px 14px;
    background: rgba(37, 99, 235, 0.12);
    border-radius: 12px;
}

.main-panel {
    flex: 1;
    padding: 32px;
}

.topbar {
    margin-bottom: 24px;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
}

.stat-card, .panel-card {
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(96, 165, 250, 0.35);
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 0 16px rgba(59, 130, 246, 0.15);
}

.stat-card span {
    display: block;
    color: #94a3b8;
    margin-bottom: 8px;
}

.stat-card strong {
    font-size: 2rem;
    color: white;
}

.panel-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 16px;
    margin-top: 20px;
}

ul {
    padding-right: 18px;
    line-height: 1.8;
}
