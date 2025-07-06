"""
Lifecycle Hooks for tracking
"""
from typing import Dict, Any
from datetime import datetime

class HookManager:
    """Simple hook manager for tracking"""
    
    def __init__(self):
        self.activity_log = []
        self.metrics = {
            'total_interactions': 0,
            'tool_usage': {},
            'handoffs': {}
        }
    
    def log_agent_start(self, agent_name: str):
        """Log when agent starts"""
        self.activity_log.append({
            'timestamp': datetime.now().isoformat(),
            'event': 'agent_start',
            'agent': agent_name
        })
        self.metrics['total_interactions'] += 1
        print(f"🤖 Agent started: {agent_name}")
    
    def log_tool_start(self, tool_name: str):
        """Log when tool starts"""
        self.activity_log.append({
            'timestamp': datetime.now().isoformat(),
            'event': 'tool_start',
            'tool': tool_name
        })
        
        if tool_name not in self.metrics['tool_usage']:
            self.metrics['tool_usage'][tool_name] = 0
        self.metrics['tool_usage'][tool_name] += 1
        
        print(f"🔧 Tool started: {tool_name}")
    
    def log_handoff(self, from_agent: str, to_agent: str):
        """Log handoff"""
        self.activity_log.append({
            'timestamp': datetime.now().isoformat(),
            'event': 'handoff',
            'from_agent': from_agent,
            'to_agent': to_agent
        })
        
        handoff_key = f"{from_agent}_to_{to_agent}"
        if handoff_key not in self.metrics['handoffs']:
            self.metrics['handoffs'][handoff_key] = 0
        self.metrics['handoffs'][handoff_key] += 1
        
        print(f"🔄 Handoff: {from_agent} → {to_agent}")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        return self.metrics

# Global hook manager
hook_manager = HookManager()