from dotenv import load_dotenv
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.core.llms import LLM

from context_generator_agent.tools import get_db_schema_ddl, read_codebase, read_documentation, \
    generate_context_model_draft, save_context_model_draft
from context_generator_agent.utils.llm_utils import get_llm

# Load environment variables
load_dotenv()


# --- Agent Definition ---


class ContextModelAgent:
    def __init__(self, llm: LLM = None):
        self.llm = llm if llm is not None else get_llm()

        # Define the tools available to the agent
        tools = [
            FunctionTool.from_defaults(fn=get_db_schema_ddl),
            FunctionTool.from_defaults(fn=read_codebase),
            FunctionTool.from_defaults(fn=read_documentation),
            FunctionTool.from_defaults(fn=generate_context_model_draft),
            FunctionTool.from_defaults(fn=save_context_model_draft),
        ]

        # System prompt to define the agent's personality and goals
        system_prompt = (
            "You are a curious senior domain expert and data architect. "
            "Your goal is to build a comprehensive context model for a client's ecosystem. "
            "You have access to a set of tools to explore their database, documentation, and codebase. "
            "When asked to build the context model, you must follow a methodical approach: "
            "1. First, explore the database schema using 'get_db_schema_ddl'. "
            "2. Use 'read_codebase' to get all Python files and 'read_documentation' to get all text files. "
            "3. Then, use the 'generate_context_model_draft' tool with the collected data: "
            "   - Pass the database schema as the first parameter (db_schema) "
            "   - Pass the documentation content as the second parameter (docs_content) "
            "   - Pass the codebase content as the third parameter (codebase_content) "
            "   This tool will call an LLM to generate a structured context model in JSON format. "
            "4. You must show your thought process and be ready to ask for clarification if you get stuck or find inconsistencies. "
            "5. After synthesizing, you should present the draft model and ask the user for verification or clarification before finalizing it. "
            "6. Once the draft is approved or finalized, use 'save_context_model_draft' to save the final model to a file."
        )

        # Initialize the agent with the defined tools and system prompt
        self.agent = ReActAgent(
            tools=tools,
            llm=llm,
            verbose=False,  # Turn off internal verbose to avoid workflow noise
            system_prompt=system_prompt,
        )

    def get_agent(self):
        return self.agent
