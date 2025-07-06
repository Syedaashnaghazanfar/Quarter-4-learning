"""
Input and Output Guardrails
"""
import re
from typing import Dict, Any

class GuardrailValidator:
    """Guardrail validator"""
    
    @staticmethod
    def validate_goal_input(goal_text: str) -> Dict[str, Any]:
        """Validate goal input"""
        # Extract quantity, metric, duration
        quantity_match = re.search(r'(\d+(?:\.\d+)?)', goal_text)
        metric_match = re.search(r'(kg|lbs|pounds)', goal_text.lower())
        duration_match = re.search(r'(\d+)\s*(days?|weeks?|months?)', goal_text.lower())
        
        quantity = float(quantity_match.group(1)) if quantity_match else None
        metric = metric_match.group(1) if metric_match else ""
        duration = duration_match.group(0) if duration_match else ""
        
        # Determine goal type
        if any(word in goal_text.lower() for word in ['lose', 'weight']):
            goal_type = "weight_loss"
        elif any(word in goal_text.lower() for word in ['gain', 'muscle']):
            goal_type = "weight_gain"
        else:
            goal_type = "fitness"
        
        return {
            'quantity': quantity,
            'metric': metric,
            'duration': duration,
            'goal_type': goal_type,
            'original_text': goal_text
        }
    
    @staticmethod
    def validate_dietary_input(diet_text: str) -> str:
        """Validate dietary input"""
        allowed_diets = ['vegetarian', 'vegan', 'keto', 'paleo', 'omnivore']
        
        for diet in allowed_diets:
            if diet in diet_text.lower():
                return diet
        
        return 'omnivore'
    
    @staticmethod
    def validate_output(response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate output format"""
        required_fields = ['response_type', 'content']
        
        for field in required_fields:
            if field not in response_data:
                response_data[field] = 'unknown' if field == 'response_type' else {}
        
        return response_data