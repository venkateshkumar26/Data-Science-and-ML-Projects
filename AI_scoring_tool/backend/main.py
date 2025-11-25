from flask import Flask, request, jsonify
from scoring import total_score

app = Flask(__name__)

@app.route("/score", methods=["POST"])
def score():
    data = request.json or {}
    transcript = data.get("transcript", "")
    duration_seconds = data.get("duration_seconds", 60)  
    final_score_result = total_score(transcript, duration_seconds)
    
    overall_score = final_score_result[0]
    metric_scores = final_score_result[1:]  
    
    response = {
        "score": overall_score,
        "metrics": [
            {"metric": "Salutation Level", "score": metric_scores[0], "weight": 5},
            {"metric": "Keyword Presence", "score": metric_scores[1], "weight": 30},
            {"metric": "Flow", "score": metric_scores[2], "weight": 5},
            {"metric": "Speech Rate", "score": metric_scores[3], "weight": 10},
            {"metric": "Grammar Score", "score": metric_scores[4], "weight": 10},
            {"metric": "Vocabulary Richness", "score": metric_scores[5], "weight": 10},
            {"metric": "Filler Word Rate", "score": metric_scores[6], "weight": 15},
            {"metric": "Sentiment/Positivity", "score": metric_scores[7], "weight": 15}
        ]
    }
    
    return jsonify(response)

if __name__=="__main__":
    app.run(debug=True)