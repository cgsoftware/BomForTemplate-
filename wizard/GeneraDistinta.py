# -*- encoding: utf-8 -*-

import wizard
import decimal_precision as dp
import pooler
import time
from tools.translate import _
from osv import osv, fields
from tools.translate import _


class genera_distinte_template(osv.osv_memory):
    _name = 'genera.distinte.template'
    _description = 'Genera una distinta base partendo da altre'
    _columns = {
         'skeletro':fields.many2one('mrp.bom', 'Distinta di Riferimento ', required=True),
         'name':fields.many2one('product.template', 'Template ', required=True),
    }
  
  
  
    def view_init(self, cr, uid, fields_list, context=None):
        #import pdb;pdb.set_trace()
        res = super(genera_distinte_template, self).view_init(cr, uid, fields_list, context=context)
        
    #    bom_obj = self.pool.get('mrp.bom')  
    #   first = True
    #    if context is None:
    #        context = {}
    #    ids = context.get('active_ids', [])
    #    for move in bom_obj.browse(cr, uid, context.get('active_ids', []), context=context):
    #        if self.cktemplate(cr,uid,ids,move.product_id.id):
    #            raise osv.except_osv(_('Invalid action !'), _('Non sembra ci sia una distinta di template !'))
        return res
    
    
    def cktemplate(self, cr, uid, ids, product_id):
      def get_products_from_product(self, cr, uid, ids, context={}):
        #import pdb;pdb.set_trace()
        
        result = []
        args = ['default_code', 'product_tmpl_id']
        dati = self.pool.get('product.product').read(cr, uid, ids, args)
        if dati:
         for product in self.pool.get('product.product').browse(cr, uid, ids, context=context):
            for product_id in product.product_tmpl_id.variant_ids:
                result.append(product_id.id)
        else:
          for product in ids:
            result.append(product)
        return result
      # prima controlla che non ci sia già una distinta di template e la vilualizza e annulla l'impostazione
      # poi obbliga che la distinta sia kit Phantom in modo che sia le componenti saranno esplose in produzione e non l'articolo
        #import pdb;pdb.set_trace()
      ok = True
      prodotti = get_products_from_product(self, cr, uid, [product_id], context={})
      if prodotti:
          lines = self.pool.get('mrp.bom').search(cr, uid, [('product_id', 'in', prodotti), ('for_template', '=', True)]) 
          if lines:  
            ok = True
          else:
            ok = False
            
        
      return ok
    
    def __get_template(self, cr, uid, context=None):
        bom_obj = self.pool.get('mrp.bom')  
        if context is None:
            context = {}
        First = True
        for riga in bom_obj.browse(cr, uid, context.get('active_ids', []), context=context):
          if First:
            # è il primo record deve inserire prima una testata
            res = riga.product_id.product_tmpl_id.id
                   
        #import pdb;pdb.set_trace()
        return res 
      
      
     

    def genera(self, cr, uid, ids, context=None):
      # VERIFICA CHE CI SIA LA DISTINTA BASE PER OGNI SINGOLO ARTICOLO DEL TEMPLATE SE C'È
      # VERIFICA ED EVENTUALMENTE AGGIUNGE LA RIGA DELLA DISTINTA DI TEMPLATE ALTRIMENTI CREA L'INTERA DISTINTA BASE PER L'ARTICOLO. 
        # legge i parametri
      param = self.pool.get('genera.distinte.template').browse(cr, uid, ids)[0]
        # cerca gli articoli del template
      cerca = [('product_tmpl_id', '=', param.name.id)]
      articoli = self.pool.get('product.product').search(cr, uid, cerca)     
      if articoli:
         riga_bom = self.pool.get('mrp.bom').browse(cr, uid, [param.skeletro.id])[0]
         for articolo_id in articoli:
           #import pdb;pdb.set_trace()
           # per ogni articolo cerca le distinte attive
           cerca = [('product_id', '=', articolo_id), ('bom_id', '=', 0), ('active', '=', True)]
           distinte = self.pool.get('mrp.bom').search(cr, uid, cerca)
           if distinte:
             # ci sono distinte
             for distinta_id in distinte:
                cerca = [('bom_id', '=', distinta_id), ('active', '=', True), ('product_id', '=', riga_bom.product_id.id)]
                righe_comp = self.pool.get('mrp.bom').search(cr, uid, cerca)
                if righe_comp:
                  # C'E' GIÀ LA RIGA CON L'ARTICOLO DISTINTA SKELETRO
                  #import pdb;pdb.set_trace()
                  pass
                else:
                  # aggiunge una riga alla distinta con la voce di skeletro
                  #import pdb;pdb.set_trace()
                  riga_distinta = {
                               'name':riga_comp.name,
                               'code':'',
                               'product_id':riga_comp.product_id.id,
                               'bom_id':distinta_id,
                               'type':'phantom',
                               'product_uom': riga_comp.product_id.uom_id.id,
                               }
                  riga_dist_id = self.pool.get('mrp.bom').create(cr, uid, riga_distinta)
           else:
             # non ci sono ditinte dell' articolo
             riga_art = self.pool.get('product.product').browse(cr, uid, [articolo_id])[0]

             testa_distinta = {
                               'name':riga_art.name,
                               'code':riga_art.default_code,
                               'product_id':riga_art.id,
                               'bom_id':0,
                               'product_uom': riga_art.uom_id.id,
                               }
             testa_id = self.pool.get('mrp.bom').create(cr, uid, testa_distinta)
             if testa_id:
                riga_comp = self.pool.get('product.product').browse(cr, uid, [riga_bom.product_id.id])[0]
                # scrive la riga componente fantasma
                riga_distinta = {
                               'name':riga_comp.name,
                               'code':'',
                               'product_id':riga_comp.id,
                               'bom_id':testa_id,
                               'type':'phantom',
                               'product_uom': riga_comp.uom_id.id,
                               }
                riga_dist_id = self.pool.get('mrp.bom').create(cr, uid, riga_distinta)
        
      return {'type': 'ir.actions.act_window_close'}
             


    
    _defaults = {
               
                 }
    
genera_distinte_template()  






class open_fiscaldoc(osv.osv_memory):
    _name = "open.fiscaldoc"
    _description = "Apre il Documento Generato"

    def open_doc(self, cr, uid, ids, context=None):

        """
             To open invoice.
             @param self: The object pointer.
             @param cr: A database cursor
             @param uid: ID of the user currently logged in
             @param ids: the ID or list of IDs if we want more than one
             @param context: A standard dictionary
             @return:

        """
 #       if context is None:
 #           context = {}
 #       mod_obj = self.pool.get('ir.model.data')
 #       for advance_pay in self.browse(cr, uid, ids, context=context):
 #           form_res = mod_obj.get_object_reference(cr, uid, 'fiscaldoc.header', 'invoice_form')
 #           form_id = form_res and form_res[1] or False
 #           tree_res = mod_obj.get_object_reference(cr, uid, 'account', 'invoice_tree')
 #           tree_id = tree_res and tree_res[1] or False

        return {
            'name': _('Documenti di Vendita'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'fiscaldoc.header',
            'res_id': int(context['doc_id'][0]),
            'view_id': False,
            'context': context,
            'type': 'ir.actions.act_window',
         }

#          'views': [(form_id, 'form'), (tree_id, 'tree')],

open_fiscaldoc()
