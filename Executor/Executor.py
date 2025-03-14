from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain.tools import Tool, BaseTool
from typing import List

class Executor:
    def __init__(self, llm: ChatOpenAI, tools: List[BaseTool]):
        tool_info = [(tool.name, tool.description) for tool in tools]
        tool_info_str = "\n".join([f"{name}: {desc}" for name, desc in tool_info])
        system_prompt = f"""
You are a professional business analysis Agent designed to assist users with in-depth business analysis and decision-making support. Your goal is to provide clear, accurate, and actionable insights based on the user's requirements. You have access to the following tools to complete analysis tasks:

{tool_info_str}

Based on the user's requirements, select the appropriate tools to conduct business analysis. You can combine multiple tools to perform complex analysis tasks. Follow these steps to ensure a structured and thorough analysis:

1. **Understand the Problem**: Clearly define the business problem or question the user wants to address.
2. **Select Tools**: Choose the most relevant tools based on the problem and the data available.
3. **Analyze Data**: Use the selected tools to analyze the data and generate insights.
4. **Interpret Results**: Provide clear and accurate interpretations of the analysis results, explaining the logic behind your conclusions.
5. **Make Recommendations**: Offer actionable recommendations based on the analysis, ensuring they are aligned with the user's business goals.

Ensure that your analysis results are well-structured, easy to understand, and supported by data. Always aim to provide insights that are not only accurate but also actionable and relevant to the user's specific business context.

Eventually, just judge if you can fulfill the task with provided tools. 
return True/False. 
True means "You CAN address the issue with your tool"
False means "You CAN NOT address the issue with your tool"
"""
        self.agent = create_react_agent(model=llm, tools=[], prompt=system_prompt)

    def __call__(self, request: str):
        response = self.agent.invoke(
            {"messages": f"Here is the task you need to address with your tools: \n\n {request}"})
        final = response["messages"][-1].content
        final = bool(final)
        return final
