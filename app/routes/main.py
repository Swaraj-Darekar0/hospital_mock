from flask import Blueprint, request, jsonify, send_file
from app.services.github_service import GitHubService
from app.services.analysis_service import AnalysisService
from app.services.report_service import ReportService
import os
import json

main_bp = Blueprint('main', __name__)

# Global variable to store current plan (in production, use database)
CURRENT_PLAN = 'basic'  # Default plan

@main_bp.route('/api/change-plan', methods=['POST'])
def change_plan():
    """Change analysis plan configuration"""
    global CURRENT_PLAN
    
    try:
        data = request.get_json()
        new_plan = data.get('plan')
        
        if new_plan not in ['basic', 'full']:
            return jsonify({'status': 'error', 'message': 'Invalid plan'}), 400
        
        # Update global plan
        CURRENT_PLAN = new_plan
        
        print(f"[/api/change-plan] Plan changed to: {new_plan}")
        
        return jsonify({
            'status': 'success',
            'plan': new_plan,
            'message': f'Plan changed to {new_plan}'
        })
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@main_bp.route('/api/get-plan', methods=['GET'])
def get_plan():
    """Get current plan"""
    global CURRENT_PLAN
    return jsonify({
        'status': 'success',
        'plan': CURRENT_PLAN
    })


@main_bp.route('/api/analyze', methods=['POST'])
def analyze_repository():
    global CURRENT_PLAN
    
    try:
        data = request.get_json()
        github_url = data.get('github_url')
        sector_hint = data.get('sector_hint', '')
        plan = data.get('plan', CURRENT_PLAN)  # Use plan from request or global
        
        print(f"[/api/analyze] Received request")
        print(f"[/api/analyze] GitHub URL: {github_url}, Sector: {sector_hint}, Plan: {plan}")
        
        # Phase 1: Input & Analysis
        print(f"[/api/analyze] Phase 1: Cloning repository...")
        github_service = GitHubService()
        repo_path = github_service.clone_repository(github_url)
        print(f"[/api/analyze] Repository cloned to: {repo_path}")
        
        # Phase 2: Data Processing & Storage (with plan configuration)
        print(f"[/api/analyze] Phase 2: Starting codebase analysis with plan: {plan}...")
        analysis_service = AnalysisService(plan=plan)  # Pass plan to service
        scan_results = analysis_service.analyze_codebase(repo_path, sector_hint)
        
        return jsonify({
            'status': 'success',
            'scan_id': scan_results['scan_id'],
            'plan_used': plan,
            'total_findings': scan_results['summary']['total_findings'],
            'message': f'Analysis completed successfully using {plan} plan'
        })
    
    except Exception as e:
        print(f"[/api/analyze] ERROR: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@main_bp.route('/api/generate-report', methods=['POST'])
def generate_report():
    try:
        data = request.get_json()
        scan_id = data.get('scan_id')
        report_type = data.get('report_type')
        
        print(f"[/api/generate-report] Scan ID: {scan_id}, Type: {report_type}")
        
        # Phase 3: Report Generation & Output
        report_service = ReportService()
        report_path = report_service.generate_report(scan_id, report_type)
        
        return send_file(report_path, as_attachment=True)
    
    except Exception as e:
        print(f"[/api/generate-report] ERROR: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500