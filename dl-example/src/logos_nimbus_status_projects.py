"""
Mock Project-Specific Data for Logos/Nimbus/Status Ecosystem
Based on requirements from dl-example/required-resources.md

This module generates comprehensive project portfolio data for the robust human-machine
project portfolio selection system, including all required attributes and constraints.
"""

import json
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Any
import random
from dataclasses import dataclass, asdict

from qualitative_evaluation_translator import (
    QualitativeEvaluation,
    EvaluationType,
    ComparisonOperator
)


@dataclass
class ProjectData:
    """Complete project data structure"""
    project_id: str
    name: str
    description: str
    ecosystem: str  # logos, nimbus, status, vac, ift
    
    # Core attributes
    construction_duration: int  # months
    construction_cost: float   # in millions USD
    
    # Multiple project values (v_ij)
    strategic_value: float     # v_i1: Strategic importance (0-1)
    technical_complexity: float  # v_i2: Technical difficulty (0-1)
    market_impact: float       # v_i3: Market potential (0-1)
    resource_requirement: float  # v_i4: Resource intensity (0-1)
    innovation_level: float    # v_i5: Innovation factor (0-1)
    
    # Constraint information
    cooperation_projects: List[str]  # H(p_i): Projects with synergistic benefits
    precedence_projects: List[str]   # Ψ(p_i): Must complete before this project
    exclusive_projects: List[str]    # Φ(p_i): Mutually exclusive projects
    
    # Budget and timeline constraints
    annual_budget_distribution: Dict[int, float]  # Year -> Budget allocation
    start_date: str
    end_date: str
    
    # Additional metadata
    team_size: int
    technology_stack: List[str]
    risk_factors: List[str]
    success_metrics: List[str]


def generate_logos_projects() -> List[ProjectData]:
    """Generate Logos ecosystem projects"""
    projects = [
        ProjectData(
            project_id="LOGOS_CORE_001",
            name="Logos Core Infrastructure",
            description="Core blockchain infrastructure for the Logos network",
            ecosystem="logos",
            construction_duration=18,
            construction_cost=2.5,
            strategic_value=0.95,
            technical_complexity=0.85,
            market_impact=0.80,
            resource_requirement=0.90,
            innovation_level=0.88,
            cooperation_projects=["LOGOS_CODEX_001", "LOGOS_NOMOS_001"],
            precedence_projects=[],
            exclusive_projects=["NIMBUS_ETH2_001"],
            annual_budget_distribution={2024: 0.8, 2025: 1.2, 2026: 0.5},
            start_date="2024-01-15",
            end_date="2025-07-15",
            team_size=12,
            technology_stack=["Rust", "Nim", "Go", "Blockchain"],
            risk_factors=["Technical complexity", "Market adoption", "Regulatory uncertainty"],
            success_metrics=["Network throughput", "Developer adoption", "Transaction volume"]
        ),
        
        ProjectData(
            project_id="LOGOS_CODEX_001",
            name="Codex Decentralized Storage",
            description="Decentralized storage network with erasure coding",
            ecosystem="logos",
            construction_duration=24,
            construction_cost=3.2,
            strategic_value=0.88,
            technical_complexity=0.92,
            market_impact=0.85,
            resource_requirement=0.85,
            innovation_level=0.90,
            cooperation_projects=["LOGOS_CORE_001", "LOGOS_WAKU_001"],
            precedence_projects=["LOGOS_CORE_001"],
            exclusive_projects=[],
            annual_budget_distribution={2024: 1.0, 2025: 1.5, 2026: 0.7},
            start_date="2024-03-01",
            end_date="2026-03-01",
            team_size=15,
            technology_stack=["Nim", "libp2p", "Erasure Coding", "IPFS"],
            risk_factors=["Storage economics", "Network effects", "Competition"],
            success_metrics=["Storage capacity", "Retrieval speed", "Cost efficiency"]
        ),
        
        ProjectData(
            project_id="LOGOS_NOMOS_001",
            name="Nomos Consensus Layer",
            description="Novel consensus mechanism for high throughput",
            ecosystem="logos",
            construction_duration=20,
            construction_cost=2.8,
            strategic_value=0.92,
            technical_complexity=0.95,
            market_impact=0.75,
            resource_requirement=0.80,
            innovation_level=0.95,
            cooperation_projects=["LOGOS_CORE_001"],
            precedence_projects=[],
            exclusive_projects=["NIMBUS_ETH1_001"],
            annual_budget_distribution={2024: 0.9, 2025: 1.3, 2026: 0.6},
            start_date="2024-02-01",
            end_date="2025-10-01",
            team_size=10,
            technology_stack=["Rust", "Cryptography", "Consensus Algorithms"],
            risk_factors=["Theoretical validation", "Security audits", "Academic acceptance"],
            success_metrics=["Transaction throughput", "Finality time", "Security guarantees"]
        ),
        
        ProjectData(
            project_id="LOGOS_WAKU_001",
            name="Waku Communication Protocol",
            description="Privacy-preserving communication layer",
            ecosystem="logos",
            construction_duration=16,
            construction_cost=1.8,
            strategic_value=0.85,
            technical_complexity=0.75,
            market_impact=0.90,
            resource_requirement=0.70,
            innovation_level=0.82,
            cooperation_projects=["LOGOS_CODEX_001", "STATUS_APP_001"],
            precedence_projects=[],
            exclusive_projects=[],
            annual_budget_distribution={2024: 0.7, 2025: 0.8, 2026: 0.3},
            start_date="2024-01-01",
            end_date="2025-05-01",
            team_size=8,
            technology_stack=["Go", "libp2p", "Cryptography", "P2P"],
            risk_factors=["Privacy regulations", "Scalability", "Adoption"],
            success_metrics=["Message throughput", "Privacy guarantees", "Network size"]
        )
    ]
    return projects


