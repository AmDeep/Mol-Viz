from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='dist/public')
CORS(app)

# Utility functions for molecular calculations
def calculate_distance(atoms):
    """Simulate distance calculation"""
    return round(4.5, 2)  # Example fixed value for testing

def calculate_angle(atoms):
    """Simulate angle calculation"""
    return round(109.5, 1)  # Example fixed value for testing

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'ok'})

@app.route('/api/gromacs/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        analysis_type = data.get('type')
        atoms = data.get('atoms', '')

        # Parse atom indices
        atom_indices = [int(i.strip()) for i in atoms.split(',') if i.strip().isdigit()]

        # Perform analysis based on type
        if analysis_type == 'distance':
            if len(atom_indices) != 2:
                raise ValueError('Distance measurement requires exactly 2 atoms')
            result = f"{calculate_distance(atom_indices)} Å"
            message = 'Distance measurement completed'
        elif analysis_type == 'angle':
            if len(atom_indices) != 3:
                raise ValueError('Angle measurement requires exactly 3 atoms')
            result = f"{calculate_angle(atom_indices)}°"
            message = 'Angle measurement completed'
        else:
            result = "0.0"
            message = f"{analysis_type} calculation simulated"

        return jsonify({
            'status': 'completed',
            'result': result,
            'message': message
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

# Serve React static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
