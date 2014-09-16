#########################################################################
# Copyright (C) 2009  Sharoon Thomas, Open Labs Business solutions      #
#                                                                       #
#This program is free software: you can redistribute it and/or modify   #
#it under the terms of the GNU General Public License as published by   #
#the Free Software Foundation, either version 3 of the License, or      #
#(at your option) any later version.                                    #
#                                                                       #
#This program is distributed in the hope that it will be useful,        #
#but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#GNU General Public License for more details.                           #
#                                                                       #
#You should have received a copy of the GNU General Public License      #
#along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#########################################################################

{
    "name" : "Stone Image Gallery",    
    "author" : "Emipro Technologies",
    "website" : "www.emiprotechnologies.com",
    "category" : "Added functionality - Stone Extension",
    "depends" : ['product_stone_search_ept'],
    "description": """
    This Module implements an Image Gallery for Stones.
    You can add images against every stone.
    """,
    "init_xml": [],
    "update_xml": [
        'security/ir.model.access.csv',
        'views/product_images_view.xml',
        'views/company_view.xml'
    ],
    "installable": True,
    "active": False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
