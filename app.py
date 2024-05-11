from flask import Flask, render_template, request
app = Flask(__name__)
from main import get_ai_response

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/sendChat', methods=['POST'])
def sendChat():
    data = request.get_json()
    user_input = data['input']
    # Pass 'user_input' to your Python script
    result = get_ai_response(user_input)
    return {'result': result}

if __name__ == '__main__':
    app.run(debug=True)
    
