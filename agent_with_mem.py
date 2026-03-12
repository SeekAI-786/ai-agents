from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import create_react_agent, AgentExecutor

memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True
)

from langchain.agents import create_structured_chat_agent
from langchain import hub

# Pull conversational prompt (has chat_history variable)
prompt = hub.pull("hwchase17/structured-chat-agent")

agent = create_structured_chat_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)

agent_executor.invoke({"input": "My name is Ali and I work at a company with 47 employees"})
agent_executor.invoke({"input": "What is my name?"})
agent_executor.invoke({"input": "How many employees does my company have? Search the web for the average company size in Pakistan's tech sector and compare."})