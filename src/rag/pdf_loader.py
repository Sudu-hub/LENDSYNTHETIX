from llama_index.readers.file import UnstructuredReader
from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.prompts import PromptTemplate
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from src.core.llm import get_llm
from src.core.state import LoanData

import json
import re


def extract_loan_data_from_pdf(pdf_path: str) -> LoanData:

    # -------------------------
    # Load PDF
    # -------------------------
    loader = UnstructuredReader()
    documents = loader.load_data(file=pdf_path)

    # -------------------------
    # Split text
    # -------------------------
    splitter = SentenceSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    nodes = splitter.get_nodes_from_documents(documents)

    # -------------------------
    # Embeddings
    # -------------------------
    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # -------------------------
    # Vector Index
    # -------------------------
    index = VectorStoreIndex(
        nodes,
        embed_model=embed_model
    )

    retriever = index.as_retriever(similarity_top_k=4)

    # -------------------------
    # LLM
    # -------------------------
    llm = get_llm()

    # -------------------------
    # Prompt
    # -------------------------
    prompt = PromptTemplate(
        """
Extract the following financial fields from the document.

Return ONLY valid JSON.

Fields:
- industry (string)
- revenue_growth (decimal like 0.40 for 40%)
- dscr (number)
- debt_to_equity (number)
- collateral_value (number)
- offshore_deposit (number)

Context:
{context_str}
"""
    )

    # -------------------------
    # Retrieve relevant text
    # -------------------------
    nodes = retriever.retrieve("loan financial metrics")

    context = "\n\n".join([node.text for node in nodes])

    # -------------------------
    # LLM Extraction
    # -------------------------
    response = llm.invoke(
        prompt.format(context_str=context)
    )

    text = response.content

    # -------------------------
    # Extract JSON
    # -------------------------
    json_match = re.search(r"\{.*\}", text, re.DOTALL)

    if json_match:
        data = json.loads(json_match.group())
    else:
        raise ValueError("LLM did not return valid JSON")

    # -------------------------
    # Convert to LoanData
    # -------------------------
    loan_data = LoanData(

        industry=data.get("industry", "Unknown"),

        revenue_growth=float(data.get("revenue_growth", 0.1)),

        dscr=float(data.get("dscr", 1.0)),

        debt_to_equity=float(data.get("debt_to_equity", 1.5)),

        collateral_value=float(data.get("collateral_value", 0)),

        offshore_deposit=float(data.get("offshore_deposit", 0)),

        director_grey_list=False,

        aml_flag=False,
    )

    return loan_data