# agents/tester.py
"""
Tester Agent:
- Analyzes user stories and generated code files
- Uses RAG to find similar historical test reports
- Generates a realistic-looking test report (markdown)
- Saves the report in the project repository
"""

import os
import datetime
from typing import List, Tuple

from langchain_ollama import ChatOllama

from rag.rag_retriever import RAGRetriever as Storage


class TesterAgent:
    def __init__(self):
        self.llm = ChatOllama(
            model="llama3.2",
            temperature=0.4,           # slightly more creative for test case variation
            num_ctx=8192,              # helps with longer contexts
            # timeout=120,             # uncomment if you experience timeouts
        )
        self.storage = Storage()

    def generate_test_report(
        self,
        code_file_paths: List[str],
        user_stories_content: str,
        project_id: str
    ) -> Tuple[str, str]:
        """
        Main method called by the workflow.

        Args:
            code_file_paths: list of absolute paths to generated source code files
            user_stories_content: full markdown/text of the user stories
            project_id: current project identifier (used for folder structure)

        Returns:
            (report_content: str, report_filepath: str)
        """

        # ── 1. Gather context from RAG ───────────────────────────────────────
        rag_query = user_stories_content[:900]  # use beginning of stories as query
        similar_docs = self.storage.similarity_search(
            query=rag_query,
            k=5,
            filter={"artifact_type": "test_reports"}
        )

        historical_examples = ""
        if similar_docs:
            historical_examples = "\n\n".join(
                f"──── Historical test report example ────\n"
                f"{doc.page_content.strip()[:700]}...\n"
                for doc in similar_docs
            )
        else:
            historical_examples = "(no similar historical test reports found)"

        # ── 2. Prepare file list summary ─────────────────────────────────────
        if code_file_paths:
            file_summary = "\n".join(
                f"  • {os.path.basename(p)} ({os.path.getsize(p)/1024:.1f} KB)"
                for p in code_file_paths
            )
        else:
            file_summary = "No code files were generated / passed to tester."

        today = datetime.date.today().strftime("%Y-%m-%d")

        # ── 3. Build strong, structured prompt ───────────────────────────────
        prompt = f"""You are a senior QA engineer creating a professional test report.

Project date: {today}
Project ID:   {project_id}

USER STORIES (requirements to be verified):
{user_stories_content[:1400]}

GENERATED CODE FILES:
{file_summary}

HISTORICAL TEST REPORT EXAMPLES (follow similar structure, language & severity):
{historical_examples}

Your task:
Create a complete, realistic **test report** in clean Markdown.

Required sections:

1. Test Summary
   - Total test cases
   - Passed / Failed / Skipped
   - Pass rate
   - Overall status (use emoji)

2. Test Scope & Strategy
   - Types of testing performed (functional, edge cases, negative, ...)
   - Assumptions & limitations

3. Detailed Test Cases (minimum 10–14 cases, more is better)
   Use this table format:

   | ID | Description | Preconditions | Steps | Expected | Actual | Status |
   |----|-------------|---------------|-------|----------|--------|--------|

   - Make realistic test cases based on the stories
   - Include happy path, edge cases, invalid input, security basics, etc.
   - Simulate results → mostly PASS, but include 2–4 realistic FAIL or partial issues

4. Defects / Issues Found
   - Number them
   - Severity (Low/Medium/High/Critical)
   - Description + steps to reproduce
   - Suggested fix (brief)

5. Recommendations & Next Steps

Style guidelines:
- Professional but readable tone
- Use :white_check_mark: :x: :warning: emojis for status
- Use tables where appropriate
- Keep total length reasonable (800–2200 words)

Output **only** the markdown report — no extra explanations or prefixes.
"""

        # ── 4. Generate report ───────────────────────────────────────────────
        response = self.llm.invoke(prompt)
        report_content = response.content.strip()

        # ── 5. Save to disk ──────────────────────────────────────────────────
        report_dir = f"ai-dev-pod-repository/{project_id}/test_reports"
        os.makedirs(report_dir, exist_ok=True)

        filename = f"test_report_{project_id}_{today}.md"
        report_path = os.path.join(report_dir, filename)

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)

        print(f"  TesterAgent → saved report: {report_path}")

        return report_content, report_path


# ── Optional standalone test / debug ────────────────────────────────────────
if __name__ == "__main__":
    # Quick smoke test
    fake_stories = """
    As a user I want to login so that I can access my account
    As a user I want to reset password when forgotten
    """

    fake_code_paths = [
        "/fake/path/project_20250312/main.py",
        "/fake/path/project_20250312/auth.py"
    ]

    agent = TesterAgent()
    content, path = agent.generate_test_report(
        code_file_paths=fake_code_paths,
        user_stories_content=fake_stories,
        project_id="debug_test_20250312"
    )

    print("\nGenerated report preview (first 400 chars):")
    print(content[:400] + "...")
    print(f"\nSaved to: {path}")