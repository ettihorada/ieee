import math
import urllib
import urllib2
import pprint
import json


class IeeeClient(object):

    # API endpoint
    __BASEURL = "http://ieeexploreapi.ieee.org/api/v1/search/articles"

    def __init__(self, api_key):
        self.api_key = api_key

        # flag that some search criteria has been provided
        self.query_provided = False

        # flag that article number has been provided, which overrides all other search criteria
        self.using_article_number = False

        # flag that a boolean method is in use
        self.using_boolean = False

        # flag that a facet is in use
        self.using_facet = False

        # flag that a facet has been applied, in the event that multiple facets are passed
        self.facet_applied = False

        # default of 25 results returned
        self.result_set_max = 25

        # maximum of 200 results returned
        self.result_set_max_cap = 1000

        # records returned default to position 1 in result set
        self.start_record = 1

        # default sort order is ascending; could also be 'desc' for descending
        self.sort_order = 'asc'

        # field name that is being used for sorting
        self.sort_field = 'article_title'

        # array of permitted search fields for searchField() method
        self.allowed_search_fields = ['abstract', 'affiliation', 'article_number', 'article_title', 'author', 'boolean_text', 'content_type', 'd-au', 'd-pubtype', 'd-publisher', 'd-year', 'doi', 'end_year', 'facet', 'index_terms', 'isbn', 'issn', 'is_number', 'meta_data', 'open_access', 'publication_number', 'publication_title', 'publication_year', 'publisher', 'querytext', 'start_year', 'thesaurus_terms']

        # dictionary of all search parameters in use and their values
        self.parameters = {}

        # dictionary of all filters in use and their values
        self.filters = {}

    def starting_result(self, start):
        self.start_record = math.ceil(start) if (start > 0) else 1

    def maximum_results(self, maximum):
        """
        set the maximum number of results
        :param maximum: int
        :return:
        """
        self.result_set_max = int(math.ceil(maximum)) if (maximum > 0) else 25
        if self.result_set_max > self.result_set_max_cap:
            self.result_set_max = self.result_set_max_cap

    def results_filter(self, filter_param, value):
        """
        setting a filter on results
        :param filter_param: Field used for filtering
        :param value: Text to filter on
        """
        filter_param = filter_param.strip().lower()
        value = value.strip()

        if len(value) > 0:
            self.filters[filter_param] = value
            self.query_provided = True

            # Standards do not have article titles, so switch to sorting by article number
            if filter_param == 'content_type' and value == 'Standards':
                self.results_sorting('publication_year', 'asc')

    def results_sorting(self, field, order):
        """
        setting sort order for results
        :param field: Data field used for sorting
        :param order: Sort order for results (ascending or descending)
        """
        field = field.strip().lower()
        order = order.strip()
        self.sort_field = field
        self.sort_order = order

    def search_field(self, field, value):
        """
        shortcut method for assigning search parameters and values
        :param field: Field used for searching
        :param value: Text to query
        """
        field = field.strip().lower()
        if field in self.allowed_search_fields:
            self.__add_parameter(field, value)
        else:
            print "Searches against field " + field + " are not supported"

    def abstract_text(self, value):
        self.__add_parameter('abstract', value)

    def affiliation_text(self, value):
        self.__add_parameter('affiliation', value)

    def article_number(self, value):
        self.__add_parameter('article_number', value)

    def article_title(self, value):
        self.__add_parameter('article_title', value)

    def author_text(self, value):
        self.__add_parameter('author', value)

    def author_facet_text(self, value):
        self.__add_parameter('d-au', value)

    def boolean_text(self, value):
        self.__add_parameter('boolean_text', value)

    def content_type_facet_text(self, value):
        self.__add_parameter('d-pubtype', value)

    def doi(self, value):
        """
        DOI (Digital Object Identifier) to query
        :param value:
        """
        self.__add_parameter('doi', value)

    def facet_text(self, value):
        self.__add_parameter('facet', value)

    def index_terms(self, value):
        """
        Author Keywords, IEEE Terms, and Mesh Terms to query
        :param value:
        """
        self.__add_parameter('index_terms', value)

    def isbn(self, value):
        """
        ISBN (International Standard Book Number) to query
        :param value:
        """
        self.__add_parameter('isbn', value)

    def issn(self, value):
        """
        ISSN (International Standard Serial number) to query
        :param value:
        """
        self.__add_parameter('issn', value)

    def issue_number(self, value):
        self.__add_parameter('is_number', value)

    def meta_data_text(self, value):
        """
        Text to query across metadata fields and the abstract
        :param value:
        """
        self.__add_parameter('meta_data', value)

    def publication_facet_text(self, value):
        self.__add_parameter('d-year', value)

    def publisher_facet_text(self, value):
        self.__add_parameter('d-publisher', value)

    def publication_title(self, value):
        self.__add_parameter('publication_title', value)

    def publication_year(self, value):
        self.__add_parameter('publication_year', value)

    def search_latest(self, from_date, to_date):
        """ranges=20180317_20180317_Search%20Latest%20Date"""
        value = '{}_{}_Search%20Latest%20Date'.format(from_date, to_date)
        self.__add_parameter('ranges', value)

    def query_text(self, value):
        """
        Text to query across metadata fields, abstract and document text
        :param value:
        """
        self.__add_parameter('querytext', value)

    def thesaurus_terms(self, value):
        """
        Thesaurus terms (IEEE Terms) to query
        :param value:
        """
        self.__add_parameter('thesaurus_terms', value)

    def __add_parameter(self, parameter, value):

        value = value.strip()

        if len(value) > 0:
            self.parameters[parameter]=value

            # viable query criteria provided
            self.query_provided = True
            # set flags based on parameter
            if parameter == 'article_number':
                self.using_article_number = True

            if parameter == 'boolean_text':
                self.using_boolean = True

            if parameter == 'facet' or parameter == 'd-au' or parameter == 'd-year' or parameter == 'd-pubtype' or parameter == 'd-publisher':
                self.using_facet = True

    def run(self):
        set_url = self.build_query()

        if self.query_provided is False:
            print "No search criteria provided"

        return IeeeClient._format_data(IeeeClient._query_api(set_url))

    def build_query(self):
        """
        creates the URL for the API call
        return string: full URL for querying the API
        """
        url = self.__BASEURL

        url += '?apikey=' + str(self.api_key)
        url += '&max_records=' + str(self.result_set_max)
        url += '&start_record=' + str(self.start_record)
        url += '&sort_order=' + str(self.sort_order)
        url += '&sort_field=' + str(self.sort_field)
        url += '&format=json'

        # add in search criteria
        # article number query takes priority over all others
        if self.using_article_number:
            url += '&article_number=' + str(self.parameters['article_number'])

        # boolean query
        elif self.using_boolean:
            url += '&querytext=(' + urllib.quote_plus(self.parameters['boolean_text']) + ')'

        else:
            for key in self.parameters:
                if self.using_facet and self.facet_applied is False:
                    url += '&querytext=' + urllib.quote_plus(self.parameters[key]) + '&facet=' + key
                    self.facet_applied = True
                else:
                    url += '&' + key + '=' + urllib.quote_plus(self.parameters[key])

        # add in filters
        for key in self.filters:
            url += '&' + key + '=' + str(self.filters[key])

        return url

    @staticmethod
    def _query_api(url):
        """
        creates the URL for the API call
        string url  Full URL to pass to API
        return string: Results from API
        :param url:
        """
        return urllib2.urlopen(url).read()

    @staticmethod
    def _format_data(data):
        """
        Formatting return data to json
        :param data: result string
        :return:
        """
        _TRANS = {
            "abstract": lambda d: d,
            "title": lambda d: d,
            "pdf_url": lambda d: d,
            "authors": lambda d: [auth["full_name"] for auth in d["authors"]],
            "index_terms": lambda d: IeeeClient.__decode_index_terms(d),
            "publication_title": lambda d: d,
            "conference_dates": lambda d: d
        }
        origin = json.loads(data)
        new_response = []
        for art in origin["articles"]:
            new_response.append({k: _TRANS[k](v) for k, v in art.iteritems() if k in _TRANS})
        return new_response

    @staticmethod
    def __decode_index_terms(d):
        try:
            return d["ieee_terms"]["terms"]
        except (TypeError, KeyError):
            return dict()


if __name__ == "__main__":
    # query = XPLORE('t9kx4t9kx4rxyfwyc732k4hugjzfh')
    query = IeeeClient('gg6gz9zkeqw6nbrkj7dg692t')
    # query.query_text('(International%20Requirements%20Engineering%20Conference%20.LB.RE.RB.)')
    query.query_text('re')
    query.maximum_results(500)
    data = query.run()
    print(len(data))

    # query.outputDataFormat = "object"
    pprint.pprint(data, indent=1)