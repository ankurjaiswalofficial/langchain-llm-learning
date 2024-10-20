from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain import hub
import os
from dotenv import load_dotenv

from tools.tools import get_profile_url_tavily

load_dotenv()


def lookup(name: str) -> str:
    llm = ChatGoogleGenerativeAI(
        temperature=0,
        model="gemini-1.5-flash"
    )

    template = """given the full name {name_of_person} I want you to get it me a link to their linkedin profile page. Your answer should contain only a URL."""

    prompt_template = PromptTemplate(
        template=template,
        input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need to get the Linkedin Profile URL"
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt
    )
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools_for_agent,
        verbose=True
    )

    result = agent_executor.invoke(
        input={
            "input": prompt_template.format_prompt(name_of_person=name)
        }
    )

    linkedin_profile_url = result["output"]
    return linkedin_profile_url


if __name__ == "__main__":
    linkedin_url = lookup(name="ankurjaiswalofficial Linkedin")
    print(linkedin_url)
