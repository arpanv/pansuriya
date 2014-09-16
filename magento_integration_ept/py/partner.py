import magento

from openerp.osv import fields, osv
from openerp.tools.translate import _
class Partner(osv.Model):
    "Partner"
    _inherit = 'res.partner'
    
    _columns = {                    
                    'anniversary_date_ept':fields.date('Anniversary Date'),
                    'birthdate_ept':fields.date('Birthdate'),
                    'gender_ept':fields.selection([('Male','Male'),('Male','Male')],string="Gender"),
                    
                    #Contact Informations
                    'alternate_email_ept':fields.char('Alternate Email'),
                    'contact_mobile_number_ept':fields.char('Contact Mobile Number'),
                    'contact_number_ept':fields.char('Contact Number'),
                    'extension_ept':fields.char('Extension'),
                    
                    #Company Informations
                    'company_name_ept':fields.char('Company Name'),
                    'owner_name_ept':fields.char('Owner Name'),
                    
                    #Business Information
                    'nature_of_business_ept':fields.char('Nature of Business'),
                    'broker_ept':fields.boolean('Broker'),
                    'agent_ept':fields.boolean('Agent'),
                    'dun_bradstreet_number_ept':fields.char('Dun & Bradstreet Number'),
                    
                    #Member Of
                    'members_of_trade_portal_ept':fields.char('Members of Trade Portal'),
                    'members_of_trade_association_ept':fields.char('Members of Trade Association'),
                    
                    #Third Party Reference
                    'third_party_name_ept':fields.char('Third Party Name'),
                    'third_party_contact_number_ept':fields.char('Third Party Contact Number'),
                    'third_party_address_ept':fields.text('Third party address'),
                    'third_party_email_ept':fields.char('Third party Email'),
                    
                    #Bank Details.
                    'branch_name_ept':fields.char('Branch Name'),
                    'branch_address_ept':fields.text('Branch Address'),
                    'branch_city_ept':fields.char('Branch City'),
                    'branch_state_ept':fields.char('Branch State'),
                    'branch_postal_code_ept':fields.char('Branch zip code'),
                    'is_manufacture' : fields.boolean('Manufacturer'),                    
                   
                    
                }
    
    def _get_title(self,cr,uid,customer_data,context):
        if customer_data.get('customer_prefix',False):
            title = customer_data.get('customer_prefix')
            title_ids = self.pool.get('res.partner.title').search(cr,uid,[('name','=',title),('domain','=','contact')])
            if title_ids:
                return title_ids[0]
            else:
                return self.pool.get('res.partner.title').create(cr,uid,{'name':title,'shortcut':title,'domain':'contact'})
        else:
            return False
    
    def import_bank_details(self,cr,uid,customer_details,partner,context={}):
        if not partner.bank_ids:
            bank_name = customer_details.get('bank_name',False)
            bank_branch_name = customer_details.get('bank_branch_name',False)
            type_of_account = customer_details.get('type_of_account',False)
            account_number = customer_details.get('account_number',False)
            bank_branch_address = customer_details.get('bank_branch_address',False)
            bank_city = customer_details.get('bank_city',False)
            bank_state = customer_details.get('bank_state',False)
            bank_zip_code = customer_details.get('bank_zip_code',False)
            
            bank_id = False   
            bank_type_id = False         
            self.write(cr,uid,[partner.id],{
                                                'branch_name_ept':bank_branch_name,
                                                'branch_address_ept':bank_branch_address,
                                                'branch_city_ept':bank_city,
                                                'branch_state_ept':bank_state,
                                                'branch_postal_code_ept':bank_zip_code
                                            })
            if bank_name and type_of_account and account_number:
                
                #Get Bank or Create New
                bank_ids = self.pool.get('res.bank').search(cr,uid,[('name','=',bank_name)])
                if bank_ids:
                    bank_id = bank_ids[0]
                else:
                    bank_id = self.pool.get('res.bank').create(cr,uid,{
                                                                'name':bank_name
                                                             })
                
                #Get Bank Account Type or Create New
                bank_type_ids = self.pool.get('res.partner.bank.type').search(cr,uid,[('name','=',type_of_account),('code','=',type_of_account)])
                if bank_type_ids:
                    bank_type_id = bank_type_ids[0]
                else:
                    bank_type_id = self.pool.get('res.partner.bank.type').create(cr,uid,{
                                                                'name':type_of_account,
                                                                'code':type_of_account
                                                             })
                
                
                created_bank_id = self.pool.get('res.partner.bank').create(cr,uid,
                                                            {
                                                                'state':type_of_account,
                                                                'acc_number':account_number,
                                                                'partner_id':partner.id,
                                                                'bank':bank_id
                                                             }
                                                         )
                return created_bank_id
            else:
                return False
            
    def create_using_magento_data(self, cursor, user, customer_data, context):
        """
        Creates record of customer values sent by magento

        :param cursor: Database cursor
        :param user: ID of current user
        :param customer_data: Dictionary of values for customer sent by magento
        :param context: Application context. Contains the magento_website
                        to which the customer has to be linked
        :return: Browse record of record created
        """
        partner_id = self.create(
            cursor, user, {
                'name': u' '.join(
                    [customer_data['firstname'], customer_data['lastname']]
                ),
                'email': customer_data['email'],                
                'magento_ids': [
                    (0, 0, {
                        'magento_id': customer_data.get('customer_id', 0),
                        'website': context.get('website',False) or context.get('magento_website',False) or '',
                    })
                ],
                #Extra Magento Fields set                                
                'title':self._get_title(cursor,user,customer_data,context=context),
                'website':customer_data.get('website', False),
                'birthdate_ept':customer_data.get('dob', False),
                'anniversary_date_ept':customer_data.get('anniversary', False),
                
                'gender_ept':customer_data.get('gender', False) and customer_data.get('gender').lstrip().rstrip() or False,
                'alternate_email_ept':customer_data.get('alternate_email_id', False),
                'extension_ept':customer_data.get('extension', False),
                'contact_mobile_number_ept':customer_data.get('contact_mobile_number', False),
                'contact_number_ept':customer_data.get('contact_number', ''),                
                'owner_name_ept':customer_data.get('owner_name', False),
                'nature_of_business_ept':customer_data.get('nature_of_business', False),
                'broker_ept':True if customer_data.get('broker', False) == 'Yes' else False,
                'agent_ept':True if customer_data.get('agent', False) == 'Yes' else False,
                'dun_bradstreet_number_ept':customer_data.get('dun_bradstreet_number', False),
                'members_of_trade_portal_ept':customer_data.get('members_of_trade_portal', False),
                'members_of_trade_association_ept':customer_data.get('members_of_trade_association', False),
                'third_party_name_ept':customer_data.get('third_party_name', False),
                'third_party_contact_number_ept':customer_data.get('third_party_contact_number', False),
                'third_party_address_ept':customer_data.get('third_party_address', False),
                'third_party_email_ept':customer_data.get('third_party_email', False),                                
            }, context=context
        )
        partner = self.browse(cursor, user, partner_id, context)
        self.import_bank_details(cursor,user,customer_data,partner,context=context)
        return partner
    
    def match_address_with_magento_data(
        self, cursor, user, address, address_data
    ):
        """Match the `address` in openerp with the `address_data` from magento
        If everything matches exactly, return True, else return False

        :param cursor: Database cursor
        :param user: ID of current user
        :param address: Browse record of address partner
        :param address_data: Dictionary of address data from magento
        :return: True if address matches else False
        """
        # Check if the name matches
        if address.name != u' '.join(
            [address_data['firstname'], address_data['lastname']]
        ):
            return False

        if not all([
            (address.street or None) == address_data.get('street'),
            (address.zip or None) == address_data.get('postcode',None),
            (address.city or None) == address_data.get('city'),
            (address.phone or None) == address_data.get('telephone'),
            (address.fax or None) == address_data.get('fax',None),
            (address.country_id and address.country_id.code or None) ==
                address_data['country_id'],
            (address.state_id and address.state_id.name or None) ==
                address_data['region']
        ]):
            return False

        return True

    def create_address_as_partner_using_magento_data(
        self, cursor, user, address_data, parent, context
    ):
        """Create a new partner with the `address_data` under the `parent`

        :param cursor: Database cursor
        :param user: ID of current user
        :param address_data: Dictionary of address data from magento
        :param parent: Parent partner for this address partner.
        :param context: Application Context
        :return: Browse record of address created
        """
        country_obj = self.pool.get('res.country')
        state_obj = self.pool.get('res.country.state')

        country = country_obj.search_using_magento_code(
            cursor, user, address_data['country_id'], context
        )
        if address_data['region']:
            state_id = state_obj.find_or_create_using_magento_region(
                cursor, user, country, address_data['region'], context
            ).id
        else:
            state_id = None
        address_id = self.create(cursor, user, {
            'name': u' '.join(
                [address_data.get('firstname',''), address_data.get('lastname','')]
            ),
            'street': address_data.get('street',False),
            'state_id': state_id,
            'country_id': country.id,
            'city': address_data.get('city',False),
            'zip': address_data.get('postcode',False),
            'phone': address_data.get('telephone',False),
            'fax': address_data.get('fax',False),
            'parent_id': parent.id,
        }, context=context)

        return self.browse(cursor, user, address_id, context=context)
Partner()
