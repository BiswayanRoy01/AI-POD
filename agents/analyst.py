from langchain_ollama import ChatOllama
from rag.rag_retriever import RAGRetriever as Storage
import os

class BusinessAnalystAgent:
    def __init__(self):
        self.llm = ChatOllama(model="phi3:mini",
    temperature=0.2,
    num_ctx=4096)
        self.storage = Storage()

    def generate_user_stories(self, rfp_text: str, project_id: str):
        similar = self.storage.similarity_search(rfp_text[:1000], k=5, filter={"artifact_type": "user_stories"})
        context = "\n---\n".join(d.page_content for d in similar)

        prompt = f"""You are a senior Business Analyst.
RFP: {rfp_text}
Historical user stories:
{context}

Generate 8-10 professional user stories with acceptance criteria in markdown."""

        resp = self.llm.invoke(prompt)
        content = resp.content

        os.makedirs(f"ai-dev-pod-repository/{project_id}/user_stories", exist_ok=True)
        path = f"ai-dev-pod-repository/{project_id}/user_stories/user_stories_{project_id}.md"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return content, path