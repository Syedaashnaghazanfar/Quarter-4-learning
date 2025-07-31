from agents import Agent, FileSearchTool, Runner, WebSearchTool, OpenAIChatCompletionsModel, AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

# Step 1: Set up OpenAI client

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 2: Create the agent with hosted tools you will need paid api key for this

agent = Agent(
    name="Assistant",
    tools=[
        WebSearchTool(),
        #you can also use file search tool if you have files to search, image generation tool to generate images and many more!
    ],
   
)

# Step 3: Run the agent

async def main():
    try:
        result = await Runner.run(agent, "Which coffee shop should I go to? something aesthetic in karachi")
        print(result.final_output)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())


# Hosted tools are provided by OpenAI and you need to have a paid API key to use them. They are build in tools that can be used with the agent to perform tasks like web search, file search, and more.
# Make sure to set the OPENAI_API_KEY environment variable with your OpenAI API key.
# You can also use other tools like FileSearchTool, ImageGenerationTool, etc. as needed.
# The agent will use the tools to perform the task and return the result.

# Output:

# If you're seeking an aesthetic coffee shop experience in Karachi, here are some notable options:

# **[Ideas Cafe](https://ideascafe.com/?utm_source=openai)**
# **Open now · Rs 1,500–2,000 · 4.7 (50 reviews)**
# _Dolmen Mall, Block 4 Clifton, Karachi, 75600, Pakistan_
# Located in Dolmen Mall Clifton, Ideas Café offers a calm, photogenic space with natural textures and wooden tones. Their signature drinks include Spanish Latte and Caramel Frappe, complemented by dishes like Truffle Pizza and Fettuccine Alfredo.

# **Sync Cafe**
# **Closed · Rs 500–1,000 · 3.9 (424 reviews)**
# _27c shop, 1 Lane 13, D.H.A Phase 6 Bukhari Commercial Area Phase 6 Defence Housing Authority, Karachi, 75500, Pakistan_
# Situated in DHA Phase 6, Sync Café boasts clean, polished interiors with warm lighting, creating an inviting atmosphere. Their menu features unique beverages such as Brown Cinnamon Iced Latte and Tiramisu Iced Latte.

# **[Koel](http://koel.com.pk?utm_source=openai)**
# **Open now · Restaurant · 3.9 (82 reviews)**
# _F-42/2, 26th St, Block 4 Scheme 5, Clifton (Tauheed Commercial Area), کراچی-76500_
# Known for its minimalist yet elegant design, Koel Café offers an open courtyard adorned with contemporary art. The menu blends local and international cuisine, providing a sophisticated dining experience.

# Each of these cafés offers a unique ambiance and menu, catering to various aesthetic preferences. Whether you're looking for a cozy corner to read, a chic spot for brunch, or a serene environment surrounded by greenery, Karachi's café scene has something to offer.