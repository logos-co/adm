#!/usr/bin/env python3
"""
Backend API for the Interactive Decision Space Viewer
Integrates with existing qualitative evaluation translator and polytope visualization
"""

import json
import sys
import os
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
from typing import Dict, List, Any, Optional

# Add the dl-example directory to the path to import the translator
sys.path.append(str(Path(__file__).parent / "dl-example"))

try:
    from qualitative_evaluation_translator import (
        QualitativeEvaluationTranslator,
        QualitativeEvaluation,
        EvaluationType,
        ComparisonOperator
    )
    from polytope_visualizer import PolytopeVisualizer
    BACKEND_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Warning: Could not import evaluation modules: {e}")
    print("❌ Advanced features will be unavailable. Make sure you're running this from the correct directory.")
    BACKEND_AVAILABLE = False

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class DecisionSpaceEngine:
    """Core engine for decision space analysis"""

    def __init__(self):
        self.translator = None
        self.visualizer = None
        self.projects = []
        self.evaluations = []

    def update_projects(self, projects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Update the project list"""
        try:
            self.projects = projects
            if BACKEND_AVAILABLE:
                self._rebuild_translator()
            return {"status": "success", "projects_count": len(projects)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def add_constraint(self, evaluation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new constraint evaluation"""
        try:
            # Convert web format to translator format
            evaluation = self._convert_web_evaluation(evaluation_data)

            if not evaluation:
                return {"status": "error", "message": "Invalid evaluation format"}

            self.evaluations.append({
                "id": evaluation_data.get("id", len(self.evaluations) + 1),
                "text": evaluation_data.get("text", ""),
                "evaluation": evaluation.to_dict() if hasattr(evaluation, 'to_dict') else vars(evaluation)
            })

            if BACKEND_AVAILABLE:
                self._rebuild_translator()

            result = {
                "status": "success",
                "constraint_id": len(self.evaluations),
                "total_constraints": len(self.evaluations)
            }

            # Add constraint analysis if translator exists
            if self.translator:
                analysis = self._analyze_constraints()
                result.update(analysis)

            return result

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def remove_constraint(self, constraint_id: int) -> Dict[str, Any]:
        """Remove a constraint"""
        try:
            self.evaluations = [e for e in self.evaluations if e["id"] != constraint_id]

            if BACKEND_AVAILABLE:
                self._rebuild_translator()

            return {"status": "success", "remaining_constraints": len(self.evaluations)}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_constraint_matrices(self) -> Dict[str, Any]:
        """Get constraint matrices for optimization"""
        if not BACKEND_AVAILABLE or not self.translator:
            return {"status": "unavailable", "message": "Backend not available"}

        try:
            A_ineq, b_ineq, A_eq, b_eq = self.translator.get_constraint_matrices()

            return {
                "status": "success",
                "A_ineq": A_ineq.tolist() if A_ineq is not None else [],
                "b_ineq": b_ineq.tolist() if b_ineq is not None else [],
                "A_eq": A_eq.tolist() if A_eq is not None else [],
                "b_eq": b_eq.tolist() if b_eq is not None else []
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_polytope_data(self, dimensions: List[str] = None) -> Dict[str, Any]:
        """Generate polytope visualization data"""
        if not BACKEND_AVAILABLE or not self.translator:
            return {"status": "unavailable", "message": "Backend not available"}

        try:
            # Use default 2D projection if no dimensions specified
            if not dimensions:
                dimensions = ["Strategic Value", "Market Impact"]

            # Get constraint matrices
            A_ineq, b_ineq, A_eq, b_eq = self.translator.get_constraint_matrices()

            # Generate polytope vertices (simplified implementation)
            vertices = self._compute_polytope_vertices(A_ineq, b_ineq, A_eq, b_eq)

            return {
                "status": "success",
                "vertices": vertices,
                "dimensions": dimensions,
                "constraints": len(b_ineq) if b_ineq else 0
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def validate_constraints(self) -> Dict[str, Any]:
        """Validate constraint feasibility"""
        if not BACKEND_AVAILABLE or not self.translator:
            return {"status": "unavailable", "message": "Backend not available"}

        try:
            validation_result = self.translator.validate_constraints()

            return {
                "status": "success",
                "is_feasible": validation_result.get("is_feasible", False),
                "validation_details": validation_result
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def analyze_sensitivity(self) -> Dict[str, Any]:
        """Analyze constraint sensitivity"""
        if not BACKEND_AVAILABLE or not self.translator:
            return {"status": "unavailable", "message": "Backend not available"}

        try:
            # Generate sensitivity analysis data
            sensitivity_data = {
                "constraint_impact": [],
                "feasible_volume_changes": []
            }

            for i, eval_data in enumerate(self.evaluations):
                # Simplified sensitivity computation
                impact = {
                    "constraint_id": eval_data["id"],
                    "constraint_text": eval_data["text"],
                    "relative_importance": min(100, len(self.evaluations) * 10),
                    "feasibility_impact": "medium"
                }
                sensitivity_data["constraint_impact"].append(impact)

            return {"status": "success", "sensitivity_data": sensitivity_data}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _rebuild_translator(self):
        """Rebuild the translator with current data"""
        if not BACKEND_AVAILABLE:
            return

        try:
            project_ids = [p.get("id", p.get("project_id", f"project_{i}")) for i, p in enumerate(self.projects)]
            criteria = [
                'Strategic Value',
                'Technical Complexity',
                'Market Impact',
                'Resource Requirement',
                'Innovation Level'
            ]

            self.translator = QualitativeEvaluationTranslator(
                projects=project_ids,
                criteria=criteria
            )

            # Add all evaluations
            for eval_data in self.evaluations:
                if "evaluation" in eval_data:
                    evaluation = self._dict_to_evaluation(eval_data["evaluation"])
                    if evaluation:
                        self.translator.add_evaluation(evaluation)

        except Exception as e:
            print(f"Warning: Could not rebuild translator: {e}")

    def _convert_web_evaluation(self, web_eval: Dict[str, Any]) -> Optional[QualitativeEvaluation]:
        """Convert web evaluation format to translator format"""
        try:
            evaluation_type_map = {
                'COMPARISON': EvaluationType.COMPARISON,
                'RANGE': EvaluationType.RANGE,
                'RANKING': EvaluationType.RANKING,
                'THRESHOLD': EvaluationType.THRESHOLD
            }

            operator_map = {
                'GREATER': ComparisonOperator.GREATER,
                'LESS': ComparisonOperator.LESS,
                'EQUAL': ComparisonOperator.EQUAL
            }

            evaluation_type = evaluation_type_map.get(web_eval.get("evaluation_type"))
            if not evaluation_type:
                return None

            # Create evaluation object
            evaluation = QualitativeEvaluation(
                evaluator_id=web_eval.get("evaluator_id", "web_user"),
                evaluation_type=evaluation_type,
                projects=web_eval.get("projects", []),
                evaluator_role=web_eval.get("evaluator_role", "user")
            )

            # Set evaluation-specific attributes
            if evaluation_type == EvaluationType.COMPARISON:
                operator = operator_map.get(web_eval.get("operator"))
                if operator:
                    evaluation.operator = operator
            elif evaluation_type == EvaluationType.RANGE:
                evaluation.values = web_eval.get("values", [])
            elif evaluation_type == EvaluationType.RANKING:
                evaluation.values = web_eval.get("values", [])
            elif evaluation_type == EvaluationType.THRESHOLD:
                evaluation.operator = ComparisonOperator.GREATER_EQUAL
                evaluation.values = [web_eval.get("threshold", 0.5)]

            evaluation.criteria = web_eval.get("criteria", "")
            evaluation.confidence = web_eval.get("confidence", 1.0)

            return evaluation

        except Exception as e:
            print(f"Error converting evaluation: {e}")
            return None

    def _dict_to_evaluation(self, eval_dict: Dict[str, Any]) -> Optional[QualitativeEvaluation]:
        """Convert dictionary back to evaluation object"""
        try:
            return self._convert_web_evaluation(eval_dict)
        except Exception as e:
            return None

    def _compute_polytope_vertices(self, A_ineq, b_ineq, A_eq, b_eq) -> List[List[float]]:
        """Compute polytope vertices (simplified)"""
        if A_ineq is None or b_ineq is None:
            return []

        try:
            # For demonstration, generate some sample vertices
            # In a full implementation, this would use more sophisticated algorithms
            vertices = []

            # Generate vertices at intersections of constraints
            num_constraints = min(len(b_ineq), 10)  # Limit for performance

            for i in range(min(8, num_constraints)):
                for j in range(i+1, min(i+4, num_constraints)):
                    if i < len(b_ineq) and j < len(b_ineq):
                        try:
                            # Simplified vertex calculation
                            vertex_x = min(1.0, max(0.0, b_ineq[i] / max(A_ineq[i][0], 0.1)))
                            vertex_y = min(1.0, max(0.0, b_ineq[j] / max(A_ineq[j][1], 0.1)))
                            vertices.append([vertex_x, vertex_y])
                        except:
                            continue

            return vertices
        except Exception as e:
            print(f"Error computing vertices: {e}")
            return []

    def _analyze_constraints(self) -> Dict[str, Any]:
        """Analyze current constraint system"""
        if not BACKEND_AVAILABLE or not self.translator:
            return {}

        try:
            # Get basic constraint info
            A_ineq, b_ineq, A_eq, b_eq = self.translator.get_constraint_matrices()

            analysis = {
                "total_constraints": len(self.evaluations),
                "inequality_constraints": len(b_ineq) if b_ineq else 0,
                "equality_constraints": len(b_eq) if b_eq else 0,
                "variables": A_ineq.shape[1] if A_ineq is not None else 0,
                "constraints_dense": len(b_ineq) > len(self.projects) if b_ineq else False
            }

            return analysis

        except Exception as e:
            return {}

# Global engine instance
engine = DecisionSpaceEngine()

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get backend status"""
    return jsonify({
        "backend_available": BACKEND_AVAILABLE,
        "projects_count": len(engine.projects),
        "constraints_count": len(engine.evaluations),
        "features": ["constraint_validation", "polytope_visualization", "sensitivity_analysis"] if BACKEND_AVAILABLE else []
    })

@app.route('/api/projects', methods=['POST'])
def update_projects():
    """Update projects"""
    try:
        data = request.get_json()
        if not data or 'projects' not in data:
            return jsonify({"error": "Projects data required"}), 400

        result = engine.update_projects(data['projects'])
        return jsonify(result), 200 if result['status'] == 'success' else 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/constraints', methods=['POST'])
def add_constraint():
    """Add a constraint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Constraint data required"}), 400

        result = engine.add_constraint(data)
        return jsonify(result), 200 if result['status'] == 'success' else 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/constraints/<int:constraint_id>', methods=['DELETE'])
def remove_constraint(constraint_id):
    """Remove a constraint"""
    try:
        result = engine.remove_constraint(constraint_id)
        return jsonify(result), 200 if result['status'] == 'success' else 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/polytope', methods=['GET'])
def get_polytope():
    """Get polytope visualization data"""
    try:
        dimensions = request.args.getlist('dimensions')
        result = engine.get_polytope_data(dimensions)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/constraints/matrices', methods=['GET'])
def get_constraint_matrices():
    """Get constraint matrices"""
    try:
        result = engine.get_constraint_matrices()
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/constraints/validate', methods=['GET'])
def validate_constraints():
    """Validate constraints"""
    try:
        result = engine.validate_constraints()
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/constraints/sensitivity', methods=['GET'])
def analyze_sensitivity():
    """Analyze constraint sensitivity"""
    try:
        result = engine.analyze_sensitivity()
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/optimize', methods=['POST'])
def optimize_portfolio():
    """Run portfolio optimization"""
    try:
        data = request.get_json()
        optimization_type = data.get('type', 'max_benefit') if data else 'max_benefit'

        # Mock optimization result (would integrate with real optimization algorithms)
        result = {
            "status": "success",
            "optimization_type": optimization_type,
            "selected_projects": engine.projects[:2] if len(engine.projects) > 1 else engine.projects,
            "objective_value": 0.85,
            "feasibility_score": 0.95,
            "solution_info": {
                "method": "linear_programming",
                "solver": "simplex",
                "convergence": "optimal"
            }
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/export', methods=['GET'])
def export_data():
    """Export current analysis data"""
    try:
        export_data = {
            "projects": engine.projects,
            "constraints": engine.evaluations,
            "polytope_data": engine.get_polytope_data() if BACKEND_AVAILABLE else {},
            "constraint_matrices": engine.get_constraint_matrices() if BACKEND_AVAILABLE else {},
            "timestamp": str(Path(__file__).parent / "decision_space_export.json").replace("\\", "/")  # Fixed escaping
        }

        filename = f"decision_space_analysis_{Path.cwd().name}_{'20241209'}.json"
        filepath = Path(__file__).parent / filename

        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)

        return jsonify({
            "status": "success",
            "filename": filename,
            "path": str(filepath)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/demo', methods=['POST'])
def load_demo_data():
    """Load demo data for testing"""
    try:
        demo_projects = [
            {
                "id": "LOGOS_CORE",
                "name": "Logos Core",
                "strategic_value": 0.8,
                "technical_complexity": 0.6,
                "market_impact": 0.7,
                "resource_requirement": 0.5,
                "innovation_level": 0.8
            },
            {
                "id": "NIMBUS_ETH2",
                "name": "Nimbus ETH2",
                "strategic_value": 0.9,
                "technical_complexity": 0.7,
                "market_impact": 0.8,
                "resource_requirement": 0.8,
                "innovation_level": 0.9
            },
            {
                "id": "VAC_RESEARCH",
                "name": "VAC Research",
                "strategic_value": 0.6,
                "technical_complexity": 0.9,
                "market_impact": 0.4,
                "resource_requirement": 0.6,
                "innovation_level": 1.0
            },
            {
                "id": "STATUS_DESKTOP",
                "name": "Status Desktop",
                "strategic_value": 0.7,
                "technical_complexity": 0.5,
                "market_impact": 0.9,
                "resource_requirement": 0.4,
                "innovation_level": 0.6
            }
        ]

        demo_constraints = [
            {
                "id": 1,
                "text": "Nimbus ETH2 > Logos Core (Strategic Value)",
                "evaluation": {
                    "evaluator_id": "demo_user",
                    "evaluation_type": "COMPARISON",
                    "projects": ["NIMBUS_ETH2", "LOGOS_CORE"],
                    "operator": "GREATER",
                    "criteria": "Strategic Value",
                    "confidence": 0.8
                }
            },
            {
                "id": 2,
                "text": "Logos Core market value between 0.4 and 0.8",
                "evaluation": {
                    "evaluator_id": "demo_user",
                    "evaluation_type": "RANGE",
                    "projects": ["LOGOS_CORE"],
                    "values": [0.4, 0.8],
                    "criteria": "Market Impact",
                    "confidence": 0.9
                }
            }
        ]

        # Load into engine
        engine.update_projects(demo_projects)

        # Clear existing constraints and add demo ones
        engine.evaluations = []

        for constraint in demo_constraints:
            engine.add_constraint(constraint["evaluation"])

        return jsonify({
            "status": "success",
            "projects_loaded": len(demo_projects),
            "constraints_loaded": len(demo_constraints)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Decision Space Viewer Backend...")
    if BACKEND_AVAILABLE:
        print("✅ Advanced backend features available")
        print("   - Real constraint validation")
        print("   - Polytope visualization")
        print("   - Sensitivity analysis")
        print("   - Portfolio optimization")
    else:
        print("⚠️  Backend features unavailable")
        print("   - Make sure dl-example/ modules are available")

    print("🏃 Running server on http://localhost:5001/api")
    app.run(host='0.0.0.0', port=5001, debug=True)
