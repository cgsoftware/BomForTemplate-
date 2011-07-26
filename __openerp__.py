##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################
{
    "name" : "Define a Bom for a Template and Generate a Bon for all product of Template",
    "version" : "1.0",
    "author" : "Tiny",
    "category" : "Mrp and variant",
    "description":"""O.
    """,
    "depends" : ["base", "product", "product_variant_multi", "mrp"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : ['bom_for_template_view.xml', 'wizard/GeneraDistinta.xml'],
    "active": False,
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

