# agents/developer.py

import os
import datetime
from typing import Tuple, List

from langchain_ollama import ChatOllama
from rag.rag_retriever import RAGRetriever as Storage


class DeveloperAgent:

    def __init__(self):

        self.llm = ChatOllama(
            model="llama3.2",
            temperature=0.2,
            num_ctx=8192
        )

        self.storage = Storage()

    def generate_code(
        self,
        user_stories: str,
        system_design: str,
        rfp_text: str,
        project_id: str
    ) -> Tuple[str, List[str]]:

        """
        Generates source code based on system design and user stories.
        Returns: (code_content, [code_file_paths])
        """

        # ── 1. Retrieve historical code via RAG ───────────────────
        rag_query = system_design[:900]

        similar_docs = self.storage.similarity_search(
            query=rag_query,
            k=5,
            filter={"artifact_type": "source_code"}
        )

        historical_examples = ""

        if similar_docs:
            historical_examples = "\n\n".join(
                f"---- Historical source code example ----\n"
                f"{doc.page_content.strip()[:700]}...\n"
                for doc in similar_docs
            )
        else:
            historical_examples = "(no similar historical code found)"

        today = datetime.date.today().strftime("%Y-%m-%d")

        # ── 2. Build prompt ───────────────────────────────────────
        prompt = f"""
You are a senior backend software engineer.

Project date: {today}
Project ID: {project_id}

USER STORIES:
{user_stories[:1200]}

SYSTEM DESIGN:
{system_design[:1200]}

HISTORICAL SOURCE CODE EXAMPLES:
{historical_examples}

Generate clean Python backend code implementing the system.

Requirements:
- modular structure
- service classes
- clear functions
- comments
- realistic backend structure

Return ONLY valid Python code.
"""

        # ── 3. Generate code ─────────────────────────────────────
        response = self.llm.invoke(prompt)

        code_content = response.content.strip()

        # ── 4. Save code file ────────────────────────────────────
        code_dir = f"ai-dev-pod-repository/{project_id}/source_code"
        os.makedirs(code_dir, exist_ok=True)

        filename = f"generated_service_{project_id}.py"
        code_path = os.path.join(code_dir, filename)

        with open(code_path, "w", encoding="utf-8") as f:
            f.write(code_content)

        print(f"DeveloperAgent → saved code: {code_path}")

        return code_content, [code_path]


# ── Debug run ─────────────────────────────────────────
if __name__ == "__main__":

    fake_design = """
Architecture: Microservices
Components:
- Authentication Service
- User Service
- API Gateway
"""

    fake_stories = """
As a user I want to login securely
As a user I want to register
"""

    agent = DeveloperAgent()

    content, paths = agent.generate_code(
        user_stories=fake_stories,
        system_design=fake_design,
        rfp_text="Build a secure authentication system",
        project_id="debug_project"
    )

    print("\nPreview:\n")
    print(content[:300])