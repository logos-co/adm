"""
Test script for Phase 2 Trade-off Analysis functionality

This script demonstrates and tests the TradeoffAnalyzer class capabilities
including sampling, Pareto frontier computation, and visualization.
"""

import numpy as np
import sys
import os

# Add the src directory to the path to import local modules
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from polytope_visualization_demo import create_logos_nimbus_status_translator
from polytope_visualizer import PolytopeVisualizer
from tradeoff_analyzer import TradeoffAnalyzer, create_example_objectives


def test_basic_functionality():
    """Test basic TradeoffAnalyzer functionality"""
    print("=" * 60)
    print("TESTING PHASE 2: TRADE-OFF ANALYSIS FUNCTIONALITY")
    print("=" * 60)
    
    # Create translator and visualizer
    print("\n1. Setting up translator and visualizer...")
    translator = create_logos_nimbus_status_translator()
    visualizer = PolytopeVisualizer(translator)
    
    # Create trade-off analyzer
    analyzer = TradeoffAnalyzer(visualizer)
    print(f"   ✓ TradeoffAnalyzer initialized")
    print(f"   ✓ Working with {len(translator.projects)} projects and {len(translator.criteria)} criteria")
    
    # Set up objectives
    print("\n2. Setting up objective functions...")
    objectives = create_example_objectives(translator)
    analyzer.set_objectives(objectives)
    print(f"   ✓ Defined {len(objectives)} objectives: {list(objectives.keys())}")
    
    return analyzer, objectives


def test_sampling_methods():
    """Test different sampling methods"""
    print("\n3. Testing sampling methods...")
    analyzer, _ = test_basic_functionality()
    
    sampling_methods = ['uniform', 'grid', 'monte_carlo', 'latin_hypercube']
    sample_results = {}
    
    for method in sampling_methods:
        try:
            samples = analyzer.sample_polytope(n_samples=100, method=method)
            sample_results[method] = len(samples)
            print(f"   ✓ {method}: Generated {len(samples)} feasible samples")
        except Exception as e:
            print(f"   ✗ {method}: Failed - {e}")
            sample_results[method] = 0
    
    return sample_results


def test_pareto_frontier():
    """Test Pareto frontier computation"""
    print("\n4. Testing Pareto frontier computation...")
    analyzer, objectives = test_basic_functionality()
    
    # Test 2D Pareto frontier
    obj_pairs = [
        ['strategic_value', 'development_cost'],
        ['strategic_value', 'technical_risk'],
        ['development_cost', 'technical_risk']
    ]
    
    pareto_results = {}
    
    for pair in obj_pairs:
        try:
            frontier = analyzer.compute_pareto_frontier(pair, resolution=50)
            pareto_results[f"{pair[0]}_vs_{pair[1]}"] = {
                'n_pareto_points': frontier['n_pareto_points'],
                'pareto_efficiency': frontier['pareto_efficiency'],
                'avg_tradeoff_rate': frontier['avg_tradeoff_rate']
            }
            print(f"   ✓ {pair[0]} vs {pair[1]}: {frontier['n_pareto_points']} Pareto points "
                  f"(efficiency: {frontier['pareto_efficiency']:.3f})")
        except Exception as e:
            print(f"   ✗ {pair[0]} vs {pair[1]}: Failed - {e}")
            pareto_results[f"{pair[0]}_vs_{pair[1]}"] = None
    
    return pareto_results


def test_tradeoff_analysis():
    """Test trade-off analysis metrics"""
    print("\n5. Testing trade-off analysis...")
    analyzer, objectives = test_basic_functionality()
    
    objective_pairs = [
        ('strategic_value', 'development_cost'),
        ('strategic_value', 'technical_risk'),
        ('development_cost', 'technical_risk')
    ]
    
    try:
        tradeoff_results = analyzer.analyze_tradeoffs(objective_pairs)
        
        print("   Trade-off Analysis Results:")
        for pair, metrics in tradeoff_results.items():
            print(f"     {pair}:")
            print(f"       Correlation: {metrics.correlation:.3f}")
            print(f"       Exchange Rate: {metrics.avg_exchange_rate:.3f}")
            print(f"       Pareto Efficiency: {metrics.pareto_efficiency:.3f}")
            print(f"       Knee Points: {len(metrics.knee_points)}")
            print(f"       Dominated Ratio: {metrics.dominated_ratio:.3f}")
        
        return tradeoff_results
        
    except Exception as e:
        print(f"   ✗ Trade-off analysis failed: {e}")
        return None


def test_visualizations():
    """Test visualization creation"""
    print("\n6. Testing visualization creation...")
    analyzer, objectives = test_basic_functionality()
    
    visualization_results = {}
    
    # Set up output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'visualizations', 'phase2')
    os.makedirs(output_dir, exist_ok=True)
    
    # Test 2D visualization
    try:
        fig_2d = analyzer.create_tradeoff_visualization(['strategic_value', 'development_cost'])
        output_path_2d = os.path.join(output_dir, "test_tradeoff_2d.html")
        fig_2d.write_html(output_path_2d)
        visualization_results['2d'] = True
        print("   ✓ 2D trade-off visualization created: visualizations/phase2/test_tradeoff_2d.html")
    except Exception as e:
        print(f"   ✗ 2D visualization failed: {e}")
        visualization_results['2d'] = False
    
    # Test 3D visualization
    try:
        fig_3d = analyzer.create_tradeoff_visualization(['strategic_value', 'development_cost', 'technical_risk'])
        output_path_3d = os.path.join(output_dir, "test_tradeoff_3d.html")
        fig_3d.write_html(output_path_3d)
        visualization_results['3d'] = True
        print("   ✓ 3D trade-off visualization created: visualizations/phase2/test_tradeoff_3d.html")
    except Exception as e:
        print(f"   ✗ 3D visualization failed: {e}")
        visualization_results['3d'] = False
    
    # Test dashboard
    try:
        dashboard = analyzer.create_tradeoff_dashboard(['strategic_value', 'development_cost', 'technical_risk'])
        output_path_dashboard = os.path.join(output_dir, "test_tradeoff_dashboard.html")
        dashboard.write_html(output_path_dashboard)
        visualization_results['dashboard'] = True
        print("   ✓ Trade-off dashboard created: visualizations/phase2/test_tradeoff_dashboard.html")
    except Exception as e:
        print(f"   ✗ Dashboard creation failed: {e}")
        visualization_results['dashboard'] = False
    
    return visualization_results


