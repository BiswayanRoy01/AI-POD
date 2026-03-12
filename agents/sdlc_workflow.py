# agents/sdlc_workflow.py
"""
Central orchestrator that runs the full SDLC pipeline:
1. Business Analyst → user stories
2. Design Agent → architecture/design
3. Developer Agent → source code
4. Tester Agent → test cases & report
5. Lead Agent → final status report
"""

import os
from datetime import datetime
from typing import Dict, List, Tuple

import streamlit as st

from agents.analyst import BusinessAnalystAgent
from agents.design import DesignAgent
from agents.developer import DeveloperAgent
from agents.tester import TesterAgent
from agents.lead_agent import ProjectLeadAgent
from rag.rag_retriever import RAGRetriever as Storage


class SDLCWorkflow:
    def __init__(self, status_container=None):
        self.status = status_container  # Optional: Streamlit st.status container
        self.storage = Storage()

        self.analyst = BusinessAnalystAgent()
        self.designer = DesignAgent()
        self.developer = DeveloperAgent()
        self.tester = TesterAgent()
        self.lead = ProjectLeadAgent()

    def log(self, msg: str, emoji: str = "→"):
        full_msg = f"{emoji} {msg}"
        print(full_msg)
        if self.status is not None:
            self.status.write(full_msg)

    def run(self, rfp_text: str) -> Tuple[List[str], Dict[str, str], str]:
        project_id = f"proj_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.log(f"Starting new project → {project_id}", "🚀")

        artifacts: Dict[str, str] = {}
        logs: List[str] = [f"Project ID: {project_id}"]

        base_path = f"ai-dev-pod-repository/{project_id}"
        for subdir in ["user_stories", "designs", "source_code", "test_reports", "project_status_reports"]:
            os.makedirs(f"{base_path}/{subdir}", exist_ok=True)

        try:
            # ── 1. Business Analyst ─────────────────────────────────────────
            self.log("Business Analyst is analyzing RFP...", "📋")
            stories_content, stories_path = self.analyst.generate_user_stories(rfp_text, project_id)
            artifacts["User Stories"] = stories_content
            logs.append("User Stories created")
            self.log("User Stories ready", "✅")

            # ── 2. Design Agent ─────────────────────────────────────────────
            self.log("Design Agent is creating architecture...", "🛠️")
            design_content, design_path = self.designer.generate_design(stories_content, rfp_text, project_id)
            artifacts["System Design"] = design_content
            logs.append("System Design created")
            self.log("Design document ready", "✅")

            # ── 3. Developer Agent ──────────────────────────────────────────
            self.log("Developer Agent is writing code...", "💻")
            code_output, code_paths = self.developer.generate_code(
                stories_content, design_content, rfp_text, project_id
            )
            artifacts["Source Code"] = f"{len(code_paths)} file(s) generated\n" + "\n".join(
                f"• {os.path.basename(p)}" for p in code_paths
            )
            logs.append(f"Code generated ({len(code_paths)} files)")
            self.log(f"Code generation finished ({len(code_paths)} files)", "✅")

            # ── 4. Tester Agent ─────────────────────────────────────────────
            self.log("Tester Agent is creating & simulating tests...", "🧪")
            test_content, test_path = self.tester.generate_test_report(
                code_paths, stories_content, project_id
            )
            artifacts["Test Report"] = test_content
            logs.append("Test report created")
            self.log("Testing phase completed", "✅")

            # ── 5. Project Lead ─────────────────────────────────────────────
            self.log("Project Lead is preparing final report...", "📊")
            status_content, status_path = self.lead.generate_status_report(project_id, artifacts)
            artifacts["Project Status Report"] = status_content
            logs.append("Final status report ready")
            self.log("Project status report ready", "✅")

            # ── Self-improvement: add to RAG ────────────────────────────────
            self.log("Adding project artifacts to historical knowledge base...", "🔄")
            self.storage.add_new_project_artifacts(project_id)
            self.log("Knowledge base updated – pod just got smarter", "🌱")

            self.log("Pipeline completed successfully", "🎉")
            logs.append("Pipeline completed")

        except Exception as e:
            error_msg = f"Pipeline failed: {str(e)}"
            self.log(error_msg, "❌")
            logs.append(error_msg)
            raise

        return logs, artifacts, project_id