def generate_nimbus_projects() -> List[ProjectData]:
    """Generate Nimbus ecosystem projects"""
    projects = [
        ProjectData(
            project_id="NIMBUS_ETH2_001",
            name="Nimbus Ethereum 2.0 Client",
            description="Lightweight Ethereum 2.0 consensus client",
            ecosystem="nimbus",
            construction_duration=22,
            construction_cost=3.5,
            strategic_value=0.90,
            technical_complexity=0.88,
            market_impact=0.95,
            resource_requirement=0.85,
            innovation_level=0.80,
            cooperation_projects=["NIMBUS_LIGHT_001"],
            precedence_projects=[],
            exclusive_projects=["LOGOS_CORE_001"],
            annual_budget_distribution={2024: 1.2, 2025: 1.5, 2026: 0.8},
            start_date="2024-01-01",
            end_date="2025-11-01",
            team_size=18,
            technology_stack=["Nim", "Ethereum", "Consensus", "Networking"],
            risk_factors=["Ethereum roadmap changes", "Competition", "Resource constraints"],
            success_metrics=["Validator adoption", "Performance benchmarks", "Stability metrics"]
        ),
        
        ProjectData(
            project_id="NIMBUS_ETH1_001",
            name="Nimbus Ethereum 1.0 Client",
            description="Execution layer client for Ethereum",
            ecosystem="nimbus",
            construction_duration=18,
            construction_cost=2.2,
            strategic_value=0.75,
            technical_complexity=0.80,
            market_impact=0.70,
            resource_requirement=0.75,
            innovation_level=0.65,
            cooperation_projects=["NIMBUS_ETH2_001"],
            precedence_projects=[],
            exclusive_projects=["LOGOS_NOMOS_001"],
            annual_budget_distribution={2024: 0.8, 2025: 1.0, 2026: 0.4},
            start_date="2024-02-15",
            end_date="2025-08-15",
            team_size=12,
            technology_stack=["Nim", "EVM", "Networking", "State Management"],
            risk_factors=["Merge timeline", "Technical debt", "Maintenance burden"],
            success_metrics=["Sync speed", "Memory usage", "Transaction processing"]
        ),
        
        ProjectData(
            project_id="NIMBUS_LIGHT_001",
            name="Nimbus Light Client",
            description="Ultra-lightweight client for mobile and IoT",
            ecosystem="nimbus",
            construction_duration=14,
            construction_cost=1.5,
            strategic_value=0.82,
            technical_complexity=0.70,
            market_impact=0.88,
            resource_requirement=0.60,
            innovation_level=0.85,
            cooperation_projects=["NIMBUS_ETH2_001", "STATUS_APP_001"],
            precedence_projects=["NIMBUS_ETH2_001"],
            exclusive_projects=[],
            annual_budget_distribution={2024: 0.5, 2025: 0.7, 2026: 0.3},
            start_date="2024-06-01",
            end_date="2025-08-01",
            team_size=6,
            technology_stack=["Nim", "Light Client Protocol", "Mobile", "Optimization"],
            risk_factors=["Protocol changes", "Mobile constraints", "Battery optimization"],
            success_metrics=["Resource usage", "Sync time", "Mobile adoption"]
        ),
        
        ProjectData(
            project_id="NIMBUS_PORTAL_001",
            name="Portal Network Implementation",
            description="Distributed state and history network",
            ecosystem="nimbus",
            construction_duration=26,
            construction_cost=2.8,
            strategic_value=0.85,
            technical_complexity=0.90,
            market_impact=0.75,
            resource_requirement=0.80,
            innovation_level=0.88,
            cooperation_projects=["NIMBUS_LIGHT_001"],
            precedence_projects=[],
            exclusive_projects=[],
            annual_budget_distribution={2024: 0.8, 2025: 1.2, 2026: 0.8},
            start_date="2024-04-01",
            end_date="2026-06-01",
            team_size=10,
            technology_stack=["Nim", "DHT", "Networking", "State Management"],
            risk_factors=["Network adoption", "Data availability", "Incentive design"],
            success_metrics=["Network coverage", "Data availability", "Query performance"]
        )
    ]
    return projects


