/*
 * author: the5fire
 * blog:  the5fire.com
 * date: 2014-03-16
 * */
define(function(require, exports, module) {
    var $ = require('jquery');
    var Backbone = require('backbone');
    var _ = require('underscore');
    var socket = require('socket');

    var Message = Backbone.Model.extend({
        urlRoot: '/message',
        sync: function(method, model, options){
            if (method === 'create') {
                socket.emit('message', model.attributes);
                $('#comment').val('');
            } else {
                return Backbone.sync(method, model, options);
            };
        },
    });

    var Messages = Backbone.Collection.extend({
        url: '/message',
        model: Message,
    });

    var MessageView = Backbone.View.extend({
        tagName:  "div class='comment'",
        templ: _.template($('#message-template').html()),

        // 渲染列表页模板
        render: function() {
          $(this.el).html(this.templ(this.model.toJSON()));
          return this;
        },
    });
    module.exports = {
        "Messages": Messages,
        "Message": Message,
        "MessageView": MessageView,
    }
});
