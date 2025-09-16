"""
Input Parser for Qualitative Evaluations

This module provides utilities to parse qualitative evaluations from various input formats
including natural language text, structured data files, and interactive interfaces.
"""

import re
import json
import csv
from typing import List, Dict, Optional, Union
from dataclasses import asdict
import pandas as pd
from datetime import datetime

from qualitative_evaluation_translator import (
    QualitativeEvaluation, 
    EvaluationType, 
    ComparisonOperator
)


class NaturalLanguageParser:
    """Parse qualitative evaluations from natural language text"""
    
    def __init__(self):
        # Patterns for different evaluation types
        self.comparison_patterns = [
            r'(\w+)\s+(?:is\s+)?(?:better|greater|higher|superior)\s+(?:than\s+)?(\w+)',
            r'(\w+)\s*>\s*(\w+)',
            r'(\w+)\s+(?:is\s+)?(?:worse|less|lower|inferior)\s+(?:than\s+)?(\w+)',
            r'(\w+)\s*<\s*(\w+)',
            r'(\w+)\s+(?:is\s+)?(?:equal|same|equivalent)\s+(?:to\s+)?(\w+)',
            r'(\w+)\s*=\s*(\w+)'
        ]
        
        self.range_patterns = [
            r'(\w+)\s+(?:is\s+|should\s+be\s+)?between\s+([\d.]+)\s+and\s+([\d.]+)',
            r'(\w+)\s+(?:value\s+)?(?:is\s+)?in\s+(?:the\s+)?range\s+\[([\d.]+),\s*([\d.]+)\]',
            r'(\w+)\s+(?:should\s+be\s+)?from\s+([\d.]+)\s+to\s+([\d.]+)'
        ]
        
        self.threshold_patterns = [
            r'(\w+)\s+(?:must\s+be\s+|should\s+be\s+)?(?:at\s+least\s+)([\d.]+)',
            r'(\w+)\s+(?:must\s+be\s+|should\s+be\s+)?(?:at\s+most\s+)([\d.]+)',
            r'(\w+)\s+(?:must\s+be\s+|should\s+be\s+)?(?:greater\s+than\s+)([\d.]+)',
            r'(\w+)\s+(?:must\s+be\s+|should\s+be\s+)?(?:less\s+than\s+)([\d.]+)',
            r'(\w+)\s+(?:>=\s*|≥\s*)([\d.]+)',
            r'(\w+)\s+(?:<=\s*|≤\s*)([\d.]+)',
            r'(\w+)\s+(?:>\s*)([\d.]+)',
            r'(\w+)\s+(?:<\s*)([\d.]+)'
        ]
        
        self.ranking_patterns = [
            r'(?:rank|order|priority):\s*([^.]+)',
            r'(\w+)\s*>\s*(\w+)\s*>\s*(\w+)',
            r'(\w+)\s+(?:then\s+)?(\w+)\s+(?:then\s+)?(\w+)'
        ]
    
    def parse_text(self, text: str, evaluator_id: str) -> List[QualitativeEvaluation]:
        """Parse natural language text into qualitative evaluations"""
        evaluations = []
        text = text.lower().strip()
        
        # Split text into sentences to avoid cross-sentence matches
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Try comparison patterns
            for pattern in self.comparison_patterns:
                matches = re.findall(pattern, sentence, re.IGNORECASE)
                for match in matches:
                    if len(match) == 2:
                        proj_a, proj_b = match
                        
                        # Skip if projects are too short (likely false matches)
                        if len(proj_a.strip()) < 3 or len(proj_b.strip()) < 3:
                            continue
                        
                        # Determine operator based on pattern
                        if any(word in pattern for word in ['better', 'greater', 'higher', 'superior', '>']):
                            operator = ComparisonOperator.GREATER
                        elif any(word in pattern for word in ['worse', 'less', 'lower', 'inferior', '<']):
                            operator = ComparisonOperator.LESS
                        else:
                            operator = ComparisonOperator.EQUAL
                        
                        evaluation = QualitativeEvaluation(
                            evaluator_id=evaluator_id,
                            evaluation_type=EvaluationType.COMPARISON,
                            projects=[proj_a.strip(), proj_b.strip()],
                            operator=operator,
                            timestamp=datetime.now().isoformat()
                        )
                        evaluations.append(evaluation)
        
            # Try range patterns
            for pattern in self.range_patterns:
                matches = re.findall(pattern, sentence, re.IGNORECASE)
                for match in matches:
                    if len(match) == 3:
                        project, min_val, max_val = match
                        
                        # Skip if project name is too short
                        if len(project.strip()) < 3:
                            continue
                            
                        try:
                            # Clean up the values by removing trailing punctuation
                            min_val = min_val.rstrip('.,')
                            max_val = max_val.rstrip('.,')
                            evaluation = QualitativeEvaluation(
                                evaluator_id=evaluator_id,
                                evaluation_type=EvaluationType.RANGE,
                                projects=[project.strip()],
                                values=[float(min_val), float(max_val)],
                                timestamp=datetime.now().isoformat()
                            )
                            evaluations.append(evaluation)
                        except ValueError:
                            continue  # Skip if can't parse numbers
        
            # Try threshold patterns
            for pattern in self.threshold_patterns:
                matches = re.findall(pattern, sentence, re.IGNORECASE)
                for match in matches:
                    if len(match) == 2:
                        project, threshold = match
                        
                        # Skip if project name is too short
                        if len(project.strip()) < 3:
                            continue
                        
                        try:
                            # Clean up the threshold value
                            threshold = threshold.rstrip('.,')
                            
                            # Determine operator based on pattern
                            if any(word in pattern for word in ['at least', '>=', '≥', 'greater than', '>']):
                                operator = ComparisonOperator.GREATER_EQUAL if 'least' in pattern or '>=' in pattern else ComparisonOperator.GREATER
                            else:
                                operator = ComparisonOperator.LESS_EQUAL if 'most' in pattern or '<=' in pattern else ComparisonOperator.LESS
                            
                            evaluation = QualitativeEvaluation(
                                evaluator_id=evaluator_id,
                                evaluation_type=EvaluationType.THRESHOLD,
                                projects=[project.strip()],
                                operator=operator,
                                values=[float(threshold)],
                                timestamp=datetime.now().isoformat()
                            )
                            evaluations.append(evaluation)
                        except ValueError:
                            continue  # Skip if can't parse number
        
        # Try ranking patterns on the full text (rankings often span sentences)
        for pattern in self.ranking_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, str):
                    # Handle comma-separated or space-separated rankings
                    projects = re.split(r'[,\s>]+', match.strip())
                    projects = [p.strip() for p in projects if p.strip() and len(p.strip()) >= 3]
                elif isinstance(match, tuple) and len(match) >= 2:
                    projects = [p.strip() for p in match if p.strip() and len(p.strip()) >= 3]
                
                if len(projects) >= 2:
                    evaluation = QualitativeEvaluation(
                        evaluator_id=evaluator_id,
                        evaluation_type=EvaluationType.RANKING,
                        projects=projects,
                        timestamp=datetime.now().isoformat()
                    )
                    evaluations.append(evaluation)
        
        return evaluations


