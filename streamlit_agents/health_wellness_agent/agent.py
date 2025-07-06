"""
🌟 Main Health & Wellness Planner Agent 🌟
Handles user goals, meal plans, workouts, progress, and specialized support.
"""

from typing import Dict, Any
from context import RunContextWrapper
from tools.goal_analyzer import GoalAnalyzerTool
from tools.meal_planner import MealPlannerTool
from tools.workout_recommender import WorkoutRecommenderTool
from tools.scheduler import CheckingSchedulerTool
from tools.tracker import ProgressTrackerTool
from handoff_agents.escalation_agent import EscalationAgent
from handoff_agents.nutrition_expert_agent import NutritionExpertAgent
from handoff_agents.injury_support_agent import InjurySupportAgent

class HealthWellnessAgent:
    """🧠 Main AI Agent for Managing Health & Wellness Interactions"""

    def __init__(self):
        self.name = "Health & Wellness Planner 🤖💪"

        # 🎯 Core Tools
        self.tools = {
            'goal_analyzer': GoalAnalyzerTool(),
            'meal_planner': MealPlannerTool(),
            'workout_recommender': WorkoutRecommenderTool(),
            'checkin_scheduler': CheckingSchedulerTool(),
            'progress_tracker': ProgressTrackerTool()
        }

        # 🧑‍⚕️ Specialized Agents
        self.agents = {
            'escalation_agent': EscalationAgent(),
            'nutrition_expert_agent': NutritionExpertAgent(),
            'injury_support_agent': InjurySupportAgent()
        }

    def process_message(self, message: str, context: RunContextWrapper) -> Dict[str, Any]:
        """💬 Main message handler routing user input to the right tool or agent"""
        
        intent = self.get_intent(message)
        handoff_agent = self.check_handoff(message)

        # 🤝 Specialized support if needed
        if handoff_agent:
            return self.handle_handoff(handoff_agent, message, context)

        # 🧰 Tool-based processing
        if intent == 'goal':
            return self.tools['goal_analyzer'].process_user_goal(message, context)
        elif intent == 'meal':
            diet_type = self.extract_diet_type(message)
            goal = context.get_context().goal or {}
            return self.tools['meal_planner'].build_weekly_plan(diet_type, goal, context)
        elif intent == 'workout':
            goal = context.get_context().goal or {}
            return self.tools['workout_recommender'].generate_plan(message, goal, context)
        elif intent == 'progress':
            progress_data = self.extract_progress_data(message)
            return self.tools['progress_tracker'].record_progress(progress_data, context)
        elif intent == 'schedule':
            frequency = self.extract_frequency(message)
            return self.tools['checkin_scheduler'].initiate_checkin_schedule(frequency, context)
        else:
            return self.handle_general_conversation(message)

    def get_intent(self, message: str) -> str:
        """🧭 Detect user intent from message keywords"""
        text = message.lower()

        if any(word in text for word in ['goal', 'want to', 'trying to']):
            return 'goal'
        elif any(word in text for word in ['meal', 'food', 'diet', 'eat']):
            return 'meal'
        elif any(word in text for word in ['workout', 'exercise', 'fitness']):
            return 'workout'
        elif any(word in text for word in ['progress', 'update', 'track']):
            return 'progress'
        elif any(word in text for word in ['schedule', 'remind', 'checkin']):
            return 'schedule'
        return 'general'

    def check_handoff(self, message: str) -> str:
        """🚦 Determine if user should be handed off to a specialist"""
        msg = message.lower()

        if any(word in msg for word in ['human', 'coach', 'trainer', 'person','escalate','doctor']):
            return 'escalation_agent'
        elif any(word in msg for word in ['diabetes', 'allergy', 'allergic','nutrition','dietitian']):
            return 'nutrition_expert_agent'
        elif any(word in msg for word in ['injury', 'pain', 'hurt','injured','fracture']):
            return 'injury_support_agent'
        return None

    def handle_handoff(self, agent_name: str, message: str, context: RunContextWrapper) -> Dict[str, Any]:
        """🧑‍⚕️ Transfer user to specialized agent for deeper assistance"""
        agent = self.agents[agent_name]

        if agent_name == 'escalation_agent':
            return agent.handle_escalation(context, message)
        elif agent_name == 'nutrition_expert_agent':
            consult_type = self.extract_nutrition_type(message)
            return agent.handle_nutrition_consultation(context, consult_type)
        elif agent_name == 'injury_support_agent':
            injury_type = self.extract_injury_type(message)
            return agent.handle_injury_consultation(context, injury_type)

    def extract_diet_type(self, message: str) -> str:
        """🥗 Figure out user’s dietary preference from message"""
        text = message.lower()

        if 'vegetarian' in text:
            return 'vegetarian'
        elif 'vegan' in text:
            return 'vegan'
        elif 'keto' in text:
            return 'keto'
        return 'omnivore'

    def extract_nutrition_type(self, message: str) -> str:
        """🍏 Determine nutrition consultation type"""
        text = message.lower()

        if 'diabetes' in text:
            return 'diabetes'
        elif 'allergy' in text:
            return 'allergies'
        return 'general'

    def extract_injury_type(self, message: str) -> str:
        """🦵 Extract body part or injury type from message"""
        text = message.lower()

        if 'knee' in text:
            return 'knee'
        elif 'back' in text:
            return 'back'
        elif 'shoulder' in text:
            return 'shoulder'
        return 'general'

    def extract_progress_data(self, message: str) -> Dict[str, Any]:
        """📈 Parse user's progress update from message"""
        import re
        text = message.lower()
        data = {'notes': message}

        weight_match = re.search(r'(\d+(?:\.\d+)?)\s*(kg|lbs)', text)
        if weight_match:
            data['weight'] = weight_match.group(1)

        workout_match = re.search(r'(\d+)\s*workout', text)
        if workout_match:
            data['workouts_completed'] = workout_match.group(1)

        return data

    def extract_frequency(self, message: str) -> str:
        """⏰ Extract check-in frequency from message"""
        text = message.lower()

        if 'daily' in text:
            return 'daily'
        elif 'weekly' in text:
            return 'weekly'
        return 'weekly'

    def handle_general_conversation(self, message: str) -> Dict[str, Any]:
        """🗨️ Handle casual conversation or questions about capabilities"""
        text = message.lower()

        if any(phrase in text for phrase in ['help', 'what can you do']):
            return {
                'response_type': 'help',
                'content': {
                    'message': "I'm your friendly AI Health & Wellness Assistant 🧘‍♀️💬 Here's what I can do:",
                    'capabilities': [
                        "🎯 Analyze your health & fitness goals",
                        "🍽️ Suggest custom meal plans",
                        "🏋️ Create personalized workout routines",
                        "📊 Track and monitor your progress",
                        "📅 Schedule your weekly check-ins",
                        "👨‍⚕️ Connect you to experts when needed"
                    ]
                }
            }

        return {
            'response_type': 'conversation',
            'content': {
                'message': "Hey! 👋 I’m here to support your health journey. What would you like to work on today?",
                'suggestions': [
                    "🎯 Set a fitness goal",
                    "🍽️ Get a meal plan",
                    "💪 Build a workout routine",
                    "📈 Track my progress"
                ]
            }
        }
