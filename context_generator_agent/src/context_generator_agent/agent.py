import json
import os
import sqlite3

from dotenv import load_dotenv
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI

# Load environment variables
load_dotenv()


# --- Agent Tools ---
def get_documentation_path() -> str:
    return os.getenv("DATA_PATH", "./client_data") + "/" + os.getenv("DOCS_FILE", "business_rules.txt")


def get_db_schema_ddl() -> str:
    """
    Connects to a SQLite DB and extracts the DDL for all tables.
    Useful for understanding the technical structure of the database.
    """
    db_path = str(os.getenv("DATA_PATH", "./client_data") + "/" + os.getenv("DB_FILE", "bakery.sqlite"))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
    schema_info = {name: ddl for name, ddl in cursor.fetchall()}
    conn.close()
    return json.dumps(schema_info, indent=2)


def read_file_content(file_path: str) -> str:
    """
    Reads the entire content of a file.
    Useful for reading documentation or code files.
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
    with open(file_path, 'r') as f:
        return f.read()


def list_files_in_directory(dir_path: str) -> str:
    """
    Lists all files in a directory and its subdirectories.
    Useful for exploring the client's codebase or documentation folders.
    """
    if not os.path.exists(dir_path):
        return f"Error: Directory not found at {dir_path}"
    files = [os.path.join(dp, f) for dp, _, filenames in os.walk(dir_path) for f in filenames]
    return json.dumps(files, indent=2)


def generate_context_model_draft(db_schema: str, docs_content: str) -> str:
    """
    Synthesizes a draft of the context model based on raw schema and docs.
    This simulates the agent's initial synthesis step.
    """
    prompt = f"""
    You are a data architect. Based on the following database schema and documentation,
    generate a draft of a context model in JSON format. The model should include:
    - Main business entities and their properties.
    - Key relationships between these entities.
    - Any explicit business rules mentioned.

    Database Schema:
    {db_schema}

    Documentation:
    {docs_content}

    Output must be a valid JSON object.
    """
    # This is a mock function, in a real agent, this would be an LLM call.
    return json.dumps({
        "entities": [
            {"name": "Product", "properties": ["product_id", "product_name"]},
            {"name": "Customer", "properties": ["customer_id", "first_name", "last_name"]},
            {"name": "Order", "properties": ["order_id", "quantity"]}
        ],
        "relationships": [
            {"source": "Customer", "target": "Order", "type": "places"},
            {"source": "Order", "target": "Product", "type": "contains"}
        ],
        "business_rules": [
            {"name": "Valid Email Format", "rule": "customer.email_address must be valid"},
            {"name": "Positive Order Quantity", "rule": "order.quantity > 0"}
        ]
    })


# --- Agent Definition ---


class ContextModelAgent:
    def __init__(self, llm: OpenAI):
        self.llm = llm

        # Define the tools available to the agent
        tools = [
            FunctionTool.from_defaults(fn=get_db_schema_ddl),
            FunctionTool.from_defaults(fn=read_file_content),
            FunctionTool.from_defaults(fn=list_files_in_directory),
            FunctionTool.from_defaults(fn=generate_context_model_draft),
        ]

        # System prompt to define the agent's personality and goals
        system_prompt = (
            "You are a curious senior domain expert and data architect. "
            "Your goal is to build a comprehensive context model for a client's ecosystem. "
            "You have access to a set of tools to explore their database, documentation, and codebase. "
            "When asked to build the context model, you must follow a methodical approach: "
            "1. First, you should explore the available files and database schemas using your tools. "
            "2. Next, read the relevant content from the files. "
            "3. Then, use the 'generate_context_model_draft' tool to synthesize a preliminary model. "
            "4. You must show your thought process and be ready to ask for clarification if you get stuck or find inconsistencies. "
            "5. After synthesizing, you should present the draft model and ask the user for verification or clarification before finalizing it."
        )

        # Initialize the agent with the defined tools and system prompt
        self.agent = ReActAgent.from_tools(
            tools=tools,
            llm=llm,
            verbose=True,  # This makes the agent "think" out loud
            system_prompt=system_prompt,
        )

    def get_agent(self):
        return self.agent
