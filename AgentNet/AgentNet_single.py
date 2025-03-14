from LazyHeap.LazyHeap import LazyHeap
from Planner.Planner import Planner
from Executor.Executor import Executor

from langchain_openai import ChatOpenAI

class AgentNet_single:
    def __init__(self, llm, tools):

        self.llm = llm

        self.executor = Executor(llm, tools)

    def __call__(self, task):

        ok = self.executor(task)
        return ok



