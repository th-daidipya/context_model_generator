import os
import asyncio
from dotenv import load_dotenv
from context_generator_agent.agent import ContextModelAgent
from context_generator_agent.utils.llm_utils import get_llm

# Load environment variables
load_dotenv()


# --- Main Execution Loop ---
async def main():
    print("--- IDQX Context Model Agent ---")

    # Define paths from environment variables
    # These are now set outside this file for better modularity

    # Initialize the LLM and Agent - now using the factory function
    llm = get_llm()
    agent_instance = ContextModelAgent(llm=llm)
    agent = agent_instance.get_agent()

    print("Agent: Hello! I'm starting the process of building the context model now.")
    print("Agent: Let me break this down into steps:")
    print("Agent: 1. First, I'll get the database schema")
    print("Agent: 2. Then, I'll read all the code files")
    print("Agent: 3. Next, I'll read all the documentation")
    print("Agent: 4. Finally, I'll generate the context model using AI and save it")
    print("Agent: Let's begin...")
    
    initial_task = "Build a context model draft by analyzing the database schema, documentation, and code. After generating the draft, save it to a file using the save_context_model_draft tool."

    print("\n🤖 Agent is working...")
    response = await agent.run(initial_task)
    print("\n✅ Agent completed the task!")
    print(f"Agent: {response}")

    # Also save the response to a backup file in case the agent didn't save it
    try:
        from datetime import datetime
        
        output_dir = os.getenv("DATA_PATH", "./client_data") + "/output"
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(output_dir, f"agent_response_backup_{timestamp}.txt")
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(f"Agent Response at {datetime.now()}:\n\n{response}")
        
        print(f"Backup saved to: {backup_file}")
    except Exception as e:
        print(f"Could not save backup: {e}")

    # Conversation loop
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Agent: Goodbye!")
            break

        # The agent's thinking and response are handled by LlamaIndex's agent.run()
        response = await agent.run(user_input)
        print(f"Agent: {response}")


if __name__ == "__main__":
    asyncio.run(main())
