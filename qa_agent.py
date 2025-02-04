import json
import os
from dotenv import load_dotenv
from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class QA:
    def __init__(self, test_case: str):
        self.test_case = test_case
        self.system_instructions = self._load_system_instructions()
        self.llm = self._initialize_llm()
        self.base_url = os.getenv("BASE_URL")

    def _load_system_instructions(self) -> str:
        try:
            with open("system_instructions.txt", "r") as f:
                return f.read()
        except FileNotFoundError:
            raise RuntimeError("system_instructions.txt not found")

    def _initialize_llm(self) -> ChatGoogleGenerativeAI:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY environment variable")
        return ChatGoogleGenerativeAI(
            model='gemini-2.0-flash-exp',
            api_key=api_key
        )

    async def execute(self) -> dict:
        """Execute the full test workflow and return dict of results"""
        full_task = self._build_task()
        agent = Agent(llm=self.llm, task=full_task)
        raw_result = await agent.run()
        last_result = raw_result.action_results()[-1].extracted_content
        return json.loads(last_result)


    def _build_task(self) -> str:
        """Combine system instructions with the test case"""
        return (
            f"{self.system_instructions}\n"
            f"Test case:\n"
            f"{self.test_case.format(base_url=self.base_url)}"
        )