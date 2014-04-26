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
        tagName:  "li class='row message'",
        templ: _.template($('#message-template').html()),

        // 渲染列表页模板
        render: function() {
          $(this.el).html(this.templ(this.model.toJSON()));
          return this;
        },
    });
    $('textarea').live('keydown', function(e) {
        var keyCode = e.keyCode || e.which;
        if (keyCode == 9) {
            e.preventDefault();
            var s = this.selectionStart;
            this.value = this.value.substring(0,this.selectionStart) + "\t" + this.value.substring(this.selectionEnd);
            this.selectionEnd = s+1;
        } 
    });
    module.exports = {
        "Messages": Messages,
        "Message": Message,
        "MessageView": MessageView,
    }
});
