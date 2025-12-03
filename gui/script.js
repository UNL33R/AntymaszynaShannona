// Game State
const gameState = {
    currentMode: 'shannon',
    shannon: {
        rounds: 0,
        wins: 0,
        losses: 0,
        humanChoices: [],
        machineChoices: [],
        patterns: {}
    },
    anti: {
        rounds: 0,
        wins: 0,
        losses: 0,
        humanChoices: [],
        machineChoices: [],
        lastHumanChoice: null,
        lastMachineChoice: null,
        patterns: {}
    },
    simulation: {
        running: false,
        totalRounds: 0,
        currentRound: 0,
        antiWins: 0,
        machineWins: 0
    }
};

const API_URL = 'http://localhost:8080';

// Mode Switching
document.querySelectorAll('.mode-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const mode = btn.dataset.mode;
        switchMode(mode);
    });
});

function switchMode(mode) {
    gameState.currentMode = mode;

    // Update buttons
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === mode);
    });

    // Update content
    document.querySelectorAll('.mode-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${mode}-mode`).classList.add('active');
}

// Shannon Mode
document.querySelectorAll('#shannon-mode .choice-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
        const choice = parseInt(btn.dataset.choice);
        await playShannonRound(choice);
    });
});

async function playShannonRound(humanChoice) {
    try {
        const response = await fetch(`${API_URL}/api/shannon/move`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ choice: humanChoice })
        });

        const data = await response.json();

        // Update state
        gameState.shannon.rounds++;
        gameState.shannon.humanChoices.push(humanChoice);
        gameState.shannon.machineChoices.push(data.machine_choice);

        if (data.result === 'win') {
            gameState.shannon.wins++;
        } else {
            gameState.shannon.losses++;
        }

        // Update UI
        updateShannonUI(data);
    } catch (error) {
        console.error('Error:', error);
        showShannonResult('❌ Błąd połączenia z serwerem', 'loss');
    }
}

function updateShannonUI(data) {
    document.getElementById('shannon-rounds').textContent = gameState.shannon.rounds;
    document.getElementById('shannon-wins').textContent = gameState.shannon.wins;
    document.getElementById('shannon-losses').textContent = gameState.shannon.losses;

    const resultMsg = data.result === 'win'
        ? `✅ WYGRAŁEŚ! Maszyna wybrała ${data.machine_choice}, ty wybrałeś ${data.human_choice}`
        : `❌ PRZEGRAŁEŚ! Maszyna zgadła - oba wybraliście ${data.machine_choice}`;

    showShannonResult(resultMsg, data.result);

    if (data.patterns) {
        updatePatternDisplay(data.patterns);
    }

    if (data.prediction !== undefined) {
        const predMsg = data.has_pattern
            ? `\n\n💡 Predykcja: Maszyna prawdopodobnie wybierze ${data.prediction} w następnej rundzie`
            : `\n\n🎲 Maszyna nie ma jeszcze potwierdzonego wzorca - będzie losować`;
        showShannonResult(resultMsg + predMsg, data.result);
    }
}

function showShannonResult(message, type) {
    const resultPanel = document.getElementById('shannon-result');
    const resultMessage = resultPanel.querySelector('.result-message');
    resultMessage.textContent = message;
    resultMessage.className = `result-message ${type}`;
}

function updatePatternDisplay(patterns) {
    const grid = document.querySelector('#shannon-patterns .patterns-grid');
    grid.innerHTML = '';

    for (const [pattern, data] of Object.entries(patterns)) {
        if (data[0] !== 'Nieznany' && data[1] > 0) {
            const item = document.createElement('div');
            item.className = 'pattern-item';
            item.textContent = `${pattern}: ${data[0]} (${data[1]}x)`;
            grid.appendChild(item);
        }
    }
}

document.getElementById('shannon-reset').addEventListener('click', async () => {
    try {
        await fetch(`${API_URL}/api/shannon/reset`, { method: 'POST' });
        gameState.shannon = {
            rounds: 0,
            wins: 0,
            losses: 0,
            humanChoices: [],
            machineChoices: [],
            patterns: {}
        };
        updateShannonUI({ result: 'neutral', machine_choice: 0, human_choice: 0 });
        showShannonResult('Nowa gra rozpoczęta! Wybierz 0 lub 1', 'neutral');
        document.querySelector('#shannon-patterns .patterns-grid').innerHTML = '';
    } catch (error) {
        console.error('Error:', error);
    }
});

// Anti-Shannon Mode
let antiHumanChoice = null;
let antiMachineChoice = null;

document.querySelectorAll('[data-anti-human]').forEach(btn => {
    btn.addEventListener('click', () => {
        antiHumanChoice = parseInt(btn.dataset.antiHuman);
        document.querySelectorAll('[data-anti-human]').forEach(b => b.style.opacity = '0.5');
        btn.style.opacity = '1';

        if (antiMachineChoice !== null) {
            submitAntiRound();
        }
    });
});

document.querySelectorAll('[data-anti-machine]').forEach(btn => {
    btn.addEventListener('click', () => {
        antiMachineChoice = parseInt(btn.dataset.antiMachine);
        document.querySelectorAll('[data-anti-machine]').forEach(b => b.style.opacity = '0.5');
        btn.style.opacity = '1';

        if (antiHumanChoice !== null) {
            submitAntiRound();
        }
    });
});

