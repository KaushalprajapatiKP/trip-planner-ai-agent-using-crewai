import json
import os
import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from unstructured.partition.html import partition_html
from crewai import Agent, Task
from langchain_groq import ChatGroq
from crewai import LLM


class WebsiteInput(BaseModel):
    website: str = Field(
        ...,
        description="The URL of the website to scrape.",
    )

class BrowserTools(BaseTool):
    name: str = "Scrape Website content"
    description: str = "Useful for scraping the content of a website and returning its HTML elements in JSON format."
    args_schema: type[BaseModel] = WebsiteInput

    def _run(self, website: str) -> str:
        try:
            url = f"https://chrome.browserless.io/content?token={os.environ['BROWSERLESS_API_KEY']}"
            payload = json.dumps({"url": website})
            headers = {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache'
            }
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()  

            if response.status_code != 200:
                return f"Failed to retrieve content from {website}. Status code: {response.status_code}"
            
            elements = partition_html(text = response.text)
            content = "\n\n".join([str(element) for element in elements ])
            content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
            summeries = []

            llm = LLM(model=ChatGroq(model_name="groq/llama-3.1-70b-instruct"))
            for chunk in content:
                agent = Agent(
                    role= "Principal Researcher",
                    llm=llm,
                    goal = "Do amazing researches and summaries based on the content you are working with. Make sure to provide a detailed summary of the content.",
                    backstory = "You are a highly skilled expert researcher with expertise in summarizing and analyzing web content. Your task is to provide detailed summaries of the content you are working with.",
                    allow_delegation=True,
                )

                task = Task(
                    name="Analyse and Summarize the content",
                    description=f'Analyze and summarize the content below, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}',
                    agent=agent
                )

                summeary = task.execute()
                summeries.append(summeary)
            return "\n\n".join(summeries)
        except requests.RequestException as e:
            return f"An error occurred while trying to scrape the website: {str(e)}"
        
        def _arun(self, website: str) -> str:
            """Asynchronous run method."""
            raise NotImplementedError("This tool does not support asynchronous execution.")
         