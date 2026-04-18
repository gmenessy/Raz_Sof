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
        } catch (e) {
            log('Error loading Akten: ' + e.message);
        }
    }

    function renderNodes(akten) {
        nodesContainer.innerHTML = '';

        // In this MVP we just use the default "Allgemeine Akte" (ID: 1)
        akten.forEach(akte => {
            akte.dokumente.forEach(doc => {
                const card = document.createElement('div');
                card.className = 'raz-card';

                let indexSnippet = doc.index_data ? doc.index_data.substring(0, 100) + '...' : 'Warte auf Analyse...';
                let essenzSnippet = doc.essenz ? doc.essenz : 'Warte auf Analyse...';

                card.innerHTML = `
                    <div class="raz-glow"></div>
                    <span class="raz-tag">Knoten_${doc.id.toString().padStart(3, '0')}</span>
                    <h3 class="raz-title">${doc.dateiname}</h3>
                    <div class="raz-excerpt"><strong>Essenz:</strong><br>${essenzSnippet}</div>
                    <div class="raz-excerpt" style="border-left-color: var(--inf-cyan);"><strong>Index:</strong><br>${indexSnippet}</div>
                    <div style="margin-top: 15px;">
                        <button class="raz-action-btn chat-trigger" data-id="${doc.id}" data-name="${doc.dateiname}">Enthüllen (Chat)</button>
                    </div>
                `;
                nodesContainer.appendChild(card);
            });
        });

        // Attach chat listeners
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
        formData.append('akte_id', 1); // MVP: Default Akte

        log(`Initiiere Ingest für: ${file.name}...`);
        uploadBtn.textContent = 'Analysiere...';
        uploadBtn.disabled = true;

        try {
            const res = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            if (res.ok) {
                log(`Analyse abgeschlossen. Knoten integriert.`);
                loadAkten();
            } else {
                log(`Fehler bei der Analyse: ${res.statusText}`);
            }
        } catch (e) {
            log(`Netzwerkfehler: ${e.message}`);
        } finally {
            uploadBtn.textContent = 'Analysieren';
            uploadBtn.disabled = false;
            fileInput.value = '';
        }
    });

    // Chat Logic
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

        // Add user msg
        chatHistory.innerHTML += `<div class="chat-msg user">${msg}</div>`;
        chatInput.value = '';
        chatHistory.scrollTop = chatHistory.scrollHeight;

        // Add loading state
        const loadingId = 'loading-' + Date.now();
        chatHistory.innerHTML += `<div id="${loadingId}" class="chat-msg agent blink">RAZ_SOF extrahiert Pfade...</div>`;
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

            document.getElementById(loadingId).remove();

            if (res.ok) {
                const data = await res.json();
                chatHistory.innerHTML += `<div class="chat-msg agent">RAZ_SOF: ${data.response}</div>`;
                log(`Antwort empfangen.`);
            } else {
                chatHistory.innerHTML += `<div class="chat-msg agent" style="color: red;">RAZ_SOF ERROR: ${res.statusText}</div>`;
            }
        } catch (e) {
            document.getElementById(loadingId).remove();
            chatHistory.innerHTML += `<div class="chat-msg agent" style="color: red;">RAZ_SOF OFFLINE: ${e.message}</div>`;
        }

        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    chatSendBtn.addEventListener('click', sendChatMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendChatMessage();
    });

    // Initial Load
    loadAkten();
});