class StructuredDataParser:
    """Parse qualitative evaluations from structured data formats"""
    
    @staticmethod
    def from_csv(file_path: str) -> List[QualitativeEvaluation]:
        """Load evaluations from CSV file"""
        evaluations = []
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Parse projects (comma-separated)
                    projects = [p.strip() for p in row['projects'].split(',')]
                    
                    # Parse evaluation type
                    eval_type = EvaluationType(row['evaluation_type'])
                    
                    # Parse operator if present
                    operator = None
                    if row.get('operator'):
                        operator = ComparisonOperator(row['operator'])
                    
                    # Parse values if present
                    values = None
                    if row.get('values'):
                        values = [float(v.strip()) for v in row['values'].split(',')]
                    
                    evaluation = QualitativeEvaluation(
                        evaluator_id=row['evaluator_id'],
                        evaluation_type=eval_type,
                        projects=projects,
                        operator=operator,
                        values=values,
                        confidence=float(row.get('confidence', 1.0)),
                        criteria=row.get('criteria'),
                        timestamp=row.get('timestamp'),
                        metadata=json.loads(row.get('metadata', '{}'))
                    )
                    evaluations.append(evaluation)
                    
                except Exception as e:
                    print(f"Error parsing row {row}: {e}")
                    continue
        
        return evaluations
    
    @staticmethod
    def from_json(file_path: str) -> List[QualitativeEvaluation]:
        """Load evaluations from JSON file"""
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        evaluations = []
        for item in data:
            try:
                # Convert string enums back to enum objects
                item['evaluation_type'] = EvaluationType(item['evaluation_type'])
                if item.get('operator'):
                    item['operator'] = ComparisonOperator(item['operator'])
                
                evaluation = QualitativeEvaluation(**item)
                evaluations.append(evaluation)
                
            except Exception as e:
                print(f"Error parsing item {item}: {e}")
                continue
        
        return evaluations
    
    @staticmethod
    def from_dataframe(df: pd.DataFrame) -> List[QualitativeEvaluation]:
        """Load evaluations from pandas DataFrame"""
        evaluations = []
        
        for _, row in df.iterrows():
            try:
                # Parse projects
                if isinstance(row['projects'], str):
                    projects = [p.strip() for p in row['projects'].split(',')]
                else:
                    projects = row['projects']
                
                # Parse evaluation type
                eval_type = EvaluationType(row['evaluation_type'])
                
                # Parse operator if present
                operator = None
                if pd.notna(row.get('operator')):
                    operator = ComparisonOperator(row['operator'])
                
                # Parse values if present
                values = None
                if pd.notna(row.get('values')):
                    if isinstance(row['values'], str):
                        values = [float(v.strip()) for v in row['values'].split(',')]
                    else:
                        values = row['values']
                
                evaluation = QualitativeEvaluation(
                    evaluator_id=row['evaluator_id'],
                    evaluation_type=eval_type,
                    projects=projects,
                    operator=operator,
                    values=values,
                    confidence=float(row.get('confidence', 1.0)),
                    criteria=row.get('criteria') if pd.notna(row.get('criteria')) else None,
                    timestamp=row.get('timestamp') if pd.notna(row.get('timestamp')) else None,
                    metadata=row.get('metadata') if pd.notna(row.get('metadata')) else None
                )
                evaluations.append(evaluation)
                
            except Exception as e:
                print(f"Error parsing row: {e}")
                continue
        
        return evaluations