def generate_status_projects() -> List[ProjectData]:
    """Generate Status ecosystem projects"""
    projects = [
        ProjectData(
            project_id="STATUS_APP_001",
            name="Status Mobile Application",
            description="Decentralized messaging and Web3 browser",
            ecosystem="status",
            construction_duration=20,
            construction_cost=4.2,
            strategic_value=0.95,
            technical_complexity=0.85,
            market_impact=0.92,
            resource_requirement=0.90,
            innovation_level=0.80,
            cooperation_projects=["STATUS_KEYCARD_001", "LOGOS_WAKU_001"],
            precedence_projects=[],
            exclusive_projects=[],
            annual_budget_distribution={2024: 1.5, 2025: 1.8, 2026: 0.9},
            start_date="2024-01-01",
            end_date="2025-09-01",
            team_size=25,
            technology_stack=["React Native", "ClojureScript", "Ethereum", "IPFS"],
            risk_factors=["App store policies", "User adoption", "Regulatory compliance"],
            success_metrics=["Daily active users", "Message volume", "DApp usage"]
        ),
        
        ProjectData(
            project_id="STATUS_DESKTOP_001",
            name="Status Desktop Application",
            description="Desktop version of Status with enhanced features",
            ecosystem="status",
            construction_duration=16,
            construction_cost=2.8,
            strategic_value=0.80,
            technical_complexity=0.75,
            market_impact=0.70,
            resource_requirement=0.75,
            innovation_level=0.70,
            cooperation_projects=["STATUS_APP_001"],
            precedence_projects=["STATUS_APP_001"],
            exclusive_projects=[],
            annual_budget_distribution={2024: 1.0, 2025: 1.2, 2026: 0.6},
            start_date="2024-04-01",
            end_date="2025-08-01",
            team_size=15,
            technology_stack=["Qt", "Nim", "React", "Ethereum"],
            risk_factors=["Platform fragmentation", "Feature parity", "Resource allocation"],
            success_metrics=["User adoption", "Feature completeness", "Performance"]
        ),
        
        ProjectData(
            project_id="STATUS_KEYCARD_001",
            name="Status Keycard Hardware",
            description="Hardware wallet and secure key storage",
            ecosystem="status",
            construction_duration=24,
            construction_cost=3.8,
            strategic_value=0.88,
            technical_complexity=0.92,
            market_impact=0.85,
            resource_requirement=0.95,
            innovation_level=0.90,
            cooperation_projects=["STATUS_APP_001"],
            precedence_projects=[],
            exclusive_projects=[],
            annual_budget_distribution={2024: 1.2, 2025: 1.5, 2026: 1.1},
            start_date="2024-02-01",
            end_date="2026-02-01",
            team_size=12,
            technology_stack=["Hardware", "Cryptography", "NFC", "Secure Elements"],
            risk_factors=["Hardware supply chain", "Security audits", "Manufacturing costs"],
            success_metrics=["Security certifications", "Manufacturing volume", "Integration success"]
        ),
        
        ProjectData(
            project_id="STATUS_NETWORK_001",
            name="Status Network Infrastructure",
            description="Decentralized network infrastructure and incentives",
            ecosystem="status",
            construction_duration=30,
            construction_cost=5.5,
            strategic_value=0.90,
            technical_complexity=0.95,
            market_impact=0.88,
            resource_requirement=0.92,
            innovation_level=0.92,
            cooperation_projects=["STATUS_APP_001", "LOGOS_WAKU_001"],
            precedence_projects=["STATUS_APP_001"],
            exclusive_projects=[],
            annual_budget_distribution={2024: 1.8, 2025: 2.2, 2026: 1.5},
            start_date="2024-03-01",
            end_date="2026-09-01",
            team_size=20,
            technology_stack=["Blockchain", "Tokenomics", "P2P", "Incentive Design"],
            risk_factors=["Token economics", "Network effects", "Regulatory landscape"],
            success_metrics=["Network participation", "Token utility", "Decentralization metrics"]
        )
    ]
    return projects


