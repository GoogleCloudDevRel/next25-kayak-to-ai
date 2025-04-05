from flask import Flask, jsonify, request
from google import genai

GEMINI_MODEL = 'gemini-2.0-flash'


app = Flask(__name__)

client = genai.Client(api_key='GEMINI_API_KEY')

@app.route('/')
def index():
    return jsonify({'message': 'Root endpoint'})

@app.route('/api/generate-location', methods=['POST'])
def test():
    return jsonify({'message': 'Test endpoint'})
    


@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from Flask!'})

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    return jsonify({'leaderboard': [ # TODO: get from database
        {
            'rank': 1,
            'name': 'AJS',
            'score': 100
        },
        {
            'rank': 2,
            'name': 'ABC',
            'score': 90
        },
        {
            'rank': 3,
            'name': 'WKE',
            'score': 80
        },
        {
            'rank': 4,
            'name': 'QWE',
            'score': 70
        }
    ]})

@app.route('api/gemini', methods=['POST'])
def gemini():
    try:
        data = request.get_json()
        prompt = data.get('prompt')

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        response = client.models.generate_content(
            model=GEMINI_MODEL, 
            contents=prompt,
        )

        # Extract the text content from the response
        text_response = response.text
        
        return jsonify({'response': text_response})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # You can specify host='0.0.0.0' if you want it accessible externally
    app.run(debug=True, port=5000)


# 1. user prompts to ask questions about where something is from
# 2. gemini returns responses
# 3. user picks location to go to
# 4. based on the location information, run the kayak
# 5. return complete when complete
# 6. display informaiton about the location@app.route('/api/start-kayak', methods=['POST'])
def start_kayak():
    # TODO: Implement logic to start the kayak
    return jsonify({'message': 'Kayak started'})

@app.route('/api/stop-kayak', methods=['POST'])
def stop_kayak():
    # TODO: Implement logic to stop the kayak
    return jsonify({'message': 'Kayak stopped'})

@app.route('/api/get-status', methods=['GET'])
def get_status():
    # TODO: Implement logic to get the kayak status
    return jsonify({'status': 'idle'})

@app.route('/api/get-location-details', methods=['POST'])
def get_location_details():
    data = request.get_json()
    location = data.get('location')
    if not location:
        return jsonify({'error': 'Location is required'}), 400
    # TODO: Implement logic to get location details
    return jsonify({'location': location, 'details': 'Details for ' + location})
