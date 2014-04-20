/*
 * author: the5fire
 * blog:  the5fire.com
 * date: 2014-03-16
 * */
define(function(require, exports, module) {
    var $ = require('jquery');
    var _ = require('underscore');
    var Backbone = require('backbone');
    var TopicModule = require('topic');
    var MessageModule = require('message');
    var socket = require('socket');

    var Topics = TopicModule.Topics;
    var TopicView = TopicModule.TopicView;
    var Topic = TopicModule.Topic;

    var Message = MessageModule.Message;
    var Messages = MessageModule.Messages;
    var MessageView = MessageModule.MessageView;

    var topics = new Topics();

    var AppView = Backbone.View.extend({
        el: "#main",
        topic_list: $("#topic_list"),
        topic_section: $("#topic_section"),
        message_section: $("#message_section"),
        message_list: $("#message_list"),
        message_head: $("#message_head"),

        events: {
            'click .submit': 'saveMessage',
            'click .submit_topic': 'saveTopic',
        },

        initialize: function() {
            _.bindAll(this, 'addTopic', 'addMessage');

            topics.bind('add', this.addTopic);

            // 定义消息列表池，每个topic有自己的message collection
            // 这样保证每个主题下得消息不冲突
            this.message_pool = {};
            this.socket = null;

            this.message_list_div = document.getElementById('message_list');
        },

        addTopic: function(topic) {
            var view = new TopicView({model: topic});
            this.topic_list.append(view.render().el);
        },

        addMessage: function(message) {
            var view = new MessageView({model: message});
            this.message_list.append(view.render().el);
            this.message_list.scrollTop(this.message_list_div.scrollHeight);
        },

        saveMessage: function(evt) {
            var comment_box = $('#comment')
            var content = comment_box.val();
            if (content == '') {
                alert('内容不能为空');
                return false;
            }
            var topic_id = comment_box.attr('topic_id');
            var message = new Message({
                content: content,
                topic_id: topic_id,
            });
            var messages = this.message_pool[topic_id];
            message.save(); // 依赖上面对sync的重载
        },

        saveTopic: function(evt) {
            var topic_title = $('#topic_title');
            if (topic_title.val() == '') {
                alert('主题不能为空！');
                return false
            }
            var topic = new Topic({
                title: topic_title.val(),
            });
            self = this;
            topic.save(null, {
                success: function(model, response, options){
                    topics.add(response);
                    topic_title.val('');
                },
                error: function(model, resp, options){
                    alert(resp.responseText);
                }
            });
        },

        showTopic: function(){
            topics.fetch();
            this.topic_section.show();
            this.message_section.addClass('hide');
            this.message_list.html('');

            this.goOut()
        },

        goOut: function(){
            // 退出房间
            socket.emit('go_out');
            socket.removeAllListeners('message');
        },

        initMessage: function(topic_id) {
            var messages = new Messages;
            messages.bind('add', this.addMessage);
            this.message_pool[topic_id] = messages;
        },

        showMessage: function(topic_id) {
            this.initMessage(topic_id);

            this.message_section.removeClass('hide');
            this.topic_section.hide();
            
            this.showMessageHead(topic_id);
            $('#comment').attr('topic_id', topic_id);

            var messages = this.message_pool[topic_id];
            // 进入房间
            socket.emit('topic', topic_id);
            // 监听message事件，添加对话到messages中
            socket.on('message', function(response) {
                messages.add(response);
            });
            messages.fetch({
                data: {topic_id: topic_id},
                success: function(resp) {
                    self.message_list.scrollTop(self.message_list_div.scrollHeight)
                },
                error: function(model, resp, options){
                    alert(resp.responseText);
                }
            });
        },

        showMessageHead: function(topic_id) {
            var topic = new Topic({id: topic_id});
            self = this;
            topic.fetch({
                success: function(resp, model, options) {
                    self.message_head.html(model.title);
                },
                error: function(model, resp, options) {
                    alert(resp.responseText);
                }
            });
        },

    });
    return AppView;
});
