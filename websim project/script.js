import confetti from 'canvas-confetti';
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const canvas = document.getElementById('vector-space');

const addWordBtn = document.getElementById('add-word-btn');
const wordInput = document.getElementById('word-input');
const analogyBtn = document.getElementById('analogy-btn');
const findSimilarBtn = document.getElementById('find-similar-btn');
const similarWordInput = document.getElementById('similar-word-input');
const recalculateLayoutBtn = document.getElementById('recalculate-layout-btn');
const loadingIndicator = document.getElementById('loading-indicator');

const analogyA = document.getElementById('analogy-a');
const analogyB = document.getElementById('analogy-b');
const analogyC = document.getElementById('analogy-c');
const analogyResultEl = document.getElementById('analogy-result');

const words = new Map();
const scale = { min: -100, max: 100 };
let analogyArrows = [];

// --- THREE.js setup ---
let scene, camera, renderer, controls;

function setupThreeJS() {
    const container = document.querySelector('.vector-space-container');
    const size = container.clientWidth;

    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf9f9f9);

    // Camera
    camera = new THREE.PerspectiveCamera(75, size / size, 0.1, 2000);
    camera.position.set(50, 50, 150);

    // Renderer
    renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
    renderer.setSize(size, size);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Controls
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.screenSpacePanning = false;
    controls.minDistance = 20;
    controls.maxDistance = 500;
    controls.maxPolarAngle = Math.PI / 2;

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.9);
    directionalLight.position.set(50, 50, 50);
    scene.add(directionalLight);

    // Grid
    const gridSize = scale.max - scale.min;
    const gridDivisions = 10;
    const gridHelper = new THREE.GridHelper(gridSize, gridDivisions, 0x95a5a6, 0xe0e0e0);
    scene.add(gridHelper);
}

function createTextSprite(text) {
    const fontface = "Roboto";
    const fontsize = 24;
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    context.font = `Bold ${fontsize}px ${fontface}`;
    
    const metrics = context.measureText(text);
    const textWidth = metrics.width;

    canvas.width = textWidth + 10;
    canvas.height = fontsize + 10;
    context.font = `Bold ${fontsize}px ${fontface}`;
    context.fillStyle = "rgba(44, 62, 80, 1.0)"; // #2c3e50
    context.fillText(text, 5, fontsize);

    const texture = new THREE.Texture(canvas);
    texture.needsUpdate = true;

    const spriteMaterial = new THREE.SpriteMaterial({ map: texture });
    const sprite = new THREE.Sprite(spriteMaterial);
    sprite.scale.set(canvas.width / 4, canvas.height / 4, 1.0);
    sprite.position.y = 8; // Offset above the sphere
    return sprite;
}

function addWordToScene(wordData) {
    const wordGroup = new THREE.Group();
    wordGroup.position.set(wordData.x, wordData.y, wordData.z);
    
    // Sphere
    const geometry = new THREE.SphereGeometry(3, 32, 32);
    const material = new THREE.MeshPhongMaterial({ color: '#3498db' });
    const sphere = new THREE.Mesh(geometry, material);
    wordGroup.add(sphere);

    // Text Label
    const sprite = createTextSprite(wordData.word);
    wordGroup.add(sprite);
    
    scene.add(wordGroup);
    
    wordData.object3D = wordGroup;
    wordData.sphere = sphere;

    gsap.from(sphere.scale, { x: 0.1, y: 0.1, z: 0.1, duration: 1.5, ease: "elastic.out(1, 0.3)" });
}

function clearAnalogyArrows() {
    analogyArrows.forEach(arrow => scene.remove(arrow));
    analogyArrows = [];
}

