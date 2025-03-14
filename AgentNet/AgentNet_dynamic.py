from LazyHeap.LazyHeap import LazyHeap
from Planner.Planner import Planner
from Executor.Executor import Executor

from langchain_openai import ChatOpenAI

class AgentNet_dynamic:
    def __init__(self, llm, executor_num, tools):
        tools_description = {tool.name: tool.description for tool in tools}
        self.planner = Planner(llm, tools_description)
        self.llm = llm

        self.counter = LazyHeap(executor_num)
        self.executor_num = executor_num
        self.executors = {}
        self.tools = tools

    def __call__(self, task):
        sublist = self.planner(task)
        for sub in sublist:
            tools = [tool for tool in self.tools if tool.name in sub.tool_list]
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

            to_delete = self.counter.push(key)
            if to_delete:
                self.executors.pop(to_delete)

            if not ok:
                return False
        return True



