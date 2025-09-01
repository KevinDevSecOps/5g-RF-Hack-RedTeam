"""
Sistema avanzado de generación de reports para pentesting 5G
"""
import logging
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from weasyprint import HTML
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from jinja2 import Environment, FileSystemLoader
import os

logger = logging.getLogger(__name__)

class AdvancedReportGenerator:
    def __init__(self, core):
        self.core = core
        self.logger = logger
        self.env = Environment(loader=FileSystemLoader('src/dashboard/templates/reports'))
        self.reports_dir = './data/reports'
        os.makedirs(self.reports_dir, exist_ok=True)
        
    def generate_executive_summary(self, scan_data, threats_data, output_format='pdf'):
        """
        Generar reporte ejecutivo resumido
        """
        try:
            # Preparar datos para el template
            report_data = {
                'title': '5G Security Assessment - Executive Summary',
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'scan_duration': scan_data.get('duration', 'N/A'),
                'total_threats': len(threats_data),
                'threats_by_severity': self._categorize_threats(threats_data),
                'top_threats': threats_data[:5],
                'risk_score': self._calculate_risk_score(threats_data),
                'recommendations': self._generate_recommendations(threats_data)
            }
            
            # Renderizar template HTML
            template = self.env.get_template('executive_summary.html')
            html_content = template.render(report_data)
            
            # Generar output
            filename = f"5g_executive_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            if output_format.lower() == 'pdf':
                return self._generate_pdf(html_content, filename)
            elif output_format.lower() == 'html':
                return self._generate_html(html_content, filename)
            else:
                return self._generate_json(report_data, filename)
                
        except Exception as e:
            self.logger.error(f"Error generating executive summary: {e}")
            return None
    
    def generate_technical_report(self, detailed_data, output_format='pdf'):
        """
        Generar reporte técnico detallado
        """
        try:
            # Datos para el reporte técnico
            report_data = {
                'title': '5G Security Technical Report',
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'scan_results': detailed_data.get('scan_results', {}),
                'threat_analysis': detailed_data.get('threat_analysis', {}),
                'signal_analysis': detailed_data.get('signal_analysis', {}),
                'network_metrics': detailed_data.get('network_metrics', {}),
                'detailed_findings': detailed_data.get('findings', []),
                'appendix': self._generate_appendix(detailed_data)
            }
            
            # Renderizar y generar reporte
            template = self.env.get_template('technical_report.html')
            html_content = template.render(report_data)
            
            filename = f"5g_technical_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            if output_format.lower() == 'pdf':
                return self._generate_pdf(html_content, filename)
            else:
                return self._generate_html(html_content, filename)
                
        except Exception as e:
            self.logger.error(f"Error generating technical report: {e}")
            return None
    
    def generate_dashboard_report(self, dashboard_data, output_format='html'):
        """
        Generar reporte con dashboards interactivos
        """
        try:
            # Crear visualizaciones
            figures = self._create_dashboard_figures(dashboard_data)
            
            report_data = {
                'title': '5G Security Dashboard Report',
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'figures': figures,
                'metrics': dashboard_data.get('metrics', {}),
                'insights': self._generate_insights(dashboard_data)
            }
            
            template = self.env.get_template('dashboard_report.html')
            html_content = template.render(report_data)
            
            filename = f"5g_dashboard_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            return self._generate_html(html_content, filename)
            
        except Exception as e:
            self.logger.error(f"Error generating dashboard report: {e}")
            return None
    
    def _create_dashboard_figures(self, data):
        """Crear figuras para el dashboard"""
        figures = []
        
        # Gráfico de amenazas por tipo
        threat_fig = go.Figure()
        threat_types = data.get('threat_types', {})
        threat_fig.add_trace(go.Bar(
            x=list(threat_types.keys()),
            y=list(threat_types.values()),
            name='Threats by Type'
        ))
        threat_fig.update_layout(title='Threats by Type')
        figures.append(threat_fig.to_html(full_html=False))
        
        # Gráfico de timeline de detecciones
        timeline_fig = go.Figure()
        timeline_data = data.get('timeline', [])
        if timeline_data:
            timeline_fig.add_trace(go.Scatter(
                x=[item['time'] for item in timeline_data],
                y=[item['count'] for item in timeline_data],
                mode='lines+markers',
                name='Detections Timeline'
            ))
            timeline_fig.update_layout(title='Detection Timeline')
            figures.append(timeline_fig.to_html(full_html=False))
        
        return figures
    
    def _categorize_threats(self, threats):
        """Categorizar amenazas por severidad"""
        categories = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        for threat in threats:
            severity = threat.get('severity', 'medium').lower()
            categories[severity] = categories.get(severity, 0) + 1
        
        return categories
    
    def _calculate_risk_score(self, threats):
        """Calcular score de riesgo general"""
        if not threats:
            return 0
        
        severity_weights = {'critical': 10, 'high': 7, 'medium': 4, 'low': 1}
        total_score = 0
        
        for threat in threats:
            severity = threat.get('severity', 'medium').lower()
            total_score += severity_weights.get(severity, 4)
        
        return min(100, total_score * 10 / len(threats))
    
    def _generate_recommendations(self, threats):
        """Generar recomendaciones basadas en amenazas"""
        recommendations = []
        
        critical_threats = [t for t in threats if t.get('severity') == 'critical']
        if critical_threats:
            recommendations.append({
                'priority': 'critical',
                'text': 'Immediate action required for critical threats detected'
            })
        
        jamming_threats = [t for t in threats if 'jamming' in t.get('type', '').lower()]
        if jamming_threats:
            recommendations.append({
                'priority': 'high',
                'text': 'Implement anti-jamming measures and frequency monitoring'
            })
        
        return recommendations
    
    def _generate_appendix(self, data):
        """Generar apéndice técnico"""
        appendix = {
            'raw_metrics': data.get('raw_metrics', {}),
            'configuration_details': data.get('config', {}),
            'signal_parameters': data.get('signal_params', {})
        }
        return appendix
    
    def _generate_insights(self, data):
        """Generar insights automáticos"""
        insights = []
        
        if data.get('total_threats', 0) > 10:
            insights.append('High number of threats detected - requires comprehensive review')
        
        if data.get('jamming_detected', False):
            insights.append('Jamming activity detected - potential denial of service attack')
        
        return insights
    
    def _generate_pdf(self, html_content, filename):
        """Generar PDF a partir de HTML"""
        try:
            filepath = f"{self.reports_dir}/{filename}.pdf"
            HTML(string=html_content).write_pdf(filepath)
            self.logger.info(f"PDF report generated: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Error generating PDF: {e}")
            return None
    
    def _generate_html(self, html_content, filename):
        """Generar archivo HTML"""
        try:
            filepath = f"{self.reports_dir}/{filename}.html"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            self.logger.info(f"HTML report generated: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Error generating HTML: {e}")
            return None
    
    def _generate_json(self, data, filename):
        """Generar archivo JSON"""
        try:
            filepath = f"{self.reports_dir}/{filename}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"JSON report generated: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Error generating JSON: {e}")
            return None
    
    def list_reports(self):
        """Listar todos los reports generados"""
        try:
            reports = []
            for file in os.listdir(self.reports_dir):
                if file.endswith(('.pdf', '.html', '.json')):
                    filepath = os.path.join(self.reports_dir, file)
                    stats = os.stat(filepath)
                    reports.append({
                        'name': file,
                        'path': filepath,
                        'size': stats.st_size,
                        'created': datetime.fromtimestamp(stats.st_ctime).isoformat()
                    })
            return sorted(reports, key=lambda x: x['created'], reverse=True)
        except Exception as e:
            self.logger.error(f"Error listing reports: {e}")
            return []