function render() {
    // This is now handled by the animate loop
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

function showLoading() {
    loadingIndicator.style.display = 'flex';
}

function hideLoading() {
    loadingIndicator.style.display = 'none';
}

async function getWordVectors(wordList, existingWordsMap) {
    showLoading();
    try {
        const systemPrompt = `You are an AI that maps English words to 3D coordinates for visualization. Your primary goal is to place semantically similar words close together in the 3D space. The coordinates for x, y, and z must be between ${scale.min} and ${scale.max}.

You will be given a list of new words to place. You may also be given a list of words that already exist in the space with their coordinates. Use the existing words as a reference to position the new words accurately. For example, if 'hot' exists and a new word is 'warm', 'warm' should be very close to 'hot'.

Respond with a JSON array of objects for the new words only. Each object must have a "word" (lowercase) and its coordinates "x", "y", and "z".`;
        
        let userContent = `Generate coordinates for the following new words: ${wordList.join(', ')}.`;

        const existingWords = Array.from(existingWordsMap.values());
        if (existingWords.length > 0) {
            const existingWordData = existingWords.map(({ word, x, y, z }) => ({ word, x, y, z }));
            userContent += `

Here are the existing words and their coordinates for context. Place the new words logically within this existing space:
${JSON.stringify(existingWordData)}`;
        }

        const completion = await websim.chat.completions.create({
            messages: [{
                role: "system",
                content: systemPrompt,
            }, {
                role: "user",
                content: userContent,
            }, ],
            json: true,
        });

        const result = JSON.parse(completion.content);
        return Array.isArray(result) ? result : []; // Ensure result is an array
    } catch (error) {
        console.error("Error fetching word vectors:", error);
        alert("The AI is having trouble thinking right now. Please try again later.");
        return [];
    } finally {
        hideLoading();
    }
}

async function addWordsToPlot(wordList) {
    const newWords = wordList.filter(w => w && !words.has(w.toLowerCase()));
    if (newWords.length === 0) {
        if (wordList.length > 0) {
             const existingWord = words.get(wordList[0].toLowerCase());
             if(existingWord && existingWord.sphere) {
                 gsap.to(existingWord.sphere.scale, { x: 1.5, y: 1.5, z: 1.5, repeat: 1, yoyo: true, duration: 0.3 });
             }
        }
        return;
    }

    const vectors = await getWordVectors(newWords, words);
    
    vectors.forEach(v => {
        const key = v.word.toLowerCase();
        if (!words.has(key)) {
            words.set(key, { ...v });
            addWordToScene(words.get(key));
        }
    });
}

async function handleAddWord() {
    const word = wordInput.value.trim().toLowerCase();
    if (!word) return;
    await addWordsToPlot([word]);
    wordInput.value = '';
}

async function handleAnalogy() {
    const terms = [
        analogyA.value.trim().toLowerCase(),
        analogyB.value.trim().toLowerCase(),
        analogyC.value.trim().toLowerCase(),
    ];
    if (terms.some(t => !t)) return;

    analogyResultEl.textContent = '?';
    showLoading();
    clearAnalogyArrows();

    try {
        const completion = await websim.chat.completions.create({
            messages: [{
                role: "system",
                content: `You are an AI assistant that solves word analogies. Given an analogy "A is to B as C is to ?", determine the best word for "?". Respond with a single JSON object containing the resulting word in lowercase, like {"result": "word"}.`,
            }, {
                role: "user",
                content: `Solve: "${terms[0]}" is to "${terms[1]}" as "${terms[2]}" is to ?`,
            }, ],
            json: true,
        });

        const response = JSON.parse(completion.content);
        const resultWord = response.result.toLowerCase();
        analogyResultEl.textContent = resultWord;
        confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
        
        const allWords = [...terms, resultWord];
        await addWordsToPlot(allWords);

        // Animate analogy in 3D
        const vA = words.get(terms[0]);
        const vB = words.get(terms[1]);
        const vC = words.get(terms[2]);
        const vD = words.get(resultWord);

        if (vA && vB && vC && vD) {
            const posA = new THREE.Vector3(vA.x, vA.y, vA.z);
            const posB = new THREE.Vector3(vB.x, vB.y, vB.z);
            const posC = new THREE.Vector3(vC.x, vC.y, vC.z);
            const posD = new THREE.Vector3(vD.x, vD.y, vD.z);

            const dir1 = new THREE.Vector3().subVectors(posA, posB);
            const arrow1 = new THREE.ArrowHelper(dir1.clone().normalize(), posB, dir1.length(), 0xe74c3c, 4, 2);
            scene.add(arrow1);
            analogyArrows.push(arrow1);

            const dir2 = new THREE.Vector3().subVectors(posD, posC);
            const arrow2 = new THREE.ArrowHelper(dir2.clone().normalize(), posC, dir2.length(), 0x2ecc71, 4, 2);
            arrow2.visible = false;
            scene.add(arrow2);
            analogyArrows.push(arrow2);
            
            gsap.from(arrow2, {
                onStart: () => { arrow2.visible = true },
                onUpdate: function() {
                    const currentLength = dir2.length() * this.progress();
                    arrow2.setLength(currentLength, 4, 2);
                },
                duration: 1.5,
                ease: "power2.out",
                delay: 0.5
            });
        }

    } catch (error) {
        console.error("Error fetching analogy:", error);
        analogyResultEl.textContent = 'Error';
        alert("The AI couldn't solve the analogy. Try different words.");
    } finally {
        hideLoading();
    }
}

async function handleFindSimilar() {
    const word = similarWordInput.value.trim().toLowerCase();
    if (!word) return;
    clearAnalogyArrows();

    showLoading();
    try {
        const completion = await websim.chat.completions.create({
            messages: [
                {
                    role: "system",
                    content: `You are an AI assistant that finds semantically related words. Given a word, provide 4 other words that are similar in meaning or context. Respond with a single JSON object with a "similar_words" key which is an array of strings.`
                },
                {
                    role: "user",
                    content: `Find words similar to "${word}".`
                }
            ],
            json: true
        });

        const response = JSON.parse(completion.content);
        const similarWords = response.similar_words.map(w => w.toLowerCase());
        
        await addWordsToPlot([word, ...similarWords]);

    } catch (error) {
        console.error("Error finding similar words:", error);
        alert("The AI had trouble finding similar words. Please try again.");
    } finally {
        hideLoading();
    }
}

async function handleRecalculateLayout() {
    showLoading();
    try {
        const allWords = Array.from(words.keys());
        if (allWords.length < 2) return;

        // Create a temporary map to pass to the vector function, but empty.
        // This forces a complete recalculation from scratch.
        const vectors = await getWordVectors(allWords, new Map());

        vectors.forEach(newVectorData => {
            const key = newVectorData.word.toLowerCase();
            const existingWord = words.get(key);
            if (existingWord) {
                // Update properties
                existingWord.x = newVectorData.x;
                existingWord.y = newVectorData.y;
                existingWord.z = newVectorData.z;
                
                // Animate the object to its new position
                if (existingWord.object3D) {
                    gsap.to(existingWord.object3D.position, {
                        x: newVectorData.x,
                        y: newVectorData.y,
                        z: newVectorData.z,
                        duration: 1.5,
                        ease: "power2.inOut"
                    });
                }
            }
        });

    } catch(error) {
        console.error("Error recalculating layout:", error);
        alert("The AI had trouble recalculating the layout. Please try again.");
    } finally {
        hideLoading();
    }
}

function setupEventListeners() {
    addWordBtn.addEventListener('click', handleAddWord);
    wordInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleAddWord();
    });

    analogyBtn.addEventListener('click', handleAnalogy);

    findSimilarBtn.addEventListener('click', handleFindSimilar);
    similarWordInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleFindSimilar();
    });
    
    recalculateLayoutBtn.addEventListener('click', handleRecalculateLayout);
}

function onWindowResize() {
    const container = document.querySelector('.vector-space-container');
    const size = container.clientWidth;

    camera.aspect = 1;
    camera.updateProjectionMatrix();

    renderer.setSize(size, size);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
}

async function init() {
    setupThreeJS();
    animate();
    window.addEventListener('resize', onWindowResize);
    setupEventListeners();
    const initialWords = ['cat', 'dog', 'animal', 'car', 'truck', 'vehicle', 'sun', 'moon', 'sky'];
    await addWordsToPlot(initialWords);
}

init();