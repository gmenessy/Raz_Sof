document.addEventListener('DOMContentLoaded', () => {
    const uploadBtn = document.getElementById('upload-btn');
    const fileInput = document.getElementById('file-upload');
    const nodesContainer = document.getElementById('nodes-container');
    const consoleLogs = document.getElementById('console-logs');

    // Chat Modal Elements
    const chatModal = document.getElementById('chat-modal');
    const closeBtn = document.getElementById('close-modal-btn');
    const chatInput = document.getElementById('chat-input');
    const chatSendBtn = document.getElementById('chat-send');
    const chatHistory = document.getElementById('chat-history');
    const chatTitle = document.getElementById('chat-title');

    let currentChatDocId = null;
    let pollInterval = null;

    function log(message) {
        const div = document.createElement('div');
        div.textContent = `> ${message}`;
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
            log('Error loading: ' + e.message);
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
                log('Analyse läuft im Hintergrund...');
                pollInterval = setInterval(loadAkten, 3000);
            }
        } else {
            if (pollInterval) {
                clearInterval(pollInterval);
                pollInterval = null;
                log('Alle Dokumente bereit.');
            }
        }
    }

    function renderNodes(akten) {
        nodesContainer.innerHTML = '';

        akten.forEach(akte => {
            akte.dokumente.forEach(doc => {
                const card = document.createElement('div');
                card.className = 'document-card liquid-glass';

                const isAnalyzing = (!doc.essenz || !doc.index_data);

                let indexSnippet = doc.index_data ? doc.index_data.substring(0, 100) + '...' : '<span class="blink" style="color: var(--highlight);">Analysiere...</span>';
                let essenzSnippet = doc.essenz ? doc.essenz : '<span class="blink" style="color: var(--highlight);">Analysiere...</span>';

                const buttonHtml = isAnalyzing ?
                    `<button class="liquid-btn" disabled>Verarbeite...</button>` :
                    `<button class="liquid-btn chat-trigger" data-id="${doc.id}" data-name="${doc.dateiname}">Wissen abrufen</button>`;

                card.innerHTML = `
                    <div class="liquid-content">
                        <div style="font-size: 0.7rem; color: var(--glow); margin-bottom: 5px; font-weight: 600; text-transform: uppercase;">ID_${doc.id.toString().padStart(4, '0')}</div>
                        <h3 class="doc-title">${doc.dateiname}</h3>

                        <div class="doc-section">
                            <strong style="color: #fff;">Essenz:</strong><br>${essenzSnippet}
                        </div>

                        <div class="doc-section" style="border-left-color: var(--glow);">
                            <strong style="color: #fff;">Index:</strong><br>${indexSnippet}
                        </div>

                        <div style="margin-top: 20px;">
                            ${buttonHtml}
                        </div>
                    </div>
                `;

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
            log('Bitte Datei wählen.');
            return;
        }

        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);
        formData.append('akte_id', 1);

        log(`Upload gestartet: ${file.name}`);
        uploadBtn.textContent = 'Lädt...';
        uploadBtn.disabled = true;

        try {
            const res = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            if (res.ok) {
                log(`Ingest erfolgreich. KI analysiert.`);
                loadAkten();
            } else {
                log(`Fehler: ${res.statusText}`);
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
        chatTitle.innerHTML = `Raz_Sof <span style="color: var(--highlight); font-weight: 300;">// ${docName}</span>`;
        chatHistory.innerHTML = '<div class="chat-msg agent">System: Agentischer Kanal geöffnet. Was möchten Sie wissen?</div>';
        chatModal.classList.add('active');
    }

    closeBtn.addEventListener('click', () => {
        chatModal.classList.remove('active');
        currentChatDocId = null;
    });

    async function sendChatMessage() {
        const msg = chatInput.value.trim();
        if (!msg || !currentChatDocId) return;

        chatHistory.innerHTML += `<div class="chat-msg user">${msg}</div>`;
        chatInput.value = '';
        chatHistory.scrollTop = chatHistory.scrollHeight;

        const responseId = 'resp-' + Date.now();
        chatHistory.innerHTML += `<div id="${responseId}" class="chat-msg agent"><span class="blink">Verarbeite (RAG)...</span></div>`;
        chatHistory.scrollTop = chatHistory.scrollHeight;

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
            responseContainer.innerHTML = '';

            if (res.ok) {
                const reader = res.body.getReader();
                const decoder = new TextDecoder("utf-8");
                let done = false;

                while (!done) {
                    const { value, done: readerDone } = await reader.read();
                    done = readerDone;
                    if (value) {
                        const chunk = decoder.decode(value, { stream: true });
                        responseContainer.innerHTML += chunk.replace(/\n/g, '<br>');
                        chatHistory.scrollTop = chatHistory.scrollHeight;
                    }
                }
            } else {
                responseContainer.innerHTML = `<span style="color: #ef4444;">API Fehler: ${res.statusText}</span>`;
            }
        } catch (e) {
            const responseContainer = document.getElementById(responseId);
            if(responseContainer) {
                responseContainer.innerHTML = `<span style="color: #ef4444;">Netzwerkfehler: ${e.message}</span>`;
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
