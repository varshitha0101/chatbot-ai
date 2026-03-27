/* =========================================================
   MindfulAI – Full Application Logic
   ========================================================= */

const API_BASE = "http://localhost:5000";

/* ── State ─────────────────────────────────── */
let token = localStorage.getItem("mindful_token") || null;
let userId = localStorage.getItem("mindful_user_id") || null;
let allHistory = [];
let activeFilter = "all";

let chartEmotion = null;
let chartDistortion = null;
let chartTrend = null;

// Session tracking
let sessionStartTime = Date.now();
let sessionMessageCount = 0;
let currentSessionEmotion = "—";

/* ── Emotion Emoji Map ─────────────────────── */
const EMOTION_EMOJI = {
    anxiety: "😰",
    sadness: "😢",
    anger: "😠",
    positive: "😊",
    uncertain: "🤔",
    fear: "😨",
};

const EMOTION_COLORS = {
    anxiety: "#8b5cf6",
    sadness: "#3b82f6",
    anger: "#ef4444",
    positive: "#10b981",
    uncertain: "#f59e0b",
    fear: "#f43f5e",
};

const DISTORTION_EXPLAIN = {
    catastrophizing: "Imagining the worst possible outcome will happen.",
    overgeneralization: "Believing one negative event means ongoing defeat.",
    mind_reading: "Assuming you know what others think — negatively.",
    all_or_nothing: "Seeing things as all-good or all-bad with no middle ground.",
};

/* ── Startup ───────────────────────────────── */
document.addEventListener("DOMContentLoaded", () => {
    lucide.createIcons();
    if (token && userId) bootApp();
    
    // Keyboard shortcuts
    document.addEventListener("keydown", (e) => {
        // Enter to send message (when focused on chat input)
        if (e.key === "Enter" && !e.shiftKey && document.activeElement.id === "chatInput") {
            e.preventDefault();
            sendMessage();
        }
        
        // Escape to close modals
        if (e.key === "Escape") {
            const modals = ["crisisModal", "exportModal", "breathingModal", "dailyCheckinModal", "journalEntryModal"];
            modals.forEach(modalId => {
                const modal = document.getElementById(modalId);
                if (modal && !modal.classList.contains("hidden")) {
                    modal.classList.add("hidden");
                }
            });
        }
    });
});

/* ── Auth ──────────────────────────────────── */
function switchTab(tab) {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const loginTab = document.getElementById("loginTab");
    const registerTab = document.getElementById("registerTab");

    if (tab === "login") {
        loginForm.classList.remove("hidden");
        registerForm.classList.add("hidden");
        loginTab.classList.add("active");
        registerTab.classList.remove("active");
    } else {
        loginForm.classList.add("hidden");
        registerForm.classList.remove("hidden");
        loginTab.classList.remove("active");
        registerTab.classList.add("active");
    }
}

async function handleLogin(e) {
    e.preventDefault();
    const uid = document.getElementById("loginUserId").value.trim();
    const pass = document.getElementById("loginPassword").value;
    const btn = document.getElementById("loginBtn");
    const err = document.getElementById("loginError");

    btn.classList.add("loading");
    err.classList.add("hidden");

    try {
        const res = await fetch(`${API_BASE}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: uid, password: pass }),
        });
        const data = await res.json();

        if (!res.ok) throw new Error(data.error || "Login failed");

        token = data.token;
        userId = uid;
        localStorage.setItem("mindful_token", token);
        localStorage.setItem("mindful_user_id", userId);
        bootApp();
    } catch (err2) {
        err.textContent = err2.message;
        err.classList.remove("hidden");
    } finally {
        btn.classList.remove("loading");
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const uid = document.getElementById("regUserId").value.trim();
    const pass = document.getElementById("regPassword").value;
    const btn = document.getElementById("registerBtn");
    const errEl = document.getElementById("registerError");
    const succEl = document.getElementById("registerSuccess");

    btn.classList.add("loading");
    errEl.classList.add("hidden");
    succEl.classList.add("hidden");

    try {
        const res = await fetch(`${API_BASE}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: uid, password: pass }),
        });
        const data = await res.json();

        if (!res.ok) throw new Error(data.error || "Registration failed");

        succEl.textContent = "✓ Account created! Please sign in.";
        succEl.classList.remove("hidden");
        setTimeout(() => switchTab("login"), 1500);
    } catch (err2) {
        errEl.textContent = err2.message;
        errEl.classList.remove("hidden");
    } finally {
        btn.classList.remove("loading");
    }
}

function handleLogout() {
    token = null; userId = null;
    localStorage.removeItem("mindful_token");
    localStorage.removeItem("mindful_user_id");
    document.getElementById("mainApp").classList.add("hidden");
    document.getElementById("authOverlay").classList.remove("hidden");
    // Reset chat
    const cw = document.getElementById("chatWindow");
    cw.innerHTML = buildWelcomeHTML();
    lucide.createIcons();
    allHistory = [];
}

/* ── Boot App ──────────────────────────────── */
function bootApp() {
    document.getElementById("authOverlay").classList.add("hidden");
    document.getElementById("mainApp").classList.remove("hidden");

    // Set user info
    const displayName = userId || "User";
    document.getElementById("welcomeName").textContent = displayName.split("_").join(" ");
    document.getElementById("sidebarUsername").textContent = displayName;
    document.getElementById("sidebarAvatar").textContent = displayName[0].toUpperCase();

    // Reset session stats
    sessionStartTime = Date.now();
    sessionMessageCount = 0;
    currentSessionEmotion = "—";
    startSessionTimer();

    lucide.createIcons();
    showPage("chat");
    loadAllAnalytics();
    loadHistory();
    buildInsights();
}

/* ── Navigation ────────────────────────────── */
function showPage(page) {
    document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
    document.querySelectorAll(".nav-item").forEach(n => n.classList.remove("active"));
    document.getElementById(`page-${page}`).classList.add("active");
    document.getElementById(`nav-${page}`).classList.add("active");

    // Close mobile sidebar on navigate
    document.getElementById("sidebar").classList.remove("open");

    if (page === "analytics") loadAllAnalytics();
    if (page === "history") loadHistory();
    if (page === "insights") buildInsights();
    if (page === "journal") loadJournalEntries();
    if (page === "progress") {
        loadAchievements();
        updateProgressStats();
        loadMoodChart();
    }
}

function toggleSidebar() {
    document.getElementById("sidebar").classList.toggle("open");
}

/* ── Chat ──────────────────────────────────── */
function buildWelcomeHTML() {
    return `
    <div class="chat-welcome">
      <div class="welcome-icon"><i data-lucide="brain-circuit"></i></div>
      <h2>Hello, <span id="welcomeName">friend</span> 👋</h2>
      <p>I'm your CBT companion. Share what's on your mind — I'll help you explore your emotions and thinking patterns with care.</p>
      <div class="quick-prompts">
        <button class="quick-prompt" onclick="usePrompt(this)">I've been feeling really anxious lately</button>
        <button class="quick-prompt" onclick="usePrompt(this)">I feel like nothing ever goes right for me</button>
        <button class="quick-prompt" onclick="usePrompt(this)">I had a great day today!</button>
        <button class="quick-prompt" onclick="usePrompt(this)">I keep thinking the worst will happen</button>
      </div>
    </div>`;
}

function usePrompt(btn) {
    document.getElementById("chatInput").value = btn.textContent;
    autoResize(document.getElementById("chatInput"));
    document.getElementById("chatInput").focus();
}

function handleChatKey(e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

function autoResize(el) {
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 160) + "px";
}

