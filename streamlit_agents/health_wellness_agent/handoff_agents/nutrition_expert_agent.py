"""
Nutrition Expert Agent - Handles complex dietary consultations and personalized guidance.
"""

from typing import Dict, Any, List
from context import RunContextWrapper
from hooks import hook_manager

class NutritionExpertAgent:
    """
    Provides expert advice and structured guidance on specialized dietary needs
    such as diabetes, food allergies, and general nutrition goals.
    """

    def __init__(self):
        self.name = "nutrition_expert_agent"

    def handle_nutrition_consultation(self, context: RunContextWrapper, consultation_type: str = "general") -> Dict[str, Any]:
        """
        Processes the nutrition consultation request by logging the handoff,
        generating targeted recommendations, and preparing additional guidance.
        """
        # Log handoff to nutrition expert agent
        hook_manager.log_handoff("main_agent", self.name)
        context.get_context().add_handoff_log(f"Nutrition consultation: {consultation_type}")

        return {
            "response_type": "nutrition_consultation",
            "content": {
                "message": "I'm here to help with your specialized nutrition needs.",
                "consultation_type": consultation_type,
                "recommendations": self._generate_recommendations(consultation_type),
                "important_notes": self._get_important_notes(consultation_type),
                "resources": self._get_resources(consultation_type)
            }
        }

    def _generate_recommendations(self, consultation_type: str) -> List[Dict[str, Any]]:
        """
        Returns a list of personalized dietary recommendations based on the consultation type.
        """
        if consultation_type == "diabetes":
            return [
                {
                    "category": "Carbohydrate Management",
                    "priority": "high",
                    "recommendation": "Focus on complex carbohydrates and monitor portions.",
                    "reason": "Helps maintain stable blood glucose levels."
                },
                {
                    "category": "Fiber Intake",
                    "priority": "high",
                    "recommendation": "Include 25-35g of fiber daily.",
                    "reason": "Supports digestion and slows glucose absorption."
                }
            ]
        elif consultation_type == "allergies":
            return [
                {
                    "category": "Allergen Avoidance",
                    "priority": "high",
                    "recommendation": "Read all food labels carefully and avoid cross-contamination.",
                    "reason": "Prevents accidental allergic reactions."
                },
                {
                    "category": "Nutrient Replacement",
                    "priority": "medium",
                    "recommendation": "Substitute allergens with nutrient-dense alternatives.",
                    "reason": "Ensures balanced nutrition despite restrictions."
                }
            ]
        else:
            return [
                {
                    "category": "General Nutrition",
                    "priority": "medium",
                    "recommendation": "Maintain a balanced diet with a variety of whole foods.",
                    "reason": "Supports overall health and wellbeing."
                }
            ]

    def _get_important_notes(self, consultation_type: str) -> List[str]:
        """
        Provides important reminders and disclaimers tailored to the consultation type.
        """
        notes = [
            "This advice is intended for educational purposes only.",
            "Always consult with a licensed healthcare provider before making major changes.",
            "Dietary needs can vary significantly between individuals."
        ]

        if consultation_type == "diabetes":
            notes.append("Monitor your blood glucose levels regularly and track your meals.")
        elif consultation_type == "allergies":
            notes.append("Keep emergency medication such as an epinephrine injector on hand.")

        return notes

    def _get_resources(self, consultation_type: str) -> List[Dict[str, str]]:
        """
        Returns a curated list of educational resources for the user to explore.
        """
        base_resources = [
            {
                "title": "Nutrition Guidelines",
                "type": "article",
                "description": "An overview of the key principles of healthy eating."
            },
            {
                "title": "Meal Planning Guide",
                "type": "guide",
                "description": "Step-by-step instructions for creating balanced meals."
            }
        ]

        # You can easily expand this to include condition-specific resources
        return base_resources
