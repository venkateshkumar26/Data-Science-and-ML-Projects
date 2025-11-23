import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000/score"

st.set_page_config(page_title="AI Communication Scoring Tool", layout="wide")

st.title("🎯 AI Communication Skill Scoring Tool")
st.write("Paste your transcript below and click **Score** to evaluate it.")

transcript = st.text_area("Enter Transcript:", height=200, placeholder="Paste your self-introduction transcript here...")

if st.button("🎯 Score Transcript", type="primary"):
    if transcript.strip() == "":
        st.warning("Please enter a transcript before scoring.")
    else:
        with st.spinner("Analyzing your transcript..."):
            try:
                payload = {"transcript": transcript}
                response = requests.post(API_URL, json=payload)

                if response.status_code == 200:
                    result = response.json()
                    overall_score = result['score']
                    
                    st.success(f"## Overall Score: **{overall_score:.2f}/100**")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📊 Detailed Metrics")
                        
                        for metric in result["metrics"]:
                            metric_name = metric["metric"]
                            score = metric["score"]
                            weight = metric["weight"]
                            percentage = (score / weight) * 100
                            
                            if percentage >= 80:
                                color = "🟢"
                            elif percentage >= 60:
                                color = "🟡"
                            else:
                                color = "🔴"
                            
                            st.markdown(f"""
                            **{color} {metric_name}**
                            - Score: **{score:.1f}/{weight}**
                            - Performance: **{percentage:.1f}%**
                            """)
                            st.progress(percentage / 100)
                            st.markdown("---")
                    
                    with col2:
                        st.subheader("📈 Score Breakdown")
                        
                        metric_names = [m["metric"] for m in result["metrics"]]
                        metric_scores = [m["score"] for m in result["metrics"]]
                        metric_weights = [m["weight"] for m in result["metrics"]]
                        
                        chart_data = {
                            "Metric": metric_names,
                            "Score": metric_scores,
                            "Max Score": metric_weights
                        }
                        
                        for i, metric in enumerate(result["metrics"]):
                            st.markdown(f"""
                            **{metric['metric']}**
                            ██████████ {metric['score']:.1f}/{metric['weight']}
                            """)
                        
                        # Summary statistics
                        st.subheader("📋 Summary")
                        total_possible = sum(metric_weights)
                        achieved_percentage = (overall_score / total_possible) * 100
                        
                        st.metric("Total Score", f"{overall_score:.1f}/{total_possible}")
                        st.metric("Performance", f"{achieved_percentage:.1f}%")
                        
                        if achieved_percentage >= 80:
                            performance_text = "Excellent 🎉"
                        elif achieved_percentage >= 70:
                            performance_text = "Good 👍"
                        elif achieved_percentage >= 60:
                            performance_text = "Average 📊"
                        else:
                            performance_text = "Needs Improvement 📝"
                            
                        st.metric("Performance Category", performance_text)

                else:
                    st.error(f"Error from backend (Status {response.status_code}): {response.text}")

            except Exception as e:
                st.error(f"Could not connect to API. Error: {e}")
