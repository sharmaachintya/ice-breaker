from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
import getpass
from langchain import hub
from linkedin_tool import get_profile_url

load_dotenv()


def lookup(name: str) -> str:

    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

    llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-1.5-flash")

    template = """
        given the full name of the person {full_name} I want you to get me their LinkedIn profile page. Your answer should contain only their LinkedIn profile's URL.
    """

    prompt_template = PromptTemplate(input_variables=["full_name"], template = template)

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url, # Tools -> tools.py
            description="useful for when you need to get the Linkedin Page URL",
        )
    ]

    react_propmt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_propmt)

    agent_executor = AgentExecutor(agent = agent, tools = tools_for_agent, verbose = True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(full_name = name)}
    )

    linkedin_url = result["output"]
    return linkedin_url

if __name__ == "__main__":
    result_url = lookup("Joe Tsang Informatica")
    print(result_url)
