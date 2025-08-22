// Crear partículas de energía
function createEnergyParticles() {
    const header = document.getElementById('dynamicHeader');
    const particleCount = 50;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.classList.add('energy-particle');

        // Tamaño y posición aleatorios
        const size = Math.random() * 5 + 2;
        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        const delay = Math.random() * 5;

        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${posX}%`;
        particle.style.top = `${posY}%`;
        particle.style.animation = `pulse ${3 + Math.random() * 4}s infinite ${delay}s`;

        header.appendChild(particle);
    }
}

// Crear líneas de energía
function createEnergyLines() {
    const header = document.getElementById('dynamicHeader');
    const lineCount = 20;

    for (let i = 0; i < lineCount; i++) {
        const line = document.createElement('div');
        line.classList.add('energy-line');

        const width = Math.random() * 200 + 50;
        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        const rotation = Math.random() * 360;
        const delay = Math.random() * 5;
        const duration = 2 + Math.random() * 3;

        line.style.width = `${width}px`;
        line.style.left = `${posX}%`;
        line.style.top = `${posY}%`;
        line.style.transform = `rotate(${rotation}deg)`;
        line.style.animation = `flow ${duration}s infinite ${delay}s`;

        header.appendChild(line);
    }
}

// Crear nodos de circuito
function createCircuitNodes() {
    const header = document.getElementById('dynamicHeader');
    const nodeCount = 15;

    for (let i = 0; i < nodeCount; i++) {
        const node = document.createElement('div');
        node.classList.add('circuit-node');

        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        const delay = Math.random() * 2;

        node.style.left = `${posX}%`;
        node.style.top = `${posY}%`;
        node.style.animation = `pulse ${2 + Math.random() * 2}s infinite ${delay}s`;

        header.appendChild(node);
    }
}

function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = Math.floor(progress * (end - start) + start);
        element.innerHTML = end === 100 ? `${value}%` : value.toLocaleString();
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Inicializar todas las animaciones
document.addEventListener('DOMContentLoaded', function () {
    createEnergyParticles();
    createEnergyLines();
    createCircuitNodes();
});