class EvaluationExporter:
    """Export qualitative evaluations to various formats"""
    
    @staticmethod
    def to_csv(evaluations: List[QualitativeEvaluation], file_path: str):
        """Export evaluations to CSV file"""
        with open(file_path, 'w', newline='') as file:
            if not evaluations:
                return
            
            fieldnames = [
                'evaluator_id', 'evaluation_type', 'projects', 'operator', 
                'values', 'confidence', 'criteria', 'timestamp', 'metadata'
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for eval in evaluations:
                row = {
                    'evaluator_id': eval.evaluator_id,
                    'evaluation_type': eval.evaluation_type.value,
                    'projects': ','.join(eval.projects),
                    'operator': eval.operator.value if eval.operator else '',
                    'values': ','.join(map(str, eval.values)) if eval.values else '',
                    'confidence': eval.confidence,
                    'criteria': eval.criteria or '',
                    'timestamp': eval.timestamp or '',
                    'metadata': json.dumps(eval.metadata) if eval.metadata else '{}'
                }
                writer.writerow(row)
    
    @staticmethod
    def to_json(evaluations: List[QualitativeEvaluation], file_path: str):
        """Export evaluations to JSON file"""
        data = []
        for eval in evaluations:
            eval_dict = asdict(eval)
            # Convert enums to strings for JSON serialization
            eval_dict['evaluation_type'] = eval.evaluation_type.value
            if eval.operator:
                eval_dict['operator'] = eval.operator.value
            data.append(eval_dict)
        
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
    
    @staticmethod
    def to_dataframe(evaluations: List[QualitativeEvaluation]) -> pd.DataFrame:
        """Export evaluations to pandas DataFrame"""
        data = []
        for eval in evaluations:
            eval_dict = asdict(eval)
            eval_dict['evaluation_type'] = eval.evaluation_type.value
            if eval.operator:
                eval_dict['operator'] = eval.operator.value
            else:
                eval_dict['operator'] = None
            data.append(eval_dict)
        
        return pd.DataFrame(data)


class InteractiveEvaluationCollector:
    """Interactive interface for collecting qualitative evaluations"""
    
    def __init__(self, projects: List[str]):
        self.projects = projects
        self.evaluations = []
    
    def collect_comparison(self, evaluator_id: str) -> QualitativeEvaluation:
        """Interactively collect a comparison evaluation"""
        print("\n=== Comparison Evaluation ===")
        print("Available projects:", ", ".join(self.projects))
        
        proj_a = input("Enter first project: ").strip()
        proj_b = input("Enter second project: ").strip()
        
        print("Comparison operators:")
        print("1. > (greater than)")
        print("2. < (less than)")
        print("3. = (equal to)")
        print("4. >= (greater than or equal)")
        print("5. <= (less than or equal)")
        
        choice = input("Select operator (1-5): ").strip()
        operator_map = {
            '1': ComparisonOperator.GREATER,
            '2': ComparisonOperator.LESS,
            '3': ComparisonOperator.EQUAL,
            '4': ComparisonOperator.GREATER_EQUAL,
            '5': ComparisonOperator.LESS_EQUAL
        }
        operator = operator_map.get(choice, ComparisonOperator.GREATER)
        
        confidence = float(input("Confidence (0-1, default 1.0): ") or "1.0")
        
        evaluation = QualitativeEvaluation(
            evaluator_id=evaluator_id,
            evaluation_type=EvaluationType.COMPARISON,
            projects=[proj_a, proj_b],
            operator=operator,
            confidence=confidence,
            timestamp=datetime.now().isoformat()
        )
        
        self.evaluations.append(evaluation)
        return evaluation
    
    def collect_range(self, evaluator_id: str) -> QualitativeEvaluation:
        """Interactively collect a range evaluation"""
        print("\n=== Range Evaluation ===")
        print("Available projects:", ", ".join(self.projects))
        
        project = input("Enter project: ").strip()
        min_val = float(input("Enter minimum value: "))
        max_val = float(input("Enter maximum value: "))
        confidence = float(input("Confidence (0-1, default 1.0): ") or "1.0")
        
        evaluation = QualitativeEvaluation(
            evaluator_id=evaluator_id,
            evaluation_type=EvaluationType.RANGE,
            projects=[project],
            values=[min_val, max_val],
            confidence=confidence,
            timestamp=datetime.now().isoformat()
        )
        
        self.evaluations.append(evaluation)
        return evaluation
    
    def collect_ranking(self, evaluator_id: str) -> QualitativeEvaluation:
        """Interactively collect a ranking evaluation"""
        print("\n=== Ranking Evaluation ===")
        print("Available projects:", ", ".join(self.projects))
        
        projects_input = input("Enter projects in order (comma-separated): ").strip()
        projects = [p.strip() for p in projects_input.split(',')]
        confidence = float(input("Confidence (0-1, default 1.0): ") or "1.0")
        
        evaluation = QualitativeEvaluation(
            evaluator_id=evaluator_id,
            evaluation_type=EvaluationType.RANKING,
            projects=projects,
            confidence=confidence,
            timestamp=datetime.now().isoformat()
        )
        
        self.evaluations.append(evaluation)
        return evaluation
    
    def collect_threshold(self, evaluator_id: str) -> QualitativeEvaluation:
        """Interactively collect a threshold evaluation"""
        print("\n=== Threshold Evaluation ===")
        print("Available projects:", ", ".join(self.projects))
        
        project = input("Enter project: ").strip()
        threshold = float(input("Enter threshold value: "))
        
        print("Threshold operators:")
        print("1. >= (greater than or equal)")
        print("2. <= (less than or equal)")
        
        choice = input("Select operator (1-2): ").strip()
        operator = ComparisonOperator.GREATER_EQUAL if choice == '1' else ComparisonOperator.LESS_EQUAL
        
        confidence = float(input("Confidence (0-1, default 1.0): ") or "1.0")
        
        evaluation = QualitativeEvaluation(
            evaluator_id=evaluator_id,
            evaluation_type=EvaluationType.THRESHOLD,
            projects=[project],
            operator=operator,
            values=[threshold],
            confidence=confidence,
            timestamp=datetime.now().isoformat()
        )
        
        self.evaluations.append(evaluation)
        return evaluation
    
    def run_interactive_session(self, evaluator_id: str):
        """Run an interactive evaluation collection session"""
        print(f"\n=== Interactive Evaluation Collection for {evaluator_id} ===")
        
        while True:
            print("\nEvaluation types:")
            print("1. Comparison (Project A > Project B)")
            print("2. Range (Project value between X and Y)")
            print("3. Ranking (Project A > Project B > Project C)")
            print("4. Threshold (Project value >= X)")
            print("5. Finish")
            
            choice = input("Select evaluation type (1-5): ").strip()
            
            if choice == '1':
                self.collect_comparison(evaluator_id)
            elif choice == '2':
                self.collect_range(evaluator_id)
            elif choice == '3':
                self.collect_ranking(evaluator_id)
            elif choice == '4':
                self.collect_threshold(evaluator_id)
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")
        
        print(f"\nCollected {len(self.evaluations)} evaluations.")
        return self.evaluations


if __name__ == "__main__":
    # Example usage
    
    # Test natural language parsing
    nl_parser = NaturalLanguageParser()
    text = """
    ProjectA is better than ProjectB.
    ProjectC should be between 0.3 and 0.7.
    ProjectD must be at least 0.5.
    Ranking: ProjectA > ProjectC > ProjectB
    """
    
    evaluations = nl_parser.parse_text(text, "expert_1")
    print(f"Parsed {len(evaluations)} evaluations from natural language")
    
    # Test export to CSV
    EvaluationExporter.to_csv(evaluations, "dl-example/sample_evaluations.csv")
    print("Exported evaluations to CSV")
    
    # Test import from CSV
    imported_evaluations = StructuredDataParser.from_csv("dl-example/sample_evaluations.csv")
    print(f"Imported {len(imported_evaluations)} evaluations from CSV")
