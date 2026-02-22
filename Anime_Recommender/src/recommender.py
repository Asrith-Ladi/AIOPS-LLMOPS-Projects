# from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from src.prompt_template import get_anime_prompt

class AnimeRecommender:
    def __init__(self, retriever, api_key: str, model_name: str):
        # Temperature 0 = deterministic (always same answer)
        # Temperature 0.7-0.9 = creative (different answers, may hallucinate)
        self.llm = ChatGroq(model=model_name, api_key=api_key, temperature=0)
        self.prompt = get_anime_prompt()
        self.retriever = retriever
        
        # Create LLM chain with our prompt template
        self.chain = self.llm | self.prompt
    
    def get_recommendations(self, query: str):
        """
        Get anime recommendations based on user query.
        
        Args:
            query: User's question or preference description
                    Example: "I like action anime with deep plots"
            
        Returns:
            str: Recommendation text with 3 anime suggestions
        """
        # Step 1: Retrieve similar anime from vector database
        retrieved_docs = self.retriever.invoke(query)
        
        # Step 2: Format retrieved documents into context string
        context = "\n".join([doc.page_content for doc in retrieved_docs])
        
        # Step 3: Create the full prompt with context and question
        prompt_input = self.prompt.format(context=context, question=query)
        
        # Step 4: Get LLM response
        result = self.llm.invoke(prompt_input)
        
        return result.content