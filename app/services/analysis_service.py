import os
import json
import uuid
from datetime import datetime
from flask import current_app
from analysis_engine.codet5_analyzer import CodeT5Analyzer
from app.services.repo_info_service import RepoInfoExtractor
import logging

logger = logging.getLogger(__name__)

class AnalysisService:
    def __init__(self, plan='basic'):
        """Initialize with plan configuration"""
        self.data_dir = current_app.config['DATA_DIR']
        self.plan = plan
        
        # Initialize analyzer with plan-specific config
        config = self._get_plan_config(plan)
        self.codet5_analyzer = CodeT5Analyzer(config=config)
        self.repo_extractor = RepoInfoExtractor()
        
        logger.info(f"AnalysisService initialized with plan: {plan}")
    
    def _get_plan_config(self, plan):
        """Get configuration based on plan"""
        if plan == 'basic':
            return {
                'regex': {'enabled': False, 'timeout': 30},
                'ast': {'enabled': False, 'timeout': 120},
                'external_tools': {'enabled': True, 'timeout': 180},
                'llm': {'enabled': False, 'timeout': 120, 'max_cost': 2.00},
                'deduplicate': True,
                'filter_low_confidence': True
            }
        elif plan == 'full':
            return {
                'regex': {'enabled': True, 'timeout': 30},
                'ast': {'enabled': True, 'timeout': 120},
                'external_tools': {'enabled': True, 'timeout': 180},
                'llm': {'enabled': True, 'timeout': 120, 'max_cost': 2.00},
                'deduplicate': True,
                'filter_low_confidence': True
            }
        else:
            # Default to basic
            return self._get_plan_config('basic')
        
    def analyze_codebase(self, repo_path, sector_hint):
        """Perform comprehensive security analysis"""
        try:
            logger.info(f"🔍 Starting comprehensive analysis for: {repo_path}")
            logger.info(f"📋 Using plan: {self.plan}")
            
            # Generate unique scan ID
            scan_id = str(uuid.uuid4())
            
            # Extract repository context (README, policies, dependencies)
            logger.info("📄 Extracting repository context...")
            repo_info = self.repo_extractor.extract(repo_path)
            
            # Perform analysis based on plan
            logger.info(f"🤖 Running security analysis with {self.plan} plan...")
            code_findings = self.codet5_analyzer.analyze(repo_path, repo_info)
            
            # Enrich findings with knowledge base
            logger.info("📚 Enriching findings with knowledge base...")
            enriched_findings = self._enrich_findings(code_findings)
            
            # Create comprehensive JSON
            scan_results = {
                'scan_id': scan_id,
                'timestamp': datetime.now().isoformat(),
                'repository_path': repo_path,
                'sector_hint': sector_hint,
                'plan_used': self.plan,  # Include plan in results
                'repository_info': repo_info,
                'findings': enriched_findings,
                'summary': self._generate_summary(enriched_findings)
            }
            
            # Save results
            self._save_scan_results(scan_id, scan_results)
            
            logger.info(f"✅ Analysis complete: {len(enriched_findings)} findings")
            
            return scan_results
            
        except Exception as e:
            logger.error(f"❌ Analysis failed: {str(e)}")
            raise Exception(f"Analysis failed: {str(e)}")
    
    def _enrich_findings(self, findings):
        """Enrich findings with knowledge base information"""
        # Load findings dictionary
        dict_path = os.path.join(self.data_dir, 'findings_dictionary.json')
        
        if not os.path.exists(dict_path):
            logger.warning(f"⚠️  Findings dictionary not found at: {dict_path}")
            return findings
        
        with open(dict_path, 'r') as f:
            findings_dict = json.load(f)
        
        enriched = []
        for finding in findings:
            keyword = finding.get('shortform_keyword')
            if keyword in findings_dict:
                # Merge finding with dictionary data
                enriched_finding = {**finding, **findings_dict[keyword]}
                enriched.append(enriched_finding)
            else:
                # Keep finding even if not in dictionary
                enriched.append(finding)
                logger.debug(f"   Finding '{keyword}' not in dictionary, keeping as-is")
        
        return enriched
    
    def _generate_summary(self, findings):
        """Generate summary statistics"""
        severity_counts = {}
        for finding in findings:
            severity = finding.get('severity', 'UNKNOWN')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        return {
            'total_findings': len(findings),
            'severity_breakdown': severity_counts
        }
    
    def _save_scan_results(self, scan_id, results):
        """Save scan results to file"""
        results_dir = os.path.join(self.data_dir, 'scanned_results')
        os.makedirs(results_dir, exist_ok=True)
        
        results_path = os.path.join(results_dir, f'{scan_id}.json')
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"💾 Scan results saved to: {results_path}")