from flask import Blueprint, jsonify, request, send_file
import logging
from src.core import get_core_instance
import os

reporting_bp = Blueprint('reporting', __name__)
logger = logging.getLogger(__name__)

@reporting_bp.route('/api/reporting/generate/executive', methods=['POST'])
def generate_executive_report():
    """Generar reporte ejecutivo"""
    try:
        data = request.get_json() or {}
        output_format = data.get('format', 'pdf')
        
        core = get_core_instance()
        report_module = core.get_modules_manager().get_module('report_generator')
        
        if not report_module:
            return jsonify({"error": "Report module not initialized"}), 500
        
        # Datos de ejemplo (en producción vendrían del scanning real)
        scan_data = {
            'duration': '2 hours',
            'frequency_range': '3.4-3.6 GHz'
        }
        
        threats_data = [
            {'type': 'jamming', 'severity': 'critical', 'description': 'Wideband jamming detected'},
            {'type': 'spoofing', 'severity': 'high', 'description': 'Base station spoofing attempt'},
            {'type': 'eavesdropping', 'severity': 'medium', 'description': 'Potential eavesdropping activity'}
        ]
        
        report_path = report_module.generate_executive_summary(
            scan_data, threats_data, output_format
        )
        
        if report_path:
            return jsonify({
                "status": "success",
                "report_path": report_path,
                "download_url": f"/api/reporting/download/{os.path.basename(report_path)}"
            })
        else:
            return jsonify({"error": "Failed to generate report"}), 500
            
    except Exception as e:
        logger.error(f"Error generating executive report: {e}")
        return jsonify({"error": str(e)}), 500

@reporting_bp.route('/api/reporting/generate/technical', methods=['POST'])
def generate_technical_report():
    """Generar reporte técnico"""
    try:
        data = request.get_json() or {}
        output_format = data.get('format', 'pdf')
        
        core = get_core_instance()
        report_module = core.get_modules_manager().get_module('report_generator')
        
        if not report_module:
            return jsonify({"error": "Report module not initialized"}), 500
        
        # Datos técnicos de ejemplo
        technical_data = {
            'scan_results': {
                'total_scans': 15,
                'frequency_coverage': '3.4-3.8 GHz',
                'signal_quality': 'Excellent'
            },
            'threat_analysis': {
                'jamming_detected': True,
                'spoofing_attempts': 3,
                'anomalies_found': 12
            }
        }
        
        report_path = report_module.generate_technical_report(
            technical_data, output_format
        )
        
        if report_path:
            return jsonify({
                "status": "success",
                "report_path": report_path,
                "download_url": f"/api/reporting/download/{os.path.basename(report_path)}"
            })
        else:
            return jsonify({"error": "Failed to generate report"}), 500
            
    except Exception as e:
        logger.error(f"Error generating technical report: {e}")
        return jsonify({"error": str(e)}), 500

@reporting_bp.route('/api/reporting/list')
def list_reports():
    """Listar todos los reports disponibles"""
    try:
        core = get_core_instance()
        report_module = core.get_modules_manager().get_module('report_generator')
        
        if not report_module:
            return jsonify({"error": "Report module not initialized"}), 500
        
        reports = report_module.list_reports()
        return jsonify({
            "status": "success",
            "reports": reports
        })
        
    except Exception as e:
        logger.error(f"Error listing reports: {e}")
        return jsonify({"error": str(e)}), 500

@reporting_bp.route('/api/reporting/download/<filename>')
def download_report(filename):
    """Descargar reporte"""
    try:
        reports_dir = './data/reports'
        filepath = os.path.join(reports_dir, filename)
        
        if not os.path.exists(filepath):
            return jsonify({"error": "File not found"}), 404
        
        return send_file(filepath, as_attachment=True)
        
    except Exception as e:
        logger.error(f"Error downloading report: {e}")
        return jsonify({"error": str(e)}), 500

@reporting_bp.route('/api/automation/workflows', methods=['GET'])
def list_workflows():
    """Listar workflows disponibles"""
    try:
        core = get_core_instance()
        automation_module = core.get_modules_manager().get_module('workflow_engine')
        
        if not automation_module:
            return jsonify({"error": "Automation module not initialized"}), 500
        
        workflows = automation_module.list_workflows()
        return jsonify({
            "status": "success",
            "workflows": workflows
        })
        
    except Exception as e:
        logger.error(f"Error listing workflows: {e}")
        return jsonify({"error": str(e)}), 500

@reporting_bp.route('/api/automation/workflow/execute', methods=['POST'])
def execute_workflow():
    """Ejecutar workflow"""
    try:
        data = request.get_json() or {}
        workflow_name = data.get('workflow_name')
        parameters = data.get('parameters', {})
        
        core = get_core_instance()
        automation_module = core.get_modules_manager().get_module('workflow_engine')
        
        if not automation_module:
            return jsonify({"error": "Automation module not initialized"}), 500
        
        execution_id = automation_module.execute_workflow(workflow_name, parameters)
        
        return jsonify({
            "status": "success",
            "execution_id": execution_id,
            "status_url": f"/api/automation/workflow/status/{execution_id}"
        })
        
    except Exception as e:
        logger.error(f"Error executing workflow: {e}")
        return jsonify({"error": str(e)}), 500

@reporting_bp.route('/api/automation/workflow/status/<execution_id>')
def get_workflow_status(execution_id):
    """Obtener estado de workflow"""
    try:
        core = get_core_instance()
        automation_module = core.get_modules_manager().get_module('workflow_engine')
        
        if not automation_module:
            return jsonify({"error": "Automation module not initialized"}), 500
        
        status = automation_module.get_workflow_status(execution_id)
        return jsonify({
            "status": "success",
            "execution_status": status
        })
        
    except Exception as e:
        logger.error(f"Error getting workflow status: {e}")
        return jsonify({"error": str(e)}), 500