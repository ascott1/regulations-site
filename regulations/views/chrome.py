from datetime import date

from django.views.generic.base import TemplateView

from regulations.generator import generator
from regulations.generator.versions import fetch_grouped_history
from regulations.views import utils
from regulations.views.reg_landing import regulation_exists, get_versions
from regulations.views.reg_landing import regulation as landing_page
from regulations.views.partial import *
from regulations.views.partial_search import PartialSearch
from regulations.views.sidebar import SideBarView
from regulations.views import error_handling


class ChromeView(TemplateView):
    """ Base class for views which wish to include chrome. """
    template_name = 'regulations/chrome.html'
    has_sidebar = True
    check_tree = True

    def get(self, request, *args, **kwargs):
        """Override GET so that we can catch and propagate any errors in the
        included partial(s)"""

        try:
            return super(ChromeView, self).get(request, *args, **kwargs)
        except BadComponentException, e:
            return e.response
        except error_handling.MissingSectionException, e:
            return error_handling.handle_missing_section_404(
                request, e.label_id, e.version, e.context)
        except error_handling.MissingContentException, e:
            return error_handling.handle_generic_404(request)

    def _assert_good(self, response):
        if response.status_code != 200:
            raise BadComponentException(response)

    def add_main_content(self, context):
        view = self.partial_class()
        view.request = self.request
        context['main_content_context'] = view.get_context_data(**context)
        context['main_content_template'] = view.template_name

    def set_chrome_context(self, context, reg_part, version):
        utils.add_extras(context)
        context['reg_part'] = reg_part
        context['history'] = fetch_grouped_history(reg_part)

        table_of_contents = utils.table_of_contents(
            reg_part,
            version,
            self.partial_class.sectional_links)
        context['TOC'] = table_of_contents

        regulation_meta = utils.regulation_meta(
            reg_part,
            version,
            self.partial_class.sectional_links)
        context['meta'] = regulation_meta

    def get_context_data(self, **kwargs):
        context = super(ChromeView, self).get_context_data(**kwargs)

        label_id = context['label_id']
        version = context['version']
        reg_part = label_id.split('-')[0]
        context['q'] = self.request.GET.get('q', '')

        error_handling.check_regulation(reg_part)
        self.set_chrome_context(context, reg_part, version)

        if self.check_tree:
            relevant_tree = generator.get_tree_paragraph(label_id, version)
            if relevant_tree is None:
                raise error_handling.MissingSectionException(label_id, version,
                                                             context)
        self.add_main_content(context)

        if self.has_sidebar:
            sidebar_view = SideBarView.as_view()
            response = sidebar_view(self.request, label_id=label_id,
                                    version=version)
            self._assert_good(response)
            response.render()
            context['sidebar_content'] = response.content

        return context


class ChromeInterpView(ChromeView):
    """Interpretation of regtext section/paragraph or appendix with chrome"""
    partial_class = PartialInterpView


class ChromeSectionView(ChromeView):
    """Regtext section with chrome"""
    partial_class = PartialSectionView


class ChromeParagraphView(ChromeView):
    """Regtext paragraph with chrome"""
    partial_class = PartialParagraphView


class ChromeRegulationView(ChromeView):
    """Entire regulation with chrome"""
    partial_class = PartialRegulationView


class ChromeSearchView(ChromeView):
    """Search results with chrome"""
    template_name = 'regulations/chrome-search.html'
    partial_class = PartialSearch
    has_sidebar = False
    check_tree = False

    def get_context_data(self, **kwargs):
        """Get the version for the chrome context"""
        kwargs['version'] = self.request.GET.get('version', '')
        kwargs['skip_count'] = True
        kwargs['label_id'] = utils.first_section(kwargs['label_id'],
                                                 kwargs['version'])
        return super(ChromeSearchView, self).get_context_data(**kwargs)

    def add_main_content(self, context):
        """Override this so that we have access to the main content's
        results field"""
        super(ChromeSearchView, self).add_main_content(context)
        context['results'] = context['main_content_context']['results']


class ChromeLandingView(ChromeView):
    """Landing page with chrome"""
    template_name = 'regulations/landing-chrome.html'
    partial_class = PartialSectionView  # Needed to know sectional status
    has_sidebar = False
    check_tree = False

    def add_main_content(self, context):
        """Landing page isn't a TemplateView"""
        response = landing_page(self.request, context['reg_part'])
        self._assert_good(response)
        context['main_content'] = response.content

    def get_context_data(self, **kwargs):
        """Add the version and replace the label_id for the chrome context"""

        reg_part = kwargs['label_id']
        if not regulation_exists(reg_part):
            raise error_handling.MissingContentException()

        current, _ = get_versions(kwargs['label_id'])
        kwargs['version'] = current['version']
        kwargs['label_id'] = utils.first_section(reg_part, current['version'])
        return super(ChromeLandingView, self).get_context_data(**kwargs)


class BadComponentException(Exception):
    """Allows us to propagate errors in loaded partials"""
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "BadComponentException(response=%s)" % repr(self.response)
