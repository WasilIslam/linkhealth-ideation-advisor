console.log(typeof marked); // Should log 'function'

const form = document.getElementById('agent-form');
const conversationDiv = document.getElementById('conversation');
const controlsDiv = document.getElementById('controls');
const quitButton = document.getElementById('quit');
const statusDiv = document.getElementById('status-message');

let pollingInterval;

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const iterations = parseInt(document.getElementById('iterations').value);
    const prompt1 = document.getElementById('prompt1');
    const prompt2 = document.getElementById('prompt2');

    // Start agents
    await fetch('/start', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt1: prompt1.value, prompt2: prompt2.value, maxIterations: iterations })
    });

    // Resize textareas and make them readonly
    prompt1.style.height = '50px';
    prompt2.style.height = '50px';
    prompt1.readOnly = true;
    prompt2.readOnly = true;

    // Increase conversation div height
    conversationDiv.style.height = '300px';

    conversationDiv.scrollTop = conversationDiv.scrollHeight;

    controlsDiv.style.display = 'flex';
    startPolling();
    setInterval(fetchLatestUpdates, 3000);
});

async function pollConversation() {
    const response = await fetch('/get_conversation');
    const data = await response.json();
    console.log(data);

    // Clear conversation div
    conversationDiv.innerHTML = '';

    data.history.forEach((msg) => {
        const div = document.createElement('div');
        div.classList.add('message', msg.agent);
        div.innerHTML = `<strong>${msg.agent === 'agent1' ? 'Agent 1' : 'Agent 2'}:</strong> ${marked.parse(msg.content)}`;
        conversationDiv.appendChild(div);
    });

    conversationDiv.scrollTop = conversationDiv.scrollHeight;

    statusDiv.textContent = data.status

    if (data.status === "The agents have concluded their work.") {
        clearInterval(pollingInterval);
        document.getElementById('download-transcript').style.display = "block"; // Show the button
    }
}

function startPolling() {
    pollingInterval = setInterval(async () => {
        await pollConversation();
    }, 3000);
}

quitButton.addEventListener('click', async () => {
    await fetch('/stop', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'}
    });

    clearInterval(pollingInterval);
    alert('Conversation ended.');
    controlsDiv.style.display = 'none';
});

document.getElementById('download-transcript').addEventListener('click', function() {
    window.location.href = '/download_transcript'; // Triggers the Flask download endpoint
});

function stopConversation() {
    document.getElementById('status-message').innerText = "The agents have concluded their work.";
}

function updateIdeaAndScore(latestIdea, latestScore) {
    document.getElementById("final-idea-text").value = latestIdea;
    document.getElementById("final-idea-text").style.height = '400px';
    document.getElementById("final-score").innerText = `Overall Score: ${latestScore}`;
}

function fetchLatestUpdates() {
    fetch('/status').then(response => response.json()).then(data => {
        updateIdeaAndScore(data.latest_idea, data.latest_score);
    });
}
