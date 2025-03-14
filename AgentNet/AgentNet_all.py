from LazyHeap.LazyHeap import LazyHeap
from Planner.Planner import Planner
from Executor.Executor import Executor

from langchain_openai import ChatOpenAI

class AgentNet_all:
    def __init__(self, llm, tools):

        tools.sort(key=lambda x: x.name)
        tools_description = {tool.name: tool.description for tool in tools}
        self.planner = Planner(llm, tools_description)
        self.llm = llm

        self.executors = {}
        for i in range(1, 2**len(tools)):
            tool_list = []
            for j in range(len(tools)):
                if (1<<j)&i:
                    tool_list.append(tools[j])
            key = "|".join([tool.name for tool in tool_list])
            new_executor = Executor(self.llm, tool_list)
            self.executors[key] = new_executor

    def __call__(self, task):
        sublist = self.planner(task)
        for sub in sublist:
            if len(sub.tool_list) == 0:
                return False
            sub.tool_list.sort()
            subtask = sub.subtask
            key = "|".join(sub.tool_list)
            executor = self.executors[key]
            ok = executor(subtask)
            if not ok:
                return False
        return True



