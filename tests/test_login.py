import pytest
from dotenv import load_dotenv
from datetime import datetime
from qa_agent import QA
import os

load_dotenv()

base_url = os.getenv("BASE_URL")
test_username = os.getenv("USERNAME")
valid_password = os.getenv('PASSWORD')

@pytest.mark.asyncio
async def test_login_valid():
    test_scenario = f"""
    TEST_ID: T001
    Feature: Login to Application
        Scenario: Successful login with valid credentials
            Given I navigate to the login page "{base_url}/login"
            When I enter valid username "{test_username}" and password "{valid_password}"
            And I click the login button
            Then I should be redirected to /profile url
            And see my username "{test_username}"
    """
    
    qa_engine = QA(test_case=test_scenario)
    result = await qa_engine.execute()
    assert result['run_result'] is True
    assert isinstance(result['test_id'], str)
    assert datetime.fromisoformat(result['run_date'])


@pytest.mark.asyncio
async def test_login_invalid():
    test_scenario = f"""
    TEST_ID: T002
    Feature: Login to Application with invalid credentials
        Scenario: Failed attempt to login with invalid credentials
            Given I navigate to the login page "{base_url}/login"
            When I enter valid username "{test_username}" and password "Invalid_password123!"
            And I click the login button
            Then I should see 'Invalid username or password!' message.
    """
    
    qa_engine = QA(test_case=test_scenario)
    result = await qa_engine.execute()
    assert result['run_result'] is False
    assert isinstance(result['test_id'], str)
    assert datetime.fromisoformat(result['run_date'])

