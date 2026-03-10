from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool
from langchain_classic import hub
import os
from dotenv import load_dotenv
from langchain_classic.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

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

# prompt = PromptTemplate.from_template("""Answer the following questions as best you can. You have access to the following tools
# {tools}
                                      
# Use the following format:
# Question: the input question you must answer
# Thought:you should always think about what to do
# Action: the action to take, should be one of [{tool_names}]
# Action Input: the input to the action
# Observation: the result of the action 

# ... (this Thought/Action/Action Input/Observation can repeat N times)
# Thought: I now know the final answer
# Final Answer: the final answer to the original input question

# Begin!

# Question: {input}
# Thought:{agent_scratchpad}""")
prompt = hub.pull('hwchase17/react')

def agent_execution(llm, tools, prompt):
    agent = create_react_agent(llm, tools,prompt, stop_sequence=False)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose =True)

    query = input('Enter your query her\n>:')

    # ReAct agents created with create_react_agent expect an "input" key.
    result = agent_executor.invoke({"input": query})
    
    print(result['output'])

try:
    agent_execution(llm_2, tools, prompt)
except Exception:
    print('\nOpenAI failed! Using Gemini Free')
    agent_execution(llm, tools,prompt)

