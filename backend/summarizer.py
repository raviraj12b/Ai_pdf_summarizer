"""
AI Summarizer Module
File: backend/summarizer.py
Description: AI-powered text summarization using various strategies
"""


class AISummarizer:
    """AI-powered text summarization using LLMs"""
    
    def __init__(self, ollama_client):
        """
        Initialize AI Summarizer
        
        Args:
            ollama_client: Instance of OllamaClient
        """
        self.ollama = ollama_client
    
    def summarize_extractive(self, text, model, length="medium"):
        """
        Extractive summarization - AI selects key sentences
        
        Args:
            text (str): Input text to summarize
            model (str): Model name to use
            length (str): Summary length (short/medium/long)
            
        Returns:
            str: Extractive summary
        """
        length_map = {
            "short": "3-4 key sentences",
            "medium": "5-7 key sentences",
            "long": "8-12 key sentences"
        }
        
        prompt = f"""You are an expert at extractive text summarization. Your task is to create a summary by selecting and combining the most important sentences from the original text.

TEXT TO SUMMARIZE:
{text[:8000]}

INSTRUCTIONS:
Select {length_map[length]} from the original text that capture the main ideas and essential information.

RULES:
1. Use ONLY sentences or phrases from the original text
2. Do NOT create new sentences or paraphrase
3. Select sentences that contain the most important information
4. Maintain the original order when possible
5. Ensure the summary flows naturally
6. Focus on key facts, findings, and conclusions

EXTRACTIVE SUMMARY:"""
        
        return self.ollama.generate(model, prompt)
    
    def summarize_abstractive(self, text, model, length="medium"):
        """
        Abstractive summarization - AI generates new summary
        
        Args:
            text (str): Input text to summarize
            model (str): Model name to use
            length (str): Summary length (short/medium/long)
            
        Returns:
            str: Abstractive summary
        """
        length_map = {
            "short": "3-4 sentences",
            "medium": "5-7 sentences",
            "long": "8-12 sentences"
        }
        
        prompt = f"""You are an expert at abstractive text summarization. Your task is to read and understand the text, then create a new summary in your own words.

TEXT TO SUMMARIZE:
{text[:8000]}

INSTRUCTIONS:
Write a {length_map[length]} summary in your own words.

RULES:
1. Read and understand the entire text
2. Identify the main ideas, key points, and important details
3. Write a NEW summary in your own words (do not copy sentences)
4. Ensure the summary is coherent and flows naturally
5. Preserve the meaning and critical information
6. Use clear, concise language
7. Focus on what matters most

ABSTRACTIVE SUMMARY:"""
        
        return self.ollama.generate(model, prompt)
    
    def summarize_bullet_points(self, text, model):
        """
        Create bullet-point summary
        
        Args:
            text (str): Input text to summarize
            model (str): Model name to use
            
        Returns:
            str: Bullet-point summary
        """
        prompt = f"""You are an expert at creating concise bullet-point summaries. Extract the key points from the following text.

TEXT TO SUMMARIZE:
{text[:8000]}

INSTRUCTIONS:
1. Create 5-10 bullet points
2. Each point should be one clear, complete sentence
3. Focus on the most important information
4. Use parallel structure
5. Start each bullet with an action verb or key concept

BULLET-POINT SUMMARY:"""
        
        return self.ollama.generate(model, prompt)
    
    def summarize_with_questions(self, text, model):
        """
        Question-based analytical summary
        
        Args:
            text (str): Input text to summarize
            model (str): Model name to use
            
        Returns:
            str: Question-based summary
        """
        prompt = f"""Analyze the following text and create a summary by answering these key questions:

TEXT:
{text[:8000]}

Create a summary that answers:
1. What is the main topic or thesis?
2. What are the key arguments or findings?
3. What evidence or examples are provided?
4. What are the conclusions or implications?
5. What are the limitations or future directions (if mentioned)?

Provide a cohesive summary addressing these questions:"""
        
        return self.ollama.generate(model, prompt)
    
    def get_key_insights(self, text, model):
        """
        Extract key insights and takeaways
        
        Args:
            text (str): Input text to summarize
            model (str): Model name to use
            
        Returns:
            str: Key insights summary
        """
        prompt = f"""You are an expert analyst. Read the following text and extract the most important insights and takeaways.

TEXT:
{text[:8000]}

Provide:
1. TOP 3-5 KEY INSIGHTS (numbered)
2. MAIN TAKEAWAYS (what should readers remember?)
3. PRACTICAL IMPLICATIONS (if applicable)

Format your response clearly with headers:"""
        
        return self.ollama.generate(model, prompt)
    
    def custom_summarize(self, text, model, custom_prompt):
        """
        Custom summarization with user-provided prompt
        
        Args:
            text (str): Input text to summarize
            model (str): Model name to use
            custom_prompt (str): Custom instructions
            
        Returns:
            str: Custom summary
        """
        full_prompt = f"""TEXT TO SUMMARIZE:
{text[:8000]}

INSTRUCTIONS:
{custom_prompt}

SUMMARY:"""
        
        return self.ollama.generate(model, full_prompt)