def test_advanced_features():
    """Test advanced features"""
    print("\n7. Testing advanced features...")
    analyzer, objectives = test_basic_functionality()
    
    advanced_results = {}
    
    # Test adaptive sampling
    try:
        adaptive_samples = analyzer.adaptive_sample_pareto_regions(
            ['strategic_value', 'development_cost'], 
            initial_samples=100, 
            refinement_iterations=2
        )
        advanced_results['adaptive_sampling'] = len(adaptive_samples)
        print(f"   ✓ Adaptive sampling: Generated {len(adaptive_samples)} focused samples")
    except Exception as e:
        print(f"   ✗ Adaptive sampling failed: {e}")
        advanced_results['adaptive_sampling'] = 0
    
    # Test weighted optimization
    try:
        weight_vectors = [[0.7, 0.3], [0.5, 0.5], [0.3, 0.7]]
        solutions = analyzer.solve_weighted_objectives(
            weight_vectors, 
            ['strategic_value', 'development_cost']
        )
        advanced_results['weighted_optimization'] = len(solutions)
        print(f"   ✓ Weighted optimization: Found {len(solutions)} solutions")
    except Exception as e:
        print(f"   ✗ Weighted optimization failed: {e}")
        advanced_results['weighted_optimization'] = 0
    
    return advanced_results


def run_comprehensive_test():
    """Run comprehensive test of all Phase 2 functionality"""
    print("Starting comprehensive Phase 2 test suite...")
    
    try:
        # Test basic functionality
        analyzer, objectives = test_basic_functionality()
        
        # Test sampling
        sampling_results = test_sampling_methods()
        
        # Test Pareto frontier
        pareto_results = test_pareto_frontier()
        
        # Test trade-off analysis
        tradeoff_results = test_tradeoff_analysis()
        
        # Test visualizations
        viz_results = test_visualizations()
        
        # Test advanced features
        advanced_results = test_advanced_features()
        
        # Summary
        print("\n" + "=" * 60)
        print("PHASE 2 TEST SUMMARY")
        print("=" * 60)
        
        print(f"\nSampling Methods:")
        for method, count in sampling_results.items():
            status = "✓" if count > 0 else "✗"
            print(f"  {status} {method}: {count} samples")
        
        print(f"\nPareto Frontier Computation:")
        if pareto_results:
            for pair, result in pareto_results.items():
                if result:
                    print(f"  ✓ {pair}: {result['n_pareto_points']} points, "
                          f"efficiency {result['pareto_efficiency']:.3f}")
                else:
                    print(f"  ✗ {pair}: Failed")
        
        print(f"\nTrade-off Analysis:")
        if tradeoff_results:
            print(f"  ✓ Successfully analyzed {len(tradeoff_results)} objective pairs")
        else:
            print(f"  ✗ Trade-off analysis failed")
        
        print(f"\nVisualizations:")
        for viz_type, success in viz_results.items():
            status = "✓" if success else "✗"
            print(f"  {status} {viz_type} visualization")
        
        print(f"\nAdvanced Features:")
        for feature, result in advanced_results.items():
            status = "✓" if result > 0 else "✗"
            print(f"  {status} {feature}: {result}")
        
        # Overall assessment
        total_tests = (
            len(sampling_results) + 
            len([r for r in pareto_results.values() if r is not None]) +
            (1 if tradeoff_results else 0) +
            len([v for v in viz_results.values() if v]) +
            len([r for r in advanced_results.values() if r > 0])
        )
        
        max_tests = (
            len(sampling_results) + 
            len(pareto_results) + 
            1 + 
            len(viz_results) + 
            len(advanced_results)
        )
        
        success_rate = total_tests / max_tests if max_tests > 0 else 0
        
        print(f"\nOVERALL SUCCESS RATE: {success_rate:.1%} ({total_tests}/{max_tests} tests passed)")
        
        if success_rate >= 0.8:
            print("🎉 PHASE 2 IMPLEMENTATION: EXCELLENT")
        elif success_rate >= 0.6:
            print("✅ PHASE 2 IMPLEMENTATION: GOOD")
        elif success_rate >= 0.4:
            print("⚠️  PHASE 2 IMPLEMENTATION: NEEDS IMPROVEMENT")
        else:
            print("❌ PHASE 2 IMPLEMENTATION: MAJOR ISSUES")
        
        print("\nGenerated files:")
        print("  - test_tradeoff_2d.html")
        print("  - test_tradeoff_3d.html") 
        print("  - test_tradeoff_dashboard.html")
        
        return success_rate
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 0.0


if __name__ == "__main__":
    success_rate = run_comprehensive_test()
    
    if success_rate >= 0.8:
        exit(0)  # Success
    else:
        exit(1)  # Failure
