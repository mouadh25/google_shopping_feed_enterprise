# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from odoo.tests.common import TransactionCase
from odoo.tests import tagged

try:
    from .. import license as core_license
except Exception:
    from odoo.addons.google_shopping_feed import license as core_license


@tagged('post_install', '-at_install')
class TestEnterpriseLicense(TransactionCase):

    def setUp(self):
        super(TestEnterpriseLicense, self).setUp()
        self.company = self.env['res.company'].create({
            'name': 'Enterprise Test Company'
        })
        self.secret = self.env['ir.config_parameter'].sudo().get_param('google_feed.license_secret')
        if not self.secret:
            self.secret = 'testsecret_enterprise'
            self.env['ir.config_parameter'].sudo().set_param('google_feed.license_secret', self.secret)

    def test_generate_and_validate_enterprise_license(self):
        expires = datetime.utcnow() + timedelta(days=30)
        license_key = core_license.generate_license_key(self.env.cr.dbname, self.company.id, expires, self.secret)
        self.company.google_feed_enterprise_license = license_key
        self.company.action_validate_google_feed_enterprise()
        self.assertTrue(self.company.google_feed_enterprise)
        self.assertEqual(self.company.google_feed_enterprise_status, 'valid')
        # Enterprise should enable Pro features in the feed service
        cache = self.env['google.feed.cache']
        self.assertTrue(cache.is_pro_active(self.company))

    def test_invalid_enterprise_license(self):
        self.company.google_feed_enterprise_license = 'GSF|db=wrong|cid=1|exp=2026-01-01T00:00:00Z|sig=bad'
        self.company.action_validate_google_feed_enterprise()
        self.assertFalse(self.company.google_feed_enterprise)
        self.assertEqual(self.company.google_feed_enterprise_status, 'invalid')
