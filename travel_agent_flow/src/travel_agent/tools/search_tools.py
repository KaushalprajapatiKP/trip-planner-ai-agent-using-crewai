import json
import requests
import os
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(
        ...,
        description="The search query to perform.",
    )

class SearchTools(BaseTool):
    name: str = "Search Engine"
    description: str = "Useful for performing a search query for given topic on the web and returning the relevant results in JSON format."
    args_schema: type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        try:
            top_results_to_return = 5
            url = "https://google.serper.dev/search"
            payload = {
                "q": query,
                "num": top_results_to_return
            }
            headers = {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
                'X-API-KEY': os.environ['SERPER_API_KEY']
            }
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()  
            if response.status_code != 200:
                return f"Failed to retrieve search results for '{query}'. Status code: {response.status_code}"
            data = response.json()
            if 'organic' not in data or not data['organic']:
                return f"No search results found for '{query}'."
            results = data['organic']
            string = []

            for result in results[:top_results_to_return]:
                try:
                    string.append('\n'.join([
                        f"Title: {result.get('title', 'No title')}",
                        f"Link: {result.get('link', 'No link')}",
                        f"Snippet: {result.get('snippet', 'No snippet')}",
                        f"Source: {result.get('source', 'No source')}",
                        "\n---------------------------------------\n"
                    ]))
                except KeyError:
                    continue
            return "\n".join(string) if string else f"No search results found for '{query}'."
        except Exception as e:
            return f"An error occurred while performing the search: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        raise NotImplementedError("SearchTools does not support async execution yet.")