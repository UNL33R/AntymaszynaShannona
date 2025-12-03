from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from shannon_engine import ShannonGame, AntiShannonGame, run_simulation
import os

app = Flask(__name__, static_folder='.')
CORS(app)

# Game instances
shannon_game = ShannonGame()
anti_game = AntiShannonGame()

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS)"""
    return send_from_directory('.', path)

# Shannon Mode Endpoints
@app.route('/api/shannon/move', methods=['POST'])
def shannon_move():
    """Process a move in Shannon mode"""
    data = request.json
    choice = data.get('choice')
    
    if choice not in [0, 1]:
        return jsonify({"error": "Invalid choice"}), 400
    
    result = shannon_game.make_move(choice)
    return jsonify(result)

@app.route('/api/shannon/reset', methods=['POST'])
def shannon_reset():
    """Reset Shannon game"""
    global shannon_game
    shannon_game = ShannonGame()
    return jsonify({"status": "reset"})

# Anti-Shannon Mode Endpoints
@app.route('/api/anti/move', methods=['POST'])
def anti_move():
    """Process a move in Anti-Shannon mode"""
    data = request.json
    human_choice = data.get('human_choice')
    machine_choice = data.get('machine_choice')
    
    if human_choice not in [0, 1] or machine_choice not in [0, 1]:
        return jsonify({"error": "Invalid choices"}), 400
    
    result = anti_game.make_move(human_choice, machine_choice)
    return jsonify(result)

@app.route('/api/anti/reset', methods=['POST'])
def anti_reset():
    """Reset Anti-Shannon game"""
    global anti_game
    anti_game = AntiShannonGame()
    return jsonify({"status": "reset"})

# Simulation Mode Endpoints
@app.route('/api/simulation/run', methods=['POST'])
def simulation_run():
    """Run a simulation"""
    data = request.json
    rounds = data.get('rounds', 100)
    
    if not isinstance(rounds, int) or rounds < 10 or rounds > 10000:
        return jsonify({"error": "Invalid number of rounds"}), 400
    
    result = run_simulation(rounds)
    return jsonify(result)

if __name__ == '__main__':
    print("=" * 60)
    print("Serwer Maszyny Shannona uruchomiony!")
    print("=" * 60)
    print("Otworz przegladarke i przejdz do:")
    print("   http://localhost:8080")
    print("=" * 60)
    print("Nacisnij Ctrl+C aby zatrzymac serwer\n")
    
    app.run(debug=True, port=8080, host='0.0.0.0')
