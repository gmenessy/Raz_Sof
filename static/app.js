document.addEventListener('DOMContentLoaded', () => {
    const uploadBtn = document.getElementById('upload-btn');
    const fileInput = document.getElementById('file-upload');
    const nodesContainer = document.getElementById('nodes-container');
    const consoleLogs = document.getElementById('console-logs');

    // Chat Modal Elements
    const chatModal = document.getElementById('chat-modal');
    const closeBtn = document.querySelector('.close-btn');
    const chatInput = document.getElementById('chat-input');
    const chatSendBtn = document.getElementById('chat-send');
    const chatHistory = document.getElementById('chat-history');
    const chatTitle = document.getElementById('chat-title');

    let currentChatDocId = null;
    let pollInterval = null;

    function log(message) {
        const div = document.createElement('div');
        div.textContent = `[SYSTEM] ${message}`;
        consoleLogs.appendChild(div);
        consoleLogs.scrollTop = consoleLogs.scrollHeight;
    }

    async function loadAkten() {
        try {
            const res = await fetch('/api/akten');
            const data = await res.json();
            renderNodes(data);
            checkPendingAnalysis(data);
        } catch (e) {
            log('Error loading Akten: ' + e.message);
        }
    }

    function checkPendingAnalysis(akten) {
        let isPending = false;
        akten.forEach(akte => {
            akte.dokumente.forEach(doc => {
                if (!doc.essenz || !doc.index_data) {
                    isPending = true;
                }
            });
        });

        if (isPending) {
            if (!pollInterval) {
                log('Knoten in Analyse... überwache Status.');
                pollInterval = setInterval(loadAkten, 3000);
            }
        } else {
            if (pollInterval) {
                clearInterval(pollInterval);
                pollInterval = null;
                log('Alle Analysen abgeschlossen.');
            }
        }
    }

    function renderNodes(akten) {
        nodesContainer.innerHTML = '';

        // In this MVP we just use the default "Allgemeine Akte" (ID: 1)
        akten.forEach(akte => {
            akte.dokumente.forEach(doc => {
                const card = document.createElement('div');
                card.className = 'raz-card';

                const isAnalyzing = (!doc.essenz || !doc.index_data);

                let indexSnippet = doc.index_data ? doc.index_data.substring(0, 100) + '...' : '<span class="blink" style="color: var(--inf-cyan);">Wird analysiert...</span>';
                let essenzSnippet = doc.essenz ? doc.essenz : '<span class="blink" style="color: var(--inf-cyan);">Wird analysiert...</span>';

                const buttonHtml = isAnalyzing ?
                    `<button class="raz-action-btn" disabled style="opacity: 0.5;">Analysiere Knoten...</button>` :
                    `<button class="raz-action-btn chat-trigger" data-id="${doc.id}" data-name="${doc.dateiname}">Enthüllen (Chat)</button>`;

                card.innerHTML = `
                    <div class="raz-glow"></div>
                    <span class="raz-tag">Knoten_${doc.id.toString().padStart(3, '0')}</span>
                    <h3 class="raz-title">${doc.dateiname}</h3>
                    <div class="raz-excerpt"><strong>Essenz:</strong><br>${essenzSnippet}</div>
                    <div class="raz-excerpt" style="border-left-color: var(--inf-cyan);"><strong>Index:</strong><br>${indexSnippet}</div>
                    <div style="margin-top: 15px;">
                        ${buttonHtml}
                    </div>
                `;

                if(isAnalyzing) {
                    card.style.borderColor = 'var(--inf-cyan)';
                    card.style.boxShadow = '0 0 10px rgba(0, 245, 255, 0.2)';
                }

                nodesContainer.appendChild(card);
            });
        });

        document.querySelectorAll('.chat-trigger').forEach(btn => {
            btn.addEventListener('click', (e) => {
                openChat(e.target.dataset.id, e.target.dataset.name);
            });
        });
    }

    uploadBtn.addEventListener('click', async () => {
        if (!fileInput.files.length) {
            log('Kein Dokument ausgewählt.');
            return;
        }

        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);
        formData.append('akte_id', 1);

        log(`Initiiere Ingest für: ${file.name}...`);
        uploadBtn.textContent = 'Upload läuft...';
        uploadBtn.disabled = true;

        try {
            const res = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            if (res.ok) {
                log(`Dokument hochgeladen. Analyse startet im Hintergrund.`);
                loadAkten();
            } else {
                log(`Fehler beim Upload: ${res.statusText}`);
            }
        } catch (e) {
            log(`Netzwerkfehler: ${e.message}`);
        } finally {
            uploadBtn.textContent = 'Analysieren';
            uploadBtn.disabled = false;
            fileInput.value = '';
        }
    });

    function openChat(docId, docName) {
        currentChatDocId = docId;
        chatTitle.textContent = `Raz_Sof Link > ${docName}`;
        chatHistory.innerHTML = '<div class="chat-msg agent">RAZ_SOF: Verbindung hergestellt. Das Wissen liegt offen. Was suchst du?</div>';
        chatModal.classList.remove('hidden');
    }

    closeBtn.addEventListener('click', () => {
        chatModal.classList.add('hidden');
        currentChatDocId = null;
    });

    async function sendChatMessage() {
        const msg = chatInput.value.trim();
        if (!msg || !currentChatDocId) return;

        chatHistory.innerHTML += `<div class="chat-msg user">${msg}</div>`;
        chatInput.value = '';
        chatHistory.scrollTop = chatHistory.scrollHeight;

        const responseId = 'resp-' + Date.now();
        chatHistory.innerHTML += `<div id="${responseId}" class="chat-msg agent"><span class="blink">RAZ_SOF extrahiert Pfade...</span></div>`;
        chatHistory.scrollTop = chatHistory.scrollHeight;

        log(`Sende Query an Knoten_${currentChatDocId.toString().padStart(3, '0')}`);

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    dokument_id: parseInt(currentChatDocId),
                    message: msg
                })
            });

            const responseContainer = document.getElementById(responseId);
            responseContainer.innerHTML = 'RAZ_SOF: ';

            if (res.ok) {
                const reader = res.body.getReader();
                const decoder = new TextDecoder("utf-8");
                let done = false;

                while (!done) {
                    const { value, done: readerDone } = await reader.read();
                    done = readerDone;
                    if (value) {
                        const chunk = decoder.decode(value, { stream: true });
                        // Render line breaks correctly for HTML
                        responseContainer.innerHTML += chunk.replace(/\n/g, '<br>');
                        chatHistory.scrollTop = chatHistory.scrollHeight;
                    }
                }
                log(`Antwortstrom beendet.`);
            } else {
                responseContainer.innerHTML = `<span style="color: red;">RAZ_SOF ERROR: ${res.statusText}</span>`;
            }
        } catch (e) {
            const responseContainer = document.getElementById(responseId);
            if(responseContainer) {
                responseContainer.innerHTML = `<span style="color: red;">RAZ_SOF OFFLINE: ${e.message}</span>`;
            }
        }

        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    chatSendBtn.addEventListener('click', sendChatMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendChatMessage();
    });

    loadAkten();
});
