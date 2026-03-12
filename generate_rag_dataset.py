# generate_rag_dataset.py
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from rag.rag_retriever import RAGRetriever
from rag.s3_uploader import S3Uploader

def load_historical_projects():
    documents = []
    base_dir = "ai-dev-pod-repository"

    if not os.path.exists(base_dir):
        print(f"Folder not found: {base_dir}")
        return documents

    for root, _, files in os.walk(base_dir):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                if filename.lower().endswith(('.txt', '.md', '.py')):
                    loader = TextLoader(filepath, encoding="utf-8")
                elif filename.lower().endswith('.pdf'):
                    loader = PyPDFLoader(filepath)
                else:
                    continue

                loaded_docs = loader.load()

                # Add metadata
                relative_path = os.path.relpath(root, base_dir)
                artifact_category = relative_path.split(os.sep)[0] if relative_path != '.' else 'misc'

                for doc in loaded_docs:
                    doc.metadata.update({
                        "artifact_type": artifact_category,
                        "source_file": filename,
                        "project": "historical"
                    })
                    documents.append(doc)

            except Exception as e:
                print(f"Failed to load {filepath}: {e}")

    return documents


if __name__ == "__main__":
    print("=== Indexing historical projects ===")
    
    # Load documents
    raw_docs = load_historical_projects()
    print(f"→ Found {len(raw_docs):,} raw documents")

    if not raw_docs:
        print("No documents found. Check ai-dev-pod-repository/ folder structure.")
        exit(1)

    # Split into chunks
    print("Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    chunks = splitter.split_documents(raw_docs)
    print(f"→ Created {len(chunks):,} chunks")

    # Use RAGRetriever to add to Chroma
    print("Adding to ChromaDB...")
    rag = RAGRetriever()
    rag.vectorstore.add_documents(chunks)   # ← this is the correct way
    print("Chroma indexing complete.")

    # Optional: upload historical projects to S3
    try:
        print("Uploading historical projects to S3...")
        s3 = S3Uploader()
        uploaded_count = 0
        for proj_dir in os.listdir("ai-dev-pod-repository"):
            full_path = os.path.join("ai-dev-pod-repository", proj_dir)
            if os.path.isdir(full_path):
                s3.upload_project(proj_dir)
                uploaded_count += 1
        print(f"→ Uploaded {uploaded_count} historical projects to S3")
    except Exception as e:
        print(f"S3 upload skipped: {e}")

    print("\n=== Done ===\nYou can now run the main app.")