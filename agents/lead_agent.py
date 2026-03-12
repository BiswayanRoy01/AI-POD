from langchain_ollama import ChatOllama
import os

class ProjectLeadAgent:
    def __init__(self):
        self.llm = ChatOllama(model="llama3.2", temperature=0.1)

    def generate_status_report(self, project_id: str, artifacts: dict):
        prompt = f"""You are the Project Lead.
Project ID: {project_id}
Artifacts created: {list(artifacts.keys())}

Generate a beautiful professional status report for the Project Manager in markdown with emojis."""

        resp = self.llm.invoke(prompt)
        content = resp.content

        os.makedirs(f"ai-dev-pod-repository/{project_id}/project_status_reports", exist_ok=True)
        path = f"ai-dev-pod-repository/{project_id}/project_status_reports/status_{project_id}.md"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return content, path