async function sendMessage() {
    const input = document.getElementById("chatInput");
    const text = input.value.trim();
    if (!text) return;

    // Clear welcome if present
    const welcome = document.querySelector(".chat-welcome");
    if (welcome) welcome.remove();

    input.value = "";
    autoResize(input);
    const sendBtn = document.getElementById("sendBtn");
    sendBtn.disabled = true;
    sendBtn.innerHTML = '<i data-lucide="loader" class="spinning"></i>';
    lucide.createIcons();

    // Append user bubble
    appendBubble("user", text, null, null, null);

    // Show typing
    const typingId = appendTyping();

    try {
        const res = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify({ message: text }),
        });
        const data = await res.json();

        removeTyping(typingId);

        // Handle expired/invalid token
        if (res.status === 401) {
            appendBubble("bot", "⚠ Your session has expired. Please log in again.", null, null, null);
            setTimeout(() => handleLogout(), 2000);
            return;
        }

        if (!res.ok) throw new Error(data.error || "Server error");

        // Check if it's a crisis response
        const isCrisis = data.response.toLowerCase().includes("mental health helpline") || 
                        data.response.toLowerCase().includes("trusted person");
        
        if (isCrisis) {
            appendBubble("bot", data.response, null, null, null);
            setTimeout(() => showCrisisModal(), 500);
        } else {
            appendBubble("bot", data.response, data.emotion, data.intensity, data.distortion, data.dominant_distortion);
            updateEmotionBar(data.emotion, data.intensity, data.distortion);
            updateSessionStats(data.emotion);
        }
        
        // Track conversation for achievements
        const history = JSON.parse(localStorage.getItem("conversation_history") || "[]");
        history.push({
            timestamp: new Date().toISOString(),
            emotion: data.emotion,
            user_message: text
        });
        localStorage.setItem("conversation_history", JSON.stringify(history));
        checkAndUnlockAchievements();

    } catch (err) {
        removeTyping(typingId);
        appendBubble("bot", `⚠ ${err.message}. Make sure the backend is running at ${API_BASE}.`, null, null, null);
    } finally {
        const sendBtn = document.getElementById("sendBtn");
        sendBtn.disabled = false;
        sendBtn.innerHTML = '<i data-lucide="send"></i>';
        lucide.createIcons();
        input.focus();
    }
}

function appendBubble(role, text, emotion, intensity, distortion, dominantDistortion) {
    const cw = document.getElementById("chatWindow");
    const wrap = document.createElement("div");
    wrap.className = `chat-message ${role}${emotion === null && role === "bot" ? " crisis-message" : ""}`;

    const initials = role === "bot" ? "🧠" : (userId || "U")[0].toUpperCase();
    const ts = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

    let metaHTML = "";
    if (role === "bot" && emotion) {
        const emoji = EMOTION_EMOJI[emotion] || "🔍";
        metaHTML += `<span class="msg-tag tag-emotion">${emoji} ${emotion}</span>`;
    }
    if (intensity) metaHTML += `<span class="msg-tag tag-intensity">${intensity} intensity</span>`;
    if (distortion && distortion !== "none")
        metaHTML += `<span class="msg-tag tag-distortion">⚠ ${distortion.replace(/_/g, " ")}</span>`;
    if (dominantDistortion && dominantDistortion !== distortion && dominantDistortion !== "none")
        metaHTML += `<span class="msg-tag tag-distortion" title="Your dominant pattern">🔁 ${dominantDistortion.replace(/_/g, " ")}</span>`;

    wrap.innerHTML = `
    <div class="msg-avatar ${role}">${initials}</div>
    <div>
      <div class="msg-bubble">${escapeHtml(text)}</div>
      ${metaHTML || intensity ? `<div class="msg-meta">${metaHTML}<span class="msg-time">${ts}</span></div>` : `<div class="msg-meta"><span class="msg-time">${ts}</span></div>`}
    </div>`;

    cw.appendChild(wrap);
    
    // Smooth scroll to bottom with animation
    setTimeout(() => {
        cw.scrollTo({
            top: cw.scrollHeight,
            behavior: 'smooth'
        });
    }, 50);
    
    lucide.createIcons();
}

function appendTyping() {
    const cw = document.getElementById("chatWindow");
    const wrap = document.createElement("div");
    const id = "typing_" + Date.now();
    wrap.id = id;
    wrap.className = "chat-message bot";
    wrap.innerHTML = `
    <div class="msg-avatar bot">🧠</div>
    <div class="typing-indicator">
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
    </div>`;
    cw.appendChild(wrap);
    cw.scrollTop = cw.scrollHeight;
    return id;
}

function removeTyping(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function updateEmotionBar(emotion, intensity, distortion) {
    const bar = document.getElementById("emotionBar");
    bar.style.display = "flex";

    const emoji = EMOTION_EMOJI[emotion] || "🔍";
    document.getElementById("emotionLabel").textContent = `${emoji} ${emotion || "unknown"}`;

    const ibadge = document.getElementById("intensityBadge");
    ibadge.textContent = "";
    if (intensity) {
        ibadge.textContent = intensity;
        ibadge.className = `intensity-badge intensity-${intensity}`;
    }

    const dtag = document.getElementById("distortionTag");
    if (distortion && distortion !== "none") {
        dtag.textContent = `⚠ ${distortion.replace(/_/g, " ")}`;
        dtag.style.display = "";
    } else {
        dtag.style.display = "none";
    }
}

/* ── Analytics ─────────────────────────────── */
async function loadAllAnalytics() {
    if (!token) return;
    try {
        const [emRes, distRes, trendRes, corrRes] = await Promise.all([
            authFetch("/analytics"),
            authFetch("/distortion_analytics"),
            authFetch("/trend"),
            authFetch("/emotion_distortion_correlation"),
        ]);

        const emData = await emRes.json();
        const distData = await distRes.json();
        const trendData = await trendRes.json();
        const corrData = await corrRes.json();

        renderStatCards(emData, distData, trendData);
        renderEmotionChart(emData.emotion_distribution || {});
        renderDistortionChart(distData);
        renderTrendChart(trendData);
        renderCorrelationHeatmap(corrData);
    } catch (e) {
        console.warn("Analytics load error:", e);
    }
}

function renderStatCards(emData, distData, trendData) {
    // Total Messages
    document.getElementById("statTotalVal").textContent = emData.total_messages ?? "–";

    // Dominant emotion
    const emotionDist = emData.emotion_distribution || {};
    const domEmotion = Object.entries(emotionDist).sort((a, b) => b[1] - a[1])[0];
    document.getElementById("statDomEmotionVal").textContent = domEmotion
        ? `${EMOTION_EMOJI[domEmotion[0]] || "🔍"} ${domEmotion[0]}`
        : "–";

    // Dominant distortion
    const distEntries = Object.entries(distData);
    const domDist = distEntries.sort((a, b) => b[1] - a[1])[0];
    document.getElementById("statDomDistortionVal").textContent = domDist
        ? domDist[0].replace(/_/g, " ")
        : "–";

    // Days Active
    const dayCount = Object.keys(trendData).length;
    document.getElementById("statDaysActiveVal").textContent = dayCount || "–";
}

function renderEmotionChart(distribution) {
    const ctx = document.getElementById("emotionChart").getContext("2d");
    if (chartEmotion) chartEmotion.destroy();

    const labels = Object.keys(distribution);
    const values = Object.values(distribution);
    const colors = labels.map(l => EMOTION_COLORS[l] || "#a78bfa");

    if (!labels.length) { showNoData("emotionChart"); return; }

    chartEmotion = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels,
            datasets: [{
                data: values,
                backgroundColor: colors.map(c => hexAlpha(c, 0.75)),
                borderColor: colors,
                borderWidth: 2,
                hoverOffset: 8,
            }],
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            cutout: "62%",
            plugins: {
                legend: {
                    position: "right",
                    labels: {
                        color: "#9090a8", font: { family: "Inter", size: 12 },
                        boxWidth: 12, padding: 12,
                        generateLabels: (chart) => {
                            const ds = chart.data.datasets[0];
                            return chart.data.labels.map((label, i) => ({
                                text: `${EMOTION_EMOJI[label] || "🔍"} ${label}`,
                                fillStyle: ds.backgroundColor[i],
                                strokeStyle: ds.borderColor[i],
                                lineWidth: 2,
                                hidden: false,
                                index: i,
                            }));
                        },
                    },
                },
                tooltip: tooltipStyle(),
            },
        },
    });
}

