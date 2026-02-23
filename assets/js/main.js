(function () {
    const canvas = document.getElementById('matrix-bg');
    const ctx = canvas.getContext('2d');

    // Optimization: Render at lower resolution for "retro" feel and performance
    const scaleFactor = 2; // 1 = full res, 2 = half res, etc. 

    function resizeCanvas() {
        canvas.width = window.innerWidth / scaleFactor;
        canvas.height = window.innerHeight / scaleFactor;
        // CSS handles the display size stretch
    }

    resizeCanvas();

    // Classic Matrix Look
    const katakana = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン';
    const latin = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const nums = '0123456789';

    const alphabet = katakana + latin + nums;

    const fontSize = 16; // Larger font size = fewer columns to calculate
    let columns = canvas.width / fontSize; // Make it mutable for resize

    const rainDrops = [];

    for (let x = 0; x < columns; x++) {
        rainDrops[x] = 1;
    }

    // Performance: Frame Throttling
    let lastTime = 0;
    const fps = 20; // Lower FPS for cinematic feel and lower CPU usage
    const interval = 1000 / fps;

    const draw = (currentTime) => {
        requestAnimationFrame(draw);

        const deltaTime = currentTime - lastTime;

        if (deltaTime > interval) {
            lastTime = currentTime - (deltaTime % interval);

            // Fade effect
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = '#0F0';
            ctx.font = fontSize + 'px monospace';

            for (let i = 0; i < rainDrops.length; i++) {
                const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
                ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);

                if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    rainDrops[i] = 0;
                }
                rainDrops[i]++;
            }
        }
    };

    // Start Animation Loop
    requestAnimationFrame(draw);

    // Handle Resize efficiently
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            const oldColumns = Math.floor(canvas.width / fontSize);
            const oldRainDrops = [...rainDrops]; // Copy existing state

            resizeCanvas();

            const newColumns = Math.floor(canvas.width / fontSize);
            columns = newColumns; // Update global columns variable

            // Resize rainDrops array
            rainDrops.length = newColumns;

            for (let x = 0; x < newColumns; x++) {
                // If column existed before, keep its Y position
                if (x < oldColumns && x < oldRainDrops.length) {
                    rainDrops[x] = oldRainDrops[x];
                } else {
                    // New column? Randomize start so it doesn't look like a solid wall
                    rainDrops[x] = Math.floor(Math.random() * -100);
                }
            }
        }, 200); // 200ms debounce
    });
})();
