# -*- coding: utf-8 -*-
"""
    Sphinx Interface
    ~~~~~~~~~~~~~~~~

    .. autofunction:: setup
    .. autofunction:: init_bibtex_cache
    .. autofunction:: purge_bibtex_cache
    .. autofunction:: process_bibliography_nodes
    .. autofunction:: process_cite_nodes
"""

import docutils.nodes
from sphinx.roles import XRefRole # for :cite:

from sphinxcontrib.bibtex.cache import Cache, BibfileCache, BibliographyCache
from sphinxcontrib.bibtex.nodes import bibliography, cite
from sphinxcontrib.bibtex.directives import BibliographyDirective

def init_bibtex_cache(app):
    """Create ``app.env.bibtex_cache`` if it does not exist yet.

    :param app: The :mod:`sphinx application <sphinx.application>`.
    :type app: :class:`sphinx.application.Sphinx`
    """
    if not hasattr(app.env, "bibtex_cache"):
        app.env.bibtex_cache = Cache()

def purge_bibtex_cache(app, env, docname):
    """Remove all information related to *docname* from the cache."""
    env.bibtex_cache.purge(docname)

def process_bibliography_nodes(app, doctree, docname):
    """Replace bibliography nodes by list of references."""

    for bibnode in doctree.traverse(bibliography):
        # get the information of this bibliography node
        # by looking up its id in the bibliography cache
        id_ = bibnode['ids'][0]
        info = [info for other_id, info
                in app.env.bibtex_cache.bibliographies.iteritems()
                if other_id == id_][0]
        # TODO handle the actual citations, for now just print .bib file names
        bibnode.replace_self(
            [docutils.nodes.inline(
                " ".join(info.bibfiles),
                " ".join(info.bibfiles))])

def process_cite_nodes(app, doctree, docname):
    """Replace cite nodes by footnote or citation nodes."""

    for citenode in doctree.traverse(cite):
        # TODO handle the actual citations
        citenode.replace_self([])

def setup(app):
    """Set up the bibtex extension:

    * register directives
    * register nodes
    * register roles
    * connect events to functions
    """

    app.add_directive("bibliography", BibliographyDirective)
    app.add_node(bibliography)
    app.add_node(cite)
    app.add_role("cite", XRefRole())
    app.connect("builder-inited", init_bibtex_cache)
    app.connect("doctree-resolved", process_bibliography_nodes)
    app.connect("doctree-resolved", process_cite_nodes)
    app.connect("env-purge-doc", purge_bibtex_cache)