def generate_vac_projects() -> List[ProjectData]:
    """Generate VAC (Vac Applied Cryptography) projects"""
    projects = [
        ProjectData(
            project_id="VAC_RESEARCH_001",
            name="Advanced Cryptography Research",
            description="Research into novel cryptographic primitives",
            ecosystem="vac",
            construction_duration=36,
            construction_cost=2.5,
            strategic_value=0.85,
            technical_complexity=0.98,
            market_impact=0.60,
            resource_requirement=0.70,
            innovation_level=0.95,
            cooperation_projects=["LOGOS_NOMOS_001", "STATUS_KEYCARD_001"],
            precedence_projects=[],
            exclusive_projects=[],
            annual_budget_distribution={2024: 0.8, 2025: 0.9, 2026: 0.8},
            start_date="2024-01-01",
            end_date="2027-01-01",
            team_size=8,
            technology_stack=["Mathematics", "Cryptography", "Formal Methods", "Research"],
            risk_factors=["Research uncertainty", "Academic timeline", "Practical applicability"],
            success_metrics=["Publications", "Protocol implementations", "Academic recognition"]
        ),
        
        ProjectData(
            project_id="VAC_ZEROKNOWLEDGE_001",
            name="Zero-Knowledge Proof Systems",
            description="Practical ZK proof systems for privacy",
            ecosystem="vac",
            construction_duration=28,
            construction_cost=3.2,
            strategic_value=0.90,
            technical_complexity=0.95,
            market_impact=0.85,
            resource_requirement=0.80,
            innovation_level=0.92,
            cooperation_projects=["LOGOS_WAKU_001", "STATUS_NETWORK_001"],
            precedence_projects=["VAC_RESEARCH_001"],
            exclusive_projects=[],
            annual_budget_distribution={2024: 1.0, 2025: 1.3, 2026: 0.9},
            start_date="2024-06-01",
            end_date="2026-10-01",
            team_size=12,
            technology_stack=["ZK-SNARKs", "ZK-STARKs", "Circom", "Cryptography"],
            risk_factors=["Performance optimization", "Trusted setup", "Complexity"],
            success_metrics=["Proof generation time", "Verification speed", "Circuit efficiency"]
        )
    ]
    return projects