async function submitAntiRound() {
    try {
        const response = await fetch(`${API_URL}/api/anti/move`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                human_choice: antiHumanChoice,
                machine_choice: antiMachineChoice
            })
        });

        const data = await response.json();

        // Update state
        gameState.anti.rounds++;
        if (data.result === 'win') {
            gameState.anti.wins++;
        } else {
            gameState.anti.losses++;
        }

        // Update UI
        updateAntiUI(data);

        // Reset selections
        antiHumanChoice = null;
        antiMachineChoice = null;
        document.querySelectorAll('[data-anti-human], [data-anti-machine]').forEach(b => b.style.opacity = '1');
    } catch (error) {
        console.error('Error:', error);
    }
}

function updateAntiUI(data) {
    document.getElementById('anti-rounds').textContent = gameState.anti.rounds;
    document.getElementById('anti-wins').textContent = gameState.anti.wins;
    document.getElementById('anti-losses').textContent = gameState.anti.losses;

    const resultMsg = data.result === 'win'
        ? '✅ WYGRAŁEŚ (maszyna się pomyliła)'
        : '❌ PRZEGRAŁEŚ (maszyna zgadła twój wybór)';

    const resultPanel = document.getElementById('anti-result');
    const resultMessage = resultPanel.querySelector('.result-message');
    resultMessage.textContent = resultMsg;
    resultMessage.className = `result-message ${data.result}`;

    // Show recommendation
    const recPanel = document.getElementById('anti-recommendation');
    const recText = recPanel.querySelector('.recommendation-text');

    if (data.recommendation) {
        recText.textContent = data.recommendation;
    } else {
        recText.textContent = 'Kontynuuj grę, aby otrzymać rekomendacje';
    }
}

document.getElementById('anti-reset').addEventListener('click', async () => {
    try {
        await fetch(`${API_URL}/api/anti/reset`, { method: 'POST' });
        gameState.anti = {
            rounds: 0,
            wins: 0,
            losses: 0,
            humanChoices: [],
            machineChoices: [],
            lastHumanChoice: null,
            lastMachineChoice: null,
            patterns: {}
        };
        document.getElementById('anti-rounds').textContent = '0';
        document.getElementById('anti-wins').textContent = '0';
        document.getElementById('anti-losses').textContent = '0';
        document.getElementById('anti-result').querySelector('.result-message').textContent = 'Nowa gra rozpoczęta!';
        document.getElementById('anti-recommendation').querySelector('.recommendation-text').textContent = 'Brak rekomendacji';
        antiHumanChoice = null;
        antiMachineChoice = null;
        document.querySelectorAll('[data-anti-human], [data-anti-machine]').forEach(b => b.style.opacity = '1');
    } catch (error) {
        console.error('Error:', error);
    }
});

// Simulation Mode
document.getElementById('start-simulation').addEventListener('click', async () => {
    const rounds = parseInt(document.getElementById('rounds-input').value);

    if (rounds < 10 || rounds > 10000) {
        alert('Liczba rund musi być między 10 a 10000');
        return;
    }

    await runSimulation(rounds);
});

async function runSimulation(totalRounds) {
    try {
        const startBtn = document.getElementById('start-simulation');
        startBtn.disabled = true;
        startBtn.textContent = '⏳ Symulacja w toku...';

        gameState.simulation.running = true;
        gameState.simulation.totalRounds = totalRounds;
        gameState.simulation.currentRound = 0;
        gameState.simulation.antiWins = 0;
        gameState.simulation.machineWins = 0;

        const response = await fetch(`${API_URL}/api/simulation/run`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rounds: totalRounds })
        });

        const data = await response.json();

        // Animate progress
        animateSimulation(data);

        startBtn.disabled = false;
        startBtn.textContent = '▶️ Rozpocznij symulację';
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('start-simulation').disabled = false;
        document.getElementById('start-simulation').textContent = '▶️ Rozpocznij symulację';
    }
}

function animateSimulation(data) {
    const duration = 2000; // 2 seconds
    const steps = 50;
    const stepDuration = duration / steps;
    let currentStep = 0;

    const interval = setInterval(() => {
        currentStep++;
        const progress = currentStep / steps;

        // Update progress bar
        document.getElementById('sim-progress').style.width = `${progress * 100}%`;

        // Update stats
        const currentRound = Math.floor(data.total_rounds * progress);
        const currentAntiWins = Math.floor(data.anti_wins * progress);
        const currentMachineWins = Math.floor(data.machine_wins * progress);

        document.getElementById('sim-rounds').textContent = `${currentRound} / ${data.total_rounds}`;
        document.getElementById('sim-anti-wins').textContent = currentAntiWins;
        document.getElementById('sim-machine-wins').textContent = currentMachineWins;

        if (currentStep >= steps) {
            clearInterval(interval);
            showSimulationResults(data);
        }
    }, stepDuration);
}

function showSimulationResults(data) {
    const resultPanel = document.getElementById('sim-result');
    const resultMessage = resultPanel.querySelector('.result-message');

    const winner = data.anti_wins > data.machine_wins ? 'Anty-Maszyna' : 'Maszyna Shannona';
    const winClass = data.anti_wins > data.machine_wins ? 'win' : 'loss';

    resultMessage.innerHTML = `
        <strong>🏆 Zwycięzca: ${winner}</strong><br>
        Procent wygranych Anty-Maszyny: ${data.anti_percentage.toFixed(2)}%<br>
        Procent trafień Maszyny: ${data.machine_percentage.toFixed(2)}%
    `;
    resultMessage.className = `result-message ${winClass}`;
}

// Initialize
(async function init() {
    try {
        // Reset all games on load
        await fetch(`${API_URL}/api/shannon/reset`, { method: 'POST' });
        await fetch(`${API_URL}/api/anti/reset`, { method: 'POST' });
    } catch (error) {
        console.error('Server not available:', error);
        alert('Nie można połączyć się z serwerem. Upewnij się, że server.py jest uruchomiony.');
    }
})();
