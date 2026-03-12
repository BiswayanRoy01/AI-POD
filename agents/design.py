from langchain_ollama import ChatOllama
from rag.rag_retriever import RAGRetriever as Storage
import os

class DesignAgent:
    def __init__(self):
        self.llm = ChatOllama(model="llama3.2", temperature=0.2)
        self.storage = Storage()

    def generate_design(self, stories: str, rfp_text: str, project_id: str):
        similar = self.storage.similarity_search(stories[:500] + rfp_text[:500], k=5, filter={"artifact_type": "designs"})
        context = "\n---\n".join(d.page_content for d in similar)

        prompt = f"""You are the System Design Agent.
RFP + Stories: {rfp_text[:600]} + {stories[:600]}
Historical designs:
{context}

Create complete system design in professional markdown."""

        resp = self.llm.invoke(prompt)
        content = resp.content

        os.makedirs(f"ai-dev-pod-repository/{project_id}/designs", exist_ok=True)
        path = f"ai-dev-pod-repository/{project_id}/designs/design_{project_id}.md"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return content, path