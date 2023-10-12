from flask import Flask, request, jsonify
from download_data import download_profile 
from model import classifyProfile

app = Flask(__name__)
print("Loading model ...")
classifier=classifyProfile()
print("Model loaded !!")

@app.route('/get_category', methods=['POST'])
def get_category():
    print("Downloading Profile ...")
    instagram_link = request.json.get('instagram_link')
    data=download_profile(instagram_link)
    print("Profile downloaded !!")
    if len(data)<2: return jsonify({'category': 'Either could not fetch data or not enough post'})
    category=classifier.classify(data)
    return jsonify({'category': category})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
