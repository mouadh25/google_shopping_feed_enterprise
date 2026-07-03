# -*- coding: utf-8 -*-
import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class IrModule(models.Model):
    _inherit = 'ir.module.module'

    @api.multi
    def button_uninstall(self):
        """Extend uninstall to clean up Enterprise data."""
        ent = self.filtered(lambda m: m.name == 'google_shopping_feed_enterprise')
        if ent:
            _logger.info('google_feed: uninstall hook triggered for google_shopping_feed_enterprise')
            self._cleanup_enterprise()
        return super(IrModule, self).button_uninstall()

    def _cleanup_enterprise(self):
        """Remove enterprise license data on uninstall."""
        _logger.info('google_feed: cleaning up Enterprise edition license data')
        
        # Clear enterprise settings from all companies
        companies = self.env['res.company'].sudo().search([])
        for company in companies:
            if hasattr(company, 'google_feed_enterprise_license'):
                company.write({
                    'google_feed_enterprise_license': False,
                    'google_feed_enterprise': False,
                    'google_feed_enterprise_status': 'none',
                    'google_feed_enterprise_expires': False,
                    'google_feed_enterprise_verified_at': False,
                })
        
        _logger.info('google_feed: Enterprise cleanup complete (cleared %d companies)', len(companies))