function renderDistortionChart(distData) {
    const ctx = document.getElementById("distortionChart").getContext("2d");
    if (chartDistortion) chartDistortion.destroy();

    const labels = Object.keys(distData).map(k => k.replace(/_/g, " "));
    const values = Object.values(distData);

    if (!labels.length) { showNoData("distortionChart"); return; }

    const palette = ["#8b5cf6", "#f59e0b", "#ec4899", "#10b981", "#3b82f6", "#f43f5e"];

    chartDistortion = new Chart(ctx, {
        type: "bar",
        data: {
            labels,
            datasets: [{
                label: "Occurrences",
                data: values,
                backgroundColor: labels.map((_, i) => hexAlpha(palette[i % palette.length], 0.65)),
                borderColor: labels.map((_, i) => palette[i % palette.length]),
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false,
            }],
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            indexAxis: "y",
            plugins: {
                legend: { display: false },
                tooltip: tooltipStyle(),
            },
            scales: {
                x: {
                    grid: { color: "rgba(255,255,255,0.05)" },
                    ticks: { color: "#9090a8", font: { family: "Inter", size: 11 } },
                },
                y: {
                    grid: { display: false },
                    ticks: { color: "#9090a8", font: { family: "Inter", size: 11 } },
                },
            },
        },
    });
}

function renderTrendChart(trendData) {
    const ctx = document.getElementById("trendChart").getContext("2d");
    if (chartTrend) chartTrend.destroy();

    const dates = Object.keys(trendData).sort();
    if (!dates.length) { showNoData("trendChart"); return; }

    const emotions = [...new Set(dates.flatMap(d => Object.keys(trendData[d])))];
    const palette = { anxiety: "#8b5cf6", sadness: "#3b82f6", anger: "#ef4444", positive: "#10b981", uncertain: "#f59e0b" };

    const datasets = emotions.map(em => ({
        label: em,
        data: dates.map(d => trendData[d][em] || 0),
        borderColor: palette[em] || "#a78bfa",
        backgroundColor: hexAlpha(palette[em] || "#a78bfa", 0.12),
        borderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6,
        tension: 0.4,
        fill: true,
    }));

    chartTrend = new Chart(ctx, {
        type: "line",
        data: { labels: dates, datasets },
        options: {
            responsive: true, maintainAspectRatio: false,
            interaction: { mode: "index", intersect: false },
            plugins: {
                legend: {
                    labels: { color: "#9090a8", font: { family: "Inter", size: 12 }, boxWidth: 12, padding: 14 },
                },
                tooltip: tooltipStyle(),
            },
            scales: {
                x: {
                    grid: { color: "rgba(255,255,255,0.04)" },
                    ticks: { color: "#9090a8", font: { family: "Inter", size: 11 } },
                },
                y: {
                    grid: { color: "rgba(255,255,255,0.04)" },
                    ticks: { color: "#9090a8", font: { family: "Inter", size: 11 }, stepSize: 1 },
                    beginAtZero: true,
                },
            },
        },
    });
}

function renderCorrelationHeatmap(corrData) {
    const container = document.getElementById("correlationHeatmap");
    const emotions = Object.keys(corrData);
    if (!emotions.length) { container.innerHTML = `<p class="no-data">No correlation data yet</p>`; return; }

    // Gather all distortions
    const distortions = [...new Set(emotions.flatMap(e => Object.keys(corrData[e])))];

    let html = "";
    for (const emotion of emotions) {
        const distMap = corrData[emotion];
        const maxVal = Math.max(...Object.values(distMap), 1);
        let cells = distortions.map(d => {
            const val = distMap[d] || 0;
            const alpha = val / maxVal;
            const clr = EMOTION_COLORS[emotion] || "#8b5cf6";
            return `<div class="heatmap-cell" style="background:${hexAlpha(clr, 0.15 + alpha * 0.6)};color:${val ? clr : '#5a5a72'};border:1px solid ${hexAlpha(clr, 0.2 + alpha * 0.3)};"
              title="${emotion} + ${d}: ${val}">
                ${d.replace(/_/g, " ")}&nbsp;&nbsp;<strong>${val || ""}</strong>
              </div>`;
        }).join("");

        html += `<div class="heatmap-row">
               <span class="heatmap-label">${EMOTION_EMOJI[emotion] || ""} ${emotion}</span>
               <div class="heatmap-cells">${cells}</div>
             </div>`;
    }
    container.innerHTML = html;
}

/* ── History ───────────────────────────────── */
async function loadHistory() {
    if (!token) return;
    try {
        const res = await authFetch("/history");
        const data = await res.json();
        allHistory = data;
        renderHistory(allHistory);
    } catch (e) {
        document.getElementById("historyList").innerHTML = `<p class="no-data">Could not load history.</p>`;
    }
}

function renderHistory(items) {
    const list = document.getElementById("historyList");
    if (!items.length) {
        list.innerHTML = `<p class="no-data">No conversation history yet. Start chatting! 💬</p>`;
        return;
    }

    list.innerHTML = items.map(item => {
        const emoji = EMOTION_EMOJI[item.emotion] || "🔍";
        const date = item.timestamp ? new Date(item.timestamp).toLocaleString() : "";
        const dist = item.distortion && item.distortion !== "none" ? `<span class="msg-tag tag-distortion">⚠ ${item.distortion.replace(/_/g, " ")}</span>` : "";
        const inten = item.intensity ? `<span class="msg-tag tag-intensity">${item.intensity}</span>` : "";
        return `<div class="history-item" data-emotion="${item.emotion || ""}">
      <div class="history-item-header">
        <span class="msg-tag tag-emotion">${emoji} ${item.emotion || "unknown"}</span>
        ${inten}${dist}
        <span class="history-timestamp">${date}</span>
      </div>
      <p class="history-message">${escapeHtml(item.message)}</p>
    </div>`;
    }).join("");
}

function filterByEmotion(emotion, btn) {
    activeFilter = emotion;
    document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    applyFilters();
}

function filterHistory() {
    applyFilters();
}

function applyFilters() {
    const query = document.getElementById("historySearch").value.toLowerCase();
    let filtered = allHistory;

    if (activeFilter !== "all") {
        filtered = filtered.filter(h => h.emotion === activeFilter);
    }
    if (query) {
        filtered = filtered.filter(h => h.message.toLowerCase().includes(query));
    }
    renderHistory(filtered);
}

/* ── Insights ──────────────────────────────── */
function buildInsights() {
    buildCBTTips();
    buildDistortionExplainer();
    renderWellnessBars();
}

function buildCBTTips() {
    const tips = [
        "Catch the thought — When you feel bad, notice the automatic thought that preceded it.",
        "Challenge the evidence — Ask: \"What facts support this? What facts don't?\"",
        "Reframe the thought — Replace with a balanced, realistic alternative.",
        "Conduct a behavioural experiment — Test your belief by trying something new.",
        "Use the downward arrow — Ask \"What would that mean?\" repeatedly to find the core belief.",
    ];
    document.getElementById("cbtTips").innerHTML = tips.map((t, i) =>
        `<div class="tip-item">
       <div class="tip-number">${i + 1}</div>
       <p class="tip-text">${t}</p>
     </div>`
    ).join("");
}

function buildDistortionExplainer() {
    document.getElementById("distortionExplainer").innerHTML =
        Object.entries(DISTORTION_EXPLAIN).map(([name, desc]) =>
            `<div class="distortion-item">
         <div class="distortion-name">${name.replace(/_/g, " ")}</div>
         <div class="distortion-desc">${desc}</div>
       </div>`
        ).join("");
}

