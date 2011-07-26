# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2008 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from tools.translate import _

from osv import fields, osv

#
# Dimensions Definition
#
class mrp_bom(osv.osv):
    _inherit = 'mrp.bom'

    _columns = {
        'for_template': fields.boolean('Distinta di Template', help="Una Distinta Base di Template può essere solo un kit le cui componeneti saranno esplose sugli articoli"),

    }
    def cktemplate(self, cr, uid, ids, for_template,product_id):
      def get_products_from_product(self,cr, uid, ids, context={}):
        #import pdb;pdb.set_trace()
        
        result = []
        args =['default_code','product_tmpl_id']
        dati = self.pool.get('product.product').read(cr,uid,ids,args)
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
      v={}
      if for_template:
        #import pdb;pdb.set_trace()
        prodotti = get_products_from_product(self,cr,uid,[product_id], context={})
        if prodotti:
          lines = self.pool.get('mrp.bom').search(cr, uid, [('product_id', 'in', prodotti),('for_template','=',True)]) 
          if lines:  
            raise osv.except_osv(_('ERRORE !'),_('HAI GIÀ UNA DISTINTA DI TEMPLATE'))
            v['for_template']=0
          else:
            if for_template:
              v['type']='phantom'
        
      return {'value':v}
mrp_bom()


