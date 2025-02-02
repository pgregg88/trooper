"""AWS Lex client for natural language processing."""

import json
from typing import Dict, Any, Optional, TypedDict
import boto3
from loguru import logger

class SessionState(TypedDict):
    """Type definition for Lex session state."""
    sessionAttributes: Dict[str, Any]

class LexRequest(TypedDict):
    """Type definition for Lex request."""
    botId: str
    botAliasId: str
    localeId: str
    sessionId: str
    text: str
    sessionState: Optional[SessionState]

class LexClient:
    """AWS Lex client for natural language processing."""
    
    def __init__(self, 
                 bot_id: str,
                 bot_alias_id: str,
                 locale_id: str = 'en_US',
                 profile_name: str = 'trooper',
                 region_name: str = 'us-east-1'):
        """Initialize Lex client.
        
        Args:
            bot_id: Lex bot ID
            bot_alias_id: Lex bot alias ID
            locale_id: Locale ID for the bot
            profile_name: AWS profile name
            region_name: AWS region name
        """
        try:
            self.session = boto3.Session(
                profile_name=profile_name,
                region_name=region_name
            )
            self.client = self.session.client('lexv2-runtime')
            
            self.bot_id = bot_id
            self.bot_alias_id = bot_alias_id
            self.locale_id = locale_id
            
            logger.info(f"Initialized Lex client for bot: {bot_id}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Lex client: {str(e)}")
            raise
    
    def process_text(self, 
                    text: str, 
                    session_id: str,
                    context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process text input through Lex bot.
        
        Args:
            text: Input text to process
            session_id: Session ID for conversation
            context: Optional session context
            
        Returns:
            Lex response dictionary
        """
        try:
            # Create base request
            request: LexRequest = {
                'botId': self.bot_id,
                'botAliasId': self.bot_alias_id,
                'localeId': self.locale_id,
                'sessionId': session_id,
                'text': text,
                'sessionState': None
            }
            
            # Add context if provided
            if context:
                request['sessionState'] = {
                    'sessionAttributes': context
                }
            
            response = self.client.recognize_text(**request)
            logger.debug(f"Lex response: {json.dumps(response, indent=2)}")
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to process text: {str(e)}")
            raise
    
    def get_session_context(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Extract session context from Lex response.
        
        Args:
            response: Lex response dictionary
            
        Returns:
            Session context dictionary
        """
        try:
            return response.get('sessionState', {}).get('sessionAttributes', {})
        except Exception as e:
            logger.error(f"Failed to get session context: {str(e)}")
            return {}
    
    def get_intent(self, response: Dict[str, Any]) -> Optional[str]:
        """Extract intent name from Lex response.
        
        Args:
            response: Lex response dictionary
            
        Returns:
            Intent name if found, None otherwise
        """
        try:
            return response.get('sessionState', {}).get('intent', {}).get('name')
        except Exception as e:
            logger.error(f"Failed to get intent: {str(e)}")
            return None
    
    def get_slots(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Extract slot values from Lex response.
        
        Args:
            response: Lex response dictionary
            
        Returns:
            Dictionary of slot names and values
        """
        try:
            slots = response.get('sessionState', {}).get('intent', {}).get('slots', {})
            return {
                name: slot.get('value', {}).get('interpretedValue')
                for name, slot in slots.items()
                if slot is not None
            }
        except Exception as e:
            logger.error(f"Failed to get slots: {str(e)}")
            return {} 