#!/usr/bin/env python3
"""
Main Test Suite

Tests the proper CrewAI structure and functionality.
"""

def test_imports():
    """Test that all imports work correctly."""
    print("🔧 Testing Imports...")
    
    try:
        # Test individual agent imports
        from agents.youtube_analyst import youtube_analyst
        from agents.local_researcher import local_researcher
        from agents.route_planner import route_planner
        from agents.itinerary_designer import itinerary_designer
        from agents.podcast_creator import podcast_creator
        from agents.calendar_manager import calendar_manager
        
        print("✅ All agent imports successful")
        
        # Test crew import
        from crew import ContentCreationCrew
        print("✅ Crew import successful")
        
        # Test main app import
        from main import CrewAIMCPApp
        print("✅ Main app import successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_agent_initialization():
    """Test that agents initialize correctly."""
    print("\n🤖 Testing Agent Initialization...")
    
    try:
        from agents.youtube_analyst import youtube_analyst
        from agents.local_researcher import local_researcher
        from agents.route_planner import route_planner
        
        agents = [
            ("YouTube Analyst", youtube_analyst),
            ("Local Researcher", local_researcher),
            ("Route Planner", route_planner)
        ]
        
        for name, agent in agents:
            print(f"✅ {name}: {agent.role}")
            
        return True
        
    except Exception as e:
        print(f"❌ Agent initialization test failed: {e}")
        return False

def test_crew_creation():
    """Test that the crew can be created."""
    print("\n🚀 Testing Crew Creation...")
    
    try:
        from crew import ContentCreationCrew
        
        crew = ContentCreationCrew()
        print("✅ ContentCreationCrew created successfully")
        
        # Test that crew has methods
        methods = ['analyze_content', 'plan_experience', 'create_content', 'complete_pipeline']
        for method in methods:
            if hasattr(crew, method):
                print(f"✅ Method exists: {method}")
            else:
                print(f"❌ Missing method: {method}")
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ Crew creation test failed: {e}")
        return False

def test_main_app():
    """Test that the main app can be created."""
    print("\n📱 Testing Main App...")
    
    try:
        from main import CrewAIMCPApp
        
        app = CrewAIMCPApp()
        print("✅ CrewAIMCPApp created successfully")
        
        # Test that app has crew
        if hasattr(app, 'crew'):
            print("✅ App has crew attribute")
        else:
            print("❌ App missing crew attribute")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Main app test failed: {e}")
        return False

if __name__ == "__main__":
    print("🎯 CrewAI MCP Pipeline - Test Suite")
    print("=" * 50)
    
    # Run all tests
    import_success = test_imports()
    agent_success = test_agent_initialization()
    crew_success = test_crew_creation()
    app_success = test_main_app()
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY:")
    print(f"   Imports: {'✅ PASS' if import_success else '❌ FAIL'}")
    print(f"   Agents: {'✅ PASS' if agent_success else '❌ FAIL'}")
    print(f"   Crew: {'✅ PASS' if crew_success else '❌ FAIL'}")
    print(f"   Main App: {'✅ PASS' if app_success else '❌ FAIL'}")
    
    if all([import_success, agent_success, crew_success, app_success]):
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Clean repository structure is working correctly")
    else:
        print("\n❌ Some tests failed")