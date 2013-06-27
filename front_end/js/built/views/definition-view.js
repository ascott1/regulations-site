define("definition-view",["jquery","underscore","backbone","regs-view","regs-data","regs-dispatch","regs-helpers"],function(e,t,n,r,i,s,o){var u=r.extend({className:"open-definition",events:{"click .close-button":"close"},render:function(){s.once("definition:callRemove",this.remove,this);var t=this.$el.find(".inline-interpretation"),n=this.$el.find("dfn.key-term"),r="#"+this.model.id,i=o.idToRef(this.model.id),u="continue-link internal",a=o.fastLink(r,i,u),f=this.model.linkText,l,c,h,p,d;this.$el.append(a),this.$el.find(".active-term").removeClass("active-term"),this.$el.find(".defined-term").filter(function(){return e(this).text().toLowerCase()===f}).addClass("active-term"),typeof t[0]!="undefined"&&(p=e("#"+this.model.id).data("interpId"),t.remove(),l="#"+p,c="Related commentary",h=o.fastLink(l,c,u),this.$el.append(h));if(typeof n[0]!="undefined"){d=n.length;for(var v=0;v<d;v++)e(n[v]).remove()}return this.$el.attr("tabindex","0").append('<a class="close-button" href="#">Close definition</a>'),s.trigger("definition:render",this.$el),this.$el.focus(),this},close:function(e){e.preventDefault(),s.trigger("definition:callRemove")},remove:function(){return this.stopListening(),this.$el.remove(),s.trigger("definition:remove"),this}});return u});