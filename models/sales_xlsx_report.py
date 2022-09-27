from odoo import models


class DailysReportXlsx(models.AbstractModel):
    _name = 'report.dailys_rep_profits.day_wise_profit_xlsx_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, delivery):
        report_name = 'Daily Report'
        sheet = workbook.add_worksheet(report_name[:31])
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, 'Reference', bold)
        sheet.write(0, 1, 'Amount', bold)
        row = 0
        for obj in delivery.sale_po_lines:
            row = row + 1
            # One sheet by partner
            format3 = workbook.add_format({'num_format': 'dd/mm/yy', 'border': 1})
            if obj.partner_id:
               sheet.write(row, 0, obj.partner_id.name)
            if obj.product_id:
                sheet.write(row, 0, obj.product_id.name)
            if obj.source:
                sheet.write(row, 0, obj.source.name)
            sheet.write(row, 1, obj.amount)
            first_row = row

class CustomerAgedReport(models.Model):
    _inherit = "customer.area.aged"

    def room_summary_test(self,res):
        print(res)

