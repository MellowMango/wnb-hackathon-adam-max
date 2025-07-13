"""
Adventure System Evaluation Script

Uses Weave to evaluate the adventure transformation system with various 
test cases and metrics for quality assessment.
"""

import os
import sys
import json
import asyncio
import weave
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from adventure_crew import transform_transcript_to_adventure
from weave_custom.trace_hooks import setup_weave_tracing

class AdventureEvaluator:
    """Evaluates adventure transformation system using Weave."""
    
    def __init__(self, project_name: str = "adventure-evaluation"):
        self.project_name = project_name
        self.test_cases = []
        self.results = []
        
    def initialize_weave(self):
        """Initialize Weave for evaluation tracking."""
        try:
            setup_weave_tracing(self.project_name)
            print(f"✅ Weave evaluation tracking initialized: {self.project_name}")
        except Exception as e:
            print(f"⚠️  Warning: Could not initialize Weave: {e}")
            
    def add_test_case(self, name: str, transcript_content: str, expected_themes: List[str]):
        """Add a test case for evaluation."""
        self.test_cases.append({
            "name": name,
            "transcript_content": transcript_content,
            "expected_themes": expected_themes,
            "timestamp": datetime.now().isoformat()
        })
        
    @weave.op(name="evaluate_creativity")
    def evaluate_creativity(self, result: Any, expected_themes: List[str]) -> Dict[str, Any]:
        """Evaluate the creativity of generated adventure ideas."""
        try:
            # Extract adventure ideas from result
            if hasattr(result, 'output') and result.output:
                content = str(result.output)
            else:
                content = str(result)
                
            # Simple creativity metrics
            creativity_score = 0
            themes_found = []
            
            # Check for expected themes
            for theme in expected_themes:
                if theme.lower() in content.lower():
                    themes_found.append(theme)
                    creativity_score += 1
                    
            # Check for creative elements
            creative_indicators = [
                "adventure", "explore", "discover", "experience",
                "journey", "immersive", "story", "narrative"
            ]
            
            creative_elements = 0
            for indicator in creative_indicators:
                if indicator.lower() in content.lower():
                    creative_elements += 1
                    
            # Calculate final score
            theme_score = len(themes_found) / len(expected_themes) if expected_themes else 0
            creative_score = min(creative_elements / len(creative_indicators), 1.0)
            final_score = (theme_score + creative_score) / 2
            
            return {
                "creativity_score": final_score,
                "themes_found": themes_found,
                "creative_elements": creative_elements,
                "theme_coverage": theme_score,
                "creative_richness": creative_score,
                "content_length": len(content)
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "creativity_score": 0,
                "themes_found": [],
                "creative_elements": 0
            }
            
    @weave.op(name="evaluate_feasibility")
    def evaluate_feasibility(self, result: Any) -> Dict[str, Any]:
        """Evaluate the feasibility of generated adventures."""
        try:
            if hasattr(result, 'output') and result.output:
                content = str(result.output)
            else:
                content = str(result)
                
            # Check for feasibility indicators
            feasibility_indicators = [
                "location", "address", "hours", "cost", "duration",
                "transportation", "accessibility", "nearby"
            ]
            
            feasibility_score = 0
            indicators_found = []
            
            for indicator in feasibility_indicators:
                if indicator.lower() in content.lower():
                    indicators_found.append(indicator)
                    feasibility_score += 1
                    
            # Calculate score
            final_score = min(feasibility_score / len(feasibility_indicators), 1.0)
            
            return {
                "feasibility_score": final_score,
                "indicators_found": indicators_found,
                "practical_elements": feasibility_score,
                "has_location_info": "location" in indicators_found,
                "has_timing_info": any(t in indicators_found for t in ["hours", "duration"]),
                "has_cost_info": "cost" in indicators_found
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "feasibility_score": 0,
                "indicators_found": []
            }
            
    @weave.op(name="evaluate_engagement")
    def evaluate_engagement(self, result: Any) -> Dict[str, Any]:
        """Evaluate the engagement level of generated adventures."""
        try:
            if hasattr(result, 'output') and result.output:
                content = str(result.output)
            else:
                content = str(result)
                
            # Check for engagement indicators
            engagement_indicators = [
                "photo", "share", "social", "experience", "memorable",
                "interactive", "hands-on", "participate", "engage"
            ]
            
            engagement_score = 0
            indicators_found = []
            
            for indicator in engagement_indicators:
                if indicator.lower() in content.lower():
                    indicators_found.append(indicator)
                    engagement_score += 1
                    
            # Calculate score
            final_score = min(engagement_score / len(engagement_indicators), 1.0)
            
            return {
                "engagement_score": final_score,
                "indicators_found": indicators_found,
                "interactive_elements": engagement_score,
                "has_photo_ops": "photo" in indicators_found,
                "has_social_elements": any(s in indicators_found for s in ["share", "social"]),
                "has_participation": any(p in indicators_found for p in ["participate", "engage", "interactive"])
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "engagement_score": 0,
                "indicators_found": []
            }
            
    @weave.op(name="run_single_evaluation")
    def run_single_evaluation(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Run evaluation for a single test case."""
        print(f"\n🧪 Testing: {test_case['name']}")
        
        # Create temporary transcript file
        transcript_file = f"test_transcript_{test_case['name'].replace(' ', '_')}.txt"
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(test_case['transcript_content'])
            
        try:
            # Transform transcript to adventure
            with weave.trace(name=f"test_case_{test_case['name']}") as trace:
                trace.add_tag("test_case", test_case['name'])
                trace.add_tag("expected_themes", test_case['expected_themes'])
                
                result = transform_transcript_to_adventure(
                    transcript_file=transcript_file,
                    user_location="Test City"
                )
                
                # Evaluate different aspects
                creativity_eval = self.evaluate_creativity(result, test_case['expected_themes'])
                feasibility_eval = self.evaluate_feasibility(result)
                engagement_eval = self.evaluate_engagement(result)
                
                # Calculate overall score
                overall_score = (
                    creativity_eval['creativity_score'] +
                    feasibility_eval['feasibility_score'] +
                    engagement_eval['engagement_score']
                ) / 3
                
                evaluation_result = {
                    "test_case": test_case['name'],
                    "overall_score": overall_score,
                    "creativity": creativity_eval,
                    "feasibility": feasibility_eval,
                    "engagement": engagement_eval,
                    "timestamp": datetime.now().isoformat(),
                    "success": True
                }
                
                trace.add_tag("overall_score", overall_score)
                trace.add_tag("status", "completed")
                
                return evaluation_result
                
        except Exception as e:
            error_result = {
                "test_case": test_case['name'],
                "error": str(e),
                "overall_score": 0,
                "success": False,
                "timestamp": datetime.now().isoformat()
            }
            
            weave.log({
                "test_case_error": test_case['name'],
                "error": str(e)
            })
            
            return error_result
            
        finally:
            # Clean up temporary file
            if os.path.exists(transcript_file):
                os.remove(transcript_file)
                
    @weave.op(name="run_full_evaluation")
    def run_full_evaluation(self) -> Dict[str, Any]:
        """Run complete evaluation suite."""
        print("🔬 Starting Adventure System Evaluation")
        print("=" * 60)
        
        # Initialize Weave
        self.initialize_weave()
        
        # Log evaluation start
        weave.log({
            "evaluation_start": datetime.now().isoformat(),
            "num_test_cases": len(self.test_cases),
            "project": self.project_name
        })
        
        # Run all test cases
        results = []
        for test_case in self.test_cases:
            result = self.run_single_evaluation(test_case)
            results.append(result)
            
            # Display result
            if result['success']:
                print(f"   ✅ {result['test_case']}: {result['overall_score']:.2f}/1.0")
            else:
                print(f"   ❌ {result['test_case']}: FAILED")
                
        # Calculate summary statistics
        successful_tests = [r for r in results if r['success']]
        total_tests = len(results)
        success_rate = len(successful_tests) / total_tests if total_tests > 0 else 0
        
        if successful_tests:
            avg_score = sum(r['overall_score'] for r in successful_tests) / len(successful_tests)
            avg_creativity = sum(r['creativity']['creativity_score'] for r in successful_tests) / len(successful_tests)
            avg_feasibility = sum(r['feasibility']['feasibility_score'] for r in successful_tests) / len(successful_tests)
            avg_engagement = sum(r['engagement']['engagement_score'] for r in successful_tests) / len(successful_tests)
        else:
            avg_score = avg_creativity = avg_feasibility = avg_engagement = 0
            
        # Create summary
        summary = {
            "evaluation_summary": {
                "total_tests": total_tests,
                "successful_tests": len(successful_tests),
                "success_rate": success_rate,
                "average_overall_score": avg_score,
                "average_creativity": avg_creativity,
                "average_feasibility": avg_feasibility,
                "average_engagement": avg_engagement,
                "timestamp": datetime.now().isoformat()
            },
            "individual_results": results
        }
        
        # Log summary
        weave.log(summary)
        
        # Display summary
        print("\n📊 Evaluation Summary:")
        print(f"   Tests Run: {total_tests}")
        print(f"   Success Rate: {success_rate:.2%}")
        print(f"   Average Score: {avg_score:.2f}/1.0")
        print(f"   Creativity: {avg_creativity:.2f}")
        print(f"   Feasibility: {avg_feasibility:.2f}")
        print(f"   Engagement: {avg_engagement:.2f}")
        
        return summary

def create_default_test_cases() -> List[Dict[str, Any]]:
    """Create default test cases for evaluation."""
    return [
        {
            "name": "Urban History",
            "transcript_content": """
            Title: The Hidden Stories of Downtown Architecture
            
            In this video, we explore the fascinating architectural history hidden in plain sight 
            in downtown areas. From Art Deco facades to modernist buildings, every structure 
            tells a story of the people who built it and the era they lived in.
            
            We'll learn about the techniques used by architects, the materials they chose, 
            and the social movements that influenced their designs. You'll discover how to 
            read buildings like books and uncover the secrets of urban development.
            """,
            "expected_themes": ["architecture", "history", "urban", "buildings", "stories"]
        },
        {
            "name": "Nature Photography",
            "transcript_content": """
            Title: Capturing the Perfect Golden Hour Shot
            
            Photography is about more than just pointing and shooting. In this tutorial, 
            we dive deep into the art of capturing natural light during the golden hour.
            
            You'll learn about composition, lighting techniques, and how to find the best 
            locations in your local area. We'll cover equipment basics, camera settings, 
            and post-processing tips that will transform your nature photography.
            """,
            "expected_themes": ["photography", "nature", "golden hour", "lighting", "composition"]
        },
        {
            "name": "Local Food Culture",
            "transcript_content": """
            Title: Street Food Around the World
            
            Food is culture, and street food is the heart of any city. This video takes you 
            on a culinary journey through different neighborhoods, exploring the stories 
            behind local dishes and the communities that created them.
            
            From food trucks to hole-in-the-wall restaurants, we'll discover how immigrants 
            and locals have shaped the food scene. You'll learn to appreciate the complexity 
            and history in every bite.
            """,
            "expected_themes": ["food", "culture", "street food", "community", "culinary"]
        }
    ]

def main():
    """Main evaluation function."""
    print("🎯 Adventure System Evaluation Tool")
    print("=" * 50)
    
    # Create evaluator
    evaluator = AdventureEvaluator("adventure-system-evaluation")
    
    # Add test cases
    test_cases = create_default_test_cases()
    for test_case in test_cases:
        evaluator.add_test_case(
            test_case["name"],
            test_case["transcript_content"],
            test_case["expected_themes"]
        )
    
    # Run evaluation
    try:
        results = evaluator.run_full_evaluation()
        
        # Save results
        results_file = f"evaluation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
            
        print(f"\n💾 Results saved to: {results_file}")
        print("🔍 Check Weave dashboard for detailed traces and metrics")
        
    except Exception as e:
        print(f"\n❌ Evaluation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 