# Google Shopping Feed - Enterprise Edition

Premium multi-company license management and advanced feed features for large-scale deployments.

## Features

- **Signed License Keys**: HMAC-SHA256 signed licenses with database and company binding.
- **License Expiry**: Automatic enforcement of subscription expiry dates.
- **Multi-Company Aggregation**: (Future) Generate aggregated feeds across multiple companies.
- **Agency Features**: (Future) Advanced reporting and analytics.
- **Pro Feature Inheritance**: Enterprise licenses automatically enable all Pro features.

## Installation

Install as an add-on and ensure the `google_shopping_feed` Pro module is installed first:

```bash
# Copy into your Odoo addons directory
cp -r google_shopping_feed_enterprise /path/to/addons

# Install via Odoo UI or command line
python odoo-bin -d mydb -i google_shopping_feed google_shopping_feed_enterprise
```

## License Management

### Validate Enterprise License

Navigate to **Companies** and paste your enterprise license key in the **Enterprise License Key** field. Click **Validate** to verify:

```python
company = env['res.company'].browse(company_id)
company.action_validate_google_feed_enterprise()
```

The license status displays as **valid**, **invalid**, or **none**.

### Check License Status

```python
company = env['res.company'].browse(company_id)
is_enterprise = company.google_feed_enterprise_status == 'valid'
expires = company.google_feed_enterprise_expires
```

## Feed Generation

Enterprise licenses unlock Pro feed features. Feeds are cached and refreshed automatically:

```python
cache = env['google.feed.cache']
xml_bytes = cache.get_feed_xml(pricelist_id=None)
```

## Testing

Unit tests cover license validation and expiry enforcement:

```bash
python -m pytest google_shopping_feed_enterprise/tests/
```

## CI/CD

GitHub Actions workflow runs static checks (`pip-audit`, `bandit`) and Python syntax checks on each push and PR.

## License

Licensed under AGPL-3.0. See LICENSE file for details.
