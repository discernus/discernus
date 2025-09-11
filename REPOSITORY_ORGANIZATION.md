# Discernus Repository Organization Strategy

## Overview

This document outlines the repository separation strategy for Discernus, organizing content into open source and private repositories based on licensing, content type, and business strategy.

## Repository Structure

### **Open Source Repositories**

#### 1. `discernus/discernus` - Core Platform
**License**: GPL v3.0-or-later  
**Purpose**: Main open source platform  
**Content**:
- Core platform code (`discernus/` package)
- CLI interface (`discernus/cli.py`)
- Agent implementations (`discernus/agents/`)
- Core utilities (`discernus/core/`)
- Gateway layer (`discernus/gateway/`)
- Documentation (`docs/`)
- Tests (`discernus/tests/`)
- Build configuration (`pyproject.toml`, `requirements.txt`)

#### 2. `discernus/frameworks` - Community Frameworks
**License**: MIT  
**Purpose**: Community-contributed framework specifications  
**Content**:
- Framework specifications (`frameworks/`)
- Framework documentation (`docs/specifications/`)
- Framework development tools (`scripts/framework_researcher/`, `scripts/framework_validation/`)

#### 3. `discernus/librarian` - Framework Management
**License**: GPL v3.0-or-later  
**Purpose**: Framework discovery and management tools  
**Content**:
- Framework management (`discernus/librarian/`)
- Auditing tools (`scripts/auditing/`)

#### 4. `discernus/tools` - Development Tools
**License**: MIT  
**Purpose**: Development and utility tools  
**Content**:
- Cursor tools (`scripts/cursor_tools/`)
- Prompt engineering (`scripts/prompt_engineering/`)
- Compliance tools (`scripts/compliance_tools/`)

#### 5. `discernus/research` - Open Research Examples
**License**: MIT  
**Purpose**: Public research examples and experiments  
**Content**:
- Simple test experiments (`projects/micro_test_experiment/`, `projects/nano_test_experiment/`)
- Basic research examples (`projects/business_ethics_experiment/`, etc.)
- Open research documentation

### **Private Repositories**

#### 1. `discernus/discernus-private` - Private Content
**License**: Private/Proprietary  
**Purpose**: Private corpus, planning, and proprietary content  
**Content**:
- Private corpus (`corpus/`)
- Corpus tools (`scripts/corpus_tools/`)
- Planning documents (`pm/`)
- Proprietary research projects
- Sensitive experimental data

#### 2. `discernus/discernus-enterprise` - Commercial Features
**License**: Commercial  
**Purpose**: Enterprise features and commercial tools  
**Content**:
- Enterprise dashboard
- Advanced analytics
- Commercial API integrations
- Enterprise support tools
- Proprietary frameworks

## Content Classification

### **Open Source Content**
- ✅ Core platform code
- ✅ CLI and interfaces
- ✅ Agent implementations
- ✅ Basic documentation
- ✅ Simple test examples
- ✅ Framework specifications
- ✅ Development tools

### **Private Content**
- ❌ Fair use corpus content
- ❌ Proprietary corpus tools
- ❌ Planning and strategy documents
- ❌ Sensitive research data
- ❌ Proprietary experimental results
- ❌ Commercial features

## Migration Strategy

### **Phase 1: Core Platform (Week 1)**
1. Create `discernus/discernus` repository
2. Move core platform code
3. Set up CI/CD and documentation
4. Initialize community infrastructure

### **Phase 2: Framework Ecosystem (Week 2)**
1. Create `discernus/frameworks` repository
2. Move framework specifications
3. Set up framework validation pipeline
4. Enable community contributions

### **Phase 3: Tools and Research (Week 3)**
1. Create `discernus/tools` and `discernus/research` repositories
2. Move appropriate content
3. Set up development workflows
4. Create research examples

### **Phase 4: Private Content (Week 4)**
1. Create `discernus/discernus-private` repository
2. Move private content
3. Set up access controls
4. Update documentation

## Trademark Strategy

### **Trademark Embedding**
- Embed "Discernus" trademark in all code
- Use trademarked naming conventions
- Maintain brand consistency across repositories
- Control official channels and domains

### **Brand Protection**
- Forks cannot use "Discernus" name
- Community extensions must follow brand guidelines
- Official recognition for validated frameworks
- Commercial licensing includes trademark usage

## Repository Management

### **Open Source Repositories**
- Public visibility
- Community contributions welcome
- Clear contribution guidelines
- Automated testing and validation
- Regular releases and updates

### **Private Repositories**
- Private visibility
- Restricted access
- Internal development only
- Proprietary content protection
- Commercial licensing

## Success Metrics

### **Open Source Success**
- GitHub stars and forks
- Community contributions
- Framework submissions
- Documentation quality
- User adoption

### **Commercial Success**
- License sales
- Enterprise adoption
- Support revenue
- Feature differentiation
- Market recognition

## Legal Considerations

### **GPL v3 Compliance**
- Core platform remains GPL v3
- Community can fork and modify
- Trademark protection separate from copyright
- Commercial licensing available

### **Content Protection**
- Private content remains proprietary
- Fair use corpus content protected
- Planning documents confidential
- Commercial features exclusive

## Implementation Checklist

### **Repository Creation**
- [ ] Create GitHub organization
- [ ] Set up repository structure
- [ ] Configure access controls
- [ ] Set up CI/CD pipelines

### **Content Migration**
- [ ] Move core platform code
- [ ] Organize framework content
- [ ] Separate private content
- [ ] Update documentation

### **Community Setup**
- [ ] Create contribution guidelines
- [ ] Set up issue templates
- [ ] Configure project boards
- [ ] Enable community features

### **Legal Setup**
- [ ] File trademark application
- [ ] Update license files
- [ ] Create brand guidelines
- [ ] Set up commercial licensing

## Conclusion

This repository organization strategy balances open source community engagement with commercial viability, ensuring that Discernus can thrive as both a community project and a sustainable business while protecting proprietary content and maintaining brand control.

The separation of concerns allows for:
- **Community growth** through open source adoption
- **Commercial success** through enterprise features
- **Content protection** through private repositories
- **Brand control** through trademark strategy
- **Sustainable development** through dual revenue streams
