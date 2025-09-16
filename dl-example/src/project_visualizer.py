"""
Project Portfolio Visualizer for Logos/Nimbus/Status Ecosystem

This module creates interactive visualizations of the project portfolio,
including project details, relationships, timelines, and key metrics.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import sys
import os

# Add the current directory to the path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logos_nimbus_status_projects import (
    generate_logos_projects,
    generate_nimbus_projects, 
    generate_status_projects,
    generate_vac_projects,
    generate_ift_projects,
    ProjectData
)


class ProjectPortfolioVisualizer:
    """Interactive visualizer for project portfolio data"""
    
    def __init__(self):
        """Initialize the visualizer with project data"""
        self.projects = self._load_all_projects()
        self.df = self._create_dataframe()
        
    def _load_all_projects(self) -> List[ProjectData]:
        """Load all projects from different ecosystems"""
        all_projects = []
        all_projects.extend(generate_logos_projects())
        all_projects.extend(generate_nimbus_projects())
        all_projects.extend(generate_status_projects())
        all_projects.extend(generate_vac_projects())
        all_projects.extend(generate_ift_projects())
        return all_projects
        
    def _create_dataframe(self) -> pd.DataFrame:
        """Convert project data to pandas DataFrame for easier manipulation"""
        data = []
        for project in self.projects:
            data.append({
                'project_id': project.project_id,
                'name': project.name,
                'description': project.description,
                'ecosystem': project.ecosystem,
                'duration': project.construction_duration,
                'cost': project.construction_cost,
                'strategic_value': project.strategic_value,
                'technical_complexity': project.technical_complexity,
                'market_impact': project.market_impact,
                'resource_requirement': project.resource_requirement,
                'innovation_level': project.innovation_level,
                'team_size': project.team_size,
                'start_date': project.start_date,
                'end_date': project.end_date,
                'cooperation_count': len(project.cooperation_projects),
                'precedence_count': len(project.precedence_projects),
                'exclusive_count': len(project.exclusive_projects),
                'technology_stack': ', '.join(project.technology_stack),
                'risk_factors': ', '.join(project.risk_factors),
                'success_metrics': ', '.join(project.success_metrics)
            })
        return pd.DataFrame(data)
        
    def create_ecosystem_overview(self) -> go.Figure:
        """Create ecosystem overview visualization"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                'Projects by Ecosystem',
                'Investment by Ecosystem', 
                'Strategic Value vs Cost',
                'Innovation vs Complexity'
            ],
            specs=[
                [{"type": "pie"}, {"type": "bar"}],
                [{"type": "scatter"}, {"type": "scatter"}]
            ]
        )
        
        # Projects by ecosystem (pie chart)
        ecosystem_counts = self.df['ecosystem'].value_counts()
        fig.add_trace(
            go.Pie(
                labels=ecosystem_counts.index,
                values=ecosystem_counts.values,
                name="Projects",
                hovertemplate="<b>%{label}</b><br>Projects: %{value}<br>Percentage: %{percent}<extra></extra>"
            ),
            row=1, col=1
        )
        
        # Investment by ecosystem (bar chart)
        ecosystem_investment = self.df.groupby('ecosystem')['cost'].sum().sort_values(ascending=True)
        fig.add_trace(
            go.Bar(
                x=ecosystem_investment.values,
                y=ecosystem_investment.index,
                orientation='h',
                name="Investment",
                marker_color=px.colors.qualitative.Set3,
                hovertemplate="<b>%{y}</b><br>Investment: $%{x:.1f}M<extra></extra>"
            ),
            row=1, col=2
        )
        
        # Strategic value vs cost scatter
        colors = px.colors.qualitative.Set1
        ecosystem_colors = {eco: colors[i % len(colors)] for i, eco in enumerate(self.df['ecosystem'].unique())}
        
        for ecosystem in self.df['ecosystem'].unique():
            eco_data = self.df[self.df['ecosystem'] == ecosystem]
            fig.add_trace(
                go.Scatter(
                    x=eco_data['cost'],
                    y=eco_data['strategic_value'],
                    mode='markers',
                    name=ecosystem,
                    marker=dict(
                        size=eco_data['team_size'],
                        color=ecosystem_colors[ecosystem],
                        sizemode='diameter',
                        sizeref=2.*max(self.df['team_size'])/(40.**2),
                        sizemin=4
                    ),
                    text=eco_data['name'],
                    hovertemplate="<b>%{text}</b><br>Cost: $%{x:.1f}M<br>Strategic Value: %{y:.2f}<br>Team Size: %{marker.size}<extra></extra>",
                    showlegend=False
                ),
                row=2, col=1
            )
            
        # Innovation vs complexity scatter
        for ecosystem in self.df['ecosystem'].unique():
            eco_data = self.df[self.df['ecosystem'] == ecosystem]
            fig.add_trace(
                go.Scatter(
                    x=eco_data['technical_complexity'],
                    y=eco_data['innovation_level'],
                    mode='markers',
                    name=ecosystem,
                    marker=dict(
                        size=eco_data['duration'],
                        color=ecosystem_colors[ecosystem],
                        sizemode='diameter',
                        sizeref=2.*max(self.df['duration'])/(40.**2),
                        sizemin=4
                    ),
                    text=eco_data['name'],
                    hovertemplate="<b>%{text}</b><br>Complexity: %{x:.2f}<br>Innovation: %{y:.2f}<br>Duration: %{marker.size} months<extra></extra>",
                    showlegend=False
                ),
                row=2, col=2
            )
        
        fig.update_layout(
            title="Project Portfolio Ecosystem Overview",
            height=800,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Investment ($M)", row=1, col=2)
        fig.update_xaxes(title_text="Cost ($M)", row=2, col=1)
        fig.update_xaxes(title_text="Technical Complexity", row=2, col=2)
        fig.update_yaxes(title_text="Strategic Value", row=2, col=1)
        fig.update_yaxes(title_text="Innovation Level", row=2, col=2)
        
        return fig
        
    def create_project_timeline(self) -> go.Figure:
        """Create project timeline Gantt chart"""
        # Prepare data for Gantt chart
        gantt_data = []
        for _, project in self.df.iterrows():
            gantt_data.append({
                'Task': project['name'],
                'Start': project['start_date'],
                'Finish': project['end_date'],
                'Resource': project['ecosystem'],
                'Cost': project['cost'],
                'Team': project['team_size']
            })
        
        gantt_df = pd.DataFrame(gantt_data)
        gantt_df['Start'] = pd.to_datetime(gantt_df['Start'])
        gantt_df['Finish'] = pd.to_datetime(gantt_df['Finish'])
        
        fig = px.timeline(
            gantt_df,
            x_start="Start",
            x_end="Finish", 
            y="Task",
            color="Resource",
            title="Project Portfolio Timeline",
            hover_data=["Cost", "Team"]
        )
        
        fig.update_yaxes(categoryorder="total ascending")
        fig.update_layout(
            height=600,
            xaxis_title="Timeline",
            yaxis_title="Projects"
        )
        
        return fig
        
    def create_project_relationships(self) -> go.Figure:
        """Create network graph showing project relationships"""
        import networkx as nx
        
        # Create network graph
        G = nx.Graph()
        
        # Add nodes (projects)
        for project in self.projects:
            G.add_node(
                project.project_id,
                name=project.name,
                ecosystem=project.ecosystem,
                cost=project.construction_cost,
                strategic_value=project.strategic_value
            )
        
        # Add edges (relationships)
        for project in self.projects:
            # Cooperation relationships
            for coop_project in project.cooperation_projects:
                # Find project by name
                coop_id = None
                for p in self.projects:
                    if p.name == coop_project:
                        coop_id = p.project_id
                        break
                if coop_id:
                    G.add_edge(project.project_id, coop_id, relationship='cooperation')
            
            # Precedence relationships
            for prec_project in project.precedence_projects:
                prec_id = None
                for p in self.projects:
                    if p.name == prec_project:
                        prec_id = p.project_id
                        break
                if prec_id:
                    G.add_edge(project.project_id, prec_id, relationship='precedence')
        
        # Generate layout
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # Create edge traces
        edge_x = []
        edge_y = []
        edge_info = []
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        # Create node traces
        node_x = []
        node_y = []
        node_text = []
        node_color = []
        node_size = []
        
        ecosystem_colors = {
            'logos': '#FF6B6B',
            'nimbus': '#4ECDC4', 
            'status': '#45B7D1',
            'vac': '#96CEB4',
            'ift': '#FFEAA7'
        }
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            node_info = G.nodes[node]
            node_text.append(f"{node_info['name']}<br>Cost: ${node_info['cost']:.1f}M<br>Strategic Value: {node_info['strategic_value']:.2f}")
            node_color.append(ecosystem_colors.get(node_info['ecosystem'], '#888'))
            node_size.append(node_info['cost'] * 5 + 10)  # Size based on cost
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=[G.nodes[node]['name'] for node in G.nodes()],
            textposition="middle center",
            hovertext=node_text,
            marker=dict(
                size=node_size,
                color=node_color,
                line=dict(width=2, color='white')
            )
        )
        
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title=dict(text='Project Relationship Network', font=dict(size=16)),
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           annotations=[ dict(
                               text="Node size represents project cost. Colors represent ecosystems.",
                               showarrow=False,
                               xref="paper", yref="paper",
                               x=0.005, y=-0.002,
                               xanchor="left", yanchor="bottom",
                               font=dict(color="#888", size=12)
                           )],
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                       ))
        
        return fig
        
    def create_project_metrics_radar(self) -> go.Figure:
        """Create radar chart comparing project metrics"""
        fig = go.Figure()
        
        metrics = ['strategic_value', 'technical_complexity', 'market_impact', 
                  'resource_requirement', 'innovation_level']
        
        # Add trace for each ecosystem
        ecosystem_colors = {
            'logos': '#FF6B6B',
            'nimbus': '#4ECDC4', 
            'status': '#45B7D1',
            'vac': '#96CEB4',
            'ift': '#FFEAA7'
        }
        
        for ecosystem in self.df['ecosystem'].unique():
            eco_data = self.df[self.df['ecosystem'] == ecosystem]
            avg_metrics = [eco_data[metric].mean() for metric in metrics]
            
            fig.add_trace(go.Scatterpolar(
                r=avg_metrics,
                theta=metrics,
                fill='toself',
                name=ecosystem.upper(),
                line_color=ecosystem_colors.get(ecosystem, '#888')
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="Average Project Metrics by Ecosystem"
        )
        
        return fig
        
    def create_detailed_project_table(self) -> go.Figure:
        """Create detailed project information table"""
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=['Project', 'Ecosystem', 'Duration<br>(months)', 'Cost<br>($M)', 
                        'Strategic<br>Value', 'Market<br>Impact', 'Team<br>Size', 'Technology Stack'],
                fill_color='paleturquoise',
                align='left',
                font=dict(size=12)
            ),
            cells=dict(
                values=[
                    self.df['name'],
                    self.df['ecosystem'].str.upper(),
                    self.df['duration'],
                    self.df['cost'].round(1),
                    self.df['strategic_value'].round(2),
                    self.df['market_impact'].round(2),
                    self.df['team_size'],
                    [tech[:50] + '...' if len(tech) > 50 else tech for tech in self.df['technology_stack']]
                ],
                fill_color='lavender',
                align='left',
                font=dict(size=10)
            )
        )])
        
        fig.update_layout(
            title="Detailed Project Information",
            height=600
        )
        
        return fig
        
    def create_budget_analysis(self) -> go.Figure:
        """Create budget analysis visualization"""
        # Calculate annual budget distribution
        budget_data = []
        for project in self.projects:
            for year, amount in project.annual_budget_distribution.items():
                budget_data.append({
                    'year': year,
                    'project': project.name,
                    'ecosystem': project.ecosystem,
                    'amount': amount
                })
        
        budget_df = pd.DataFrame(budget_data)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                'Annual Budget Distribution',
                'Budget by Ecosystem per Year',
                'Cumulative Investment Timeline',
                'Project Cost Distribution'
            ],
            specs=[
                [{"type": "bar"}, {"type": "bar"}],
                [{"type": "scatter"}, {"type": "histogram"}]
            ]
        )
        
        # Annual budget distribution
        annual_totals = budget_df.groupby('year')['amount'].sum()
        fig.add_trace(
            go.Bar(
                x=annual_totals.index,
                y=annual_totals.values,
                name="Total Budget",
                marker_color='lightblue',
                hovertemplate="Year: %{x}<br>Budget: $%{y:.1f}M<extra></extra>"
            ),
            row=1, col=1
        )
        
        # Budget by ecosystem per year
        ecosystem_budget = budget_df.groupby(['year', 'ecosystem'])['amount'].sum().unstack(fill_value=0)
        for ecosystem in ecosystem_budget.columns:
            fig.add_trace(
                go.Bar(
                    x=ecosystem_budget.index,
                    y=ecosystem_budget[ecosystem],
                    name=ecosystem.upper(),
                    hovertemplate=f"{ecosystem.upper()}<br>Year: %{{x}}<br>Budget: $%{{y:.1f}}M<extra></extra>"
                ),
                row=1, col=2
            )
        
        # Cumulative investment timeline
        self.df['start_date_dt'] = pd.to_datetime(self.df['start_date'])
        sorted_projects = self.df.sort_values('start_date_dt')
        cumulative_cost = sorted_projects['cost'].cumsum()
        
        fig.add_trace(
            go.Scatter(
                x=sorted_projects['start_date_dt'],
                y=cumulative_cost,
                mode='lines+markers',
                name="Cumulative Investment",
                line=dict(color='green', width=3),
                hovertemplate="Date: %{x}<br>Cumulative: $%{y:.1f}M<extra></extra>"
            ),
            row=2, col=1
        )
        
        # Project cost distribution
        fig.add_trace(
            go.Histogram(
                x=self.df['cost'],
                nbinsx=10,
                name="Cost Distribution",
                marker_color='orange',
                hovertemplate="Cost Range: $%{x:.1f}M<br>Count: %{y}<extra></extra>"
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title="Budget and Investment Analysis",
            height=800,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Year", row=1, col=1)
        fig.update_xaxes(title_text="Year", row=1, col=2)
        fig.update_xaxes(title_text="Start Date", row=2, col=1)
        fig.update_xaxes(title_text="Project Cost ($M)", row=2, col=2)
        fig.update_yaxes(title_text="Budget ($M)", row=1, col=1)
        fig.update_yaxes(title_text="Budget ($M)", row=1, col=2)
        fig.update_yaxes(title_text="Cumulative Investment ($M)", row=2, col=1)
        fig.update_yaxes(title_text="Number of Projects", row=2, col=2)
        
        return fig
        
    def create_comprehensive_dashboard(self) -> go.Figure:
        """Create comprehensive project portfolio dashboard"""
        # This will be a multi-tab dashboard combining all visualizations
        # For now, we'll create a summary dashboard with key metrics
        
        fig = make_subplots(
            rows=3, cols=3,
            subplot_titles=[
                'Portfolio Summary', 'Risk vs Innovation', 'Team Size Distribution',
                'Duration vs Cost', 'Strategic Value Ranking', 'Technology Diversity',
                'Ecosystem Investment', 'Project Complexity', 'Success Factors'
            ],
            specs=[
                [{"type": "indicator"}, {"type": "scatter"}, {"type": "box"}],
                [{"type": "scatter"}, {"type": "bar"}, {"type": "pie"}],
                [{"type": "bar"}, {"type": "heatmap"}, {"type": "bar"}]
            ]
        )
        
        # Portfolio summary indicators
        total_projects = len(self.df)
        total_investment = self.df['cost'].sum()
        avg_strategic_value = self.df['strategic_value'].mean()
        
        fig.add_trace(
            go.Indicator(
                mode="number+gauge+delta",
                value=total_investment,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={"text": f"Total Investment<br>${total_investment:.1f}M<br>{total_projects} Projects"},
                gauge={'axis': {'range': [None, 50]},
                      'bar': {'color': "darkblue"},
                      'steps': [{'range': [0, 25], 'color': "lightgray"},
                               {'range': [25, 50], 'color': "gray"}],
                      'threshold': {'line': {'color': "red", 'width': 4},
                                   'thickness': 0.75, 'value': 40}}
            ),
            row=1, col=1
        )
        
        # Risk vs Innovation scatter
        fig.add_trace(
            go.Scatter(
                x=self.df['technical_complexity'],
                y=self.df['innovation_level'],
                mode='markers',
                marker=dict(
                    size=self.df['cost']*3,
                    color=self.df['strategic_value'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Strategic Value")
                ),
                text=self.df['name'],
                hovertemplate="<b>%{text}</b><br>Complexity: %{x:.2f}<br>Innovation: %{y:.2f}<extra></extra>",
                showlegend=False
            ),
            row=1, col=2
        )
        
        # Team size distribution by ecosystem
        for ecosystem in self.df['ecosystem'].unique():
            eco_data = self.df[self.df['ecosystem'] == ecosystem]
            fig.add_trace(
                go.Box(
                    y=eco_data['team_size'],
                    name=ecosystem.upper(),
                    showlegend=False
                ),
                row=1, col=3
            )
        
        # Duration vs Cost
        fig.add_trace(
            go.Scatter(
                x=self.df['duration'],
                y=self.df['cost'],
                mode='markers',
                marker=dict(size=8, color='red'),
                text=self.df['name'],
                hovertemplate="<b>%{text}</b><br>Duration: %{x} months<br>Cost: $%{y:.1f}M<extra></extra>",
                showlegend=False
            ),
            row=2, col=1
        )
        
        # Strategic value ranking
        top_projects = self.df.nlargest(8, 'strategic_value')
        fig.add_trace(
            go.Bar(
                x=top_projects['strategic_value'],
                y=top_projects['name'],
                orientation='h',
                marker_color='green',
                showlegend=False,
                hovertemplate="<b>%{y}</b><br>Strategic Value: %{x:.2f}<extra></extra>"
            ),
            row=2, col=2
        )
        
        # Technology diversity (simplified)
        tech_counts = {}
        for tech_stack in self.df['technology_stack']:
            for tech in tech_stack.split(', '):
                tech = tech.strip()
                if tech:
                    tech_counts[tech] = tech_counts.get(tech, 0) + 1
        
        top_techs = sorted(tech_counts.items(), key=lambda x: x[1], reverse=True)[:8]
        fig.add_trace(
            go.Pie(
                labels=[tech[0] for tech in top_techs],
                values=[tech[1] for tech in top_techs],
                showlegend=False,
                hovertemplate="<b>%{label}</b><br>Projects: %{value}<extra></extra>"
            ),
            row=2, col=3
        )
        
        # Ecosystem investment
        ecosystem_investment = self.df.groupby('ecosystem')['cost'].sum().sort_values()
        fig.add_trace(
            go.Bar(
                x=ecosystem_investment.index,
                y=ecosystem_investment.values,
                marker_color='blue',
                showlegend=False,
                hovertemplate="<b>%{x}</b><br>Investment: $%{y:.1f}M<extra></extra>"
            ),
            row=3, col=1
        )
        
        # Project complexity heatmap (simplified)
        metrics_matrix = self.df[['strategic_value', 'technical_complexity', 'market_impact', 'innovation_level']].head(8)
        fig.add_trace(
            go.Heatmap(
                z=metrics_matrix.values,
                x=['Strategic', 'Technical', 'Market', 'Innovation'],
                y=self.df['name'].head(8),
                colorscale='RdYlBu',
                showscale=False,
                hovertemplate="Project: %{y}<br>Metric: %{x}<br>Value: %{z:.2f}<extra></extra>"
            ),
            row=3, col=2
        )
        
        # Success factors (risk count)
        risk_counts = [len(risk.split(', ')) for risk in self.df['risk_factors']]
        fig.add_trace(
            go.Bar(
                x=self.df['name'][:8],
                y=risk_counts[:8],
                marker_color='orange',
                showlegend=False,
                hovertemplate="<b>%{x}</b><br>Risk Factors: %{y}<extra></extra>"
            ),
            row=3, col=3
        )
        
        fig.update_layout(
            title="Project Portfolio Comprehensive Dashboard",
            height=1200,
            showlegend=False
        )
        
        # Update axis labels
        fig.update_xaxes(title_text="Technical Complexity", row=1, col=2)
        fig.update_yaxes(title_text="Innovation Level", row=1, col=2)
        fig.update_yaxes(title_text="Team Size", row=1, col=3)
        fig.update_xaxes(title_text="Duration (months)", row=2, col=1)
        fig.update_yaxes(title_text="Cost ($M)", row=2, col=1)
        fig.update_xaxes(title_text="Strategic Value", row=2, col=2)
        fig.update_xaxes(title_text="Ecosystem", row=3, col=1)
        fig.update_yaxes(title_text="Investment ($M)", row=3, col=1)
        fig.update_xaxes(title_text="Projects", row=3, col=3)
        fig.update_yaxes(title_text="Risk Factors", row=3, col=3)
        
        return fig
        
    def generate_all_visualizations(self):
        """Generate and save all visualizations"""
        print("🎨 Generating Project Portfolio Visualizations...")
        print("=" * 60)
        
        # Generate all visualizations
        visualizations = {
            'ecosystem_overview': self.create_ecosystem_overview(),
            'project_timeline': self.create_project_timeline(),
            'project_relationships': self.create_project_relationships(),
            'metrics_radar': self.create_project_metrics_radar(),
            'project_table': self.create_detailed_project_table(),
            'budget_analysis': self.create_budget_analysis(),
            'comprehensive_dashboard': self.create_comprehensive_dashboard()
        }
        
        # Save visualizations to proper directory
        import os
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'visualizations', 'portfolio')
        os.makedirs(output_dir, exist_ok=True)
        
        for name, fig in visualizations.items():
            filename = f"project_portfolio_{name}.html"
            filepath = os.path.join(output_dir, filename)
            fig.write_html(filepath)
            print(f"   ✓ {filename}")
        
        print()
        print("📊 PORTFOLIO STATISTICS")
        print("=" * 30)
        print(f"Total Projects: {len(self.df)}")
        print(f"Total Investment: ${self.df['cost'].sum():.1f}M")
        print(f"Average Project Cost: ${self.df['cost'].mean():.1f}M")
        print(f"Average Duration: {self.df['duration'].mean():.1f} months")
        print(f"Average Team Size: {self.df['team_size'].mean():.1f} people")
        print()
        
        print("🏢 BY ECOSYSTEM")
        print("=" * 20)
        for ecosystem in self.df['ecosystem'].unique():
            eco_data = self.df[self.df['ecosystem'] == ecosystem]
            print(f"{ecosystem.upper()}:")
            print(f"  Projects: {len(eco_data)}")
            print(f"  Investment: ${eco_data['cost'].sum():.1f}M")
            print(f"  Avg Strategic Value: {eco_data['strategic_value'].mean():.2f}")
        print()
        
        print("🎯 TOP PROJECTS BY STRATEGIC VALUE")
        print("=" * 40)
        top_strategic = self.df.nlargest(5, 'strategic_value')[['name', 'ecosystem', 'strategic_value', 'cost']]
        for _, project in top_strategic.iterrows():
            print(f"  {project['name']} ({project['ecosystem'].upper()})")
            print(f"    Strategic Value: {project['strategic_value']:.2f}, Cost: ${project['cost']:.1f}M")
        print()
        
        print("💡 INNOVATION LEADERS")
        print("=" * 25)
        top_innovation = self.df.nlargest(5, 'innovation_level')[['name', 'ecosystem', 'innovation_level', 'technical_complexity']]
        for _, project in top_innovation.iterrows():
            print(f"  {project['name']} ({project['ecosystem'].upper()})")
            print(f"    Innovation: {project['innovation_level']:.2f}, Complexity: {project['technical_complexity']:.2f}")
        print()
        
        print("🌐 Generated Interactive Visualizations:")
        print("  • project_portfolio_ecosystem_overview.html - Ecosystem analysis")
        print("  • project_portfolio_project_timeline.html - Project timeline")
        print("  • project_portfolio_project_relationships.html - Relationship network")
        print("  • project_portfolio_metrics_radar.html - Metrics comparison")
        print("  • project_portfolio_project_table.html - Detailed project table")
        print("  • project_portfolio_budget_analysis.html - Budget and investment analysis")
        print("  • project_portfolio_comprehensive_dashboard.html - Complete dashboard")
        print()
        print("Open these HTML files in a web browser to explore the interactive visualizations!")


def main():
    """Main function to generate project portfolio visualizations"""
    visualizer = ProjectPortfolioVisualizer()
    visualizer.generate_all_visualizations()


if __name__ == "__main__":
    main()