def generate_ift_projects() -> List[ProjectData]:
    """Generate IFT (Institute of Free Technology) projects"""
    projects = [
        ProjectData(
            project_id="IFT_FINANCE_001",
            name="Decentralized Finance Infrastructure",
            description="Core DeFi protocols and financial primitives",
            ecosystem="ift",
            construction_duration=22,
            construction_cost=4.5,
            strategic_value=0.92,
            technical_complexity=0.88,
            market_impact=0.95,
            resource_requirement=0.85,
            innovation_level=0.85,
            cooperation_projects=["STATUS_NETWORK_001", "LOGOS_CORE_001"],
            precedence_projects=[],
            exclusive_projects=[],
            annual_budget_distribution={2024: 1.5, 2025: 2.0, 2026: 1.0},
            start_date="2024-02-01",
            end_date="2025-12-01",
            team_size=18,
            technology_stack=["Solidity", "DeFi", "Smart Contracts", "Economics"],
            risk_factors=["Regulatory compliance", "Smart contract security", "Market volatility"],
            success_metrics=["Total value locked", "Transaction volume", "Protocol adoption"]
        ),
        
        ProjectData(
            project_id="IFT_GOVERNANCE_001",
            name="Decentralized Governance Platform",
            description="On-chain governance and decision-making tools",
            ecosystem="ift",
            construction_duration=18,
            construction_cost=2.8,
            strategic_value=0.88,
            technical_complexity=0.80,
            market_impact=0.75,
            resource_requirement=0.75,
            innovation_level=0.82,
            cooperation_projects=["IFT_FINANCE_001", "STATUS_APP_001"],
            precedence_projects=[],
            exclusive_projects=[],
            annual_budget_distribution={2024: 1.0, 2025: 1.2, 2026: 0.6},
            start_date="2024-03-15",
            end_date="2025-09-15",
            team_size=12,
            technology_stack=["Governance", "Voting", "Smart Contracts", "UI/UX"],
            risk_factors=["Governance attacks", "Voter apathy", "Complexity"],
            success_metrics=["Proposal volume", "Voter participation", "Decision quality"]
        )
    ]
    return projects


def generate_stakeholder_evaluations(projects: List[ProjectData]) -> List[QualitativeEvaluation]:
    """Generate qualitative evaluations from various stakeholders"""
    evaluations = []
    project_names = [p.name for p in projects]
    
    # CEO/Leadership evaluations - Strategic focus
    evaluations.extend([
        QualitativeEvaluation(
            evaluator_id="CEO_Logos",
            evaluation_type=EvaluationType.RANKING,
            projects=["Logos Core Infrastructure", "Status Mobile Application", "Nimbus Ethereum 2.0 Client", "Decentralized Finance Infrastructure"],
            confidence=0.95,
            criteria="strategic_value",
            metadata={"role": "executive", "focus": "strategic_alignment"}
        ),
        
        QualitativeEvaluation(
            evaluator_id="CEO_Logos",
            evaluation_type=EvaluationType.THRESHOLD,
            projects=["Status Network Infrastructure"],
            operator=ComparisonOperator.GREATER_EQUAL,
            values=[0.85],
            confidence=0.90,
            criteria="strategic_value",
            metadata={"role": "executive", "rationale": "critical_for_ecosystem"}
        )
    ])
    
    # CTO evaluations - Technical complexity and innovation
    evaluations.extend([
        QualitativeEvaluation(
            evaluator_id="CTO_Technical",
            evaluation_type=EvaluationType.COMPARISON,
            projects=["Advanced Cryptography Research", "Nomos Consensus Layer"],
            operator=ComparisonOperator.GREATER,
            confidence=0.85,
            criteria="technical_complexity",
            metadata={"role": "technical", "focus": "innovation"}
        ),
        
        QualitativeEvaluation(
            evaluator_id="CTO_Technical",
            evaluation_type=EvaluationType.RANGE,
            projects=["Nimbus Light Client"],
            values=[0.6, 0.8],
            confidence=0.80,
            criteria="technical_complexity",
            metadata={"role": "technical", "rationale": "moderate_complexity"}
        )
    ])
    
    # CFO evaluations - Cost and resource efficiency
    evaluations.extend([
        QualitativeEvaluation(
            evaluator_id="CFO_Finance",
            evaluation_type=EvaluationType.COMPARISON,
            projects=["Status Network Infrastructure", "Status Keycard Hardware"],
            operator=ComparisonOperator.GREATER,
            confidence=0.90,
            criteria="resource_requirement",
            metadata={"role": "financial", "focus": "resource_optimization"}
        ),
        
        QualitativeEvaluation(
            evaluator_id="CFO_Finance",
            evaluation_type=EvaluationType.THRESHOLD,
            projects=["Waku Communication Protocol"],
            operator=ComparisonOperator.LESS_EQUAL,
            values=[0.75],
            confidence=0.85,
            criteria="resource_requirement",
            metadata={"role": "financial", "rationale": "budget_constraint"}
        )
    ])
    
    # Product Manager evaluations - Market impact
    evaluations.extend([
        QualitativeEvaluation(
            evaluator_id="PM_Product",
            evaluation_type=EvaluationType.RANKING,
            projects=["Status Mobile Application", "Nimbus Ethereum 2.0 Client", "Decentralized Finance Infrastructure"],
            confidence=0.88,
            criteria="market_impact",
            metadata={"role": "product", "focus": "user_adoption"}
        ),
        
        QualitativeEvaluation(
            evaluator_id="PM_Product",
            evaluation_type=EvaluationType.RANGE,
            projects=["Portal Network Implementation"],
            values=[0.7, 0.8],
            confidence=0.75,
            criteria="market_impact",
            metadata={"role": "product", "rationale": "niche_but_important"}
        )
    ])
    
    # Research Director evaluations - Innovation level
    evaluations.extend([
        QualitativeEvaluation(
            evaluator_id="Research_Director",
            evaluation_type=EvaluationType.COMPARISON,
            projects=["Zero-Knowledge Proof Systems", "Advanced Cryptography Research"],
            operator=ComparisonOperator.EQUAL,
            confidence=0.92,
            criteria="innovation_level",
            metadata={"role": "research", "focus": "breakthrough_potential"}
        ),
        
        QualitativeEvaluation(
            evaluator_id="Research_Director",
            evaluation_type=EvaluationType.THRESHOLD,
            projects=["Nomos Consensus Layer"],
            operator=ComparisonOperator.GREATER_EQUAL,
            values=[0.90],
            confidence=0.88,
            criteria="innovation_level",
            metadata={"role": "research", "rationale": "novel_consensus"}
        )
    ])
    
    # Community Representative evaluations
    evaluations.extend([
        QualitativeEvaluation(
            evaluator_id="Community_Rep",
            evaluation_type=EvaluationType.COMPARISON,
            projects=["Status Mobile Application", "Status Desktop Application"],
            operator=ComparisonOperator.GREATER,
            confidence=0.80,
            criteria="market_impact",
            metadata={"role": "community", "focus": "user_experience"}
        ),
        
        QualitativeEvaluation(
            evaluator_id="Community_Rep",
            evaluation_type=EvaluationType.RANKING,
            projects=["Waku Communication Protocol", "Status Keycard Hardware", "Nimbus Light Client"],
            confidence=0.75,
            criteria="strategic_value",
            metadata={"role": "community", "focus": "ecosystem_value"}
        )
    ])
    
    return evaluations


