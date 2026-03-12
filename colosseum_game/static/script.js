let myPlayerId = null;
let gameState = null;
let selectedToMove = false;

function setPlayer(id) {
    myPlayerId = id;
    document.querySelector('h1').innerText = `You are Player ${id}`;
    setInterval(fetchState, 1000); // Start the AJAX polling loop
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
            
            // Determine if it's a tile or a gap
            const isTile = (x % 2 === 0 && y % 2 === 0);
            cell.className = isTile ? 'tile' : 'gap';

            // Check Fog of War
            if (myData.ready && !gameState.winner) {
                // King distance calculation
                const dist = Math.max(Math.abs(myData.x - x), Math.abs(myData.y - y));
                // 3 tiles = 6 grid units. If eye is active, distance is irrelevant.
                if (dist > 6 && !myData.eye_active) {
                    cell.classList.add('fog');
                }
            }

            // Draw Walls
            if (gameState.walls.find(w => w.x === x && w.y === y)) {
                cell.classList.add('wall-placed');
            }

            // Draw Items
            if (gameState.items.find(i => i.x === x && i.y === y)) {
                if (!cell.classList.contains('fog')) cell.classList.add('item-eye');
            }

            // Draw Players
            if (gameState.players["1"].x === x && gameState.players["1"].y === y && !cell.classList.contains('fog')) {
                cell.classList.add('player1');
            }
            if (gameState.players["2"].x === x && gameState.players["2"].y === y && !cell.classList.contains('fog')) {
                cell.classList.add('player2');
            }

            // Click Logic
            cell.onclick = () => handleCellClick(x, y, isTile, cell);
            board.appendChild(cell);
        }
    }
}

async function handleCellClick(x, y, isTile, cellElement) {
    if (gameState.turn != myPlayerId) return;
    const myData = gameState.players[myPlayerId];

    // Setup Phase: Choosing starting tile
    if (!myData.ready && isTile) {
        if ((myPlayerId === "1" && y === 0) || (myPlayerId === "2" && y === 18)) {
            await sendAction({ type: "setup", x: x, y: y, player_id: myPlayerId });
        } else {
            alert("Must start on your home row!");
        }
        return;
    }

    // Play Phase
    if (!myData.ready) return;

    if (isTile) {
        // First click selects player, second click moves
        if (myData.x === x && myData.y === y) {
            selectedToMove = true;
            cellElement.style.border = "2px solid yellow";
        } else if (selectedToMove) {
            // Check King Movement range (max 2 grid units away)
            if (Math.abs(myData.x - x) <= 2 && Math.abs(myData.y - y) <= 2) {
                await sendAction({ type: "move", x: x, y: y, player_id: myPlayerId });
                selectedToMove = false;
            }
        }
    } else {
        // Place Wall
        const res = await sendAction({ type: "wall", x: x, y: y, player_id: myPlayerId });
        if (res.error) alert(res.error); // Show alert if wall traps player
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