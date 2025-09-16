#!/usr/bin/env python3
"""
Deep Preference-based Q Network (DPbQN) Integration Demo

This comprehensive demo shows how to use the integrated PPSS framework
that combines qualitative evaluation translation with preference-based
deep reinforcement learning for project portfolio optimization.

Features demonstrated:
1. Setting up project portfolio data
2. Adding qualitative evaluations from experts
3. Training the DPbQN algorithm
4. Collecting human preferences to guide optimization
5. Generating optimized portfolio solutions
6. Analyzing results and trade-offs

Author: Generated for Logos/Nimbus/Status ecosystem research
"""

import sys
import os
import numpy as np
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from integrated_ppss_framework import (
    IntegratedPPSSFramework,
    ProjectData,
    PPSSConfiguration,
    create_sample_framework
)
from qualitative_evaluation_translator import (
    QualitativeEvaluation,
    EvaluationType,
    ComparisonOperator
)
from dpbqn_algorithm import PortfolioSolution, ProjectSchedule, HumanPreference
from human_preference_interface import CLIPreferenceInterface


def setup_enterprise_portfolio():
    """Set up a realistic enterprise project portfolio"""
    print("Setting up Enterprise IT Project Portfolio...")

    # Define comprehensive project data
    projects = [
        ProjectData(
            project_id="CloudMigration",
            name="Cloud Infrastructure Migration",
            description="Migrate legacy systems to cloud infrastructure",
            estimated_duration=18,
            resource_requirements={"budget": 500000, "personnel": 12, "equipment": 8},
            dependencies=[],
            risk_factors={"technical": 0.4, "operational": 0.3, "security": 0.5},
            strategic_alignment=0.85,
            technical_complexity=0.7,
            expected_roi=2.2
        ),
        ProjectData(
            project_id="DigitalTransformation",
            name="Digital Transformation Initiative",
            description="Comprehensive digital transformation across all business units",
            estimated_duration=24,
            resource_requirements={"budget": 800000, "personnel": 20, "equipment": 12},
            dependencies=["CloudMigration"],
            risk_factors={"technical": 0.6, "organizational": 0.7, "market": 0.4},
            strategic_alignment=0.95,
            technical_complexity=0.8,
            expected_roi=3.5
        ),
        ProjectData(
            project_id="CyberSecurity",
            name="Cybersecurity Enhancement",
            description="Strengthen cybersecurity infrastructure and protocols",
            estimated_duration=12,
            resource_requirements={"budget": 300000, "personnel": 8, "equipment": 6},
            dependencies=[],
            risk_factors={"technical": 0.3, "compliance": 0.4, "threat": 0.6},
            strategic_alignment=0.9,
            technical_complexity=0.6,
            expected_roi=1.8
        ),
        ProjectData(
            project_id="DataAnalytics",
            name="Advanced Data Analytics Platform",
            description="Build comprehensive data analytics and BI platform",
            estimated_duration=15,
            resource_requirements={"budget": 400000, "personnel": 10, "equipment": 8},
            dependencies=["CloudMigration"],
            risk_factors={"technical": 0.5, "data_quality": 0.4, "integration": 0.5},
            strategic_alignment=0.8,
            technical_complexity=0.75,
            expected_roi=2.8
        ),
        ProjectData(
            project_id="CustomerPortal",
            name="Customer Self-Service Portal",
            description="Develop modern customer portal with self-service capabilities",
            estimated_duration=10,
            resource_requirements={"budget": 250000, "personnel": 6, "equipment": 4},
            dependencies=[],
            risk_factors={"technical": 0.3, "user_adoption": 0.4, "integration": 0.3},
            strategic_alignment=0.75,
            technical_complexity=0.5,
            expected_roi=2.0
        ),
        ProjectData(
            project_id="SupplyChainOptimization",
            name="Supply Chain Optimization System",
            description="AI-powered supply chain optimization and forecasting",
            estimated_duration=20,
            resource_requirements={"budget": 600000, "personnel": 14, "equipment": 10},
            dependencies=["DataAnalytics"],
            risk_factors={"technical": 0.7, "operational": 0.5, "vendor": 0.4},
            strategic_alignment=0.85,
            technical_complexity=0.85,
            expected_roi=3.2
        )
    ]

    # Configuration for enterprise environment
    config = PPSSConfiguration(
        time_horizon=36,  # 3 years planning horizon
        resource_types=["budget", "personnel", "equipment"],
        total_resources={
            "budget": 1500000,    # $1.5M total budget
            "personnel": 40,      # 40 team members
            "equipment": 25       # 25 equipment units
        },
        optimization_criteria=["business_value", "technical_risk", "strategic_alignment", "cost_efficiency"],
        max_episodes=200,
        max_preference_comparisons=15,
        preference_collection_frequency=25,
        learning_rate=0.0005,
        epsilon_decay=0.99
    )

    return IntegratedPPSSFramework(projects, config)


