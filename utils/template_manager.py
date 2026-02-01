"""
Template Manager for Question Templates
Handles loading, saving, adding, and deleting question templates from JSON storage.
"""

import json
import os
from typing import List, Dict, Optional
from pathlib import Path

class TemplateManager:
    """
    Manages question templates stored in JSON format.
    Provides CRUD operations and template retrieval functionality.
    """
    
    def __init__(self, templates_file: str = "config/question_templates.json",
                 default_templates_file: str = "config/default_templates.json"):
        """
        Initialize the template manager.
        
        Args:
            templates_file: Path to user's custom templates JSON file
            default_templates_file: Path to default templates JSON file
        """
        self.templates_file = templates_file
        self.default_templates_file = default_templates_file
        
        # Ensure config directory exists
        os.makedirs(os.path.dirname(templates_file), exist_ok=True)
        
        # Load or initialize templates
        self._initialize_templates()
    
    def _initialize_templates(self):
        """
        Initialize templates from file or create from defaults.
        If user templates file doesn't exist, copy from defaults.
        """
        if not os.path.exists(self.templates_file):
            # Copy default templates to user templates file
            if os.path.exists(self.default_templates_file):
                with open(self.default_templates_file, 'r', encoding='utf-8') as f:
                    default_data = json.load(f)
                with open(self.templates_file, 'w', encoding='utf-8') as f:
                    json.dump(default_data, f, indent=2, ensure_ascii=False)
            else:
                # Create empty templates file
                with open(self.templates_file, 'w', encoding='utf-8') as f:
                    json.dump({"templates": []}, f, indent=2)
    
    def load_templates(self) -> List[Dict]:
        """
        Load all templates from the JSON file.
        
        Returns:
            List of template dictionaries
        """
        try:
            with open(self.templates_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("templates", [])
        except Exception as e:
            print(f"Error loading templates: {e}")
            return []
    
    def save_templates(self, templates: List[Dict]) -> bool:
        """
        Save templates to the JSON file.
        
        Args:
            templates: List of template dictionaries to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump({"templates": templates}, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving templates: {e}")
            return False
    
    def add_template(self, name: str, template: str, category: str = "Custom",
                     requires_input: bool = True, input_label: str = "",
                     description: str = "") -> bool:
        """
        Add a new template to the collection.
        
        Args:
            name: Display name for the template
            template: The actual template text/question
            category: Category for organization (default: "Custom")
            requires_input: Whether template needs user input
            input_label: Label for input field if requires_input is True
            description: Brief description of what the template does
            
        Returns:
            True if successful, False otherwise
        """
        templates = self.load_templates()
        
        # Generate unique ID based on name
        template_id = name.lower().replace(" ", "_").replace("-", "_")
        
        # Ensure ID is unique
        existing_ids = [t.get("id") for t in templates]
        counter = 1
        original_id = template_id
        while template_id in existing_ids:
            template_id = f"{original_id}_{counter}"
            counter += 1
        
        new_template = {
            "id": template_id,
            "name": name,
            "template": template,
            "category": category,
            "requires_input": requires_input,
            "input_label": input_label or f"Enter content for {name}:",
            "description": description
        }
        
        templates.append(new_template)
        return self.save_templates(templates)
    
    def delete_template(self, template_id: str) -> bool:
        """
        Delete a template by its ID.
        
        Args:
            template_id: The ID of the template to delete
            
        Returns:
            True if successful, False otherwise
        """
        templates = self.load_templates()
        original_count = len(templates)
        
        # Filter out the template to delete
        templates = [t for t in templates if t.get("id") != template_id]
        
        if len(templates) < original_count:
            return self.save_templates(templates)
        else:
            return False  # Template not found
    
    def get_template_by_id(self, template_id: str) -> Optional[Dict]:
        """
        Retrieve a specific template by its ID.
        
        Args:
            template_id: The ID of the template to retrieve
            
        Returns:
            Template dictionary if found, None otherwise
        """
        templates = self.load_templates()
        for template in templates:
            if template.get("id") == template_id:
                return template
        return None
    
    def get_template_by_name(self, name: str) -> Optional[Dict]:
        """
        Retrieve a specific template by its name.
        
        Args:
            name: The name of the template to retrieve
            
        Returns:
            Template dictionary if found, None otherwise
        """
        templates = self.load_templates()
        for template in templates:
            if template.get("name") == name:
                return template
        return None
    
    def get_templates_by_category(self, category: str) -> List[Dict]:
        """
        Retrieve all templates in a specific category.
        
        Args:
            category: The category to filter by
            
        Returns:
            List of template dictionaries in that category
        """
        templates = self.load_templates()
        return [t for t in templates if t.get("category") == category]
    
    def get_all_categories(self) -> List[str]:
        """
        Get list of all unique categories.
        
        Returns:
            Sorted list of category names
        """
        templates = self.load_templates()
        categories = set(t.get("category", "Uncategorized") for t in templates)
        return sorted(list(categories))
    
    def reset_to_defaults(self) -> bool:
        """
        Reset templates to default set (useful if user wants to start over).
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if os.path.exists(self.default_templates_file):
                with open(self.default_templates_file, 'r', encoding='utf-8') as f:
                    default_data = json.load(f)
                with open(self.templates_file, 'w', encoding='utf-8') as f:
                    json.dump(default_data, f, indent=2, ensure_ascii=False)
                return True
            return False
        except Exception as e:
            print(f"Error resetting templates: {e}")
            return False