async function renderWellnessBars() {
    if (!token) return;
    try {
        const res = await authFetch("/analytics");
        const data = await res.json();
        const dist = data.emotion_distribution || {};
        const total = data.total_messages || 1;

        const emotionGradients = {
            positive: "linear-gradient(90deg,#059669,#10b981)",
            anxiety: "linear-gradient(90deg,#7c3aed,#8b5cf6)",
            sadness: "linear-gradient(90deg,#1d4ed8,#3b82f6)",
            anger: "linear-gradient(90deg,#b91c1c,#ef4444)",
            uncertain: "linear-gradient(90deg,#b45309,#f59e0b)",
        };

        const html = Object.entries(dist).map(([em, cnt]) => {
            const pct = Math.round((cnt / total) * 100);
            const gradient = emotionGradients[em] || "linear-gradient(90deg,#6d28d9,#8b5cf6)";
            return `<div class="wellness-item">
        <div class="wellness-item-header">
          <span class="wellness-label">${EMOTION_EMOJI[em] || ""} ${em}</span>
          <span class="wellness-pct">${pct}% (${cnt})</span>
        </div>
        <div class="wellness-track">
          <div class="wellness-fill" style="width:0%;background:${gradient};"
               data-target="${pct}"></div>
        </div>
      </div>`;
        }).join("");

        document.getElementById("wellnessProgress").innerHTML = html || `<p class="no-data">Start chatting to track wellness.</p>`;

        // Animate bars
        requestAnimationFrame(() => {
            document.querySelectorAll(".wellness-fill[data-target]").forEach(el => {
                setTimeout(() => { el.style.width = el.dataset.target + "%"; }, 100);
            });
        });
    } catch (e) {
        document.getElementById("wellnessProgress").innerHTML = `<p class="no-data">Start chatting to track wellness.</p>`;
    }
}

/* ── Helpers ───────────────────────────────── */
async function authFetch(endpoint, options = {}) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers: {
            ...(options.headers || {}),
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
        },
    });
    
    // Handle expired/invalid token
    if (response.status === 401) {
        showToast("Your session has expired. Please log in again.", "error");
        setTimeout(() => handleLogout(), 2000);
        throw new Error("Session expired");
    }
    
    return response;
}

function showNoData(canvasId) {
    const cvs = document.getElementById(canvasId);
    if (!cvs) return;
    const parent = cvs.parentElement;
    cvs.style.display = "none";
    const p = document.createElement("p");
    p.className = "no-data";
    p.textContent = "No data yet — start chatting!";
    parent.appendChild(p);
}

function tooltipStyle() {
    return {
        callbacks: {},
        backgroundColor: "rgba(12,12,20,0.95)",
        titleColor: "#f0f0f5",
        bodyColor: "#9090a8",
        borderColor: "rgba(255,255,255,0.08)",
        borderWidth: 1,
        padding: 10,
        cornerRadius: 10,
        titleFont: { family: "Space Grotesk", weight: "700" },
        bodyFont: { family: "Inter", size: 12 },
    };
}

function hexAlpha(hex, alpha) {
    // Works for both 6-char hex and named as fallback
    try {
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        return `rgba(${r},${g},${b},${alpha})`;
    } catch { return hex; }
}

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

/* ── Toast ─────────────────────────────────── */
function showToast(msg, type = "info") {
    const toast = document.getElementById("toast");
    toast.textContent = msg;
    toast.className = `toast ${type}`;
    setTimeout(() => toast.classList.add("hidden"), 3200);
}

/* ── Crisis Modal ──────────────────────────── */
function showCrisisModal() {
    const modal = document.getElementById("crisisModal");
    modal.classList.remove("hidden");
    lucide.createIcons();
}

function closeCrisisModal() {
    const modal = document.getElementById("crisisModal");
    modal.classList.add("hidden");
}

/* ── Export Modal ──────────────────────────── */
function openExportModal() {
    const modal = document.getElementById("exportModal");
    modal.classList.remove("hidden");
    lucide.createIcons();
}

function closeExportModal() {
    const modal = document.getElementById("exportModal");
    modal.classList.add("hidden");
}

async function exportChatHistory() {
    try {
        if (!allHistory.length) await loadHistory();
        const dataStr = JSON.stringify(allHistory, null, 2);
        downloadFile(dataStr, `mindfulai-chat-history-${Date.now()}.json`, "application/json");
        showToast("Chat history exported successfully!", "success");
        closeExportModal();
    } catch (e) {
        showToast("Failed to export chat history", "error");
    }
}

async function exportAnalytics() {
    try {
        const [emRes, distRes, trendRes, corrRes] = await Promise.all([
            authFetch("/analytics"),
            authFetch("/distortion_analytics"),
            authFetch("/trend"),
            authFetch("/emotion_distortion_correlation"),
        ]);

        const analytics = {
            emotions: await emRes.json(),
            distortions: await distRes.json(),
            trends: await trendRes.json(),
            correlations: await corrRes.json(),
            exportedAt: new Date().toISOString(),
            userId: userId
        };

        const dataStr = JSON.stringify(analytics, null, 2);
        downloadFile(dataStr, `mindfulai-analytics-${Date.now()}.json`, "application/json");
        showToast("Analytics exported successfully!", "success");
        closeExportModal();
    } catch (e) {
        showToast("Failed to export analytics", "error");
    }
}

async function exportFullData() {
    try {
        const [historyRes, emRes, distRes, trendRes, corrRes] = await Promise.all([
            authFetch("/history"),
            authFetch("/analytics"),
            authFetch("/distortion_analytics"),
            authFetch("/trend"),
            authFetch("/emotion_distortion_correlation"),
        ]);

        const fullData = {
            history: await historyRes.json(),
            analytics: {
                emotions: await emRes.json(),
                distortions: await distRes.json(),
                trends: await trendRes.json(),
                correlations: await corrRes.json(),
            },
            metadata: {
                exportedAt: new Date().toISOString(),
                userId: userId,
                version: "1.0"
            }
        };

        const dataStr = JSON.stringify(fullData, null, 2);
        downloadFile(dataStr, `mindfulai-complete-data-${Date.now()}.json`, "application/json");
        showToast("Complete data exported successfully!", "success");
        closeExportModal();
    } catch (e) {
        showToast("Failed to export complete data", "error");
    }
}

