from odoo import models, fields, api, _
from datetime import datetime, date


class DayWiseProfit(models.Model):
    _name = 'day.wise.profit'

    today_date = fields.Date(default=fields.Date.today())
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id)
    sale_po_lines = fields.One2many('day.wise.profit.lines', 'daily_sales_id')
    type = fields.Selection([('day', 'Day Wise'), ('brand', 'Brand Wise'), ('party', 'Party Wise')], copy=False,
                            string="Type", default='day')

    @api.onchange('today_date','type')
    def _onchange_today_date(self):
        if self.today_date:
            if self.type == 'day':
                # profit_loss = 0.0;
                # invoices = self.env['account.move'].search(
                #     [('invoice_date', '=', self.today_date),
                #      ('move_type', '=', 'out_invoice'),('state', '=', 'posted'),
                #      ('company_id', '=', self.company_id.id)])
                #
                # list = []
                # all = (0, 0, {
                #     'source': 'Sales',
                #     'amount': sum(invoices.mapped('amount_total')),
                #     # 'tax_amount': sum(invoices.mapped('amount_tax'))
                #
                # })
                # profit_loss += sum(invoices.mapped('amount_total'))
                # invoices = self.env['account.move'].search(
                #     [('invoice_date', '=', self.today_date),
                #      ('move_type', '=', 'out_invoice'),('state', '=', 'posted'),
                #      ('company_id', '=', self.company_id.id)])
                # vat_receivable = (0, 0, {
                #     'source': 'Vat Receivable',
                #     'amount': sum(invoices.mapped('amount_tax'))
                # })
                # profit_loss += sum(invoices.mapped('amount_tax'))
                # # list.append(vat_receivable)
                # bills = self.env['account.move'].search(
                #     [('invoice_date', '=', self.today_date),
                #      ('move_type', '=', 'in_invoice'),('state', '=', 'posted'),
                #      ('company_id', '=', self.company_id.id)])
                #
                # po_all = (0, 0, {
                #     'source': 'Purchase',
                #     'amount': sum(bills.mapped('amount_total')),
                #     # 'tax_amount': sum(bills.mapped('amount_tax'))
                #
                # })
                # # list.append(po_all)
                # profit_loss -= sum(bills.mapped('amount_total'))
                # branch_expenses = self.env['hr.expense'].search(
                #     [('date', '=', self.today_date),
                #      ])
                # exp_all = (0, 0, {
                #     'source': 'Expenses',
                #     'amount': sum(branch_expenses.mapped('total_amount')),
                #     # 'tax_amount': sum(bills.mapped('amount_tax'))
                #
                # })
                # # list.append(exp_all)
                # profit_loss -= sum(branch_expenses.mapped('total_amount'))
                # bills = self.env['account.move'].search(
                #     [('invoice_date', '=', self.today_date),
                #      ('move_type', '=', 'in_invoice'),('state', '=', 'posted'),
                #      ('company_id', '=', self.company_id.id)])
                #
                # vat_payable = (0, 0, {
                #     'source': 'Vat Payable',
                #     'amount': sum(bills.mapped('amount_tax')),
                # })
                # # list.append(vat_payable)
                # profit_loss -= sum(bills.mapped('amount_tax'))
                # print('profit_loss', profit_loss)
                # vat_payable = (0, 0, {
                #     'source': 'Profit/Loss',
                #     'amount': profit_loss,
                # })
                # list.append(vat_payable)
                list = []
                profit = 0
                for each in self.env['sale.estimate'].search([('c_date', '=', self.today_date)]):
                    for line in each.estimate_ids:
                        amount = sum(
                            self.env['purchase.order.line'].search([('product_id', '=', line.product_id.id)]).mapped(
                                'price_unit'))
                        quantity = sum(
                            self.env['purchase.order.line'].search([('product_id', '=', line.product_id.id)]).mapped(
                                'product_qty'))
                        purchased_price =0
                        if amount:
                            purchased_price = amount / quantity
                        per_unit = line.price_unit - purchased_price
                        profit += line.product_uom_qty * per_unit
                vat_payable = (0, 0, {
                    'source': 'Profit/Loss',
                    # 'partner_id': each.partner_id.id,
                    'amount': profit,
                })
                list.append(vat_payable)




            if self.type == 'party':
               list = []
               for partner in self.env['res.partner'].search([('estimator', '=', True)]):
                   profit = 0
                   for each in self.env['sale.estimate'].search([('partner_id','=',partner.id),('c_date','=',self.today_date)]):
                       for line in each.estimate_ids:
                           amount = sum(self.env['purchase.order.line'].search([('product_id','=',line.product_id.id)]).mapped('price_unit'))
                           quantity = sum(self.env['purchase.order.line'].search([('product_id','=',line.product_id.id)]).mapped('product_qty'))
                           purchased_price = amount/quantity
                           per_unit = line.price_unit - purchased_price
                           profit += line.product_uom_qty *per_unit
                   vat_payable = (0, 0, {
                       # 'source': 'Profit/Loss',
                       'partner_id': partner.id,
                       'amount': profit,
                   })
                   list.append(vat_payable)
            if self.type == 'brand':
               list = []
               for product in self.env['product.template'].search([('grouped','=',True)]):
                   profit = 0
                   for each in self.env['sale.estimate'].search([('c_date', '=', self.today_date)]):
                       for line in each.estimate_ids:
                           if product == line.product_id.parent_id:
                                   amount = sum(self.env['purchase.order.line'].search([('product_id','=',line.product_id.id)]).mapped('price_unit'))
                                   quantity = sum(self.env['purchase.order.line'].search([('product_id','=',line.product_id.id)]).mapped('product_qty'))
                                   purchased_price = amount/quantity
                                   per_unit = line.price_unit - purchased_price
                                   profit += line.product_uom_qty *per_unit
                   vat_payable = (0, 0, {
                       # 'source': 'Profit/Loss',
                       # 'partner_id': each.partner_id.id,
                       'product_id': product.id,
                       'amount': profit,
                   })
                   list.append(vat_payable)
            self.sale_po_lines = False
            self.sale_po_lines = list


class DayWiseProfitLines(models.Model):
    _name = 'day.wise.profit.lines'

    daily_sales_id = fields.Many2one('day.wise.profit')
    source = fields.Char(string="Source")
    partner_id = fields.Many2one('res.partner', string="Customer")
    product_id = fields.Many2one('product.template', string="Brand Wise")
    amount = fields.Float(string="Amount")

class RtgsNeftCollections(models.Model):
    _inherit = "neft.rtgs.collection"

    def action_bulk_validate(self):
        for each in self.env['neft.rtgs.collection'].search([('state','=','draft')],limit=20):
            each.action_confirm()