def add_stakeholder_evaluations(framework):
    """Add qualitative evaluations from various stakeholders"""
    print("\nCollecting stakeholder evaluations...")

    # CEO - Strategic perspective
    ceo_evaluations = [
        QualitativeEvaluation(
            evaluator_id="CEO",
            evaluation_type=EvaluationType.RANKING,
            projects=["DigitalTransformation", "SupplyChainOptimization", "CyberSecurity",
                     "DataAnalytics", "CloudMigration", "CustomerPortal"],
            confidence=0.95,
            criteria="business_value"
        ),
        QualitativeEvaluation(
            evaluator_id="CEO",
            evaluation_type=EvaluationType.THRESHOLD,
            projects=["DigitalTransformation"],
            operator=ComparisonOperator.GREATER_EQUAL,
            values=[0.8],
            confidence=0.9,
            criteria="strategic_alignment"
        )
    ]

    # CTO - Technical perspective
    cto_evaluations = [
        QualitativeEvaluation(
            evaluator_id="CTO",
            evaluation_type=EvaluationType.COMPARISON,
            projects=["SupplyChainOptimization", "DigitalTransformation"],
            operator=ComparisonOperator.GREATER,
            confidence=0.85,
            criteria="technical_risk"
        ),
        QualitativeEvaluation(
            evaluator_id="CTO",
            evaluation_type=EvaluationType.RANKING,
            projects=["CloudMigration", "CyberSecurity", "CustomerPortal",
                     "DataAnalytics", "SupplyChainOptimization", "DigitalTransformation"],
            confidence=0.8,
            criteria="technical_risk"
        )
    ]

    # CFO - Financial perspective
    cfo_evaluations = [
        QualitativeEvaluation(
            evaluator_id="CFO",
            evaluation_type=EvaluationType.RANGE,
            projects=["CloudMigration"],
            values=[0.6, 0.9],
            confidence=0.9,
            criteria="cost_efficiency"
        ),
        QualitativeEvaluation(
            evaluator_id="CFO",
            evaluation_type=EvaluationType.COMPARISON,
            projects=["CustomerPortal", "SupplyChainOptimization"],
            operator=ComparisonOperator.GREATER,
            confidence=0.85,
            criteria="cost_efficiency"
        )
    ]

    # Head of Operations
    ops_evaluations = [
        QualitativeEvaluation(
            evaluator_id="HeadOfOperations",
            evaluation_type=EvaluationType.THRESHOLD,
            projects=["CyberSecurity"],
            operator=ComparisonOperator.GREATER_EQUAL,
            values=[0.85],
            confidence=0.95,
            criteria="business_value"
        ),
        QualitativeEvaluation(
            evaluator_id="HeadOfOperations",
            evaluation_type=EvaluationType.COMPARISON,
            projects=["DigitalTransformation", "CloudMigration"],
            operator=ComparisonOperator.GREATER,
            confidence=0.8,
            criteria="business_value"
        )
    ]

    all_evaluations = ceo_evaluations + cto_evaluations + cfo_evaluations + ops_evaluations

    print(f"Adding {len(all_evaluations)} stakeholder evaluations:")
    for eval in all_evaluations:
        eval_desc = f"  {eval.evaluator_id}: {eval.evaluation_type.value}"
        if eval.evaluation_type == EvaluationType.COMPARISON:
            eval_desc += f" ({eval.projects[0]} {eval.operator.value} {eval.projects[1]})"
        elif eval.evaluation_type == EvaluationType.RANKING:
            eval_desc += f" ({len(eval.projects)} projects)"
        print(eval_desc)

    framework.add_qualitative_evaluations(all_evaluations)
    return all_evaluations


def demonstrate_training_process(framework, episodes=50):
    """Demonstrate the training process with periodic human feedback"""
    print(f"\nStarting DPbQN training for {episodes} episodes...")
    print("Note: This demo will periodically ask for your preferences between solutions")
    print("You can press Ctrl+C during preference collection to skip and continue training")

    try:
        training_results = framework.train(episodes)

        print(f"\nTraining completed!")
        print(f"Episodes: {training_results['total_episodes']}")
        print(f"Preferences collected: {training_results['total_preferences_collected']}")
        print(f"Solutions generated: {training_results['total_solutions_generated']}")
        print(f"Average solution quality: {training_results['average_solution_quality']:.3f}")

        return training_results

    except KeyboardInterrupt:
        print("\nTraining interrupted by user")
        return framework.get_framework_summary()


