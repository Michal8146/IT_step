let myPlayerId = null;
let gameState = null;
let selectedToMove = false;

function setPlayer(id) {
    myPlayerId = id;
    document.querySelector('h1').innerText = `You are Player ${id}`;
    setInterval(fetchState, 1000);
}

async function fetchState() {
    if (!myPlayerId) return;
    const response = await fetch('/state');
    gameState = await response.json();
    renderBoard();
}

function renderBoard() {
    const board = document.getElementById('board');
    board.innerHTML = '';
    
    const status = document.getElementById('status');
    if (gameState.winner) {
        status.innerText = `Player ${gameState.winner} Wins!`;
    } else {
        status.innerText = gameState.turn == myPlayerId ? "YOUR TURN" : "Enemy Turn...";
    }

    const myData = gameState.players[myPlayerId];
    
    for (let y = 0; y < 19; y++) {
        for (let x = 0; x < 19; x++) {
            const cell = document.createElement('div');
            
            // Determine exact cell type
            const isTile = (x % 2 === 0 && y % 2 === 0);
            const isGapH = (x % 2 === 0 && y % 2 !== 0); // Top/Bottom gaps
            const isGapV = (x % 2 !== 0 && y % 2 === 0); // Left/Right gaps
            
            if (isTile) cell.className = 'tile';
            else if (isGapH) cell.className = 'gap-h';
            else if (isGapV) cell.className = 'gap-v';
            else cell.className = 'intersection'; // Dead space

            // Fog of War Logic
            if (myData.ready && !gameState.winner) {
                const dist = Math.max(Math.abs(myData.x - x), Math.abs(myData.y - y));
                if (dist > 6 && !myData.eye_active) {
                    cell.classList.add('fog');
                }
            }

            // Draw Walls
            if (gameState.walls.find(w => w.x === x && w.y === y)) {
                cell.classList.add('wall-placed');
            }

            // Draw Items (if not covered by fog)
            if (gameState.items.find(i => i.x === x && i.y === y) && !cell.classList.contains('fog')) {
                const eye = document.createElement('div');
                eye.className = 'item-eye';
                cell.appendChild(eye);
            }

            // Draw Players (if not covered by fog)
            if (!cell.classList.contains('fog')) {
                if (gameState.players["1"].x === x && gameState.players["1"].y === y) {
                    const p1 = document.createElement('div'); p1.className = 'player p1'; cell.appendChild(p1);
                }
                if (gameState.players["2"].x === x && gameState.players["2"].y === y) {
                    const p2 = document.createElement('div'); p2.className = 'player p2'; cell.appendChild(p2);
                }
            }

            // Click Logic
            cell.onclick = () => handleCellClick(x, y, isTile, isGapH, isGapV, cell);
            board.appendChild(cell);
        }
    }
}

async function handleCellClick(x, y, isTile, isGapH, isGapV, cellElement) {
    if (gameState.turn != myPlayerId) return;
    const myData = gameState.players[myPlayerId];

    // Setup Phase: Place your gladiator
    if (!myData.ready && isTile) {
        if ((myPlayerId === "1" && y === 0) || (myPlayerId === "2" && y === 18)) {
            await sendAction({ type: "setup", x: x, y: y, player_id: myPlayerId });
        } else {
            alert("Must start on your home row!");
        }
        return;
    }

    if (!myData.ready) return;

    if (isTile) {
        // First click selects player
        if (myData.x === x && myData.y === y) {
            selectedToMove = true;
            cellElement.style.border = "2px solid yellow";
        } else if (selectedToMove) {
            // Check Orthogonal Movement (Up, Down, Left, Right - steps of 2)
            const isOrthogonal = (Math.abs(myData.x - x) === 2 && myData.y === y) || (Math.abs(myData.y - y) === 2 && myData.x === x);
            
            if (isOrthogonal) {
                // Check if a wall is blocking the path
                const wallX = myData.x + (x - myData.x) / 2;
                const wallY = myData.y + (y - myData.y) / 2;
                const isBlocked = gameState.walls.find(w => w.x === wallX && w.y === wallY);

                if (!isBlocked) {
                    await sendAction({ type: "move", x: x, y: y, player_id: myPlayerId });
                    selectedToMove = false;
                } else {
                    alert("A wall is blocking that path!");
                }
            }
        }
    } else if (isGapH || isGapV) {
        // Place Wall in the gap
        const res = await sendAction({ type: "wall", x: x, y: y, player_id: myPlayerId });
        if (res.error) alert(res.error); 
    }
}

async function sendAction(data) {
    const response = await fetch('/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    const resData = await response.json();
    fetchState();
    return resData;
}