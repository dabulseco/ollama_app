"""
Prompt Builder for Dynamic System Prompts
Constructs context-aware system prompts based on perspective and audience settings.
"""

from typing import Dict

class PromptBuilder:
    """
    Builds dynamic system prompts tailored to specific perspective and audience combinations.
    Ensures AI responses are appropriately contextualized for the intended communication style.
    """
    
    # Perspective definitions: Who is writing/explaining
    PERSPECTIVES = {
        "Scientist": {
            "description": "Expert researcher with deep technical knowledge",
            "style": "precise, evidence-based, technical terminology when appropriate"
        },
        "High School Teacher": {
            "description": "Experienced educator skilled at explaining complex topics",
            "style": "clear, pedagogical, uses examples and scaffolding"
        },
        "Lay Person": {
            "description": "Knowledgeable individual without specialized training",
            "style": "conversational, relatable, avoids jargon"
        }
    }
    
    # Audience definitions: Who is reading/learning
    AUDIENCES = {
        "Scientist": {
            "description": "Expert with advanced technical background",
            "level": "advanced technical detail, assumes prior knowledge"
        },
        "College Student": {
            "description": "Undergraduate with foundational science knowledge",
            "level": "intermediate detail with clear explanations"
        },
        "High School Student": {
            "description": "Secondary education student building science literacy",
            "level": "accessible language with foundational concepts explained"
        },
        "Middle School Student": {
            "description": "Young learner developing basic science understanding",
            "level": "simple language, concrete examples, age-appropriate content"
        },
        "High School Teacher": {
            "description": "Educator seeking content for teaching or professional development",
            "level": "pedagogically structured with teaching applications"
        },
        "Lay Person": {
            "description": "General public with varied science background",
            "level": "clear, engaging explanations without assuming technical knowledge"
        }
    }
    
    @staticmethod
    def build_system_prompt(perspective: str, audience: str, has_documents: bool = False) -> str:
        """
        Construct a system prompt based on selected perspective and audience.
        
        Args:
            perspective: Who is writing (Scientist, High School Teacher, Lay Person)
            audience: Who is reading (Scientist, College Student, etc.)
            has_documents: Whether documents have been uploaded (for reference only)
            
        Returns:
            Formatted system prompt string for the LLM
        """
        # Get perspective and audience details
        persp_info = PromptBuilder.PERSPECTIVES.get(perspective, PromptBuilder.PERSPECTIVES["Scientist"])
        aud_info = PromptBuilder.AUDIENCES.get(audience, PromptBuilder.AUDIENCES["Lay Person"])
        
        # Build the system prompt
        prompt = f"""You are a {persp_info['description']} communicating with {aud_info['description']}.

Your communication style should be {persp_info['style']}.

Your explanations should be pitched at {aud_info['level']}.

{PromptBuilder._get_specific_guidance(perspective, audience)}

Core principles:
- Provide accurate, evidence-based information
- Never fabricate information if unsure; acknowledge limitations
- Be concise yet thorough
- Use examples and analogies when helpful
- Maintain a helpful and supportive tone
- When document content is provided, respect the specific instructions about how to use it
"""
        
        return prompt.strip()
    
    @staticmethod
    def _get_specific_guidance(perspective: str, audience: str) -> str:
        """
        Provide specific guidance for particular perspective-audience combinations.
        
        Args:
            perspective: Selected perspective
            audience: Selected audience
            
        Returns:
            Additional guidance text
        """
        guidance = []
        
        # Audience-specific guidance
        if audience == "Middle School Student":
            guidance.append("- Use age-appropriate language and avoid complex jargon")
            guidance.append("- Include relatable, everyday examples")
            guidance.append("- Break complex ideas into smaller, digestible parts")
            guidance.append("- Encourage curiosity and critical thinking")
        
        elif audience == "High School Student":
            guidance.append("- Explain technical terms when you introduce them")
            guidance.append("- Connect concepts to real-world applications")
            guidance.append("- Support understanding with clear examples")
            guidance.append("- Build on foundational knowledge appropriately")
        
        elif audience == "College Student":
            guidance.append("- Assume foundational science literacy")
            guidance.append("- Include appropriate technical detail")
            guidance.append("- Reference current research where relevant")
            guidance.append("- Encourage deeper analytical thinking")
        
        elif audience == "Scientist":
            guidance.append("- Use precise technical terminology")
            guidance.append("- Reference relevant literature and methods")
            guidance.append("- Discuss nuances, limitations, and implications")
            guidance.append("- Engage with current debates and developments")
        
        elif audience == "High School Teacher":
            guidance.append("- Consider pedagogical applications")
            guidance.append("- Suggest teaching strategies or activities when relevant")
            guidance.append("- Provide content at appropriate depth for teaching context")
            guidance.append("- Include potential student misconceptions to address")
        
        elif audience == "Lay Person":
            guidance.append("- Avoid unnecessary jargon; define technical terms clearly")
            guidance.append("- Use analogies and everyday examples")
            guidance.append("- Focus on core concepts and practical relevance")
            guidance.append("- Make science accessible and engaging")
        
        # Perspective-specific guidance
        if perspective == "Scientist":
            guidance.append("- Emphasize scientific rigor and evidence")
            guidance.append("- Acknowledge uncertainty and current state of knowledge")
        
        elif perspective == "High School Teacher":
            guidance.append("- Structure information for learning progression")
            guidance.append("- Anticipate common questions and difficulties")
        
        elif perspective == "Lay Person":
            guidance.append("- Relate science to everyday experiences")
            guidance.append("- Communicate enthusiasm for the subject")
        
        # Combine guidance
        if guidance:
            return "Additional guidance:\n" + "\n".join(guidance)
        return ""
    
    @staticmethod
    def get_available_perspectives() -> list:
        """
        Get list of available perspective options.
        
        Returns:
            List of perspective names
        """
        return list(PromptBuilder.PERSPECTIVES.keys())
    
    @staticmethod
    def get_available_audiences() -> list:
        """
        Get list of available audience options.
        
        Returns:
            List of audience names
        """
        return list(PromptBuilder.AUDIENCES.keys())
