/**
 * SpamShield AI — Full-Stack Interactive Frontend Orchestrator
 */

document.addEventListener('DOMContentLoaded', () => {
    // ----------------------------------------------------------------------
    // 1. Initialize Particles.js Mesh Background
    // ----------------------------------------------------------------------
    if (document.getElementById('particles-js') && typeof particlesJS !== 'undefined') {
        particlesJS('particles-js', {
            "particles": {
                "number": { "value": 60, "density": { "enable": true, "value_area": 800 } },
                "color": { "value": "#00E5FF" },
                "shape": { "type": "circle" },
                "opacity": { "value": 0.25, "random": true },
                "size": { "value": 3, "random": true },
                "line_linked": {
                    "enable": true,
                    "distance": 150,
                    "color": "#7B2FFF",
                    "opacity": 0.15,
                    "width": 1
                },
                "move": {
                    "enable": true,
                    "speed": 1.5,
                    "direction": "none",
                    "random": true,
                    "straight": false,
                    "out_mode": "out",
                    "bounce": false
                }
            },
            "interactivity": {
                "detect_on": "canvas",
                "events": {
                    "onhover": { "enable": true, "mode": "bubble" },
                    "onclick": { "enable": true, "mode": "push" },
                    "resize": true
                },
                "modes": {
                    "bubble": { "distance": 200, "size": 6, "duration": 2, "opacity": 0.8, "speed": 3 },
                    "push": { "particles_nb": 4 }
                }
            },
            "retina_detect": true
        });
    }

    // ----------------------------------------------------------------------
    // 2. Initialize AOS (Animate on Scroll)
    // ----------------------------------------------------------------------
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true,
            mirror: false
        });
    }

    // ----------------------------------------------------------------------
    // 3. Navbar Mobile Toggle
    // ----------------------------------------------------------------------
    const menuBtn = document.getElementById('menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');

    if (menuBtn && mobileMenu) {
        menuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
            if (mobileMenu.classList.contains('hidden')) {
                menuIcon.className = 'fa-solid fa-bars text-2xl';
            } else {
                menuIcon.className = 'fa-solid fa-xmark text-2xl';
            }
        });
    }

    // ----------------------------------------------------------------------
    // 4. Hero Section Typing Effect
    // ----------------------------------------------------------------------
    const typingHero = document.getElementById('typing-hero');
    if (typingHero) {
        const phrases = ["Real-Time Detection.", "Phishing Protection.", "Scam Prevention.", "AI-Powered Defense."];
        let phraseIdx = 0;
        let charIdx = 0;
        let isDeleting = false;
        let typeSpeed = 100;

        function typeEffect() {
            const currentPhrase = phrases[phraseIdx];
            if (isDeleting) {
                typingHero.textContent = currentPhrase.substring(0, charIdx - 1);
                charIdx--;
                typeSpeed = 40;
            } else {
                typingHero.textContent = currentPhrase.substring(0, charIdx + 1);
                charIdx++;
                typeSpeed = 120;
            }

            if (!isDeleting && charIdx === currentPhrase.length) {
                isDeleting = true;
                typeSpeed = 1500; // Delay before starting to backspace
            } else if (isDeleting && charIdx === 0) {
                isDeleting = false;
                phraseIdx = (phraseIdx + 1) % phrases.length;
                typeSpeed = 400; // Pause before typing next phrase
            }

            setTimeout(typeEffect, typeSpeed);
        }
        setTimeout(typeEffect, 1000);
    }

    // ----------------------------------------------------------------------
    // 5. SMS Detector Scanner Actions
    // ----------------------------------------------------------------------
    const smsInput = document.getElementById('sms-input');
    const charCounter = document.getElementById('char-counter');
    const clearBtn = document.getElementById('clear-btn');
    const analyzeBtn = document.getElementById('analyze-btn');
    const scanLaser = document.getElementById('cyber-scan-laser');
    const errorAlert = document.getElementById('error-alert');
    const errorMessage = document.getElementById('error-message');
    const resultContainer = document.getElementById('result-container');

    // Focus glow effects
    if (smsInput) {
        smsInput.addEventListener('focus', () => {
            smsInput.parentElement.parentElement.classList.add('cyan-glow');
        });
        smsInput.addEventListener('blur', () => {
            smsInput.parentElement.parentElement.classList.remove('cyan-glow');
        });

        // Real-time character counter
        smsInput.addEventListener('input', () => {
            const len = smsInput.value.length;
            charCounter.textContent = `${len} / 1000`;
            if (len > 1000) {
                charCounter.classList.add('text-red-500');
            } else {
                charCounter.classList.remove('text-red-500');
            }
        });
    }

    // Clear input handler
    if (clearBtn && smsInput) {
        clearBtn.addEventListener('click', () => {
            smsInput.value = '';
            charCounter.textContent = '0 / 1000';
            errorAlert.classList.add('hidden');
            resultContainer.classList.add('hidden');
            resultContainer.innerHTML = '';
            smsInput.focus();
        });
    }

    // Submit handler
    if (analyzeBtn && smsInput) {
        analyzeBtn.addEventListener('click', async () => {
            const rawMessage = smsInput.value.trim();
            errorAlert.classList.add('hidden');

            // Validation
            if (!rawMessage) {
                showError("Please enter a valid message to analyze.");
                return;
            }

            if (rawMessage.length > 1000) {
                showError("Message exceeds the maximum length of 1000 characters.");
                return;
            }

            // Start Cyber Scanning Animation
            scanLaser.classList.remove('hidden');
            scanLaser.classList.add('cyber-scan-indicator');
            analyzeBtn.disabled = true;
            analyzeBtn.innerHTML = `<i class="fa-solid fa-spinner animate-spin"></i> <span>Scanning Network Vectors...</span>`;
            resultContainer.classList.add('hidden');

            try {
                // Post request to local prediction route
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: rawMessage })
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || "Server responded with an error.");
                }

                // Render dynamic result cards
                renderResult(rawMessage, data);
                
                // Save locally
                saveToLocalStorage(rawMessage, data);

            } catch (err) {
                showError(err.message || "Failed to establish a connection with the prediction gateway.");
            } finally {
                // Stop animations
                scanLaser.classList.add('hidden');
                scanLaser.classList.remove('cyber-scan-indicator');
                analyzeBtn.disabled = false;
                analyzeBtn.innerHTML = `<i class="fa-solid fa-circle-nodes"></i> <span>Analyze Message</span>`;
            }
        });
    }

    function showError(msg) {
        if (errorMessage && errorAlert) {
            errorMessage.textContent = msg;
            errorAlert.classList.remove('hidden');
            // GSAP Shake
            if (typeof gsap !== 'undefined') {
                gsap.fromTo("#error-alert", { x: -10 }, { x: 0, duration: 0.4, ease: "rough", repeat: 3 });
            }
        }
    }

    function renderResult(message, data) {
        if (!resultContainer) return;
        
        const isSpam = data.prediction === 'Spam';
        const borderGlowClass = isSpam ? 'danger-glow' : 'success-glow';
        
        let keywordTags = '';
        if (data.keywords && data.keywords.length > 0) {
            keywordTags = data.keywords.map(kw => `
                <span class="px-2.5 py-1 text-xs font-semibold rounded bg-[#050816] text-[#00E5FF] border border-[#00E5FF]/20 mono-text">
                    ${kw}
                </span>
            `).join('');
        } else {
            keywordTags = `<span class="text-xs text-slate-500 italic">None detected</span>`;
        }

        const riskBadgeColor = {
            'High': 'bg-[#FF3B5C]/20 text-[#FF3B5C] border border-[#FF3B5C]/40',
            'Medium': 'bg-amber-500/20 text-amber-400 border border-amber-500/40',
            'Low': 'bg-[#00FFB2]/20 text-[#00FFB2] border border-[#00FFB2]/40'
        }[data.risk_level] || 'bg-slate-800 text-slate-300';

        resultContainer.innerHTML = `
            <div class="glass-card p-6 md:p-8 ${borderGlowClass} relative overflow-hidden transition-all duration-300">
                <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
                    <!-- Verdict Title -->
                    <div class="flex items-center space-x-4">
                        <div class="w-16 h-16 rounded-xl flex items-center justify-center text-4xl shadow-lg ${isSpam ? 'bg-red-500/10 text-red-500 shadow-red-500/10' : 'bg-emerald-500/10 text-emerald-500 shadow-emerald-500/10'}">
                            <i class="${isSpam ? 'fa-solid fa-triangle-exclamation' : 'fa-solid fa-shield-halved'}"></i>
                        </div>
                        <div>
                            <div class="text-xs text-[#AAB4C5] uppercase tracking-widest mono-text">Prediction outcome</div>
                            <h3 class="text-2xl font-bold orbitron-title text-white flex items-center gap-3">
                                <span>Message Verdict:</span>
                                <span class="${isSpam ? 'text-[#FF3B5C]' : 'text-[#00FFB2]'}">${data.prediction}</span>
                            </h3>
                        </div>
                    </div>
                    
                    <!-- Risk Level Badge -->
                    <div class="flex flex-col items-start md:items-end">
                        <div class="text-xs text-[#AAB4C5] uppercase tracking-widest mono-text mb-1.5">Threat risk score</div>
                        <span class="px-4 py-1.5 rounded-full font-bold text-xs uppercase tracking-wider ${riskBadgeColor}">
                            ${data.risk_level} Risk
                        </span>
                    </div>
                </div>

                <!-- Probability Weight Progress bar -->
                <div class="mt-8 space-y-2">
                    <div class="flex justify-between items-center text-xs text-[#AAB4C5] mono-text">
                        <span>Spam Probability Weight</span>
                        <span>${(data.probability * 100).toFixed(1)}%</span>
                    </div>
                    <div class="w-full h-3 rounded-full bg-slate-950 overflow-hidden border border-slate-900">
                        <div class="h-full rounded-full transition-all duration-1000 ease-out" 
                             style="width: 0%; background: ${isSpam ? 'var(--gradient-danger)' : 'var(--gradient-success)'}" 
                             id="result-prob-bar"></div>
                    </div>
                </div>

                <!-- Metrics breakdown -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8 border-t border-slate-800/80 pt-6">
                    <div>
                        <div class="text-xs text-[#AAB4C5] uppercase tracking-widest mono-text mb-2">Model Confidence</div>
                        <div class="text-2xl font-extrabold text-white orbitron-title">${data.confidence}%</div>
                        <p class="text-xs text-[#AAB4C5] mt-1">Joint class conditional probability matching weight.</p>
                    </div>
                    <div>
                        <div class="text-xs text-[#AAB4C5] uppercase tracking-widest mono-text mb-2">Flagged Threat Keywords</div>
                        <div class="flex flex-wrap gap-2 mt-1">
                            ${keywordTags}
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        resultContainer.classList.remove('hidden');

        // GSAP animate result reveal
        if (typeof gsap !== 'undefined') {
            gsap.fromTo(resultContainer, { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: "power2.out" });
            setTimeout(() => {
                const probPercent = data.probability * 100;
                const bar = document.getElementById('result-prob-bar');
                if (bar) bar.style.width = `${probPercent}%`;
            }, 100);
        } else {
            const bar = document.getElementById('result-prob-bar');
            if (bar) bar.style.width = `${data.probability * 100}%`;
        }
    }

    // ----------------------------------------------------------------------
    // 6. LocalStorage Analytics Persistent State
    // ----------------------------------------------------------------------
    function saveToLocalStorage(message, data) {
        let scans = JSON.parse(localStorage.getItem('spamshield_scans') || '[]');
        
        // Structure entry
        const entry = {
            message: message,
            prediction: data.prediction,
            confidence: data.confidence,
            risk_level: data.risk_level,
            probability: data.probability,
            keywords: data.keywords,
            created_at: new Date().toISOString()
        };

        // Prepend and cap at 50
        scans.unshift(entry);
        if (scans.length > 50) {
            scans.pop();
        }

        localStorage.setItem('spamshield_scans', JSON.stringify(scans));
    }

    // ----------------------------------------------------------------------
    // 7. Security Dashboard Rendering (Only active on /dashboard page)
    // ----------------------------------------------------------------------
    if (document.getElementById('stat-total')) {
        renderDashboardData();
        
        const clearHistoryBtn = document.getElementById('clear-history-btn');
        if (clearHistoryBtn) {
            clearHistoryBtn.addEventListener('click', () => {
                if (confirm("Are you sure you want to wipe all local scanning logs?")) {
                    localStorage.removeItem('spamshield_scans');
                    renderDashboardData();
                }
            });
        }
    }

    async function renderDashboardData() {
        // Read local
        let localScans = JSON.parse(localStorage.getItem('spamshield_scans') || '[]');
        
        // Try fetching server-side sqlite database history
        try {
            const response = await fetch('/api/history');
            if (response.ok) {
                const dbScans = await response.json();
                if (dbScans && dbScans.length > 0) {
                    // Merge local and server scans, avoiding duplicate messages
                    const merged = [...localScans];
                    dbScans.forEach(db => {
                        const exists = merged.some(local => local.message === db.message);
                        if (!exists) {
                            merged.push(db);
                        }
                    });
                    // Sort descending by time
                    merged.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
                    localScans = merged.slice(0, 50);
                }
            }
        } catch (err) {
            console.warn("Could not sync with backend SQLite. Displaying local data instead.", err);
        }

        const totalCount = localScans.length;
        const spamCount = localScans.filter(s => s.prediction === 'Spam' || s.prediction === 'spam').length;
        const safeCount = totalCount - spamCount;
        
        const spamRatio = totalCount > 0 ? Math.round((spamCount / totalCount) * 100) : 0;
        const safeRatio = totalCount > 0 ? Math.round((safeCount / totalCount) * 100) : 0;

        // Animate counter displays
        animateCounter('stat-total', totalCount);
        animateCounter('stat-spam', spamCount);
        animateCounter('stat-safe', safeCount);

        const spamRatioEl = document.getElementById('stat-spam-ratio');
        if (spamRatioEl) spamRatioEl.textContent = `${spamRatio}% threat ratio`;
        
        const safeRatioEl = document.getElementById('stat-safe-ratio');
        if (safeRatioEl) safeRatioEl.textContent = `${safeRatio}% safe ratio`;

        // Render history table (last 10)
        const tableBody = document.getElementById('history-table-body');
        if (tableBody) {
            if (localScans.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="5" class="py-12 text-center text-[#AAB4C5]/50 italic">
                            <i class="fa-solid fa-shield-halved text-4xl text-slate-800 mb-2 block"></i>
                            No scans recorded yet. Use the scanner tool on the Home page to start.
                        </td>
                    </tr>
                `;
            } else {
                tableBody.innerHTML = localScans.slice(0, 10).map(s => {
                    const isSpam = s.prediction === 'Spam' || s.prediction === 'spam';
                    const displayPrediction = isSpam ? 'Spam' : 'Safe';
                    const badgeClass = isSpam ? 'bg-[#FF3B5C]/15 text-[#FF3B5C]' : 'bg-[#00FFB2]/15 text-[#00FFB2]';
                    const riskColor = {
                        'High': 'text-[#FF3B5C] font-semibold',
                        'Medium': 'text-amber-400 font-semibold',
                        'Low': 'text-[#00FFB2] font-semibold'
                    }[s.risk_level] || 'text-slate-300';

                    // Format date
                    let dateStr = 'Just Now';
                    if (s.created_at) {
                        try {
                            const dateObj = new Date(s.created_at);
                            dateStr = dateObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                        } catch (e) {
                            dateStr = 'Just Now';
                        }
                    }

                    // Excerpt
                    const excerpt = s.message.length > 50 ? s.message.substring(0, 47) + '...' : s.message;

                    return `
                        <tr class="hover:bg-slate-900/30 transition-colors duration-150 border-b border-slate-800/50">
                            <td class="py-3.5 pr-4 font-medium text-slate-200" title="${escapeHTML(s.message)}">${escapeHTML(excerpt)}</td>
                            <td class="py-3.5"><span class="px-2 py-0.5 rounded text-xs uppercase font-bold tracking-wider ${badgeClass}">${displayPrediction}</span></td>
                            <td class="py-3.5 font-bold mono-text text-white">${s.confidence}%</td>
                            <td class="py-3.5 ${riskColor} uppercase text-xs mono-text">${s.risk_level}</td>
                            <td class="py-3.5 text-right text-xs text-[#AAB4C5] mono-text">${dateStr}</td>
                        </tr>
                    `;
                }).join('');
            }
        }

        // Render dynamic Chart.js doughnut
        renderChart(safeCount, spamCount);
    }

    function animateCounter(id, targetVal) {
        const el = document.getElementById(id);
        if (!el) return;
        const currentVal = parseInt(el.textContent) || 0;
        
        if (typeof gsap !== 'undefined') {
            const obj = { val: currentVal };
            gsap.to(obj, {
                val: targetVal,
                duration: 1,
                ease: "power2.out",
                onUpdate: () => {
                    el.textContent = Math.floor(obj.val);
                }
            });
        } else {
            el.textContent = targetVal;
        }
    }

    let myChart = null;
    function renderChart(safeVal, spamVal) {
        const ctx = document.getElementById('ratioChart');
        if (!ctx) return;

        const fallback = document.getElementById('chart-fallback');
        
        if (safeVal === 0 && spamVal === 0) {
            if (fallback) fallback.classList.remove('hidden');
            ctx.classList.add('hidden');
            return;
        } else {
            if (fallback) fallback.classList.add('hidden');
            ctx.classList.remove('hidden');
        }

        if (myChart) {
            myChart.destroy();
        }

        if (typeof Chart !== 'undefined') {
            myChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Safe passed', 'Spam Flagged'],
                    borderColor: '#050816',
                    datasets: [{
                        data: [safeVal, spamVal],
                        backgroundColor: ['#00FFB2', '#FF3B5C'],
                        borderColor: '#050816',
                        borderWidth: 2,
                        hoverOffset: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                color: '#AAB4C5',
                                font: { family: 'Outfit', size: 11 },
                                padding: 15
                            }
                        }
                    },
                    cutout: '70%'
                }
            });
        }
    }

    function escapeHTML(str) {
        if (!str) return '';
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
});
