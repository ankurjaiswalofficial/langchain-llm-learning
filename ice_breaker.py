from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent


def ice_break_with(name: str) -> str:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)

    summary_template = """
    given the linkedin {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
    )
    chain = summary_prompt_template | llm | StrOutputParser()
    print(linkedin_data)
    res = chain.invoke({"information": linkedin_data})
    print(res)
    return ""


if __name__ == "__main__":
    load_dotenv()
    print("Init")
    ice_break_with(name="ankurjaiswalofficial Linkedin")
