import math
import urllib
import urllib2
import pprint

try:
    import simplejson as json
except ImportError:
    import json


class IeeeClient(object):

    # API endpoint
    __BASEURL = "http://ieeexploreapi.ieee.org/api/v1/search/articles"

    def __init__(self, apiKey):
        self.apiKey = apiKey

        # flag that some search criteria has been provided
        self.queryProvided = False

        # flag that article number has been provided, which overrides all other search criteria
        self.usingArticleNumber = False

        # flag that a boolean method is in use
        self.usingBoolean = False

        # flag that a facet is in use
        self.usingFacet = False

        # flag that a facet has been applied, in the event that multiple facets are passed
        self.facetApplied = False

        # default of 25 results returned
        self.resultSetMax = 25

        # maximum of 200 results returned
        self.resultSetMaxCap = 200

        # records returned default to position 1 in result set
        self.startRecord = 1

        # default sort order is ascending; could also be 'desc' for descending
        self.sortOrder = 'asc'

        # field name that is being used for sorting
        self.sortField = 'article_title'

        # array of permitted search fields for searchField() method
        self.allowedSearchFields = ['abstract', 'affiliation', 'article_number', 'article_title', 'author', 'boolean_text', 'content_type', 'd-au', 'd-pubtype', 'd-publisher', 'd-year', 'doi', 'end_year', 'facet', 'index_terms', 'isbn', 'issn', 'is_number', 'meta_data', 'open_access', 'publication_number', 'publication_title', 'publication_year', 'publisher', 'querytext', 'start_year', 'thesaurus_terms']

        # dictionary of all search parameters in use and their values
        self.parameters = {}

        # dictionary of all filters in use and their values
        self.filters = {}

    def starting_result(self, start):
        self.startRecord = math.ceil(start) if (start > 0) else 1

    def maximum_results(self, maximum):
        """
        set the maximum number of results
        :param maximum: int
        :return:
        """
        self.resultSetMax = math.ceil(maximum) if (maximum > 0) else 25
        if self.resultSetMax > self.resultSetMaxCap:
            self.resultSetMax = self.resultSetMaxCap

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
            self.queryProvided = True

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
        self.sortField = field
        self.sortOrder = order

    def search_field(self, field, value):
        """
        shortcut method for assigning search parameters and values
        :param field: Field used for searching
        :param value: Text to query
        """
        field = field.strip().lower()
        if field in self.allowedSearchFields:
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
            self.queryProvided = True
            # set flags based on parameter
            if parameter == 'article_number':
                self.usingArticleNumber = True

            if parameter == 'boolean_text':
                self.usingBoolean = True

            if parameter == 'facet' or parameter == 'd-au' or parameter == 'd-year' or parameter == 'd-pubtype' or parameter == 'd-publisher':
                self.usingFacet = True

    def run(self):
        set_url = self.build_query()

        if self.queryProvided is False:
            print "No search criteria provided"

        return IeeeClient._format_data(IeeeClient._query_api(set_url))

    def build_query(self):
        """
        creates the URL for the API call
        return string: full URL for querying the API
        """
        url = self.__BASEURL

        url += '?apikey=' + str(self.apiKey)
        url += '&max_records=' + str(self.resultSetMax)
        url += '&start_record=' + str(self.startRecord)
        url += '&sort_order=' + str(self.sortOrder)
        url += '&sort_field=' + str(self.sortField)
        url += '&format=json'

        # add in search criteria
        # article number query takes priority over all others
        if self.usingArticleNumber:
            url += '&article_number=' + str(self.parameters['article_number'])

        # boolean query
        elif self.usingBoolean:
            url += '&querytext=(' + urllib.quote_plus(self.parameters['boolean_text']) + ')'

        else:
            for key in self.parameters:
                if self.usingFacet and self.facetApplied is False:
                    url += '&querytext=' + urllib.quote_plus(self.parameters[key]) + '&facet=' + key
                    self.facetApplied = True
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
        return json.loads(data)


def __decode_index_terms(d):
    try:
        return d["ieee_terms"]["terms"]
    except TypeError:
        return dict()


class ParamsDecoder(json.JSONDecoder):

    _TRANS = {
        "abstract": lambda d: d,
        "title": lambda d: d,
        "pdf_url": lambda d: d,
        "authors": lambda d: d["authors"],
        "index_terms": lambda d: __decode_index_terms(d),
        "publication_title": lambda d: d,
        "conference_dates": lambda d: d
    }

    def __init__(self, *args, **kwargs):
        super(ParamsDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dictionary):
        print(dictionary)
        # raw_input("...")
        # l = []
        # for element in dictionary["articles"]:
        #     d = dict()
        #     for k, v in ParamsDecoder._TRANS.iteritems():
        #         if k in element:
        #             d[k] = v(element[k])
        #     l.append(d)
        #
        # return d


if __name__ == "__main__":
    # query = XPLORE('t9kx4t9kx4rxyfwyc732k4hugjzfh')
    query = IeeeClient('gg6gz9zkeqw6nbrkj7dg692t')
    # query.query_text('(International%20Requirements%20Engineering%20Conference%20.LB.RE.RB.)')
    query.query_text('re')
    data = query.run()

    # query.outputDataFormat = "object"
    pprint.pprint(data, indent=1)