from unittest import TestCase
from mock import Mock, patch

from layers.external_citation import ExternalCitationLayer

class ExternalCitationsTest(TestCase):
    @patch('layers.external_citation.ExternalCitationLayer.generate_fdsys_href_tag')
    def test_statues_at_large_link(self, generate_fdsys_href_tag):
        text = '124 Stat. 2859'
        citation = text.split()
        link = ExternalCitationLayer.generate_statutes_at_large_link(text, citation)
        parameters = generate_fdsys_href_tag.call_args[0][1]
        self.assertEqual(parameters['statutecitation'], '124 stat 2859')

    @patch('layers.external_citation.ExternalCitationLayer.generate_fdsys_href_tag')
    def test_public_law_link(self, generate_fdsys_href_tag):
        text = 'Public Law 111-203'
        citation = [111, 203]
        link = ExternalCitationLayer.generate_public_law_link(text, citation)
        parameters = generate_fdsys_href_tag.call_args[0][1]
        self.assertEqual(parameters.keys(), ['collection', 'lawnum', 'congress', 'lawtype'])
        self.assertEqual(parameters['collection'], 'plaw')
        self.assertEqual(parameters['congress'], 111)
        self.assertEqual(parameters['lawnum'], 203)
        self.assertEqual(parameters['lawtype'], 'public')


    def test_citation_type_to_generator(self):
        citation_type = 'STATUTES_AT_LARGE'
        layer = ExternalCitationLayer(None, None)
        generator = layer.citation_type_to_generator(citation_type)
        self.assertEqual(generator, ExternalCitationLayer.generate_statutes_at_large_link)

        citation_type = 'PUBLIC_LAW'
        generator = layer.citation_type_to_generator(citation_type)
        self.assertEqual(generator, ExternalCitationLayer.generate_public_law_link)
