"""
Main entry point for the Medical Diagnostic Agent application.
"""
import asyncio
import logging
import subprocess
import time
import requests
import uuid

from google.adk.runners import Runner
from google.genai import types

import utils.logging_config
from utils.config import get_google_api_key, APP_NAME, USER_ID, IMAGING_AGENT_URL
from agents.diagnostic_agent import get_diagnostic_agent
from services.session_manager import get_session_service
from services.memory_manager import get_memory_service

logger = logging.getLogger(__name__)

def start_imaging_server():
    """Starts the Uvicorn server for the imaging agent in a background process."""
    try:
        # Check if the API key is available before starting the server
        get_google_api_key()
    except ValueError as e:
        logger.error(f"Cannot start imaging server: {e}")
        return None

    command = [
        "uvicorn",
        "imaging.imaging_server:app",
        "--host", "localhost",
        "--port", "8001"
    ]
    
    logger.info("Starting Imaging Agent A2A server in the background...")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for the server to be ready
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{IMAGING_AGENT_URL}/.well-known/agent-card.json", timeout=2)
            if response.status_code == 200:
                logger.info("✅ Imaging Agent server is running and accessible.")
                return process
        except requests.exceptions.RequestException:
            time.sleep(1)
            
    logger.error("Imaging Agent server failed to start. Continuing without imaging capabilities.")
    process.terminate()
    return None

async def main():
    """Main application loop."""
    logger.info("Initializing Medical Diagnostic Agent System...")

    try:
        # This will raise an error if the key is not set, stopping execution early.
        get_google_api_key()
    except ValueError as e:
        logger.critical(f"FATAL: {e}")
        logger.critical("Please set your GOOGLE_API_KEY in the .env file and restart.")
        return

    # Start the imaging server as a separate process
    imaging_server_process = start_imaging_server()
    
    # Setup ADK components
    session_service = get_session_service()
    memory_service = get_memory_service()
    diagnostic_agent = get_diagnostic_agent()

    runner = Runner(
        agent=diagnostic_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service
    )

    session_id = f"diag_session_{uuid.uuid4().hex[:8]}"
    logger.info(f"Starting new diagnostic session: {session_id}")
    
    try:
        await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
    except Exception:
        await session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)

    print("\n--- Medical Diagnostic Assistant ---")
    print("Welcome, Doctor. Please describe the patient's initial symptoms.")
    print("Type 'exit' to end the session.")

    try:
        while True:
            user_input = input("\n> ")
            if user_input.lower() == 'exit':
                break

            message = types.Content(role="user", parts=[types.Part(text=user_input)])
            
            async for event in runner.run_async(
                user_id=USER_ID, session_id=session_id, new_message=message
            ):
                if event.is_final_response() and event.content:
                    for part in event.content.parts:
                        if part.text:
                            print(f"\nAssistant:\n{part.text}")
                
                # Handle human-in-the-loop for clarifying questions or approvals
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.function_call and part.function_call.name == "adk_request_confirmation":
                            hint = part.function_call.args.get("hint", "Awaiting input...")
                            print(f"\n[ACTION REQUIRED] {hint}")
                            
                            # In a real app, this would involve a UI. Here we simulate with CLI input.
                            human_response = input("> ")
                            
                            confirmation_response = types.FunctionResponse(
                                id=part.function_call.id,
                                name="adk_request_confirmation",
                                response={"confirmed": True, "details": human_response}
                            )
                            response_message = types.Content(role="user", parts=[types.Part(function_response=confirmation_response)])
                            
                            # Resume the runner
                            async for resume_event in runner.run_async(
                                user_id=USER_ID, session_id=session_id, new_message=response_message, invocation_id=event.invocation_id
                            ):
                                if resume_event.is_final_response() and resume_event.content:
                                    for resume_part in resume_event.content.parts:
                                        if resume_part.text:
                                            print(f"\nAssistant:\n{resume_part.text}")

    except KeyboardInterrupt:
        print("\nSession interrupted by user.")
    finally:
        if imaging_server_process:
            logger.info("Shutting down the imaging server...")
            imaging_server_process.terminate()
            imaging_server_process.wait()
        print("Session ended. Goodbye.")


if __name__ == "__main__":
    asyncio.run(main())

