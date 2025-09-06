from flask import Flask,request,jsonify
import joblib

app=Flask(__name__)

model=joblib.load("spam_detector_pipeline.pkl")

@app.post("/predict")

def predict():
    data=request.get_json(force=True)
    mails=data.get("mails",[])
    
    if not mails:
        return jsonify({"error":"No mails provided"})
    
    prediction=model.predict(mails)
    label_map={1:"spam",0:"not spam"}
    prediction=[label_map.get(item) for item in prediction]
    return jsonify({"predictions":prediction.tolist()})

if __name__=="__main__":
    app.run(debug=True)

