from LazyHeap.LazyHeap import LazyHeap
from Planner.Planner import Planner
from Executor.Executor import Executor

from langchain_openai import ChatOpenAI

class AgentNet_fixed:
    def __init__(self, llm, tools):

        tools_description = {tool.name: tool.description for tool in tools}
        self.planner = Planner(llm, tools_description)
        self.llm = llm

        self.executors = {}
        for tool in tools:
            self.executors[tool.name] = Executor(self.llm, [tool])

    def __call__(self, task):
        sublist = self.planner(task)
        for sub in sublist:
            if len(sub.tool_list) != 1:
                return False

            key = sub.tool_list[0]
            subtask = sub.subtask
            executor = self.executors[key]
            ok = executor(subtask)
            if not ok:
                return False
        return True



