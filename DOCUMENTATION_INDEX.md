# Complete Documentation Index

Master index for all Financial News Classifier documentation. Navigate by role or topic.

---

## Quick Navigation

**I want to...** | **Read**
---|---
Get started quickly | [Quick Start Guide](#quick-start)
Understand the project | [README.md](README.md)
Use the command line | [CLI Reference](CLI_REFERENCE.md)
Write Python code | [API Reference](API.md)
Run it offline | [Local Model Setup](LOCAL_MODEL_SETUP.md)
Deploy to production | [Deployment Guide](DEPLOYMENT.md)
Contribute code | [Contributing Guide](CONTRIBUTING.md)
See version history | [Changelog](CHANGELOG.md)

---

## By User Role

### 👤 End Users

**Getting Started:**
1. [README.md](README.md) - Overview and quick start
2. [Installation section](README.md#installation) - Setup instructions
3. [GUI Usage section](README.md#usage) - Web interface tutorial

**Daily Usage:**
- [CLI Reference](CLI_REFERENCE.md) - All commands with examples
- [GUI tabs documentation](README.md#gui-interface) - Interface guide

**Troubleshooting:**
- [README Troubleshooting](README.md#troubleshooting)
- [CLI Error Handling](CLI_REFERENCE.md#error-handling)

---

### 👨‍💻 Python Developers

**Getting Started:**
1. [API.md](API.md) - Complete Python API reference
2. [API Examples](API.md#usage-examples) - Code samples

**Integration:**
- [Single Classification](API.md#example-single-classification)
- [Batch Processing](API.md#example-batch-processing)
- [Custom Integration](API.md#complete-integration-example)

**Performance:**
- [Performance Considerations](API.md#performance-considerations)
- [Caching Patterns](API.md#caching-and-model-reuse)
- [Type Hints](API.md#type-hints-and-validation)

---

### 🛠️ DevOps / Deployment

**Setup:**
1. [Deployment Guide](DEPLOYMENT.md) - All deployment options
2. [Choose platform](DEPLOYMENT.md#cloud-platforms) - AWS/GCP/Azure
3. [Configure environment](DEPLOYMENT.md#environment-configuration)

**Monitoring:**
- [Logging Setup](DEPLOYMENT.md#monitoring-and-logging)
- [Performance Tuning](DEPLOYMENT.md#performance-tuning)
- [Scaling Options](DEPLOYMENT.md#scaling-considerations)

**Maintenance:**
- [Backup and Recovery](DEPLOYMENT.md#backup-and-recovery)
- [Troubleshooting](DEPLOYMENT.md#troubleshooting-deployment)

---

### 👷 Project Contributors

**Setup:**
1. [Contributing Guide](CONTRIBUTING.md) - Overview
2. [Development Setup](CONTRIBUTING.md#development-setup)
3. [Code Style](CONTRIBUTING.md#code-style-guide)

**Workflow:**
- [Git Workflow](CONTRIBUTING.md#git-workflow)
- [Creating PR](CONTRIBUTING.md#creating-a-pull-request)
- [Code Review](CONTRIBUTING.md#code-review-process)

**Development:**
- [Test Structure](CONTRIBUTING.md#testing)
- [Key Components](CONTRIBUTING.md#key-components-to-modify)
- [Debugging](CONTRIBUTING.md#debugging-tips)

---

### 📊 Data Scientists

**Understanding the Model:**
- [Model Details](README.md#model-architecture)
- [Performance Benchmarks](README.md#performance-benchmarks)
- [Local Model Setup](LOCAL_MODEL_SETUP.md) - For fine-tuning

**Integration with ML Workflows:**
- [Batch Processing API](API.md#batch-processing)
- [File I/O Module](API.md#file-io-module)
- [Custom Integration](API.md#complete-integration-example)

---

## By Topic

### Installation & Setup

**Quick Start:**
- [Installation](README.md#installation)
- [Quick Start](README.md#quick-start)

**Advanced Setup:**
- [Local Model Setup](LOCAL_MODEL_SETUP.md) - Offline configuration
- [GPU Setup](DEPLOYMENT.md#gpu-setup-optional) - NVIDIA CUDA
- [Docker Setup](DEPLOYMENT.md#docker-deployment)

---

### Usage & Examples

**Web Interface (GUI):**
- [GUI Tutorial](README.md#gui-interface)
- [Gradio Features](README.md#features)

**Command Line (CLI):**
- [CLI Reference - Complete](CLI_REFERENCE.md)
- [classify Command](CLI_REFERENCE.md#classify-command)
- [batch Command](CLI_REFERENCE.md#batch-command)
- [rss Command](CLI_REFERENCE.md#rss-command)
- [Examples](CLI_REFERENCE.md#examples)

**Python Code (API):**
- [API Reference - Complete](API.md)
- [Core Module](API.md#core-inference-module)
- [File I/O Module](API.md#file-io-module)
- [RSS Module](API.md#rss-module)
- [7 Usage Examples](API.md#usage-examples)

---

### Deployment & Production

**Local Deployment:**
- [Local Setup](DEPLOYMENT.md#local-development)
- [Systemd Service](DEPLOYMENT.md#systemd-service-linux)

**Container Deployment:**
- [Docker Basics](DEPLOYMENT.md#docker-deployment)
- [Docker Compose](DEPLOYMENT.md#docker-deployment)

**Cloud Deployment:**
- [AWS Options](DEPLOYMENT.md#aws-deployment)
- [Google Cloud](DEPLOYMENT.md#google-cloud)
- [Azure Setup](DEPLOYMENT.md#azure)

**Advanced:**
- [Kubernetes](DEPLOYMENT.md#kubernetes-deployment)
- [Load Balancing](DEPLOYMENT.md#load-balancing)
- [API Server](DEPLOYMENT.md#api-server-for-batch-processing)

---

### Offline Operation

**Local Model:**
- [Local Model Setup](LOCAL_MODEL_SETUP.md) - Complete guide
- [Directory Structure](LOCAL_MODEL_SETUP.md#directory-structure)
- [Verification](LOCAL_MODEL_SETUP.md#verification)
- [Troubleshooting](LOCAL_MODEL_SETUP.md#troubleshooting)

**Deployment:**
- [Model Path Configuration](DEPLOYMENT.md#environment-configuration)
- [Air-Gapped Systems](DEPLOYMENT.md#environment-configuration)

---

### Development

**Getting Started:**
- [Development Setup](CONTRIBUTING.md#development-setup)
- [Project Structure](CONTRIBUTING.md#project-structure)

**Code Quality:**
- [Code Style](CONTRIBUTING.md#code-style-guide)
- [Testing](CONTRIBUTING.md#testing)
- [Type Hints](CONTRIBUTING.md#code-structure)

**Workflow:**
- [Git Workflow](CONTRIBUTING.md#git-workflow)
- [Commit Messages](CONTRIBUTING.md#commit-messages)
- [Pull Requests](CONTRIBUTING.md#creating-a-pull-request)

**Extending:**
- [Adding CLI Commands](CONTRIBUTING.md#adding-new-cli-command)
- [Adding GUI Tabs](CONTRIBUTING.md#adding-gui-tab)
- [Extending Model](CONTRIBUTING.md#extending-model-features)

---

### Version & History

**Current Status:**
- [Changelog](CHANGELOG.md) - Complete version history
- [v1.0.0 Release](CHANGELOG.md#100---2024-01-15)
- [Known Issues](CHANGELOG.md#known-issues)

**Future:**
- [Planned Features](CHANGELOG.md#planned-features)
- [Roadmap](CHANGELOG.md#future-roadmap)

**Migration:**
- [Upgrade Guide](CHANGELOG.md#upgrade-guide)
- [Migration Guide](CHANGELOG.md#migration-guides)

---

## Feature Documentation

### Core Features

**Sentiment Classification:**
- Model: [Model Architecture](README.md#model-architecture)
- API: [predict() function](API.md#predict)
- CLI: [classify command](CLI_REFERENCE.md#classify-command)
- GUI: [Classification tab](README.md#gui-interface)

**Batch Processing:**
- API: [predict_batch() function](API.md#predict_batch)
- CLI: [batch command](CLI_REFERENCE.md#batch-command)
- GUI: [Batch Processing tab](README.md#gui-interface)
- File Formats: [Supported formats](CLI_REFERENCE.md#batch-command)

**RSS Analysis:**
- API: [fetch_rss() function](API.md#rss-module)
- CLI: [rss command](CLI_REFERENCE.md#rss-command)
- GUI: [RSS Analysis tab](README.md#gui-interface)
- Feed Examples: [Popular feeds](CLI_REFERENCE.md#rss-command)

**Offline Support:**
- Detection: [Model Detection](LOCAL_MODEL_SETUP.md#verification)
- Setup: [Local Model Setup](LOCAL_MODEL_SETUP.md)
- API: [check_local_model()](API.md#model-loader)
- CLI: [Device Options](CLI_REFERENCE.md#global-options)

---

### File Support

**Input Formats:**
- CSV: [CSV Processing](CLI_REFERENCE.md#file-formats)
- JSON: [JSON Processing](CLI_REFERENCE.md#file-formats)
- TXT: [TXT Processing](CLI_REFERENCE.md#file-formats)
- Markdown: [MD Processing](CLI_REFERENCE.md#file-formats)

**Output Formats:**
- CSV: [CSV Output](CLI_REFERENCE.md#output-formats)
- JSON: [JSON Output](CLI_REFERENCE.md#output-formats)
- Database: [DB Integration](API.md#complete-integration-example)

---

### Interface Documentation

**Command Line (CLI):**
- Full Reference: [CLI_REFERENCE.md](CLI_REFERENCE.md)
- Global Options: [Global Options](CLI_REFERENCE.md#global-options)
- Device Selection: [Device Selection](CLI_REFERENCE.md#device-selection)

**Web Interface (GUI):**
- Overview: [GUI Interface](README.md#gui-interface)
- Tabs: [4-Tab Layout](README.md#gui-interface)
- Features: [GUI Features](README.md#features)

**Python API:**
- Full Reference: [API.md](API.md)
- Core Module: [core.infer](API.md#core-inference-module)
- I/O Module: [core.io_utils](API.md#file-io-module)
- RSS Module: [core.rss](API.md#rss-module)

---

## Troubleshooting Guide

**Common Issues:**

| Issue | Resource |
|-------|----------|
| Installation problems | [README Installation](README.md#installation) |
| Model not loading | [Local Model Setup](LOCAL_MODEL_SETUP.md#troubleshooting) |
| Slow inference | [Performance Tips](API.md#performance-considerations) |
| Memory errors | [Deployment Troubleshooting](DEPLOYMENT.md#troubleshooting-deployment) |
| CLI errors | [CLI Error Handling](CLI_REFERENCE.md#error-handling) |
| GPU not working | [GPU Setup](DEPLOYMENT.md#gpu-setup-optional) |
| Port conflicts | [Troubleshooting](DEPLOYMENT.md#troubleshooting-deployment) |
| Import errors | [Contributing Development](CONTRIBUTING.md#development-setup) |

---

## Learning Paths

### 📚 Beginner Path (1-2 hours)

1. Read [README.md](README.md) - Overview
2. Install from [Installation](README.md#installation)
3. Try [Quick Start CLI](README.md#quick-start)
4. Explore [GUI Interface](README.md#gui-interface)
5. Read [Troubleshooting](README.md#troubleshooting)

### 💻 CLI Power User Path (2-3 hours)

1. Start with [README Quick Start](README.md#quick-start)
2. Complete [CLI Reference](CLI_REFERENCE.md) - all commands
3. Try [Scripting Examples](CLI_REFERENCE.md#scripting-examples)
4. Review [Global Options](CLI_REFERENCE.md#global-options)
5. Practice with your data

### 🐍 Python Developer Path (3-4 hours)

1. Understand [Project Structure](CONTRIBUTING.md#project-structure)
2. Read [API Reference](API.md) - complete guide
3. Work through [7 Usage Examples](API.md#usage-examples)
4. Study [Integration Example](API.md#complete-integration-example)
5. Try [Performance Tips](API.md#performance-considerations)

### 🚀 DevOps/Deployment Path (4-5 hours)

1. Review [Deployment Guide](DEPLOYMENT.md#overview)
2. Choose platform: [Cloud Platforms](DEPLOYMENT.md#cloud-platforms)
3. Setup environment: [Environment Configuration](DEPLOYMENT.md#environment-configuration)
4. Configure monitoring: [Monitoring](DEPLOYMENT.md#monitoring-and-logging)
5. Test scaling: [Scaling Considerations](DEPLOYMENT.md#scaling-considerations)

### 🛠️ Contributor Path (5+ hours)

1. Read [Contributing Guide](CONTRIBUTING.md) - overview
2. Setup [Development Environment](CONTRIBUTING.md#development-setup)
3. Review [Code Standards](CONTRIBUTING.md#code-style-guide)
4. Study [Git Workflow](CONTRIBUTING.md#git-workflow)
5. Explore [Key Components](CONTRIBUTING.md#key-components-to-modify)
6. Check [Testing Guide](CONTRIBUTING.md#testing)

---

## Document Overview

### README.md
**Purpose:** Main project documentation
**Audience:** All users
**Contents:** Overview, installation, usage, features, troubleshooting
**Length:** ~1000 lines

### CLI_REFERENCE.md
**Purpose:** Complete CLI command reference
**Audience:** CLI users, system integrators
**Contents:** All commands, options, examples, performance benchmarks
**Length:** ~800 lines

### API.md
**Purpose:** Python API integration guide
**Audience:** Python developers
**Contents:** All modules, functions, examples, integration patterns
**Length:** ~900 lines

### LOCAL_MODEL_SETUP.md
**Purpose:** Offline model configuration
**Audience:** Users with offline requirements
**Contents:** Setup options, verification, troubleshooting
**Length:** ~600 lines

### DEPLOYMENT.md
**Purpose:** Production deployment guide
**Audience:** DevOps, system administrators
**Contents:** Docker, cloud platforms, scaling, monitoring
**Length:** ~1200 lines

### CONTRIBUTING.md
**Purpose:** Development contribution guide
**Audience:** Developers, contributors
**Contents:** Setup, code standards, workflow, extending
**Length:** ~1000 lines

### CHANGELOG.md
**Purpose:** Version history and roadmap
**Audience:** All users (reference)
**Contents:** Version history, features, breaking changes, planned work
**Length:** ~700 lines

### DOCUMENTATION_INDEX.md (this file)
**Purpose:** Navigation and overview
**Audience:** All users
**Contents:** Quick navigation, learning paths, document index

---

## Key Sections by Document

### README.md
- Quick Start
- Installation (pip, conda, Docker)
- Usage (CLI/GUI/API)
- Features
- Model Architecture & Performance
- Project Structure
- Troubleshooting
- Development

### CLI_REFERENCE.md
- Command Reference (classify, batch, rss, gui, info, version)
- Options and Arguments
- Output Formats
- Environment Variables
- Performance Benchmarks
- Scripting Examples
- Integration with Shell/Python

### API.md
- Core Module (predict, predict_batch, set_device, check_local_model)
- File I/O Module (load_file, save_results, validate_file)
- RSS Module (fetch_rss, validate_rss_feed)
- 7 Complete Usage Examples
- Integration Example
- Performance Considerations
- Error Handling

### LOCAL_MODEL_SETUP.md
- Directory Structure
- Required Files
- Setup Options (3 methods)
- Verification Process
- Benefits & Limitations
- Logging Output
- Troubleshooting

### DEPLOYMENT.md
- Local Development
- Docker Deployment
- Production Setup (systemd, Nginx)
- Cloud Platforms (AWS, GCP, Azure)
- Scaling & Load Balancing
- Monitoring & Logging
- Security (authentication, SSL)
- Backup & Recovery

### CONTRIBUTING.md
- Development Setup
- Project Structure
- Code Style (black, ruff, type hints)
- Testing & Fixtures
- Git Workflow
- PR Process
- Key Components
- Debugging Tips

### CHANGELOG.md
- v1.0.0 Release Details
- Features & Dependencies
- Known Issues & Limitations
- Planned Features & Roadmap
- Upgrade Guide
- Security Policy

---

## Document Relationships

```
README.md (Master Overview)
├── Quick Start
├── Installation
├── Usage
│   ├── CLI → CLI_REFERENCE.md
│   ├── GUI → DEPLOYMENT.md (GUI setup)
│   └── API → API.md
└── Troubleshooting → (links to specific docs)

CLI_REFERENCE.md (CLI Users)
├── Commands with examples
├── Performance tips → DEPLOYMENT.md
└── Integration → API.md

API.md (Developers)
├── Core modules
├── Usage examples
├── Integration → DEPLOYMENT.md
└── Performance → DEPLOYMENT.md

LOCAL_MODEL_SETUP.md (Offline)
├── Setup options
├── Troubleshooting → README.md
└── Deployment → DEPLOYMENT.md

DEPLOYMENT.md (DevOps/Production)
├── Platforms
├── Configuration
├── Monitoring
└── Troubleshooting → README.md

CONTRIBUTING.md (Developers)
├── Setup
├── Code standards
├── Workflow
└── Testing

CHANGELOG.md (Reference)
├── Version history
├── Features
└── Roadmap
```

---

## Cross-References

### By Topic

**Installation:**
- README.md § Installation
- DEPLOYMENT.md § Local Development
- CONTRIBUTING.md § Development Setup

**CLI Usage:**
- README.md § Quick Start
- CLI_REFERENCE.md (complete)
- CONTRIBUTING.md § Adding CLI Commands

**Python Integration:**
- API.md (complete)
- CONTRIBUTING.md § Extending Model Features
- README.md § Usage

**Deployment:**
- DEPLOYMENT.md (complete)
- README.md § Installation
- CONTRIBUTING.md § CI/CD Integration

**Offline Operation:**
- LOCAL_MODEL_SETUP.md (complete)
- DEPLOYMENT.md § Environment Configuration
- README.md § Local Model Support

**Development:**
- CONTRIBUTING.md (complete)
- README.md § Development
- CHANGELOG.md § Roadmap

---

## Search Tips

**Finding Information:**

Topic | Search Strategy
---|---
How to classify text | README.md Quick Start or CLI_REFERENCE.md classify command
How to process files | CLI_REFERENCE.md batch command or API.md predict_batch example
How to use GPU | DEPLOYMENT.md GPU Setup or CLI_REFERENCE.md device selection
How to deploy | DEPLOYMENT.md (choose platform section)
How to contribute | CONTRIBUTING.md from top
How to add feature | CONTRIBUTING.md Key Components section
Performance optimization | API.md Performance Considerations or DEPLOYMENT.md Performance Tuning
Troubleshooting | README.md Troubleshooting or specific doc's Troubleshooting section

---

## External Resources

**Related Documentation:**
- [PyTorch Documentation](https://pytorch.org/docs/)
- [Transformers Documentation](https://huggingface.co/docs/transformers/)
- [Gradio Documentation](https://gradio.app/docs/)
- [Typer Documentation](https://typer.tiangolo.com/)
- [Rich Documentation](https://rich.readthedocs.io/)

**Community:**
- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: Questions and discussions
- Discord: Community chat (link in README)

---

## FAQ

**Q: Where do I start?**
A: Start with [README.md](README.md) for overview, then choose your path:
- User? → [Quick Start](README.md#quick-start)
- Developer? → [API.md](API.md)
- DevOps? → [DEPLOYMENT.md](DEPLOYMENT.md)
- Contributor? → [CONTRIBUTING.md](CONTRIBUTING.md)

**Q: How do I install?**
A: See [Installation](README.md#installation) in README.md

**Q: How do I use the CLI?**
A: See [CLI_REFERENCE.md](CLI_REFERENCE.md) for complete command reference

**Q: How do I use in Python code?**
A: See [API.md](API.md) for complete API reference with 7 examples

**Q: How do I deploy to production?**
A: See [DEPLOYMENT.md](DEPLOYMENT.md) for all platform options

**Q: How do I contribute code?**
A: See [CONTRIBUTING.md](CONTRIBUTING.md) for workflow and standards

**Q: What's the roadmap?**
A: See [CHANGELOG.md](CHANGELOG.md) § Planned Features

**Q: Found a bug?**
A: See [CONTRIBUTING.md](CONTRIBUTING.md) § Communication § Reporting Bugs

---

## Glossary

**Term** | **Definition** | **Reference**
---|---|---
API | Python interface for programmatic access | [API.md](API.md)
Batch Processing | Process multiple texts efficiently | [CLI_REFERENCE.md](CLI_REFERENCE.md) § batch command
CLI | Command-line interface | [CLI_REFERENCE.md](CLI_REFERENCE.md)
DistilBERT | Lightweight BERT model used | [README.md](README.md) § Model Architecture
GPU | Graphics Processing Unit for acceleration | [DEPLOYMENT.md](DEPLOYMENT.md) § GPU Setup
GUI | Graphical User Interface (Gradio) | [README.md](README.md) § GUI Interface
Local Model | Model stored locally for offline use | [LOCAL_MODEL_SETUP.md](LOCAL_MODEL_SETUP.md)
RSS | Rich Site Summary feed format | [CLI_REFERENCE.md](CLI_REFERENCE.md) § rss command
Sentiment | Classification as Bullish/Bearish/Neutral | [README.md](README.md) § Features

---

## Version

- **Documentation Version:** 1.0.0
- **Last Updated:** 2024-01-15
- **Maintained By:** TADS Tech Team
- **License:** Apache 2.0

---

## Navigation Tips

- **Table of Contents** at top for quick navigation
- **Ctrl+F** (Cmd+F on Mac) to search within documents
- **Breadcrumbs** show document hierarchy
- **Related documents** links at bottom of each section
- **Back to index** links available in all docs

---

**Need Help?**
- Check this index first
- Search specific documentation
- Review [README Troubleshooting](README.md#troubleshooting)
- Open GitHub Issue if needed

---

**Happy Exploring! 🚀**
