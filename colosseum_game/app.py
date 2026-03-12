from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Global Game State (For local testing with 2 browsers)
game_state = {
    "players": {
        "1": {"x": None, "y": 0, "ready": False, "eye_active": False, "eye_duration": 0},
        "2": {"x": None, "y": 18, "ready": False, "eye_active": False, "eye_duration": 0}
    },
    "turn": 1,
    "walls": [], # Stores coordinates of placed walls
    "items": [], # Stores the Ancient Eye coordinates
    "winner": None
}

# Generate 2 random Ancient Eyes on playable tiles (even coordinates)
for _ in range(2):
    game_state["items"].append({
        "x": random.choice(range(2, 18, 2)), 
        "y": random.choice(range(4, 14, 2))
    })

def has_path(start_x, start_y, target_y, walls):
    """BFS Algorithm to check if a player can still reach their goal."""
    queue = [(start_x, start_y)]
    visited = set([(start_x, start_y)])
    
    while queue:
        cx, cy = queue.pop(0)
        if cy == target_y:
            return True
        
        # Check 8 directions (King Movement). Steps of 2 because tiles are at even numbers.
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0), (-2, -2), (2, -2), (-2, 2), (2, 2)]
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx <= 18 and 0 <= ny <= 18 and (nx, ny) not in visited:
                # Basic collision check: is there a wall between current and next?
                wall_x, wall_y = cx + (dx//2), cy + (dy//2)
                if {"x": wall_x, "y": wall_y} not in walls:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
    return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/state", methods=["GET"])
def get_state():
    return jsonify(game_state)

@app.route("/action", methods=["POST"])
def action():
    data = request.json
    player_id = data.get("player_id")
    action_type = data.get("type")
    
    if str(game_state["turn"]) != player_id and action_type != "setup":
        return jsonify({"error": "Not your turn!"}), 400

    p_data = game_state["players"][player_id]

    if action_type == "setup":
        p_data["x"] = data["x"]
        p_data["ready"] = True
        return jsonify({"success": True})

    if action_type == "move":
        nx, ny = data["x"], data["y"]
        p_data["x"], p_data["y"] = nx, ny
        
        # Check for Ancient Eye
        for item in game_state["items"]:
            if item["x"] == nx and item["y"] == ny:
                p_data["eye_active"] = True
                p_data["eye_duration"] = 2 # Lasts this turn + enemy turn
                game_state["items"].remove(item)

        # Win condition
        if (player_id == "1" and ny == 18) or (player_id == "2" and ny == 0):
            game_state["winner"] = player_id

    elif action_type == "wall":
        wx, wy = data["x"], data["y"]
        temp_walls = game_state["walls"] + [{"x": wx, "y": wy}]
        
        # Check if this traps ANY player
        p1 = game_state["players"]["1"]
        p2 = game_state["players"]["2"]
        if not has_path(p1["x"], p1["y"], 18, temp_walls) or not has_path(p2["x"], p2["y"], 0, temp_walls):
            return jsonify({"error": "Cannot trap player!"}), 400
        
        game_state["walls"].append({"x": wx, "y": wy})

    # Turn management and Eye duration
    if p_data["eye_duration"] > 0:
        p_data["eye_duration"] -= 1
        if p_data["eye_duration"] == 0:
            p_data["eye_active"] = False

    game_state["turn"] = 2 if game_state["turn"] == 1 else 1
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True, port=5000)