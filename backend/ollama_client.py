"""
Ollama Client Module
File: backend/ollama_client.py
Description: Handles all Ollama API communication
"""

import requests
import streamlit as st


class OllamaClient:
    """Client for Ollama API communication"""
    
    def __init__(self, base_url="http://localhost:11434"):
        """
        Initialize Ollama client
        
        Args:
            base_url (str): Base URL for Ollama server
        """
        self.base_url = base_url
        self.generate_url = f"{base_url}/api/generate"
        self.chat_url = f"{base_url}/api/chat"
        self.models_url = f"{base_url}/api/tags"
    
    def check_connection(self):
        """
        Check if Ollama server is running
        
        Returns:
            bool: True if connected, False otherwise
        """
        try:
            response = requests.get(self.models_url, timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def list_models(self):
        """
        Get list of available models
        
        Returns:
            list: List of model names
        """
        try:
            response = requests.get(self.models_url, timeout=5)
            if response.status_code == 200:
                models_data = response.json()
                return [model['name'] for model in models_data.get('models', [])]
            return []
        except Exception:
            return []
    
    def generate(self, model, prompt, stream=False):
        """
        Generate text using Ollama model
        
        Args:
            model (str): Model name to use
            prompt (str): Input prompt
            stream (bool): Whether to stream response
            
        Returns:
            str: Generated text or None if failed
        """
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": stream
            }
            
            response = requests.post(
                self.generate_url,
                json=payload,
                timeout=300  # 5 minutes timeout
            )
            
            if response.status_code == 200:
                if stream:
                    return response
                else:
                    return response.json()['response']
            else:
                st.error(f"Ollama API returned status code: {response.status_code}")
                return None
                
        except requests.Timeout:
            st.error("Request timed out. Try a shorter document or different model.")
            return None
        except requests.ConnectionError:
            st.error("Cannot connect to Ollama. Ensure it's running: ollama serve")
            return None
        except Exception as e:
            st.error(f"Generation error: {str(e)}")
            return None
    
    def chat(self, model, messages, stream=False):
        """
        Chat completion using Ollama
        
        Args:
            model (str): Model name
            messages (list): List of message dictionaries
            stream (bool): Whether to stream response
            
        Returns:
            str: Response text or None if failed
        """
        try:
            payload = {
                "model": model,
                "messages": messages,
                "stream": stream
            }
            
            response = requests.post(
                self.chat_url,
                json=payload,
                timeout=300
            )
            
            if response.status_code == 200:
                if stream:
                    return response
                else:
                    return response.json()['message']['content']
            return None
            
        except Exception as e:
            st.error(f"Chat error: {str(e)}")
            return None
    
    def get_model_info(self, model_name):
        """
        Get information about a specific model
        
        Args:
            model_name (str): Name of the model
            
        Returns:
            dict: Model information or None
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/show",
                json={"name": model_name},
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception:
            return None
