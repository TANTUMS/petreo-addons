 #-*- coding: utf 8 -*-
import pdb
import pooler
from report import report_sxw
import calendar
import datetime
import time
from datetime import datetime, date, time, timedelta
import math

class ReportStatus(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(ReportStatus, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_result': self.get_result,
            'get_date': self.get_date,
            'get_week': self.get_week,
        })
        self.invoice_ids = []
        self.moves_obj = []

    def get_result(self, form):
        
        #DECLARAMOS VARIABLES
        Insumos = None
        Planta = None
        Proveedor = None
        Periodo = None
        list_invoice = []
        objs_purchase_orders= None
        ids_purchase_orders = None
        list_po=[]
        list_products=[]
        obj_purchase=None
        lista_po=[]
        id_partners=[]
        warehouse=[]

        if form['form']['product_id']:
            Insumos = form['form']['product_id'][0]

        if form['form']['warehouse_id']:
            Planta =  form['form']['warehouse_id'][0]

        if form['form']['partner_id']:
            Proveedor = form['form']['partner_id'][0]

        if form['form']['start_date']:
            Fecha_Inicial = form['form']['start_date']

        if form['form']['end_date']:
            Fecha_Final = form['form']['end_date']


    #FORMAR FILTRO INICIAL Y LO FORMAMOS SEGUN LOS DATOS ELEGIDOS DEL WIZARD
        filtro = [('type', '=', 'in'),('state', '=', 'done'),('purchase_id','!=',None),('date_done','>=',Fecha_Inicial),('date_done','<=',Fecha_Final)]
       
        if Proveedor:
            partner = self.pool.get('stock.picking').search(self.cr, self.uid, [('partner_id','=', Proveedor)])
            obj_partner = self.pool.get('stock.picking').browse(self.cr, self.uid, partner)
            for e in obj_partner:
                id_partners.append(e.partner_id['id'])
            filtro.append(('partner_id','in',id_partners))

       #SI ELIGE INSUMOS
        if Insumos:
            ids_products = self.pool.get('stock.picking').search(self.cr, self.uid,[('product_id', '=',Insumos)])
            obj_products = self.pool.get('stock.picking').browse(self.cr, self.uid, ids_products)
            for i in obj_products:
                if i.product_id['id'] == Insumos:
                    list_products.append(i.product_id['id'])
                    filtro.append(('product_id','in',list_products))


        if Planta:
            ids_warehouse = self.pool.get('purchase.order').search(self.cr, self.uid, [('warehouse_id','=',Planta)])
            obj_warehouse = self.pool.get('purchase.order').browse(self.cr, self.uid, ids_warehouse)
            for o in obj_warehouse:
                warehouse.append(o.id)
            filtro.append(('purchase_id','in',warehouse))

        self.invoice_ids= self.pool.get('stock.picking').search(self.cr, self.uid, filtro, order="date_done")
        invoice_obj= self.pool.get('stock.picking').browse(self.cr, self.uid, self.invoice_ids )
        return {'invoice_obj': invoice_obj}

    def get_date(self,date_done):
        fecha = str(date_done)
        date_object = datetime.strptime(fecha[:10],'%Y-%m-%d')
        date_time = str(date_object)[:10]
        return date_time

    def get_week(self,date_time):
        week = []
        e,a,b = date_time.split("-")
        b = int(b)
        return b

report_sxw.report_sxw('report.purchase', 'reporte.compras.wizard', 'reporte_compras/reports/report_sale_webkit.mako', parser = ReportStatus)