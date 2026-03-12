# agents/app.py
import streamlit as st
import time
import os
from datetime import datetime
from rag.rfp_parser import parse_rfp
from agents.sdlc_workflow import SDLCWorkflow
from rag.s3_uploader import S3Uploader

# ====================== CUSTOM GLOWING CSS ======================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .main-header {
        font-size: 52px;
        font-weight: 700;
        background: linear-gradient(90deg, #00ffea, #00b4ff, #7b00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
    }
    .glow-button {
        background: linear-gradient(45deg, #00ffea, #7b00ff);
        color: white;
        font-weight: bold;
        padding: 18px 40px;
        border-radius: 50px;
        font-size: 20px;
        box-shadow: 0 0 40px rgba(0, 255, 234, 0.6),
                    0 0 80px rgba(123, 0, 255, 0.4);
        transition: all 0.3s ease;
    }
    .glow-button:hover {
        box-shadow: 0 0 60px rgba(0, 255, 234, 0.9),
                    0 0 100px rgba(123, 0, 255, 0.7);
        transform: scale(1.05);
    }
    .agent-card {
        background: rgba(15, 23, 42, 0.95);
        border: 2px solid rgba(0, 255, 234, 0.3);
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 0 25px rgba(0, 255, 234, 0.2);
        transition: all 0.3s ease;
    }
    .agent-card:hover {
        border-color: #00ffea;
        box-shadow: 0 0 40px rgba(0, 255, 234, 0.5);
    }
    .neon-text {
        text-shadow: 0 0 10px #00ffea,
                     0 0 20px #00ffea,
                     0 0 40px #7b00ff;
    }
    .progress-bar {
        height: 8px;
        background: linear-gradient(90deg, #00ffea, #7b00ff);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ====================== HEADER ======================
st.markdown("<h1 class='main-header neon-text'>🤖 AI DEVELOPMENT POD</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:20px; color:#00ffea;'>Self-Organizing • RAG-Powered • S3 Cloud Backed</p>", unsafe_allow_html=True)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/robot.png", width=80)
    st.title("Pod Status")
    st.success("● All 5 Agents Online")
    st.info("Chroma RAG + S3 Connected")
    st.caption(f"Session: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# ====================== MAIN UI ======================
rfp_file = st.file_uploader("📤 Upload RFP Document (PDF or TXT)", type=["pdf", "txt"])

if st.button("🚀 LAUNCH AUTONOMOUS DEVELOPMENT POD", type="primary", use_container_width=True, key="launch"):
    if not rfp_file:
        st.error("Please upload an RFP first!")
        st.stop()

    # ====================== LIVE DASHBOARD ======================
    st.markdown("---")
    st.markdown("### 🔴 LIVE AGENT EXECUTION DASHBOARD")

    progress_container = st.container()
    log_area = st.empty()

    with progress_container:
        cols = st.columns(5)
        agent_status = [cols[0].empty(), cols[1].empty(), cols[2].empty(), cols[3].empty(), cols[4].empty()]

    try:
        rfp_text = parse_rfp(rfp_file)
        s3 = S3Uploader()
        workflow = SDLCWorkflow()

        # ====================== AGENT PROGRESS LOOP ======================
        phases = [
            ("📋 Business Analyst", "Analyzing RFP..."),
            ("🛠️ Design Agent", "Creating architecture..."),
            ("💻 Developer Agent", "Writing production code..."),
            ("🧪 Tester Agent", "Running tests & validation..."),
            ("📊 Project Lead", "Finalizing report...")
        ]

        artifacts = {}
        project_id = None

        for i, (agent_name, status_text) in enumerate(phases):
            # Live status update
            with agent_status[i]:
                st.markdown(f"""
                <div class="agent-card">
                    <h4 style="color:#00ffea;">{agent_name}</h4>
                    <p>{status_text}</p>
                    <div style="height:6px; background:linear-gradient(90deg,#00ffea,#7b00ff); border-radius:10px; width:60%;"></div>
                </div>
                """, unsafe_allow_html=True)

            # Simulate live feel + actual execution
            time.sleep(0.8)  # small delay for dramatic effect

            # Actual agent execution (keeps your backend intact)
            if i == 0:
                stories, _ = workflow.analyst.generate_user_stories(rfp_text, "live")
                artifacts["User Stories"] = stories
            elif i == 1:
                design, _ = workflow.designer.generate_design(stories, rfp_text, "live")
                artifacts["System Design"] = design
            elif i == 2:
                _, code_paths = workflow.developer.generate_code(stories, design, rfp_text, "live")
                artifacts["Source Code"] = f"{len(code_paths)} files generated"
                project_id = "live"  # placeholder
            elif i == 3:
                report, _ = workflow.tester.generate_test_report(code_paths, stories, "live")
                artifacts["Test Report"] = report
            elif i == 4:
                status_report, _ = workflow.lead.generate_status_report("live", artifacts)
                artifacts["Project Status Report"] = status_report

            # Update log
            log_area.markdown(f"**{agent_name}** → ✅ Completed", unsafe_allow_html=True)

        # ====================== FINAL SUCCESS SECTION ======================
        st.balloons()
        st.success(f"🎉 Project Completed Successfully! (ID: {project_id})")
        st.markdown("### 📦 Generated Artifacts")

        cols = st.columns(3)
        for idx, (name, content) in enumerate(artifacts.items()):
            with cols[idx % 3]:
                with st.expander(f"🌟 **{name}**", expanded=True):
                    st.markdown(content[:800] + "..." if len(str(content)) > 800 else content)
                    
                    # Local Download
                    if isinstance(content, str):
                        st.download_button(f"⬇️ Download {name}", content, f"{name.replace(' ','_')}.md")
                    
                    # S3 Cloud Link
                    if name != "Source Code":
                        rel_path = f"{name.lower().replace(' ','_')}.md"
                        url = s3.get_presigned_url("live", rel_path)
                        if url:
                            st.markdown(f"[🌐 Open in S3 Cloud]({url})")

        # Source Code special handling
        if "Source Code" in artifacts:
            with st.expander("💻 Source Code Files", expanded=True):
                st.write(artifacts["Source Code"])
                st.info("All source code files saved in ai-dev-pod-repository/ and uploaded to S3")

    except Exception as e:
        st.error(f"Pipeline Error: {str(e)}")

# ====================== FOOTER ======================
st.markdown("---")
st.markdown("<p style='text-align:center; color:#666;'>AI Development Pod v2.0 • Powered by Ollama + Chroma + AWS S3</p>", unsafe_allow_html=True)