function downloadFile(content, filename, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

/* ── Session Statistics ────────────────────── */
function updateSessionStats(emotion) {
    sessionMessageCount++;
    currentSessionEmotion = emotion || currentSessionEmotion;

    document.getElementById("sessionMsgCount").textContent = sessionMessageCount;
    document.getElementById("sessionEmotion").textContent = 
        (EMOTION_EMOJI[currentSessionEmotion] || "") + " " + currentSessionEmotion;
}

function startSessionTimer() {
    setInterval(() => {
        const elapsed = Math.floor((Date.now() - sessionStartTime) / 1000);
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        document.getElementById("sessionDuration").textContent = 
            `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
    }, 1000);
}

/* ==============================================================
   NEW FEATURES - Breathing, Journal, Progress, Tools
============================================================== */

// ── Breathing Exercise ──────────────────────────────────────
let breathingInterval = null;
let breathingCycle = 0;
let breathingType = "478";
const BREATHING_PATTERNS = {
    "478": { inhale: 4, hold: 7, exhale: 8, name: "4-7-8 Breathing" },
    "box": { inhale: 4, hold: 4, exhale: 4, pause: 4, name: "Box Breathing" },
    "deep": { inhale: 5, hold: 2, exhale: 7, name: "Deep Breathing" }
};

function openBreathingModal() {
    document.getElementById("breathingModal").classList.remove("hidden");
    lucide.createIcons();
}

function closeBreathingModal() {
    stopBreathing();
    document.getElementById("breathingModal").classList.add("hidden");
}

function selectBreathingType(type) {
    breathingType = type;
    document.querySelectorAll(".breathing-option").forEach(btn => btn.classList.remove("active"));
    document.querySelector(`[data-type="${type}"]`).classList.add("active");
    stopBreathing();
}

function startBreathing() {
    breathingCycle = 0;
    document.getElementById("breathingStartBtn").classList.add("hidden");
    document.getElementById("breathingStopBtn").classList.remove("hidden");

    const pattern = BREATHING_PATTERNS[breathingType];
    const circle = document.getElementById("breathingCircle");
    const instruction = document.getElementById("breathingInstruction");
    const counter = document.getElementById("breathingCounter");
    
    const runCycle = () => {
        if (breathingCycle >= 5) {
            stopBreathing();
            instruction.textContent = "Great job! You completed 5 cycles.";
            setTimeout(() => {
                instruction.textContent = "Click 'Start' to begin";
                counter.textContent = "0 / 5 cycles";
            }, 3000);
            return;
        }

        breathingCycle++;
        counter.textContent = `${breathingCycle} / 5 cycles`;

        // Inhale
        instruction.textContent = `Breathe in (${pattern.inhale}s)`;
        circle.style.transform = "scale(1.5)";
        circle.style.transition = `transform ${pattern.inhale}s ease-in-out`;

        setTimeout(() => {
            // Hold
            instruction.textContent = `Hold (${pattern.hold}s)`;
            circle.style.transform = "scale(1.5)";
        }, pattern.inhale * 1000);

        setTimeout(() => {
            // Exhale
            instruction.textContent = `Breathe out (${pattern.exhale}s)`;
            circle.style.transform = "scale(1)";
            circle.style.transition = `transform ${pattern.exhale}s ease-in-out`;
        }, (pattern.inhale + pattern.hold) * 1000);

        const cycleTime = (pattern.inhale + pattern.hold + pattern.exhale + (pattern.pause || 0)) * 1000;
        breathingInterval = setTimeout(runCycle, cycleTime);
    };

    runCycle();
}

function stopBreathing() {
    if (breathingInterval) {
        clearTimeout(breathingInterval);
        breathingInterval = null;
    }
    document.getElementById("breathingStartBtn").classList.remove("hidden");
    document.getElementById("breathingStopBtn").classList.add("hidden");
    const circle = document.getElementById("breathingCircle");
    circle.style.transform = "scale(1)";
    
    // Track breathing session
    if (breathingCycle > 0) {
        const sessions = parseInt(localStorage.getItem("breathing_sessions") || "0") + 1;
        localStorage.setItem("breathing_sessions", sessions.toString());
        const techniques = parseInt(localStorage.getItem("techniques_practiced") || "0") + 1;
        localStorage.setItem("techniques_practiced", techniques.toString());
        checkAndUnlockAchievements();
    }
}

// ── Daily Check-In ──────────────────────────────────────────
let selectedMood = null;

function openDailyCheckin() {
    document.getElementById("dailyCheckinModal").classList.remove("hidden");
    lucide.createIcons();
}

function closeDailyCheckin() {
    document.getElementById("dailyCheckinModal").classList.add("hidden");
    selectedMood = null;
    document.querySelectorAll(".mood-option").forEach(btn => btn.classList.remove("selected"));
    document.getElementById("checkinNotes").value = "";
}

function selectMood(mood) {
    selectedMood = mood;
    document.querySelectorAll(".mood-option").forEach(btn => btn.classList.remove("selected"));
    document.querySelector(`[data-mood="${mood}"]`).classList.add("selected");
}

function submitDailyCheckin() {
    if (!selectedMood) {
        showToast("Please select a mood", "error");
        return;
    }

    const notes = document.getElementById("checkinNotes").value;
    const today = new Date().toDateString();
    const checkin = {
        date: new Date().toISOString(),
        mood: selectedMood,
        notes: notes
    };

    // Save to localStorage
    let checkins = JSON.parse(localStorage.getItem("daily_checkins") || "[]");
    checkins.push(checkin);
    localStorage.setItem("daily_checkins", JSON.stringify(checkins));
    localStorage.setItem("last_checkin_date", today);

    showToast("Daily check-in saved!", "success");
    closeDailyCheckin();
    updateProgressStats();
}

// ── Thought Journal ─────────────────────────────────────────
function openNewJournalEntry() {
    document.getElementById("journalEntryModal").classList.remove("hidden");
    lucide.createIcons();
}

function closeJournalEntryModal() {
    document.getElementById("journalEntryModal").classList.add("hidden");
    // Clear form
    document.getElementById("journalSituation").value = "";
    document.getElementById("journalThought").value = "";
    document.getElementById("journalEmotion").value = "";
    document.getElementById("journalDistortion").value = "";
    document.getElementById("journalReframe").value = "";
}

function saveJournalEntry() {
    const situation = document.getElementById("journalSituation").value.trim();
    const thought = document.getElementById("journalThought").value.trim();
    const emotion = document.getElementById("journalEmotion").value;
    const distortion = document.getElementById("journalDistortion").value;
    const reframe = document.getElementById("journalReframe").value.trim();

    if (!situation || !thought || !emotion) {
        showToast("Please fill in situation, thought, and emotion", "error");
        return;
    }

    const entry = {
        id: Date.now(),
        date: new Date().toISOString(),
        situation,
        thought,
        emotion,
        distortion,
        reframe
    };

    // Save to localStorage
    let journal = JSON.parse(localStorage.getItem("thought_journal") || "[]");
    journal.push(entry);
    localStorage.setItem("thought_journal", JSON.stringify(journal));

    showToast("Journal entry saved!", "success");
    closeJournalEntryModal();
    loadJournalEntries();
    checkAndUnlockAchievements();
}

function loadJournalEntries() {
    const journal = JSON.parse(localStorage.getItem("thought_journal") || "[]");
    const container = document.getElementById("journalEntries");

    if (journal.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i data-lucide="book-open"></i>
                <h3>No journal entries yet</h3>
                <p>Start recording your thoughts and challenging distortions</p>
            </div>`;
        lucide.createIcons();
        return;
    }

    // Update stats
    document.getElementById("journalTotalEntries").textContent = journal.length;
    document.getElementById("journalDistortionsIdentified").textContent = 
        journal.filter(e => e.distortion).length;
    document.getElementById("journalReframesWritten").textContent = 
        journal.filter(e => e.reframe).length;

    // Display entries (most recent first)
    container.innerHTML = journal.reverse().map(entry => {
        const date = new Date(entry.date);
        return `
            <div class="journal-entry-card">
                <div class="journal-entry-header">
                    <span class="journal-entry-date">${date.toLocaleDateString()} at ${date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
                    <span class="journal-entry-emotion">${EMOTION_EMOJI[entry.emotion] || ''} ${entry.emotion}</span>
                </div>
                <div class="journal-entry-content">
                    <div class="journal-entry-section">
                        <strong>Situation:</strong>
                        <p>${escapeHtml(entry.situation)}</p>
                    </div>
                    <div class="journal-entry-section">
                        <strong>Automatic Thought:</strong>
                        <p>${escapeHtml(entry.thought)}</p>
                    </div>
                    ${entry.distortion ? `
                        <div class="journal-entry-section">
                            <strong>Distortion:</strong>
                            <span class="distortion-badge">${entry.distortion.replace('_', ' ')}</span>
                        </div>
                    ` : ''}
                    ${entry.reframe ? `
                        <div class="journal-entry-section reframe-section">
                            <strong>Balanced Thought:</strong>
                            <p>${escapeHtml(entry.reframe)}</p>
                        </div>
                    ` : ''}
                </div>
            </div>`;
    }).join('');
    lucide.createIcons();
}

// ── Quick Tools ─────────────────────────────────────────────
function showGroundingTechnique() {
    const content = document.getElementById("toolContent");
    content.innerHTML = `
        <div class="tool-content-active">
            <h3>5-4-3-2-1 Grounding Technique</h3>
            <p>This sensory awareness exercise helps anchor you to the present moment.</p>
            <div class="grounding-steps">
                <div class="grounding-step">
                    <strong>5 things you can SEE</strong>
                    <p>Look around and name 5 things you can see right now</p>
                </div>
                <div class="grounding-step">
                    <strong>4 things you can TOUCH</strong>
                    <p>Notice 4 things you can physically feel (your feet on the floor, your back against the chair, etc.)</p>
                </div>
                <div class="grounding-step">
                    <strong>3 things you can HEAR</strong>
                    <p>Pause and listen for 3 sounds in your environment</p>
                </div>
                <div class="grounding-step">
                    <strong>2 things you can SMELL</strong>
                    <p>Identify 2 scents around you (or 2 you like to smell)</p>
                </div>
                <div class="grounding-step">
                    <strong>1 thing you can TASTE</strong>
                    <p>Notice 1 thing you can taste, or take a sip of water mindfully</p>
                </div>
            </div>
            <button class="btn-secondary" onclick="hideToolContent()">Close</button>
        </div>`;
    content.classList.remove("hidden");
    lucide.createIcons();
}

function showProgressiveRelaxation() {
    const content = document.getElementById("toolContent");
    content.innerHTML = `
        <div class="tool-content-active">
            <h3>Progressive Muscle Relaxation</h3>
            <p>Systematically tense and release muscle groups to release physical tension.</p>
            <div class="pmr-steps">
                <p><strong>Instructions:</strong> Tense each muscle group for 5 seconds, then release for 10 seconds.</p>
                <ol>
                    <li>Hands: Make tight fists</li>
                    <li>Arms: Flex biceps</li>
                    <li>Shoulders: Raise to ears</li>
                    <li>Face: Scrunch facial muscles</li>
                    <li>Chest: Take deep breath and hold</li>
                    <li>Stomach: Tighten abdominal muscles</li>
                    <li>Legs: Point toes and tighten thighs</li>
                    <li>Feet: Curl toes under</li>
                </ol>
                <p>Notice the difference between tension and relaxation in each area.</p>
            </div>
            <button class="btn-secondary" onclick="hideToolContent()">Close</button>
        </div>`;
    content.classList.remove("hidden");
    lucide.createIcons();
}

function showEmergencyCalming() {
    const content = document.getElementById("toolContent");
    content.innerHTML = `
        <div class="tool-content-active">
            <h3>TIPP Technique (Emergency Calming)</h3>
            <p>For intense emotional moments when you need immediate relief:</p>
            <div class="tipp-technique">
                <div class="tipp-item">
                    <strong>T - Temperature</strong>
                    <p>Splash cold water on your face or hold ice cubes. This triggers the dive reflex, slowing your heart rate.</p>
                </div>
                <div class="tipp-item">
                    <strong>I - Intense Exercise</strong>
                    <p>Do jumping jacks, run in place, or do push-ups for 60 seconds to burn off stress hormones.</p>
                </div>
                <div class="tipp-item">
                    <strong>P - Paced Breathing</strong>
                    <p>Breathe in for 4, out for 6. Make exhales longer than inhales to activate calm.</p>
                </div>
                <div class="tipp-item">
                    <strong>P - Paired Muscle Relaxation</strong>
                    <p>Tense muscles on inhale, release completely on exhale. Start with hands, move through body.</p>
                </div>
            </div>
            <button class="btn-secondary" onclick="hideToolContent()">Close</button>
        </div>`;
    content.classList.remove("hidden");
    lucide.createIcons();
}

function showSelfCompassion() {
    const content = document.getElementById("toolContent");
    content.innerHTML = `
        <div class="tool-content-active">
            <h3>Self-Compassion Break</h3>
            <p>When you're struggling, offer yourself the same kindness you'd give a good friend:</p>
            <div class="self-compassion-steps">
                <div class="compassion-step">
                    <strong>1. Acknowledge the difficulty</strong>
                    <p>"This is really hard right now" or "I'm suffering in this moment"</p>
                </div>
                <div class="compassion-step">
                    <strong>2. Recognize common humanity</strong>
                    <p>"Everyone struggles sometimes" or "I'm not alone in feeling this way"</p>
                </div>
                <div class="compassion-step">
                    <strong>3. Offer yourself kindness</strong>
                    <p>"May I be kind to myself" or "May I give myself the compassion I need"</p>
                </div>
                <div class="compassion-step">
                    <strong>4. Physical gesture (optional)</strong>
                    <p>Place your hand on your heart or give yourself a gentle hug</p>
                </div>
            </div>
            <button class="btn-secondary" onclick="hideToolContent()">Close</button>
        </div>`;
    content.classList.remove("hidden");
    lucide.createIcons();
}

function showThoughtDefusion() {
    const content = document.getElementById("toolContent");
    content.innerHTML = `
        <div class="tool-content-active">
            <h3>Thought Defusion</h3>
            <p>Create distance from unhelpful thoughts instead of fighting them:</p>
            <div class="defusion-techniques">
                <div class="defusion-item">
                    <strong>Name it</strong>
                    <p>"I'm having the thought that..." instead of "I am..."</p>
                </div>
                <div class="defusion-item">
                    <strong>Thank your mind</strong>
                    <p>"Thanks mind, I see you're trying to protect me with this worry"</p>
                </div>
                <div class="defusion-item">
                    <strong>Silly voice</strong>
                    <p>Repeat the thought in a cartoon character voice to reduce its power</p>
                </div>
                <div class="defusion-item">
                    <strong>Leaves on a stream</strong>
                    <p>Imagine placing the thought on a leaf floating down a stream, watching it drift away</p>
                </div>
                <div class="defusion-item">
                    <strong>Notice, don't judge</strong>
                    <p>"I'm noticing feelings of anxiety" vs "I AM anxious"</p>
                </div>
            </div>
            <button class="btn-secondary" onclick="hideToolContent()">Close</button>
        </div>`;
    content.classList.remove("hidden");
    lucide.createIcons();
}

function hideToolContent() {
    document.getElementById("toolContent").classList.add("hidden");
}

// ── Progress & Achievements ─────────────────────────────────
function loadAchievements() {
    const unlocked = JSON.parse(localStorage.getItem("unlocked_achievements") || "[]");
    const history = JSON.parse(localStorage.getItem("conversation_history") || "[]");
    const journal = JSON.parse(localStorage.getItem("thought_journal") || "[]");
    const checkins = JSON.parse(localStorage.getItem("daily_checkins") || "[]");
    const breathingSessions = parseInt(localStorage.getItem("breathing_sessions") || "0");
    
    const achievements = [
        { id: "first_chat", name: "First Steps", description: "Started your first conversation", icon: "message-circle", unlocked: unlocked.includes("first_chat") || history.length >= 1 },
        { id: "5_sessions", name: "Getting Started", description: "Completed 5 chat sessions", icon: "target", unlocked: unlocked.includes("5_sessions") || history.length >= 5 },
        { id: "breathing_master", name: "Breath Master", description: "Practiced breathing exercises 10 times", icon: "wind", unlocked: unlocked.includes("breathing_master") || breathingSessions >= 10 },
        { id: "journal_keeper", name: "Journal Keeper", description: "Created 5 thought journal entries", icon: "book-open", unlocked: unlocked.includes("journal_keeper") || journal.length >= 5 },
        { id: "7_day_streak", name: "Week Warrior", description: "7-day check-in streak", icon: "flame", unlocked: unlocked.includes("7_day_streak") || calculateStreak(checkins) >= 7 },
        { id: "distortion_detective", name: "Distortion Detective", description: "Identified 20 cognitive distortions", icon: "search", unlocked: unlocked.includes("distortion_detective") || journal.filter(e => e.distortion).length >= 20 },
        { id: "self_compassion", name: "Self-Compassion Champion", description: "Practiced self-kindness techniques 15 times", icon: "heart", unlocked: false },
        { id: "wellness_warrior", name: "Wellness Warrior", description: "30 days of active engagement", icon: "trophy", unlocked: calculateActiveDays() >= 30 }
    ];

    const grid = document.getElementById("achievementsGrid");
    grid.innerHTML = achievements.map(ach => `
        <div class="achievement-card ${ach.unlocked ? 'unlocked' : 'locked'}">
            <div class="achievement-icon">
                <i data-lucide="${ach.icon}"></i>
            </div>
            <div class="achievement-content">
                <h4>${ach.name}</h4>
                <p>${ach.description}</p>
            </div>
            ${ach.unlocked ? '<div class="achievement-badge">✓</div>' : ''}
        </div>
    `).join('');
    lucide.createIcons();
}

function updateProgressStats() {
    // Calculate stats from localStorage
    const history = JSON.parse(localStorage.getItem("conversation_history") || "[]");
    const journal = JSON.parse(localStorage.getItem("thought_journal") || "[]");
    const checkins = JSON.parse(localStorage.getItem("daily_checkins") || "[]");

    document.getElementById("daysActive").textContent = calculateActiveDays();
    document.getElementById("totalConversations").textContent = history.length;
    document.getElementById("techniquesUsed").textContent = calculateTechniquesUsed();
    document.getElementById("checkInStreak").textContent = calculateStreak(checkins);

    // Update level progress
    const xp = history.length * 10 + journal.length * 15 + checkins.length * 5;
    const level = Math.floor(xp / 100);
    const levelNames = ["Beginner", "Practitioner", "Advanced", "Expert", "Master"];
    
    document.getElementById("currentLevel").textContent = levelNames[Math.min(level, 4)];
    document.getElementById("levelXP").textContent = `${xp % 100} / 100 XP`;
    document.getElementById("levelProgressFill").style.width = `${(xp % 100)}%`;
}

function calculateActiveDays() {
    const history = JSON.parse(localStorage.getItem("conversation_history") || "[]");
    const uniqueDays = new Set(history.map(h => new Date(h.timestamp).toDateString()));
    return uniqueDays.size;
}

function calculateTechniquesUsed() {
    return parseInt(localStorage.getItem("techniques_practiced") || "0");
}

function calculateStreak(checkins) {
    if (checkins.length === 0) return 0;
    
    checkins.sort((a, b) => new Date(b.date) - new Date(a.date));
    let streak = 1;
    const today = new Date().toDateString();
    
    if (new Date(checkins[0].date).toDateString() !== today) return 0;
    
    for (let i = 1; i < checkins.length; i++) {
        const current = new Date(checkins[i].date);
        const previous = new Date(checkins[i-1].date);
        const dayDiff = Math.floor((previous - current) / (1000 * 60 * 60 * 24));
        
        if (dayDiff === 1) streak++;
        else break;
    }
    
    return streak;
}

// ── Mood Tracking Chart ─────────────────────────────────────
function loadMoodChart() {
    const checkins = JSON.parse(localStorage.getItem("daily_checkins") || "[]");
    
    if (checkins.length === 0) {
        document.getElementById("moodChartContainer").innerHTML = `
            <div class="empty-state">
                <i data-lucide="smile"></i>
                <h3>No mood data yet</h3>
                <p>Start tracking your daily mood to see trends over time</p>
            </div>`;
        lucide.createIcons();
        return;
    }

    // Get last 30 days
    const last30Days = checkins.slice(-30);
    const labels = last30Days.map(c => new Date(c.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
    
    // Map moods to numeric values
    const moodValues = {
        'great': 5,
        'good': 4,
        'okay': 3,
        'struggling': 2,
        'difficult': 1
    };
    
    const data = last30Days.map(c => moodValues[c.mood] || 3);

    const ctx = document.getElementById("moodChart");
    if (window.moodChartInstance) window.moodChartInstance.destroy();
    
    window.moodChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Mood Level',
                data: data,
                borderColor: 'rgb(124, 58, 237)',
                backgroundColor: 'rgba(124, 58, 237, 0.1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const moodLabels = ['', 'Difficult', 'Struggling', 'Okay', 'Good', 'Great'];
                            return moodLabels[context.parsed.y];
                        }
                    }
                }
            },
            scales: {
                y: {
                    min: 1,
                    max: 5,
                    ticks: {
                        stepSize: 1,
                        callback: function(value) {
                            const labels = ['', 'Difficult', 'Struggling', 'Okay', 'Good', 'Great'];
                            return labels[value];
                        },
                        color: '#9090a8'
                    },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' }
                },
                x: {
                    ticks: { color: '#9090a8', maxRotation: 45 },
                    grid: { display: false }
                }
            }
        }
    });
}

