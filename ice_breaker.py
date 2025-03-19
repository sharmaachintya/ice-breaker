import os
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import langchain
from dotenv import load_dotenv
from linkedin import scrape_linkedin_profile
from linkedin_lookup_agent import lookup
import getpass

def ice_break_with(name: str) -> str:

    username = lookup(name = name)

    linkedin_data = scrape_linkedin_profile(linkedin_profile_url= username)

    summary_template = """
        given the LinkedIn information {information} about a person from I want you to crate:
        1. A short Summary
        2. Two interesting facts about them
        3. Some interesting points to talk to him about when I meet him

        Don't create any hypothetical profile. Stick to the one provided to you.
    """

    summary_prompt_template = PromptTemplate(input_variables=["information"], template = summary_template)

    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

    # For OpenAI model
    #llm = ChatOpenAI(temperature=8, model_name="gpt-3.5-turbo")

    #For Ollama Llama 3 model
    #llm = ChatOllama(temperature=10, model="llama3")

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash") # Gemini-1.5-Flash

    chain = summary_prompt_template | llm  | StrOutputParser()
    result = chain.invoke(input={"information": linkedin_data})

    print(result)

if __name__ == "__main__":

    load_dotenv()

    name = "Sushant Nanda Informatica"
    print(f"Let's Break ice with: {name}")
    ice_break_with(name="Sushant Nanda Informatica")

    

    

    