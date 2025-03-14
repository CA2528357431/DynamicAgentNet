from langchain.agents import Agent

from LazyHeap.LazyHeap import LazyHeap
from Planner.Planner import Planner
from Executor.Executor import Executor

from langchain_openai import ChatOpenAI

class AgentNet_nolazy:
    def __init__(self, llm, executor_num, tools):
        tools_description = {tool.name: tool.description for tool in tools}
        self.planner = Planner(llm, tools_description)
        self.llm = llm

        self.counter = {}
        self.executor_num = executor_num
        self.executors = {}
        self.tools = {tool.name: tool for tool in tools}

    def __call__(self, task):
        sublist = self.planner(task)
        for sub in sublist:
            tools = [self.tools[tool] for tool in sub.tool_list]
            if len(tools) == 0:
                return False
            tools.sort(key=lambda x: x.name)

            key = "|".join([tool.name for tool in tools])
            subtask = sub.subtask
            if key not in self.executors:
                new_executor = Executor(self.llm, tools)
                self.executors[key] = new_executor
            executor = self.executors[key]
            ok = executor(subtask)

            if key not in self.counter:
                self.counter[key] = 0
            self.counter[key] += 1
            keys = [k for k in self.counter]
            keys.sort(key=lambda x: -self.counter[x])
            topk = keys[:self.executor_num]

            self.executors = {k:self.executors[k] for k in topk}

            if not ok:
                return False
        return True



