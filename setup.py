"""
Smart Repository Assistant - Setup Script
Initialize and configure the system
"""

import os
import sys
from pathlib import Path
import subprocess

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from template...")
        with open(env_example, 'r') as src, open(env_file, 'w') as dst:
            content = src.read()
            dst.write(content)
        print("   ✅ .env file created. Please edit it with your settings.")
        return True
    elif env_file.exists():
        print("   ℹ️ .env file already exists")
        return True
    else:
        print("   ⚠️ .env.example not found")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("   ✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error installing dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "logs",
        "reports",
        "templates"
    ]
    
    print("📁 Creating directories...")
    for dir_name in directories:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir()
            print(f"   ✅ Created {dir_name}/ directory")
        else:
            print(f"   ℹ️ {dir_name}/ directory already exists")
    
    return True

def setup_github_templates():
    """Set up GitHub issue and PR templates"""
    github_dir = Path(".github")
    template_dir = github_dir / "ISSUE_TEMPLATE"
    
    print("📋 Setting up GitHub templates...")
    
    # Create directories
    template_dir.mkdir(parents=True, exist_ok=True)
    
    # Bug report template
    bug_template = template_dir / "bug_report.md"
    if not bug_template.exists():
        with open(bug_template, 'w') as f:
            f.write("""---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: 'bug, needs-triage'
assignees: ''
---

## Bug Description
A clear and concise description of what the bug is.

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## Expected Behavior
A clear description of what you expected to happen.

## Screenshots
If applicable, add screenshots to help explain your problem.

## Environment
- OS: [e.g. Windows, macOS, Linux]
- Browser: [e.g. Chrome, Firefox, Safari]
- Version: [e.g. 1.0.0]

## Additional Context
Add any other context about the problem here.
""")
        print("   ✅ Created bug report template")
    
    # Feature request template
    feature_template = template_dir / "feature_request.md"
    if not feature_template.exists():
        with open(feature_template, 'w') as f:
            f.write("""---
name: Feature request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: 'enhancement, needs-triage'
assignees: ''
---

## Problem Description
Is your feature request related to a problem? Please describe.
A clear and concise description of what the problem is.

## Proposed Solution
Describe the solution you'd like.
A clear and concise description of what you want to happen.

## Alternatives Considered
Describe alternatives you've considered.
A clear and concise description of any alternative solutions or features you've considered.

## Additional Context
Add any other context or screenshots about the feature request here.
""")
        print("   ✅ Created feature request template")
    
    # Pull request template
    pr_template = github_dir / "pull_request_template.md"
    if not pr_template.exists():
        with open(pr_template, 'w') as f:
            f.write("""## Description
Brief description of the changes in this pull request.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Testing
- [ ] I have tested my changes locally
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] All new and existing tests pass

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have checked my code and corrected any misspellings

## Related Issues
Closes #(issue number)

## Screenshots (if applicable)
Add screenshots to help explain your changes.
""")
        print("   ✅ Created pull request template")
    
    return True

def display_setup_complete():
    """Display setup completion message"""
    print("\n" + "=" * 60)
    print("🎉 Smart Repository Assistant Setup Complete!")
    print("=" * 60)
    
    print("\n📋 Next Steps:")
    print("1. Edit .env file with your GitHub token and repository settings")
    print("2. Test the system: python test_system.py")
    print("3. Start the webhook server: python app.py")
    print("4. Launch the dashboard: streamlit run dashboard.py")
    
    print("\n🔗 GitHub Webhook Configuration:")
    print("- Payload URL: http://your-server:5000/webhook")
    print("- Content type: application/json")
    print("- Events: Issues, Pull requests, Push")
    
    print("\n📊 Dashboard Access:")
    print("- Analytics Dashboard: http://localhost:8501")
    print("- API Health Check: http://localhost:5000/health")
    print("- API Analytics: http://localhost:5000/analytics")
    
    print("\n📖 Documentation:")
    print("- README.md contains detailed setup and usage instructions")
    print("- Check test_system.py for system validation")

def main():
    """Main setup function"""
    print("🚀 Smart Repository Assistant - Setup")
    print("=" * 50)
    
    steps = [
        ("Environment Configuration", create_env_file),
        ("Dependencies Installation", install_dependencies),
        ("Directory Structure", create_directories),
        ("GitHub Templates", setup_github_templates)
    ]
    
    all_success = True
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        try:
            success = step_func()
            all_success = all_success and success
        except Exception as e:
            print(f"   ❌ Error in {step_name}: {e}")
            all_success = False
    
    if all_success:
        display_setup_complete()
    else:
        print("\n⚠️ Setup completed with some errors. Please review the messages above.")
    
    return all_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)