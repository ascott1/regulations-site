// **Extends** Backbone.View
//
// **Usage** ```require(['toc-view'], function(TOCView) {})```
//
// **Jurisdiction** Expandable Table of Contents
define('toc-view', ['jquery', 'underscore', 'backbone', 'regs-helpers', 'drawer-view', './regs-router', 'main-controller', 'drawer-controller'], function($, _, Backbone, RegsHelpers, Drawer, Router, MainEvents, DrawerEvents) {
    'use strict';
    var TOCView = Backbone.View.extend({
        el: '#table-of-contents',

        events: {
            'click a': 'sendClickEvent'
        },

        initialize: function() {
            var openSection = $('section[data-page-type]').attr('id');

            MainEvents.on('section:open', this.setActive, this);

            if (openSection) {
                this.setActive(openSection);
            }

            if (this.$el.hasClass('diff-toc')) {
                this.diffMode = true;
            }

            // **TODO** need to work out a bug where it scrolls the content section
            // $('#menu-link:not(.active)').on('click', this.scrollToActive);

            // if the browser doesn't support pushState, don't 
            // trigger click events for links
            // also! if we're in diffmode, suspend events
            if (Router.hasPushState === false || this.diffMode) {
                this.events = {};
            }
        },

        // update active classes, find new active based on the reg entity id in the anchor
        setActive: function(id) {
            this.$el.find('.current').removeClass('current');
            this.$el.find('a[data-section-id=' + RegsHelpers.findBaseSection(id) + ']').addClass('current');

            return this;
        },

        // **Event trigger**
        // when a TOC link is clicked, send an event along with the href of the clicked link
        sendClickEvent: function(e) {
            e.preventDefault();

            var sectionId = $(e.currentTarget).data('section-id');
            DrawerEvents.trigger('section:open', sectionId);
            MainEvents.trigger('section:open', sectionId, {}, 'reg-section');
        },

        // **Inactive** 
        // Intended to keep the active link in view as the user moves around the doc
        scrollToActive: function() {
            var activeLink = document.querySelectorAll('#table-of-contents .current');

            if (activeLink[0]) {
                activeLink[0].scrollIntoView();
            }
        }
    });

    return TOCView;
});
