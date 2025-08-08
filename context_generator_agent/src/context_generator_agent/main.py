import os
import asyncio
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from agent import ContextModelAgent


# Load environment variables
load_dotenv()


# --- Main Execution Loop ---
async def main():
    print("--- IDQX Context Model Agent ---")
    print("Agent: Hello! I'm ready to begin building the context model. I will ask you inputs when i am stuck")

    # Define paths from environment variables
    # These are now set outside this file for better modularity



    # Initialize the LLM and Agent
    llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4-turbo")
    agent_instance = ContextModelAgent(llm=llm)
    agent = agent_instance.get_agent()

    # Conversation loop
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Agent: Goodbye!")
            break

        # The agent's thinking and response are handled by LlamaIndex's agent.chat()
        response = await agent.achat(user_input)
        print(f"Agent: {response.response}")


if __name__ == "__main__":
    asyncio.run(main())
