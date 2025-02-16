from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import ast

def search_words(segments):
    words = []
    for segment in segments['segments']:
        for word_info in segment['words']:
            words.append(word_info['word'])

    model = ChatGroq(temperature = 0.3, model_name = "llama-3.1-8b-instant")
    prompt = """
        You are expert at picking up subjects/verbs/objects from the given list of text.
        You will be given a list of text and you will output words which are subjects/verbs/objects single word from the list.
        Examples:
        Given: ['There', 'was', 'once', 'a', 'man', 'roaming', 'around', 'the', 'streets']
        Output: ['man', 'streets']

        Given: ['my', 'friends', 'went', 'to', 'the', 'beach']
        Output: ['friends', 'beach']

        Given: ['I', 'really', 'like', 'programming']
        Output: ['programming']

        Given: ['Michael', 'Jackson', 'is', 'the', 'best', 'music', 'artist', 'ever']
        Output: ['music', 'artist']

        Note: Do not pick a lot of words, and only pick according to the subject/verb/object, and also no names should be picked. You can only pick max upto 7 words.

        Output must be only the list of words, no other text is allowed, and no code identifiers such as upper back tick -> ` should be used in output, only the list of words which will be in strings is allowed or else you will get penalty.

        Here is the given list of words:
        {words}
    """
    prompt_template = PromptTemplate(
        template = prompt,
        input_variables = ["words"],
    )
    chain = prompt_template | model 
    response = chain.invoke({ "words": words })
    return ast.literal_eval(response.content)