// ── Achievement System ──────────────────────────────────────
function checkAndUnlockAchievements() {
    const unlocked = JSON.parse(localStorage.getItem("unlocked_achievements") || "[]");
    const history = JSON.parse(localStorage.getItem("conversation_history") || "[]");
    const journal = JSON.parse(localStorage.getItem("thought_journal") || "[]");
    const checkins = JSON.parse(localStorage.getItem("daily_checkins") || "[]");
    const breathingSessions = parseInt(localStorage.getItem("breathing_sessions") || "0");
    
    const achievements = [
        { id: "first_chat", condition: history.length >= 1, name: "First Steps", icon: "message-circle" },
        { id: "5_sessions", condition: history.length >= 5, name: "Getting Started", icon: "target" },
        { id: "breathing_master", condition: breathingSessions >= 10, name: "Breath Master", icon: "wind" },
        { id: "journal_keeper", condition: journal.length >= 5, name: "Journal Keeper", icon: "book-open" },
        { id: "7_day_streak", condition: calculateStreak(checkins) >= 7, name: "Week Warrior", icon: "flame" },
        { id: "distortion_detective", condition: journal.filter(e => e.distortion).length >= 20, name: "Distortion Detective", icon: "search" },
    ];

    achievements.forEach(ach => {
        if (ach.condition && !unlocked.includes(ach.id)) {
            unlocked.push(ach.id);
            localStorage.setItem("unlocked_achievements", JSON.stringify(unlocked));
            showAchievementToast(ach.name, ach.icon);
        }
    });
}

