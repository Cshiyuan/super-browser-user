from browser_use import Agent, ChatOpenAI

agent = Agent(
    task="Search for latest news about AI",
    llm=ChatOpenAI(model="gpt-4.1-mini"),
)

async def main():
    history = await agent.run(
        max_steps=100

    )