# -*- coding: utf-8 -*-
import secrets
from datetime import datetime

from odoo import api, fields, models

try:
    # Import the shared license helpers from the Pro package
    from odoo.addons.google_shopping_feed import license as gsf_license
except Exception:
    gsf_license = None


class ResCompanyEnterprise(models.Model):
    _inherit = 'res.company'

    google_feed_enterprise = fields.Boolean(
        string='Google Shopping Feed Enterprise',
        default=False,
        help='Enable enterprise-grade multi-company feed features for this company.',
    )
    google_feed_enterprise_license = fields.Char(
        string='Enterprise License Key',
        help='Paste the enterprise license key issued for this database/company.',
    )
    google_feed_enterprise_status = fields.Selection([
        ('none', 'None'),
        ('valid', 'Valid'),
        ('invalid', 'Invalid'),
    ],
        string='Enterprise License Status',
        default='none',
        store=True,
    )
    google_feed_enterprise_expires = fields.Datetime(
        string='Enterprise License Expires',
        readonly=True,
    )
    google_feed_enterprise_verified_at = fields.Datetime(
        string='Enterprise License Verified At',
        readonly=True,
    )

    def _get_license_secret(self):
        IrParam = self.env['ir.config_parameter'].sudo()
        secret = IrParam.get_param('google_feed.license_secret')
        if not secret:
            secret = secrets.token_hex(32)
            IrParam.set_param('google_feed.license_secret', secret)
        return secret

    def _validate_enterprise_key(self, license_key):
        """Validate the enterprise license key using shared helper when available.

        Returns (valid: bool, expires: datetime|None)
        """
        if not license_key:
            return False, None
        secret = self._get_license_secret()
        if gsf_license and hasattr(gsf_license, 'validate_license_key'):
            try:
                valid, exp_str = gsf_license.validate_license_key(license_key, self.env.cr.dbname, self.id, secret)
            except Exception:
                return False, None
            if not valid:
                return False, None
            try:
                # `exp_str` may be an ISO string
                expires = datetime.strptime(exp_str, '%Y-%m-%dT%H:%M:%SZ')
            except Exception:
                expires = None
            if expires and expires < datetime.utcnow():
                return False, None
            return True, expires
        # Fallback: simple presence check (not secure)
        return False, None

    def action_validate_google_feed_enterprise(self):
        for record in self:
            valid, expires = record._validate_enterprise_key(record.google_feed_enterprise_license)
            if valid:
                record.google_feed_enterprise = True
                record.google_feed_enterprise_status = 'valid'
                record.google_feed_enterprise_expires = expires
                record.google_feed_enterprise_verified_at = fields.Datetime.now()
            else:
                record.google_feed_enterprise = False
                record.google_feed_enterprise_status = 'invalid' if record.google_feed_enterprise_license else 'none'
                record.google_feed_enterprise_expires = False
                record.google_feed_enterprise_verified_at = False
        return True

    def action_clear_google_feed_enterprise(self):
        for record in self:
            record.google_feed_enterprise_license = False
            record.google_feed_enterprise = False
            record.google_feed_enterprise_status = 'none'
            record.google_feed_enterprise_expires = False
            record.google_feed_enterprise_verified_at = False
        return True
