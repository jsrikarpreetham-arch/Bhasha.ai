<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bhasha AI - Advanced English Improvement</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @keyframes slideIn {
            from { transform: translateX(400px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        .animate-slide-in { animation: slideIn 0.3s ease-out; }
        @keyframes ping {
            75%, 100% { transform: scale(2); opacity: 0; }
        }
        .animate-ping { animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite; }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .animate-spin { animation: spin 1s linear infinite; }
    </style>
</head>
<body class="bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 min-h-screen">
    <div id="app"></div>
    <script>
        let state = {
            inputText: '', outputText: '', detectedEmotion: null, emotionExplanation: '',
            isListening: false, isContinuousListening: false, isProcessing: false,
            copied: false, currentPage: null, toastMessage: ''
        };
        let recognition = null;
        let continuousDesired = false;

        function showToast(msg) {
            state.toastMessage = msg;
            render();
            setTimeout(() => { state.toastMessage = ''; render(); }, 3000);
        }

        function startListening(continuous = false) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                showToast('⚠️ Speech not supported. Use Chrome/Edge.');
                return;
            }
            continuousDesired = continuous;
            if (recognition) { try { recognition.stop(); } catch(e) {} }
            recognition = new SpeechRecognition();
            recognition.continuous = continuous;
            recognition.interimResults = true;
            recognition.lang = 'en-US';
            let finalTranscript = state.inputText || '';

            recognition.onstart = () => {
                state.isListening = true;
                state.isContinuousListening = continuous;
                render();
                showToast(continuous ? '🎙️ Meeting mode active' : '🎤 Listening...');
            };

            recognition.onresult = (event) => {
                let interimTranscript = '';
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript;
                    if (event.results[i].isFinal) {
                        finalTranscript = (finalTranscript + ' ' + transcript).trim();
                        state.inputText = finalTranscript;
                    } else {
                        interimTranscript += transcript;
                    }
                }
                if (interimTranscript) {
                    state.inputText = (finalTranscript + ' ' + interimTranscript).trim();
                }
                render();
            };

            recognition.onerror = (event) => {
                if (event.error === 'not-allowed') {
                    showToast('🚫 Microphone denied.');
                } else if (event.error !== 'no-speech') {
                    showToast('⚠️ Error: ' + event.error);
                }
                if (event.error !== 'no-speech') {
                    continuousDesired = false;
                    state.isListening = false;
                    state.isContinuousListening = false;
                    render();
                }
            };

            recognition.onend = () => {
                if (continuousDesired) {
                    setTimeout(() => {
                        if (continuousDesired) {
                            try { recognition.start(); } catch(e) {}
                        }
                    }, 150);
                } else {
                    state.isListening = false;
                    render();
                }
            };
            try { recognition.start(); } catch(e) { showToast('❌ Could not start voice.'); }
        }

        function stopListening() {
            continuousDesired = false;
            if (recognition) { try { recognition.stop(); } catch(e) {} }
            state.isListening = false;
            state.isContinuousListening = false;
            render();
            showToast('⏹️ Stopped');
        }

        function improveText(text, feature) {
            const improvements = {
                email: (t) => {
                    let improved = t.replace(/\bhi\b/gi, 'Dear').replace(/\bhello\b/gi, 'Dear')
                        .replace(/\bthanks\b/gi, 'Thank you for your consideration')
                        .replace(/\bplease\b/gi, 'I would appreciate if you could kindly')
                        .replace(/\bcan you\b/gi, 'Would you be able to')
                        .replace(/\basap\b/gi, 'at your earliest convenience')
                        .replace(/\bi need\b/gi, 'I would require');
                    improved = improved.charAt(0).toUpperCase() + improved.slice(1);
                    if (!improved.match(/best regards|sincerely/i)) {
                        improved += '\n\nBest regards,';
                    }
                    return improved;
                },
                social: (t) => {
                    let improved = t.replace(/\bgood\b/gi, 'amazing').replace(/\bnice\b/gi, 'fantastic')
                        .replace(/\bcool\b/gi, 'incredible').replace(/\bgreat\b/gi, 'awesome');
                    improved = '✨ ' + improved;
                    const hashtags = [];
                    const lower = improved.toLowerCase();
                    if (lower.includes('travel') || lower.includes('beach')) hashtags.push('#TravelGoals', '#Wanderlust');
                    if (lower.includes('food')) hashtags.push('#Foodie', '#Delicious');
                    if (lower.includes('work')) hashtags.push('#Motivation', '#Success');
                    if (hashtags.length === 0) hashtags.push('#LifeUpdate', '#DailyVibes');
                    improved += ' 💫\n\n' + hashtags.slice(0, 3).join(' ');
                    return improved;
                },
                tone: (t) => {
                    let improved = t.charAt(0).toUpperCase() + t.slice(1);
                    const lower = t.toLowerCase();
                    if (lower.includes('urgent') || lower.includes('asap')) {
                        improved = improved.replace(/!/g, '.').replace(/\basap\b/gi, 'soon');
                        improved = 'I wanted to bring to your attention that ' + improved;
                    } else if (lower.length < 20) {
                        improved = 'I hope this message finds you well. ' + improved + ' Thank you.';
                    }
                    return improved;
                },
                grammar: (t) => {
                    let improved = t.replace(/\bi\b/g, 'I')
                        .replace(/\byour\s+welcome\b/gi, "you're welcome")
                        .replace(/\btheir\s+going\b/gi, "they're going")
                        .replace(/\bits\s+a\b/gi, "it's a")
                        .replace(/\bshould\s+of\b/gi, 'should have')
                        .replace(/\bcould\s+of\b/gi, 'could have')
                        .replace(/\balot\b/gi, 'a lot')
                        .replace(/\bwanna\b/gi, 'want to')
                        .replace(/\bgonna\b/gi, 'going to')
                        .replace(/\bu\b/g, 'you')
                        .replace(/\bur\b/g, 'your')
                        .replace(/\s+([.,!?])/g, '$1')
                        .replace(/\s+/g, ' ').trim();
                    improved = improved.replace(/(^|[.!?]\s+)([a-z])/g, (m, p1, p2) => p1 + p2.toUpperCase());
                    return improved;
                },
                style: (t) => {
                    let improved = t.replace(/\bvery good\b/gi, 'exceptional')
                        .replace(/\bgood\b/gi, 'excellent').replace(/\bbad\b/gi, 'unfavorable')
                        .replace(/\bbig\b/gi, 'substantial').replace(/\bsmall\b/gi, 'modest')
                        .replace(/\bget\b/gi, 'acquire').replace(/\bmake\b/gi, 'create')
                        .replace(/\bshow\b/gi, 'demonstrate').replace(/\buse\b/gi, 'utilize')
                        .replace(/\bthink\b/gi, 'believe').replace(/\bso\b/gi, 'therefore');
                    improved = improved.charAt(0).toUpperCase() + improved.slice(1);
                    return improved;
                },
                business: (t) => {
                    let improved = t.replace(/\bhi\b/gi, 'Dear Esteemed Colleague')
                        .replace(/\bthanks\b/gi, 'We appreciate your prompt attention')
                        .replace(/\bi think\b/gi, 'In my professional assessment')
                        .replace(/\bwe need\b/gi, 'We require')
                        .replace(/\basap\b/gi, 'at your earliest convenience')
                        .replace(/\bproject\b/gi, 'strategic initiative')
                        .replace(/\bproblem\b/gi, 'challenge');
                    improved = improved.charAt(0).toUpperCase() + improved.slice(1);
                    if (!improved.match(/regards|sincerely/i)) {
                        improved += '\n\nRespectfully,\n[Your Name]\n[Your Title]';
                    }
                    return improved;
                }
            };
            const improver = improvements[feature] || improvements.grammar;
            return improver(text);
        }

        function detectTone(text) {
            const lower = text.toLowerCase();
            if (lower.includes('urgent') || lower.includes('asap')) {
                return { emoji: '⚡', tone: 'Urgent', explanation: 'Contains urgent language.' };
            }
            if (lower.includes('dear') || lower.includes('sincerely')) {
                return { emoji: '🎩', tone: 'Formal', explanation: 'Uses formal language.' };
            }
            if (lower.includes('thanks') || lower.includes('happy')) {
                return { emoji: '😊', tone: 'Friendly', explanation: 'Conveys warmth.' };
            }
            if (lower.includes('meeting') || lower.includes('project')) {
                return { emoji: '💼', tone: 'Professional', explanation: 'Business focused.' };
            }
            if (lower.includes('excited') || lower.includes('amazing')) {
                return { emoji: '🎉', tone: 'Enthusiastic', explanation: 'High energy.' };
            }
            if (lower.includes('hey') || lower.includes('cool')) {
                return { emoji: '😎', tone: 'Casual', explanation: 'Informal language.' };
            }
            return { emoji: '💬', tone: 'Neutral', explanation: 'Balanced tone.' };
        }

        function handleImprove() {
            if (!state.inputText.trim()) {
                showToast('⚠️ Please enter text!');
                return;
            }
            state.isProcessing = true;
            state.outputText = '';
            state.detectedEmotion = null;
            render();
            setTimeout(() => {
                const feature = state.currentPage || 'grammar';
                const improved = improveText(state.inputText, feature);
                const tone = detectTone(state.inputText);
                state.outputText = improved;
                state.detectedEmotion = { emoji: tone.emoji, tone: tone.tone };
                state.emotionExplanation = tone.explanation;
                state.isProcessing = false;
                render();
                showToast('✅ Improved!');
            }, 1500);
        }

        function handleCopy() {
            navigator.clipboard.writeText(state.outputText).then(() => {
                state.copied = true;
                render();
                showToast('📋 Copied!');
                setTimeout(() => { state.copied = false; render(); }, 2000);
            }).catch(() => { showToast('❌ Failed'); });
        }

        const features = {
            email: { title: 'Email & Message', desc: 'Professional communication', gradient: 'from-blue-500 to-indigo-600' },
            social: { title: 'Social Media', desc: 'Engaging posts', gradient: 'from-pink-500 to-rose-600' },
            tone: { title: 'Tone Analysis', desc: 'Adjust tone', gradient: 'from-purple-500 to-violet-600' },
            grammar: { title: 'Grammar Check', desc: 'Fix errors', gradient: 'from-green-500 to-emerald-600' },
            style: { title: 'Style Enhancement', desc: 'Sophisticated vocabulary', gradient: 'from-amber-500 to-orange-600' },
            business: { title: 'Business Writing', desc: 'Professional documents', gradient: 'from-slate-600 to-gray-700' }
        };function render() {
            const app = document.getElementById('app');
            const toast = state.toastMessage ? `
                <div class="fixed top-4 right-4 z-50 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-4 rounded-xl shadow-2xl animate-slide-in flex items-center gap-3 max-w-sm">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                    </svg>
                    <span class="text-sm">${state.toastMessage}</span>
                </div>
            ` : '';

            if (state.currentPage) {
                const feature = features[state.currentPage];
                app.innerHTML = toast + `
                    <div class="container mx-auto px-4 py-6 max-w-7xl">
                        <button onclick="state.currentPage = null; state.inputText=''; state.outputText=''; render();" 
                            class="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6 font-semibold">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
                            </svg>
                            Back to Dashboard
                        </button>
                        <div class="text-center mb-8">
                            <div class="inline-block bg-gradient-to-r ${feature.gradient} text-white px-5 py-2 rounded-full text-xs font-bold mb-3 uppercase">
                                ${state.currentPage} MODE
                            </div>
                            <h1 class="text-4xl md:text-5xl font-black bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-3">
                                ${feature.title}
                            </h1>
                            <p class="text-gray-600 text-lg">${feature.desc}</p>
                        </div>
                        <div class="bg-white rounded-3xl shadow-2xl p-4 md:p-8">
                            <div class="flex items-center justify-between mb-6 pb-6 border-b">
                                <div>
                                    <h2 class="text-2xl font-bold text-gray-800">Transform Your Text</h2>
                                    <p class="text-sm text-gray-500">Speak or type below</p>
                                </div>
                                <div class="flex gap-2">
                                    <button onclick="startListening(false)" ${state.isListening || state.isProcessing ? 'disabled' : ''}
                                        class="p-3 rounded-xl ${state.isListening ? 'bg-red-500 text-white animate-pulse' : 'bg-gradient-to-br from-blue-500 to-purple-600 text-white hover:shadow-lg'} disabled:opacity-50">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/>
                                        </svg>
                                    </button>
                                    <button onclick="startListening(true)" ${state.isContinuousListening || state.isProcessing ? 'disabled' : ''}
                                        class="p-3 rounded-xl ${state.isContinuousListening ? 'bg-red-500 text-white animate-pulse' : 'bg-gradient-to-br from-purple-500 to-pink-600 text-white hover:shadow-lg'} disabled:opacity-50">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                                        </svg>
                                    </button>
                                    ${state.isListening || state.isContinuousListening ? `
                                        <button onclick="stopListening()" class="p-3 rounded-xl bg-gray-600 text-white hover:bg-gray-700">
                                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 10h6v4H9z"/>
                                            </svg>
                                        </button>
                                    ` : ''}
                                </div>
                            </div>
                            <div class="grid md:grid-cols-2 gap-6">
                                <div>
                                    <label class="block text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                                        <span class="w-2 h-2 bg-blue-500 rounded-full"></span>
                                        Your Text
                                    </label>
                                    <textarea oninput="state.inputText = this.value; render();" 
                                        placeholder="Type or speak your message..." 
                                        class="w-full h-64 p-5 border-2 border-gray-200 rounded-2xl focus:ring-2 focus:ring-purple-500 resize-none"
                                    >${state.inputText}</textarea>
                                    ${state.isListening ? `
                                        <div class="mt-3 text-sm text-blue-600 font-medium flex items-center gap-2">
                                            <span class="relative flex h-3 w-3">
                                                <span class="animate-ping absolute h-full w-full rounded-full bg-red-400 opacity-75"></span>
                                                <span class="relative rounded-full h-3 w-3 bg-red-500"></span>
                                            </span>
                                            ${state.isContinuousListening ? 'Meeting mode...' : 'Listening...'}
                                        </div>
                                    ` : ''}
                                </div>
                                <div>
                                    <label class="block text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                                        <span class="w-2 h-2 bg-green-500 rounded-full"></span>
                                        Improved Text
                                    </label>
                                    <div class="relative">
                                        <textarea readonly placeholder="Your improved text appears here..." 
                                            class="w-full h-64 p-5 border-2 rounded-2xl bg-gradient-to-br from-gray-50 to-blue-50 resize-none"
                                        >${state.outputText}</textarea>
                                        ${state.outputText ? `
                                            <button onclick="handleCopy()" class="absolute top-3 right-3 p-3 bg-white rounded-xl shadow-lg hover:shadow-xl">
                                                ${state.copied ? `
                                                    <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                                                    </svg>
                                                ` : `
                                                    <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                                                    </svg>
                                                `}
                                            </button>
                                        ` : ''}
                                    </div>
                                </div>
                            </div>
                            <div class="mt-8 flex justify-center">
                                <button onclick="handleImprove()" ${!state.inputText.trim() || state.isProcessing ? 'disabled' : ''}
                                    class="px-10 py-4 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white rounded-2xl font-bold text-lg hover:shadow-2xl transform hover:-translate-y-1 transition-all disabled:opacity-50 disabled:transform-none flex items-center gap-3">
                                    ${state.isProcessing ? `
                                        <svg class="animate-spin h-6 w-6" fill="none" viewBox="0 0 24 24">
                                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                        </svg>
                                        Processing...
                                    ` : `
                                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"/>
                                        </svg>
                                        Improve My Text
                                    `}
                                </button>
                            </div>
                            ${state.detectedEmotion ? `
                                <div class="mt-8 p-6 bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 rounded-2xl border-2 border-purple-200">
                                    <div class="flex items-start gap-4">
                                        <div class="text-5xl">${state.detectedEmotion.emoji}</div>
                                        <div>
                                            <h3 class="text-xl font-bold text-gray-800 mb-2">
                                                Detected Tone: <span class="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">${state.detectedEmotion.tone}</span>
                                            </h3>
                                            <p class="text-gray-700">${state.emotionExplanation}</p>
                                        </div>
                                    </div>
                                </div>
                            ` : ''}
                        </div>
                    </div>
                `;
            } else {
                app.innerHTML = toast + `
                    <div class="container mx-auto px-4 py-12 max-w-7xl">
                        <div class="text-center mb-12">
                            <div class="inline-block bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-full text-sm font-bold mb-6 shadow-lg">
                                ✨ BHASHA AI
                            </div>
                            <h1 class="text-5xl md:text-6xl font-black bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-4 leading-tight">
                                Advanced English<br>Improvement Dashboard
                            </h1>
                            <p class="text-gray-600 text-xl max-w-2xl mx-auto">
                                Transform your communication with AI-powered language enhancement 🚀
                            </p>
                        </div>
                        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
                            ${Object.entries(features).map(([key, f]) => `
                                <div onclick="state.currentPage = '${key}'; render();" 
                                    class="bg-white rounded-xl p-6 shadow-lg hover:shadow-2xl transition-all transform hover:-translate-y-1 cursor-pointer border-2 border-transparent hover:border-purple-200">
                                    <div class="w-14 h-14 bg-gradient-to-br ${f.gradient} rounded-xl flex items-center justify-center mb-4 shadow-md">
                                        <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                                        </svg>
                                    </div>
                                    <h3 class="text-xl font-bold text-gray-800 mb-2">${f.title}</h3>
                                    <p class="text-gray-600 text-sm">${f.desc}</p>
                                </div>
                            `).join('')}
                        </div>
                        <footer class="mt-12 text-center text-gray-500 text-sm">
                            <p>© 2024 Bhasha AI - Advanced English Improvement Tool</p>
                            <p class="mt-2">💡 Use Chrome or Edge for voice input</p>
                        </footer>
                    </div>