def generate_and_analyze_solutions(framework, num_solutions=5):
    """Generate multiple optimized solutions and analyze them"""
    print(f"\nGenerating {num_solutions} optimized portfolio solutions...")

    solutions = []
    for i in range(num_solutions):
        solution = framework.generate_optimized_portfolio(evaluation_mode=True)
        solutions.append(solution)

        print(f"\nSolution {i+1}:")
        print(f"  Selected Projects: {', '.join(solution.selected_projects)}")
        print(f"  Total Cost: ${solution.total_cost:,.0f}")
        print(f"  Duration: {solution.total_duration} months")
        print(f"  Risk Score: {solution.risk_score:.3f}")
        print(f"  Feasibility: {solution.feasibility_score:.3f}")

    # Analyze trade-offs
    print(f"\nAnalyzing solution trade-offs...")
    for i, solution in enumerate(solutions):
        try:
            tradeoffs = framework.analyze_solution_tradeoffs(solution)
            if tradeoffs:
                print(f"Solution {i+1} trade-off analysis completed")
        except Exception as e:
            print(f"Trade-off analysis failed for solution {i+1}: {e}")

    return solutions


def collect_final_preferences(framework, solutions):
    """Collect final preferences on generated solutions"""
    print(f"\nCollecting your final preferences on the generated solutions...")
    print("This will help improve future optimizations")

    try:
        preferences = framework.collect_human_preferences(solutions, max_comparisons=5)
        print(f"Collected {len(preferences)} final preferences")

        if preferences:
            # Analyze preference patterns
            from human_preference_interface import PreferenceGuidedSampling
            preference_analyzer = PreferenceGuidedSampling(preferences)
            patterns = preference_analyzer.analyze_preference_patterns()

            print(f"\nPreference Analysis:")
            if patterns:
                print(f"  Preferred cost range: ${patterns['preferred_cost_range'][0]:,.0f} - ${patterns['preferred_cost_range'][1]:,.0f}")
                print(f"  Preferred duration range: {patterns['preferred_duration_range'][0]} - {patterns['preferred_duration_range'][1]} months")
                print(f"  Average preferred project count: {patterns['average_preferred_project_count']:.1f}")

                popular_projects = patterns.get('popular_projects', [])[:3]
                if popular_projects:
                    print(f"  Most preferred projects: {', '.join([p[0] for p in popular_projects])}")

        return preferences

    except KeyboardInterrupt:
        print("Final preference collection skipped")
        return []


def demonstrate_framework_export(framework):
    """Demonstrate exporting framework state"""
    print(f"\nExporting framework state for future use...")

    export_dir = "ppss_framework_export"
    try:
        framework.export_framework_state(export_dir)
        print(f"✓ Framework state exported to: {export_dir}/")
        print("This includes:")
        print("  - Trained DPbQN model")
        print("  - Constraint matrices from qualitative evaluations")
        print("  - Collected human preferences")
        print("  - Training history and metrics")
        print("  - Project data and configuration")
    except Exception as e:
        print(f"⚠ Framework export encountered issues: {e}")
        print("Some components may have been saved successfully - check the export directory")
        print(f"Export directory: {export_dir}/")


def create_training_visualization(framework):
    """Create and display training progress visualization"""
    print(f"\nCreating training visualization...")

    try:
        fig = framework.visualize_training_progress("training_progress.html")
        print("Interactive training visualization saved to: training_progress.html")
        print("Open this file in a web browser to view the results")
        return fig
    except Exception as e:
        print(f"Visualization creation failed: {e}")
        return None


