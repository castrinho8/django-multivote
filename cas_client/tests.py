# coding: utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_parse_xml(self):
        xml_case = '''

<cas:serviceResponse xmlns:cas='http://www.yale.edu/tp/cas'>
    <cas:authenticationSuccess>
        <cas:user>santiago.saavedral</cas:user>
        
        

        <!-- TODO: Maybe we need a c:if here... Or so I think!!! xD -->
        <cas:attributes>
                            
                <cas:documentType>NIF</cas:documentType>
                            
                <cas:surname1>MySurname</cas:surname1>
                            
                <cas:roles>[srv.accedys, mat.alumno.123456789.1314, mat.alumno.234567890.1314, srv.vpn.estudantes.fi, curso.1314]</cas:roles>
                            
                <cas:surname2>MySecondSurname</cas:surname2>
                            
                <cas:documentNumber>12345678Z</cas:documentNumber>
                            
                <cas:login>user.login</cas:login>
                            
                <cas:firstName>UserName</cas:firstName>
            
        </cas:attributes>

    </cas:authenticationSuccess>
</cas:serviceResponse>
'''

        from cas_client.models import CasBackend

        backend = CasBackend()
        data = backend.parse_cas_xml(xml_case)

        self.assertEqual(data['login'], u'user.login')
        self.assertEqual(data['first_name'], u'UserName')
        self.assertEqual(data['last_name'], u'MySurname MySecondSurname')
        self.assertEqual(data['nif'], u'12345678Z')
        self.assertEqual(data['doctype'], u'NIF')
        self.assertTrue('srv.accedys' in data['roles'])