function showAchievementToast(name, icon) {
    const toast = document.createElement('div');
    toast.className = 'toast achievement-toast';
    toast.innerHTML = `
        <div class="achievement-unlock">
            <i data-lucide="${icon}"></i>
            <div>
                <strong>Achievement Unlocked!</strong>
                <p>${name}</p>
            </div>
        </div>`;
    document.body.appendChild(toast);
    lucide.createIcons();
    
    setTimeout(() => {
        toast.style.animation = 'slideDown 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// ── Auto Daily Check-In Prompt ──────────────────────────────
// Check for daily check-in on app boot
if (token && userId) {
    const lastCheckin = localStorage.getItem("last_checkin_date");
    const today = new Date().toDateString();
    
    if (lastCheckin !== today) {
        setTimeout(() => {
            openDailyCheckin();
        }, 2000); // Show after 2 seconds
    }
}

/* =========================================================
   ACTIVITY SPACES - Dedicated mental health topic spaces
   ========================================================= */

let currentActivity = null;
let activityMessages = [];

const ACTIVITY_SPACES = {
    'stress': {
        'name': 'Stress Management',
        'icon': 'wind',
        'color': '#f59e0b',
        'gradient': 'linear-gradient(135deg, #d97706, #f59e0b)',
        'description': 'Find calm in chaos. Techniques for managing daily stress.',
        'greeting': "Welcome to your stress management space. This is where we work on finding calm in the chaos. What's feeling stressful today?",
        'prompts': [
            "I'm feeling overwhelmed with everything",
            "Work stress is getting to be too much",
            "I can't seem to relax anymore",
            "Everything feels urgent and pressing"
        ]
    },
    'anxiety': {
        'name': 'Anxiety Support',
        'icon': 'heart-pulse',
        'color': '#8b5cf6',
        'gradient': 'linear-gradient(135deg, #7c3aed, #a855f7)',
        'description': 'Ground yourself. Tools to manage anxious thoughts and feelings.',
        'greeting': "Welcome to your anxiety support space. Let's work together to understand and manage these anxious feelings. What's been on your mind?",
        'prompts': [
            "I can't stop worrying about the future",
            "My anxiety is making it hard to focus",
            "I'm having panic-like symptoms",
            "I feel anxious but don't know why"
        ]
    },
    'mood': {
        'name': 'Mood Boosting',
        'icon': 'sparkles',
        'color': '#10b981',
        'gradient': 'linear-gradient(135deg, #059669, #10b981)',
        'description': 'Lift your spirits. Activities and insights for better mood.',
        'greeting': "Welcome to your mood boosting space! Let's focus on what brings you joy and energy. How are you feeling today?",
        'prompts': [
            "I've been feeling down lately",
            "I want to feel more positive",
            "Nothing seems fun anymore",
            "Help me find motivation"
        ]
    },
    'fear': {
        'name': 'Fear Processing',
        'icon': 'shield',
        'color': '#f43f5e',
        'gradient': 'linear-gradient(135deg, #db2777, #f43f5e)',
        'description': 'Face your fears. A safe space to explore and process fear.',
        'greeting': "This is your safe space for working with fear. Let's explore what's feeling scary and figure out how to work through it together. What brings you here today?",
        'prompts': [
            "I'm scared something bad will happen",
            "A specific situation makes me really afraid",
            "I avoid things because of fear",
            "My fear feels irrational but won't go away"
        ]
    },
    'sleep': {
        'name': 'Sleep & Rest',
        'icon': 'moon',
        'color': '#06b6d4',
        'gradient': 'linear-gradient(135deg, #0891b2, #06b6d4)',
        'description': 'Rest well. Support for better sleep and evening wind-down.',
        'greeting': "Welcome to your sleep and rest space. Let's work on helping you get the quality rest you deserve. What's been going on with your sleep?",
        'prompts': [
            "I can't fall asleep at night",
            "I wake up tired even after sleeping",
            "My mind races when I try to sleep",
            "I need help with a bedtime routine"
        ]
    },
    'relationships': {
        'name': 'Relationship Support',
        'icon': 'users',
        'color': '#ec4899',
        'gradient': 'linear-gradient(135deg, #db2777, #ec4899)',
        'description': 'Connect better. Navigate relationship challenges with clarity.',
        'greeting': "Welcome to your relationship support space. Let's talk through what's happening in your relationships and find healthy ways forward. What's on your mind?",
        'prompts': [
            "I'm having issues with my partner",
            "A friendship is feeling strained",
            "I don't know how to communicate my needs",
            "I feel misunderstood by people close to me"
        ]
    },
    'confidence': {
        'name': 'Self-Confidence',
        'icon': 'star',
        'color': '#facc15',
        'gradient': 'linear-gradient(135deg, #eab308, #facc15)',
        'description': 'Believe in yourself. Build confidence and self-worth.',
        'greeting': "Welcome to your confidence-building space. Let's work on recognizing your strengths and building genuine self-worth. What would you like to work on?",
        'prompts': [
            "I don't feel good enough",
            "I struggle with self-doubt",
            "I want to be more confident",
            "I compare myself to others constantly"
        ]
    },
    'focus': {
        'name': 'Focus & Clarity',
        'icon': 'target',
        'color': '#14b8a6',
        'gradient': 'linear-gradient(135deg, #0d9488, #14b8a6)',
        'description': 'Clear your mind. Improve focus and mental clarity.',
        'greeting': "Welcome to your focus and clarity space. Let's work on clearing the mental fog and improving your concentration. What's making it hard to focus?",
        'prompts': [
            "I can't concentrate on anything",
            "My mind feels scattered",
            "I'm easily distracted",
            "I need help staying on task"
        ]
    }
};

function openActivitySpace(activityType) {
    currentActivity = activityType;
    activityMessages = [];
    
    const activity = ACTIVITY_SPACES[activityType];
    if (!activity) return;
    
    // Update modal header
    document.getElementById('activitySpaceTitle').textContent = activity.name;
    document.getElementById('activitySpaceDescription').textContent = activity.description;
    
    const iconHeader = document.getElementById('activityIconHeader');
    iconHeader.style.background = activity.gradient;
    iconHeader.innerHTML = `<i data-lucide="${activity.icon}"></i>`;
    
    // Show quick prompts
    const promptsContainer = document.getElementById('activityQuickPrompts');
    promptsContainer.innerHTML = activity.prompts.map(prompt => 
        `<button class="activity-prompt-btn" onclick="useActivityPrompt('${prompt.replace(/'/g, "\\'")}')">${prompt}</button>`
    ).join('');
    
    // Show greeting message
    const messagesContainer = document.getElementById('activityMessages');
    messagesContainer.innerHTML = `
        <div class="activity-welcome">
            <div class="activity-welcome-icon" style="background: ${activity.gradient};">
                <i data-lucide="${activity.icon}"></i>
            </div>
            <h3>${activity.name}</h3>
            <p>${activity.greeting}</p>
        </div>
    `;
    
    // Show modal
    document.getElementById('activitySpaceModal').classList.remove('hidden');
    document.getElementById('activityInput').focus();
    
    lucide.createIcons();
}

function closeActivitySpace() {
    document.getElementById('activitySpaceModal').classList.add('hidden');
    currentActivity = null;
    activityMessages = [];
}

function useActivityPrompt(prompt) {
    document.getElementById('activityInput').value = prompt;
    sendActivityMessage();
}

async function sendActivityMessage() {
    const input = document.getElementById('activityInput');
    const message = input.value.trim();
    
    if (!message || !currentActivity) return;
    
    // Clear input
    input.value = '';
    
    // Hide quick prompts after first message
    if (activityMessages.length === 0) {
        document.getElementById('activityQuickPrompts').style.display = 'none';
    }
    
    // Add user message to UI
    addActivityMessage(message, 'user');
    
    // Show typing indicator
    const typingId = showActivityTyping();
    
    try {
        // Send to activity-specific endpoint
        const response = await fetch(`${API_BASE}/activity-chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                message,
                activity_type: currentActivity
            })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeActivityTyping(typingId);
        
        if (data.response) {
            addActivityMessage(data.response, 'bot');
        } else {
            addActivityMessage("I'm here to help. Could you tell me more about what's on your mind?", 'bot');
        }
    } catch (error) {
        console.error('Activity chat error:', error);
        removeActivityTyping(typingId);
        addActivityMessage("I'm having trouble connecting right now. Please try again.", 'bot');
    }
}

function addActivityMessage(text, sender) {
    const messagesContainer = document.getElementById('activityMessages');
    
    // Remove welcome screen if it exists
    const welcome = messagesContainer.querySelector('.activity-welcome');
    if (welcome) {
        welcome.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `activity-message ${sender}`;
    messageDiv.innerHTML = `
        <div class="activity-message-content">${formatMessage(text)}</div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    activityMessages.push({ text, sender });
    
    lucide.createIcons();
}

function showActivityTyping() {
    const messagesContainer = document.getElementById('activityMessages');
    const typingDiv = document.createElement('div');
    const typingId = 'typing-' + Date.now();
    typingDiv.id = typingId;
    typingDiv.className = 'activity-message bot';
    typingDiv.innerHTML = `
        <div class="activity-message-content">
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return typingId;
}

function removeActivityTyping(typingId) {
    const typingEl = document.getElementById(typingId);
    if (typingEl) typingEl.remove();
}

function handleActivityInputKey(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendActivityMessage();
    }
}

// Format message helper (reuse from main chat)
function formatMessage(text) {
    // Convert markdown-style formatting to HTML
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
}