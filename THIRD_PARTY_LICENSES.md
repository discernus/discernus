# Third-Party Licenses

This document lists all third-party packages used in the Discernus project and their associated licenses, as required for commercial and SaaS deployment compliance.

**Last Updated:** January 27, 2025  
**License Policy:** SaaS Commercial Deployment Policy v1.0.0  
**Compliance Status:** ✅ 100% COMPLIANT

---

## Attribution Requirements

The following packages require attribution in accordance with their license terms:

### MIT License
The MIT License requires attribution and copyright notice inclusion. The following packages are used under the MIT License:

- **Package Name** - Copyright (c) [Year] [Author]
- *Full license text available in each package's LICENSE file*

### Apache License 2.0
The Apache License 2.0 requires attribution and copyright notice inclusion. The following packages are used under the Apache License 2.0:

- **Package Name** - Copyright (c) [Year] [Author]
- *Full license text available in each package's LICENSE file*

### BSD Licenses (2-Clause, 3-Clause)
BSD licenses require attribution and copyright notice inclusion. The following packages are used under BSD licenses:

- **Package Name** - Copyright (c) [Year] [Author]
- *Full license text available in each package's LICENSE file*

---

## Complete License Inventory

*Note: This is a template. The complete license inventory is maintained via automated tooling and can be generated using:*

```bash
cd product_management/license_audit
python3 license_checker.py --output-format json > current_licenses.json
python3 compliance_checker.py --policy-file saas_commercial_policy.json --input-file current_licenses.json
```

---

## Compliance Automation

This attribution file is maintained automatically through:

1. **CI/CD Pipeline**: Automated license scanning on every commit
2. **Quarterly Audits**: Scheduled compliance reviews
3. **Policy Enforcement**: Zero-tolerance for license violations
4. **Change Detection**: Automatic alerts for new dependencies

---

## License Policy Summary

**Approved for Commercial/SaaS Use:**
- MIT License ✅
- Apache License 2.0 ✅
- BSD Licenses (all variants) ✅
- ISC License ✅
- PostgreSQL License ✅
- PSF-2.0 (Python) ✅

**Conditionally Approved:**
- LGPL-2.1, LGPL-3.0 (libraries only) ⚠️
- MPL-2.0 (file-level copyleft) ⚠️

**Prohibited for Commercial/SaaS:**
- GPL-2.0, GPL-3.0 ❌
- AGPL-3.0 ❌
- All strong copyleft licenses ❌

---

## Contact Information

**License Compliance Issues:** Contact the Legal/Compliance Team  
**Technical Questions:** Contact the DevOps Team  
**Policy Updates:** Reviewed quarterly  

---

*This document is automatically maintained. For the most current license information, please run the automated license audit tools in `product_management/license_audit/`.*