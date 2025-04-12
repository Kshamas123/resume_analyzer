from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/score_resume', methods=['POST'])
def score_resume():
    data = request.get_json()
    resume_text = data.get('resume_text', '')

    score, feedback = calculate_score(resume_text)

    return jsonify({
        "score": score,
        "feedback": feedback
    })

def calculate_score(text):
    score = 0
    feedback = []

    # Criteria 1: Length check
    word_count = len(text.split())
    if word_count > 300:
        score += 10
        feedback.append("Good resume length.")
    else:
        feedback.append("Try to add more details to your resume.")

    # Criteria 2: Check for key skills
    required_keywords = ["Python", "JavaScript", "React", "MySQL", "Node.js", "Git"]
    found_keywords = [kw for kw in required_keywords if kw.lower() in text.lower()]

    score += len(found_keywords) * 5
    if found_keywords:
        feedback.append(f"Good use of keywords: {', '.join(found_keywords)}.")
    else:
        feedback.append("Try to include more relevant technical keywords.")

    # Criteria 3: Contact info
    if "@gmail.com" in text or "@outlook.com" in text:
        score += 5
        feedback.append("Email found.")
    else:
        feedback.append("Add an email to your resume.")

    return score, feedback

if __name__ == '__main__':
    # Get port from environment variable (for cloud platforms)
    port = int(os.environ.get("PORT", 5000))
    
    # Run the app with '0.0.0.0' for external access
    app.run(debug=True, host="0.0.0.0", port=port)


