# agents/test_team.py
"""
Simple script to test agents one by one without Streamlit
Usage:
    python agents/test_team.py
"""

import os
from datetime import datetime
from analyst import BusinessAnalystAgent
from design import DesignAgent
from developer import DeveloperAgent
from tester import TesterAgent
from lead_agent import ProjectLeadAgent
from rag.rag_retriever import RAGRetriever

def main():
    print("=== AI Dev Pod - Agent Test Runner ===\n")

    project_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M')}"
    print(f"Project ID: {project_id}\n")

    # Fake but realistic inputs
    rfp_text = """
    RFP: Build a simple task management web application
    Users should be able to register, login, create/update/delete tasks,
    mark tasks as completed. Use modern web technologies.
    """

    print("1. Business Analyst Agent")
    analyst = BusinessAnalystAgent()
    stories, stories_path = analyst.generate_user_stories(rfp_text, project_id)
    print(f"Stories saved to: {stories_path}")
    print(f"First 3 lines:\n{stories.splitlines()[:3]}\n")

    print("2. Design Agent")
    design_agent = DesignAgent()
    design, design_path = design_agent.generate_design(stories, rfp_text, project_id)
    print(f"Design saved to: {design_path}")
    print(f"First 3 lines:\n{design.splitlines()[:3]}\n")

    print("3. Developer Agent")
    dev_agent = DeveloperAgent()
    raw_code, code_paths = dev_agent.generate_code(stories, design, rfp_text, project_id)
    print(f"Generated {len(code_paths)} code files:")
    for p in code_paths:
        print(f"  - {os.path.basename(p)}")
    print("")

    print("4. Tester Agent")
    tester = TesterAgent()
    report, report_path = tester.generate_test_report(code_paths, stories, project_id)
    print(f"Test report saved to: {report_path}")
    print(f"Report preview (first 200 chars):\n{report[:200]}...\n")

    print("5. Lead Agent (status report)")
    lead = ProjectLeadAgent()
    artifacts = {
        "User Stories": stories,
        "Design": design,
        "Code files": len(code_paths),
        "Test Report": report
    }
    status, status_path = lead.generate_status_report(project_id, artifacts)
    print(f"Status report saved to: {status_path}")
    print(f"Status preview:\n{status[:300]}...\n")

    print("=== Test completed ===")


if __name__ == "__main__":
    # Make sure chroma is loaded (for RAG)
    RAGRetriever()  # just initialize
    main()