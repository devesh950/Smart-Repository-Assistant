# 🤖 Smart Repository Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Issues](https://img.shields.io/github/issues/devesh950/smart-repository-assistant)](https://github.com/devesh950/smart-repository-assistant/issues)
[![GitHub Stars](https://img.shields.io/github/stars/devesh950/smart-repository-assistant)](https://github.com/devesh950/smart-repository-assistant/stargazers)

> **An intelligent GitHub repository management system that revolutionizes how you track, analyze, and maintain your projects.**

A comprehensive GitHub repository management tool that automatically identifies issue types, manages labels, tracks repository health, and provides detailed analytics with a beautiful interactive dashboard.

![Smart Repository Assistant Dashboard](https://via.placeholder.com/800x400/4CAF50/FFFFFF?text=Interactive+Analytics+Dashboard)

## ✨ Features

- 🤖 **Intelligent Issue Classification**: Automatically categorizes issues using advanced NLP
- 🏷️ **Auto-Labeling System**: Smart labeling for issues and PRs with custom colors
- 📊 **Repository Health Monitoring**: Real-time health scoring and trend analysis
- 👥 **Contributor Activity Analysis**: Deep insights into contributor engagement
- 📈 **Interactive Analytics Dashboard**: Beautiful Streamlit dashboard with 13+ chart types
- 🔔 **Real-time Webhook Processing**: Instant issue and PR processing
- 🎯 **Priority Detection**: Automatic priority assignment based on content analysis
- 🌐 **Multi-Repository Support**: Analyze and compare multiple repositories
- 🔥 **Activity Heatmaps**: Visual contributor activity patterns
- ⚡ **Live Monitoring**: Real-time metrics and alerts
- 📱 **Responsive Design**: Works perfectly on desktop and mobile
- 🚀 **Easy Deployment**: One-click deployment to Heroku, Railway, or any cloud platform

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd SMART-REPO
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   Create a `.env` file with:
   ```env
   GITHUB_TOKEN=your_github_personal_access_token
   GITHUB_WEBHOOK_SECRET=your_webhook_secret
   DEFAULT_REPO=owner/repo-name
   FLASK_HOST=0.0.0.0
   FLASK_PORT=5000
   FLASK_DEBUG=True
   ```

4. **GitHub App Setup**
   - Create a GitHub App in your repository settings
   - Set webhook URL to `http://your-server:5000/webhook`
   - Subscribe to Issues and Pull Request events
   - Install the app on your repository

## Usage

### Start the Flask Webhook Server
```bash
python app.py
```

### Launch the Analytics Dashboard
```bash
streamlit run dashboard.py
```

### Manual Repository Analysis
```python
from analytics import RepositoryAnalyzer
analyzer = RepositoryAnalyzer('owner/repo-name')
health_score = analyzer.calculate_health_score()
contributor_stats = analyzer.get_contributor_activity()
```

## Components

- **app.py**: Flask webhook server for GitHub events
- **issue_bot.py**: Intelligent issue processing and auto-labeling
- **analytics.py**: Repository analysis and health monitoring
- **dashboard.py**: Interactive Streamlit dashboard
- **config.py**: Configuration and settings management

## API Endpoints

- `POST /webhook`: GitHub webhook endpoint
- `GET /health`: Repository health status
- `GET /analytics`: Repository analytics data

## Dashboard Features

- Repository overview and health score
- Issue and PR statistics
- Contributor activity trends
- Commit frequency analysis
- Label distribution charts
- Response time metrics

## 🚀 Live Demo

Try the live demo: **[Smart Repository Assistant Demo](https://smart-repo-assistant.herokuapp.com)**

**Sample Analytics:**
- View demo at: `https://smart-repo-assistant.herokuapp.com/analytics/facebook/react`
- Health check: `https://smart-repo-assistant.herokuapp.com/health?repo=microsoft/vscode`

## 📊 Dashboard Screenshots

### Main Analytics Dashboard
![Main Dashboard](https://via.placeholder.com/600x400/2196F3/FFFFFF?text=Repository+Analytics+Overview)

### Contributor Activity Heatmap
![Contributor Heatmap](https://via.placeholder.com/600x300/FF9800/FFFFFF?text=Contributor+Activity+Heatmap)

### Health Monitoring
![Health Monitoring](https://via.placeholder.com/600x300/4CAF50/FFFFFF?text=Repository+Health+Radar)

## 🌐 Deployment Options

### Option 1: Heroku (Recommended)
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/devesh950/smart-repository-assistant)

### Option 2: Railway
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/devesh950/smart-repository-assistant)

### Option 3: Vercel
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/devesh950/smart-repository-assistant)

### Option 4: Docker
```bash
docker build -t smart-repo-assistant .
docker run -p 5000:5000 -p 8501:8501 smart-repo-assistant
```

## 🔧 Configuration for Deployment

### Environment Variables
Set these in your deployment platform:

```env
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_WEBHOOK_SECRET=your_webhook_secret
DEFAULT_REPO=your-username/your-repo
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

### GitHub App Setup (Optional)
1. Create a GitHub App in your organization
2. Set webhook URL to your deployed app: `https://your-app.herokuapp.com/webhook`
3. Subscribe to Issues and Pull Request events
4. Install the app on repositories you want to monitor

## 🤝 Contributing

We love contributions! Here's how you can help:

1. **🍴 Fork the repository**
2. **🔀 Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **✅ Commit your changes**: `git commit -m 'Add amazing feature'`
4. **📤 Push to branch**: `git push origin feature/amazing-feature`
5. **🔄 Open a Pull Request**

### Development Setup
```bash
git clone https://github.com/devesh950/smart-repository-assistant.git
cd smart-repository-assistant
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
python app.py
```

## 📈 Roadmap

- [ ] 🔍 Advanced ML-based issue classification
- [ ] 📧 Email notifications and reports
- [ ] 🎨 Custom dashboard themes
- [ ] 📱 Mobile app
- [ ] 🔐 Enterprise SSO integration
- [ ] 🤖 Slack/Discord bot integration
- [ ] 📊 Advanced forecasting and predictions
- [ ] 🌍 Multi-language support

## ❓ FAQ

**Q: Is this free to use?**
A: Yes! It's completely free and open-source under MIT license.

**Q: Can I use it for private repositories?**
A: Yes, just make sure your GitHub token has access to private repos.

**Q: How secure is my data?**
A: We don't store any repository data. Everything is processed in real-time via GitHub's API.

**Q: Can I customize the analytics?**
A: Absolutely! The system is designed to be easily extensible. Check the documentation for custom analytics.

## 🆘 Support

- 📖 **Documentation**: [Full Documentation](https://github.com/devesh950/smart-repository-assistant/wiki)
- 🐛 **Bug Reports**: [Issues](https://github.com/devesh950/smart-repository-assistant/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/devesh950/smart-repository-assistant/discussions)
- 📧 **Email**: devesh950@example.com

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=devesh950/smart-repository-assistant&type=Date)](https://star-history.com/#devesh950/smart-repository-assistant&Date)

## 🙏 Acknowledgments

- Thanks to all contributors who have helped shape this project
- Built with love using Python, Flask, Streamlit, and Plotly
- Special thanks to the GitHub API and PyGithub library

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**[🌟 Star this repository](https://github.com/devesh950/smart-repository-assistant) | [🍴 Fork it](https://github.com/devesh950/smart-repository-assistant/fork) | [🐛 Report Issues](https://github.com/devesh950/smart-repository-assistant/issues)**

Made with ❤️ by [Devesh](https://github.com/devesh950)

</div>