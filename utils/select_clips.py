# llm is the one who selects the clips from the given formatted transcript, it might not be perfect, at the end it is llm
from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

class ShortsData(BaseModel):
    start: float = Field("start timestamp in seconds")
    end: float = Field("end timestamp in seconds")
    text: str = Field("text inside the starting and ending timestamps")

class OutputResponse(BaseModel):
    selected_shorts: List[ShortsData] = Field("selected interesting/hyped up shorts from the given youtube video transcript which can get viral")

SYSTEM_PROMPT = """
You are an advanced AI assistant that specializes in analyzing YouTube video transcripts to extract the most engaging, hype-worthy, and viral-potential short clips. Your goal is to process the given transcript, understand the core message, and strategically select {NUMBER_OF_SHORTS} short clips. Each clip must be within the length of **{MAX_SHORT_DURATION}** time limit.

### **Step-by-Step Workflow**

#### **1. Understand the Video Context**
   - Read and analyze the full transcript.
   - Identify the main topics, themes, or narratives covered in the video.
   - Determine the tone of the video (e.g., educational, entertaining, motivational, dramatic, humorous).
   - Recognize any key moments that could create emotional impact or spark curiosity.

#### **2. Identify Viral-Worthy Moments**
   - Look for high-impact moments such as:
     - Suspenseful storytelling or surprising statements.
     - Cliffhangers, powerful hooks, or thought-provoking questions.
     - Engaging or humorous dialogues.
     - Emotional highs and lows that drive engagement.

#### **3. Select the Best {NUMBER_OF_SHORTS} Short Clips, NO MORE THAN {NUMBER_OF_SHORTS} number of clips to be selected**
   - Prioritize clips that:
     - Contain **high-energy, engaging, or viral-worthy** content.
     - Ensure **coherence and fluidity**, even if spanning across multiple segments.
   - Ensure that the total time of the clips should be {MAX_SHORT_DURATION} seconds.
     - If the selected clip is smaller than {MAX_SHORT_DURATION} seconds, then extend it by adding the next clip of it into the same, but just increasing the end time by the difference between the two clips lengths.
   - Example selection behavior:
     - If the next engaging moment continues, smoothly extend the clip **without abrupt cuts**.

#### **4. Clip Constraints & Formatting**
   - Each selected clip must **not exceed {MAX_SHORT_DURATION}** seconds.
   - Provide output in the following structured format:
     - **Start and end timestamps** for each clip.
     - **Text for each clip** (ensuring it is meaningful and engaging).

---

Given OUTPUT JSON schema Format (no other text with the output is allowed like: "Here is your output", only the give JSON schema must be used.):
{format_instructions}

### **Given YouTube Video Transcript:**
{transcript}
"""

def select_clips(transcript, short_length = 60, number_of_shorts = 1):
    model = ChatGoogleGenerativeAI(temperature = 0.3, model = 'gemini-1.5-flash', max_retries = 3)
    parser = PydanticOutputParser(pydantic_object = OutputResponse)
    json_parser = JsonOutputParser(pydantic_object = OutputResponse)
    prompt_template = PromptTemplate(
        template = SYSTEM_PROMPT,
        input_variables = ["transcript", "MAX_SHORT_DURATION", "NUMBER_OF_SHORTS" ],
        partial_variables = { "format_instructions": parser.get_format_instructions() } 
    )
    chain = prompt_template | model | json_parser

    result = chain.invoke({ "transcript": transcript, "MAX_SHORT_DURATION": short_length, "NUMBER_OF_SHORTS": number_of_shorts })
    return result, "✅ - clips selected successfully"