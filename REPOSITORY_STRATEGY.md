# Repository Strategy for Open Source Release

## Overview

This document outlines the repository strategy for Discernus's open source release, including repository separation, naming conventions, and maintenance workflows.

## Repository Structure

### Primary Repository: `discernus/discernus`

**Purpose**: Main open source repository  
**License**: GPL v3.0-or-later  
**Visibility**: Public  
**Content**: Core platform, agents, CLI, documentation

**Contents**:
- Core platform code (`discernus/` package)
- CLI interface (`discernus/cli.py`)
- Agent implementations (`discernus/agents/`)
- Core utilities (`discernus/core/`)
- Gateway layer (`discernus/gateway/`)
- Documentation (`docs/`)
- Frameworks (`frameworks/`)
- Corpus tools (`corpus/tools/`)
- Tests (`discernus/tests/`)

### Commercial Repository: `discernus/discernus-enterprise`

**Purpose**: Enterprise features and commercial components  
**License**: Commercial  
**Visibility**: Private (initially)  
**Content**: Enterprise features, commercial integrations, proprietary tools

**Contents**:
- Enterprise dashboard
- Advanced analytics
- Commercial API integrations
- Enterprise support tools
- Proprietary frameworks
- Commercial documentation

### Framework Repository: `discernus/discernus-frameworks`

**Purpose**: Community-contributed frameworks  
**License**: MIT (permissive for maximum adoption)  
**Visibility**: Public  
**Content**: Framework specifications and implementations

**Contents**:
- Framework specifications (`frameworks/`)
- Community contributions
- Framework validation tools
- Framework documentation

## Repository Naming Convention

### Open Source Repositories
- `discernus/discernus` - Main platform
- `discernus/discernus-frameworks` - Community frameworks
- `discernus/discernus-docs` - Documentation site
- `discernus/discernus-examples` - Example experiments

### Commercial Repositories
- `discernus/discernus-enterprise` - Enterprise features
- `discernus/discernus-cloud` - Cloud services
- `discernus/discernus-support` - Support tools

## Migration Strategy

### Phase 1: Open Source Release
1. **Create main repository**: `discernus/discernus`
2. **Migrate core code**: Move all open source components
3. **Set up CI/CD**: GitHub Actions for testing and releases
4. **Create documentation**: Comprehensive README and docs
5. **Community setup**: Issue templates, contributing guidelines

### Phase 2: Framework Separation
1. **Create framework repository**: `discernus/discernus-frameworks`
2. **Move framework specs**: Transfer framework specifications
3. **Set up framework CI**: Automated framework validation
4. **Community contribution**: Enable framework contributions

### Phase 3: Commercial Development
1. **Create enterprise repository**: `discernus/discernus-enterprise`
2. **Develop commercial features**: Enterprise-specific functionality
3. **Set up commercial CI**: Separate build and deployment
4. **Commercial documentation**: Enterprise-specific docs

## Repository Management

### Main Repository (`discernus/discernus`)

**Branching Strategy**:
- `main` - Stable releases
- `develop` - Development branch
- `feature/*` - Feature branches
- `hotfix/*` - Critical fixes

**Release Strategy**:
- Semantic versioning (v2.0.0, v2.1.0, etc.)
- GitHub releases with changelog
- PyPI package distribution
- Docker images for easy deployment

**Community Management**:
- Issue templates for bugs, features, questions
- Pull request templates
- Code of conduct
- Contributing guidelines
- Security policy

### Framework Repository (`discernus/discernus-frameworks`)

**Branching Strategy**:
- `main` - Approved frameworks
- `draft/*` - Framework drafts
- `review/*` - Frameworks under review

**Framework Lifecycle**:
1. **Draft**: Community creates framework specification
2. **Review**: Community reviews and validates
3. **Approval**: Maintainers approve for inclusion
4. **Maintenance**: Ongoing updates and improvements

### Enterprise Repository (`discernus/discernus-enterprise`)

**Branching Strategy**:
- `main` - Stable enterprise releases
- `develop` - Enterprise development
- `feature/*` - Enterprise features
- `integration/*` - Integration branches

**Release Strategy**:
- Separate versioning (v1.0.0-enterprise)
- Private package registry
- Enterprise support channels
- Commercial licensing

## CI/CD Strategy

### Open Source CI/CD

**GitHub Actions Workflows**:
- **Test**: Run test suite on multiple Python versions
- **Lint**: Code quality checks (black, isort, flake8)
- **Security**: Dependency vulnerability scanning
- **Build**: Create distribution packages
- **Release**: Automated PyPI publishing
- **Docker**: Build and push Docker images

**Quality Gates**:
- All tests must pass
- Code coverage threshold (80%)
- No security vulnerabilities
- Documentation up to date

### Enterprise CI/CD

**Separate Workflows**:
- **Enterprise Tests**: Run enterprise-specific tests
- **Integration Tests**: Test commercial integrations
- **Security Scan**: Enhanced security scanning
- **Deployment**: Deploy to enterprise environments

## Documentation Strategy

### Open Source Documentation

**Location**: `discernus/discernus-docs`  
**Platform**: GitHub Pages or dedicated site  
**Content**:
- User guides
- API documentation
- Framework documentation
- Contributing guidelines
- Community resources

### Enterprise Documentation

**Location**: Private documentation site  
**Content**:
- Enterprise setup guides
- Commercial API documentation
- Support procedures
- Integration guides

## Community Management

### Open Source Community

**Channels**:
- GitHub Issues for bug reports
- GitHub Discussions for questions
- Discord/Slack for real-time chat
- Mailing list for announcements

**Governance**:
- Maintainer team
- Community guidelines
- Code of conduct
- Decision-making process

### Enterprise Community

**Channels**:
- Private support portal
- Enterprise Slack workspace
- Dedicated support team
- Commercial documentation

## Security Strategy

### Open Source Security

**Vulnerability Management**:
- GitHub security advisories
- Dependabot for dependency updates
- Security policy in repository
- Responsible disclosure process

**Access Control**:
- Public read access
- Maintainer write access
- Community contributor access
- Security team access

### Enterprise Security

**Enhanced Security**:
- Private repository access
- Enterprise security scanning
- Compliance reporting
- Audit logging

## Success Metrics

### Open Source Success

**Adoption Metrics**:
- GitHub stars and forks
- PyPI download statistics
- Community contributions
- Framework submissions

**Quality Metrics**:
- Test coverage
- Bug report resolution time
- Documentation completeness
- User satisfaction

### Enterprise Success

**Commercial Metrics**:
- License sales
- Customer satisfaction
- Support ticket resolution
- Feature adoption

## Timeline

### Phase 1: Open Source Release (Weeks 1-2)
- [ ] Create main repository
- [ ] Migrate core code
- [ ] Set up CI/CD
- [ ] Create documentation
- [ ] Community setup

### Phase 2: Framework Separation (Weeks 3-4)
- [ ] Create framework repository
- [ ] Move framework specs
- [ ] Set up framework CI
- [ ] Enable contributions

### Phase 3: Commercial Development (Ongoing)
- [ ] Create enterprise repository
- [ ] Develop commercial features
- [ ] Set up commercial CI
- [ ] Commercial documentation

## Conclusion

This repository strategy balances open source community engagement with commercial viability, ensuring that Discernus can thrive as both a community project and a sustainable business.

The separation of concerns allows for:
- **Community growth** through open source adoption
- **Commercial success** through enterprise features
- **Framework innovation** through community contributions
- **Sustainable development** through dual revenue streams
