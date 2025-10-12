import git
import os
import shutil
from datetime import datetime
import stat
from flask import current_app

def _remove_readonly(func, path, _):
    """
    Error handler for `shutil.rmtree`.
    If the error is due to an access error (read-only file), it attempts to
    add write permission and then retries the operation.
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)

class GitHubService:
    def __init__(self):
        self.pulled_code_dir = current_app.config['PULLED_CODE_DIR']
        
    def clone_repository(self, github_url):
        """Clone GitHub repository to PulledCode directory (overwrites existing files)"""
        try:
            if os.path.exists(self.pulled_code_dir):
                shutil.rmtree(self.pulled_code_dir, onerror=_remove_readonly)
            os.makedirs(self.pulled_code_dir, exist_ok=True)
            
            # Clone repository
            repo_name = github_url.split('/')[-1].replace('.git', '')
            clone_path = os.path.join(self.pulled_code_dir, repo_name)
            
            print(f"Cloning {github_url} to {clone_path}")
            git.Repo.clone_from(github_url, clone_path)
            
            # Log the operation
            self._log_clone_operation(github_url, clone_path)
            
            return clone_path
            
        except Exception as e:
            raise Exception(f"Failed to clone repository: {str(e)}")
    
    def _log_clone_operation(self, github_url, clone_path):
        """Log clone operation for tracking"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'github_url': github_url,
            'local_path': clone_path,
            'status': 'success'
        }
        # You can implement logging to file or database here
        print(f"Repository cloned: {log_entry}")
    
    def get_repository_info(self, repo_path):
        """Extract basic repository information"""
        info = {}
        
        # Read README.md if exists
        readme_path = os.path.join(repo_path, 'README.md')
        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8') as f:
                info['readme'] = f.read()
        
        # Get package files for dependency analysis
        package_files = ['requirements.txt', 'package.json', 'Pipfile', 'pom.xml']
        info['dependencies'] = {}
        
        for file in package_files:
            file_path = os.path.join(repo_path, file)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    info['dependencies'][file] = f.read()
        
        return info
