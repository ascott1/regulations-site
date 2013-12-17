define('regs-router', ['underscore', 'backbone', 'main-controller', 'queryparams'], function(_, Backbone, MainEvents) {
    'use strict';

    var RegsRouter;

    if (typeof window.history.pushState === 'undefined') {
        RegsRouter = function() {
            this.start = function() {};
            this.navigate = function() {};
            this.hasPushState = false;
        };
    }
    else {
        RegsRouter = Backbone.Router.extend({
            routes: {
                'sxs/:section/:version': 'toSxS',
                'search/:reg': 'backToSearchResults',
                ':section/:version': 'loadSection'
            },

            loadSection: function(section) {
                var options = {id: section};

                // to scroll to paragraph if there is a hadh
                options.scrollToId = Backbone.history.getHash();

                // ask the view not to route, its not needed
                options.noRoute = true;

                MainEvents.trigger('section:open', section, options, 'reg-section'); 
            },

            toSxS: function(section, version, params) {
                /* jshint camelcase: false */
                Dispatch.trigger('sxs:route', {
                    'regParagraph': section,
                    'docNumber': version,
                    'fromVersion': params.from_version
                });
            },

            backToSearchResults: function(reg, params) {
                /* jshint unused: false */
                var config = {
                    query: params.q,
                    version: params.version
                };

                // if there is a page number for the query string
                if (typeof params.page !== 'undefined') {
                    config.page = params.page;
                }

                MainEvents.trigger('search-results:open', config);
            },

            start:  function() {
                var root = '/';

                // if the site is running under a subdirectory, create urls accordingly
                if (window.APP_PREFIX.length > 1) {
                    root = window.APP_PREFIX.substring(1);
                }

                Backbone.history.start({
                    pushState: 'pushState' in window.history,
                    silent: true,
                    root: root
                });
            },

            hasPushState: true
        });
    }

    var router = new RegsRouter();
    return router;
});