def export_project_data(projects: List[ProjectData], filename: str):
    """Export project data to JSON and CSV formats"""
    
    # Export to JSON
    json_data = {
        "metadata": {
            "generated_date": datetime.now().isoformat(),
            "total_projects": len(projects),
            "ecosystems": list(set(p.ecosystem for p in projects)),
            "total_budget": sum(p.construction_cost for p in projects),
            "description": "Mock project data for Logos/Nimbus/Status ecosystem portfolio selection"
        },
        "projects": [asdict(project) for project in projects]
    }
    
    with open(f"{filename}.json", 'w') as f:
        json.dump(json_data, f, indent=2)
    
    # Export to CSV
    with open(f"{filename}.csv", 'w', newline='') as f:
        if projects:
            fieldnames = list(asdict(projects[0]).keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for project in projects:
                row = asdict(project)
                # Convert lists and dicts to strings for CSV
                for key, value in row.items():
                    if isinstance(value, (list, dict)):
                        row[key] = json.dumps(value)
                writer.writerow(row)


def generate_budget_constraints(projects: List[ProjectData]) -> Dict[str, Any]:
    """Generate annual budget constraints B_t"""
    budget_constraints = {
        "annual_budgets": {
            2024: 12.0,  # $12M budget for 2024
            2025: 15.0,  # $15M budget for 2025
            2026: 8.0    # $8M budget for 2026
        },
        "constraint_violations": [],
        "utilization_rates": {}
    }
    
    # Calculate utilization for each year
    for year in [2024, 2025, 2026]:
        total_allocated = sum(
            project.annual_budget_distribution.get(year, 0) 
            for project in projects
        )
        budget_limit = budget_constraints["annual_budgets"][year]
        utilization = total_allocated / budget_limit
        
        budget_constraints["utilization_rates"][year] = {
            "allocated": total_allocated,
            "limit": budget_limit,
            "utilization_rate": utilization,
            "over_budget": utilization > 1.0
        }
        
        if utilization > 1.0:
            budget_constraints["constraint_violations"].append({
                "year": year,
                "excess": total_allocated - budget_limit,
                "projects_affected": [
                    p.project_id for p in projects 
                    if p.annual_budget_distribution.get(year, 0) > 0
                ]
            })
    
    return budget_constraints


def main():
    """Generate complete project portfolio dataset"""
    print("Generating Logos/Nimbus/Status Project Portfolio Data...")
    
    # Generate all projects
    all_projects = []
    all_projects.extend(generate_logos_projects())
    all_projects.extend(generate_nimbus_projects())
    all_projects.extend(generate_status_projects())
    all_projects.extend(generate_vac_projects())
    all_projects.extend(generate_ift_projects())
    
    print(f"Generated {len(all_projects)} projects across {len(set(p.ecosystem for p in all_projects))} ecosystems")
    
    # Generate stakeholder evaluations
    evaluations = generate_stakeholder_evaluations(all_projects)
    print(f"Generated {len(evaluations)} stakeholder evaluations")
    
    # Generate budget constraints
    budget_constraints = generate_budget_constraints(all_projects)
    print(f"Generated budget constraints for {len(budget_constraints['annual_budgets'])} years")
    
    # Export data
    export_project_data(all_projects, "logos_nimbus_status_projects")
    
    # Export evaluations
    from evaluation_input_parser import EvaluationExporter
    EvaluationExporter.to_json(evaluations, "stakeholder_evaluations.json")
    EvaluationExporter.to_csv(evaluations, "stakeholder_evaluations.csv")
    
    # Export budget constraints
    with open("budget_constraints.json", 'w') as f:
        json.dump(budget_constraints, f, indent=2)
    
    # Summary statistics
    print("\n" + "="*60)
    print("PROJECT PORTFOLIO SUMMARY")
    print("="*60)
    
    ecosystems = {}
    for project in all_projects:
        if project.ecosystem not in ecosystems:
            ecosystems[project.ecosystem] = []
        ecosystems[project.ecosystem].append(project)
    
    for ecosystem, projects in ecosystems.items():
        total_cost = sum(p.construction_cost for p in projects)
        avg_duration = sum(p.construction_duration for p in projects) / len(projects)
        avg_strategic_value = sum(p.strategic_value for p in projects) / len(projects)
        
        print(f"\n{ecosystem.upper()} Ecosystem:")
        print(f"  Projects: {len(projects)}")
        print(f"  Total Cost: ${total_cost:.1f}M")
        print(f"  Average Duration: {avg_duration:.1f} months")
        print(f"  Average Strategic Value: {avg_strategic_value:.2f}")
        
        for project in projects:
            print(f"    - {project.name} (${project.construction_cost:.1f}M, {project.construction_duration}mo)")
    
    # Overall statistics
    total_cost = sum(p.construction_cost for p in all_projects)
    total_duration = sum(p.construction_duration for p in all_projects)
    
    print(f"\nOVERALL PORTFOLIO:")
    print(f"  Total Projects: {len(all_projects)}")
    print(f"  Total Investment: ${total_cost:.1f}M")
    print(f"  Total Development Time: {total_duration} project-months")
    print(f"  Average Project Cost: ${total_cost/len(all_projects):.1f}M")
    print(f"  Budget Utilization: {sum(budget_constraints['utilization_rates'][year]['utilization_rate'] for year in [2024, 2025, 2026])/3:.1%}")
    
    # Constraint analysis
    print(f"\nCONSTRAINT ANALYSIS:")
    cooperation_count = sum(len(p.cooperation_projects) for p in all_projects)
    precedence_count = sum(len(p.precedence_projects) for p in all_projects)
    exclusive_count = sum(len(p.exclusive_projects) for p in all_projects)
    
    print(f"  Cooperation constraints: {cooperation_count}")
    print(f"  Precedence constraints: {precedence_count}")
    print(f"  Exclusivity constraints: {exclusive_count}")
    print(f"  Budget violations: {len(budget_constraints['constraint_violations'])}")
    
    print(f"\nData exported to:")
    print(f"  - logos_nimbus_status_projects.json")
    print(f"  - logos_nimbus_status_projects.csv")
    print(f"  - stakeholder_evaluations.json")
    print(f"  - stakeholder_evaluations.csv")
    print(f"  - budget_constraints.json")


if __name__ == "__main__":
    main()
