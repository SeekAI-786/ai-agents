from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool
from langchain_classic import hub
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_classic.agents import create_structured_chat_agent

memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True
)


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash',
    google_api_key = os.getenv('GEMINI_API_KEY'))

llm_2 = ChatOpenAI(
    model = 'gpt-5-mini', temperature=0.7, api_key=os.getenv('OPEN_API_KEY'))


search = DuckDuckGoSearchRun()

@tool
def calculator(expression: str) -> str:
    """
    Evaluates a mathematical expression. Input should be a valid Python math expression.
    """
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

@tool
def read_file(filename: str) -> str:
    """read the contents of a local txt file. Input should be the filename
    """    
    try: 
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return f"File {filename} not found"
    except Exception as e:
        return f"Error {e} reading this file"

tools = [search, calculator, read_file]

# prompt = hub.pull('hwchase17/react')
prompt = hub.pull("hwchase17/structured-chat-agent")

def agent_execution(llm, tools, prompt, query):
    # agent = create_react_agent(llm, tools,prompt, stop_sequence=False)

    # agent_executor = AgentExecutor(
    #     agent=agent,
    #     tools=tools,
    #     verbose=False,
    #     handle_parsing_errors="Output format issue. Retry using strict ReAct format.",
    #     max_iterations=2,
    #     early_stopping_method="generate",
    # )

    # ReAct agents created with create_react_agent expect an "input" key.
    


# Pull conversational prompt (has chat_history variable)
    agent = create_structured_chat_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5)
    
    result = agent_executor.invoke({"input": query})
    print("\n=== FINAL ANSWER ===")
    print(result["output"])
    print("====================\n")
    
    
for i in range(100):
    if input=='c':
        break
    else:
        query = input('Enter your query here (WIRTE "c" to EXIT)\n>:')

        try:
            agent_execution(llm_2, tools, prompt, query)
        except Exception as e:
            print(f'\nOpenAI failed! Using Gemini Free: {e}')
            agent_execution(llm, tools, prompt, query)