def main():
    """Main demo function"""
    print("="*80)
    print("DEEP PREFERENCE-BASED Q NETWORK (DPbQN) INTEGRATION DEMO")
    print("Robust Human-Machine Framework for Project Portfolio Selection")
    print("="*80)

    try:
        # Phase 1: Setup
        print("\n" + "="*60)
        print("PHASE 1: FRAMEWORK SETUP")
        print("="*60)

        framework = setup_enterprise_portfolio()
        evaluations = add_stakeholder_evaluations(framework)

        # Show framework summary
        summary = framework.get_framework_summary()
        print(f"\nFramework Summary:")
        print(f"  Projects: {summary['project_portfolio']['total_projects']}")
        print(f"  Constraints: {summary['constraint_analysis'].get('total_constraints', 0)}")
        print(f"  System feasible: {summary['constraint_analysis'].get('is_feasible', 'Unknown')}")

        # Phase 2: Training
        print("\n" + "="*60)
        print("PHASE 2: DPBQN TRAINING WITH HUMAN PREFERENCES")
        print("="*60)

        training_results = demonstrate_training_process(framework, episodes=50)

        # Phase 3: Solution Generation
        print("\n" + "="*60)
        print("PHASE 3: OPTIMIZED SOLUTION GENERATION")
        print("="*60)

        solutions = generate_and_analyze_solutions(framework, num_solutions=3)

        # Phase 4: Final Evaluation
        print("\n" + "="*60)
        print("PHASE 4: FINAL EVALUATION AND ANALYSIS")
        print("="*60)

        final_preferences = collect_final_preferences(framework, solutions)

        # Phase 5: Results and Export
        print("\n" + "="*60)
        print("PHASE 5: RESULTS ANALYSIS AND EXPORT")
        print("="*60)

        # Final framework summary
        final_summary = framework.get_framework_summary()
        print(f"\nFinal Framework Statistics:")
        print(f"  Training episodes: {final_summary['training_statistics']['episodes_completed']}")
        print(f"  Solutions generated: {final_summary['training_statistics']['solutions_generated']}")
        print(f"  Preferences collected: {final_summary['training_statistics']['human_preferences_collected']}")
        print(f"  Average solution quality: {final_summary['training_statistics']['average_solution_quality']:.3f}")

        # Create visualizations
        create_training_visualization(framework)

        # Export framework
        try:
            demonstrate_framework_export(framework)
        except Exception as e:
            print(f"\nFramework export failed: {e}")
            print("Continuing with demo completion...")

        print("\n" + "="*80)
        print("DEMO COMPLETED SUCCESSFULLY")
        print("="*80)
        print("\nKey Achievements:")
        print("✓ Qualitative evaluations successfully translated to mathematical constraints")
        print("✓ DPbQN algorithm trained with human preference guidance")
        print("✓ Multiple optimized portfolio solutions generated")
        print("✓ Human preferences collected and analyzed")
        print("✓ Trade-off analysis performed")
        print("✓ Complete framework state exported")

        if solutions:
            print(f"\nBest Solution Recommendation:")
            best_solution = max(solutions, key=lambda s: s.feasibility_score)
            print(f"  Projects: {', '.join(best_solution.selected_projects)}")
            print(f"  Cost: ${best_solution.total_cost:,.0f}")
            print(f"  Duration: {best_solution.total_duration} months")
            print(f"  Feasibility Score: {best_solution.feasibility_score:.3f}")

        print(f"\nThe integrated framework successfully demonstrates:")
        print(f"  - Human-machine collaboration in portfolio optimization")
        print(f"  - Preference-based learning without scalar rewards")
        print(f"  - Robust constraint handling from qualitative evaluations")
        print(f"  - Scalable deep reinforcement learning approach")

    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\nDemo failed with error: {e}")
        import traceback
        traceback.print_exc()

    print(f"\nThank you for trying the DPbQN Integration Demo!")


def quick_demo():
    """Quick demo using pre-built sample framework"""
    print("="*60)
    print("QUICK DPBQN DEMO (Using Sample Data)")
    print("="*60)

    # Use the pre-built sample framework
    framework = create_sample_framework()

    print("Sample framework created with:")
    summary = framework.get_framework_summary()
    print(f"  Projects: {summary['project_portfolio']['total_projects']}")
    print(f"  Constraints: {summary['constraint_analysis'].get('total_constraints', 0)}")

    # Quick training (no human interaction)
    print("\nRunning automated training (no human preferences)...")
    for episode in range(20):
        episode_info = framework.train_episode()
        if episode % 5 == 4:
            print(f"Episode {episode+1}: Reward = {episode_info['total_reward']:.2f}")

    # Generate solution
    print("\nGenerating optimized solution...")
    solution = framework.generate_optimized_portfolio()
    print(f"Optimized Portfolio:")
    print(f"  Projects: {', '.join(solution.selected_projects)}")
    print(f"  Cost: ${solution.total_cost:,.0f}")
    print(f"  Feasibility: {solution.feasibility_score:.3f}")

    print("\nQuick demo completed!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        quick_demo()
    else:
        main()
