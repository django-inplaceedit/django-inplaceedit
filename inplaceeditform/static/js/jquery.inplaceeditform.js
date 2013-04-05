(function ($) {
    "use strict";
    $.fn.inplaceeditform = function (method) {
        var methods = $.inplaceeditform.methods;

        // method calling logic
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + method + ' does not exist on jQuery.inplaceeditform');
        }
    };

    $.inplaceeditform = {
        opts: {
            "getFieldUrl": "/inplaceeditform/get_field/",
            "saveURL": "/inplaceeditform/save/",
            "successText": "Successfully saved",
            "eventInplaceEdit": "dblclick",
            "disableClick": true,
            "autoSave": false,
            "unsavedChanges": "You have unsaved changes!"
        },
        formSelector: "form.inplaceeditform",
        enabled: false,
        inplaceeditfields: null,
        methods: {},

        extend: function (newMethods) {
            this.methods = $.extend(this.methods, newMethods);
        }
    };

    $.inplaceeditform.extend(
        {
            init: function (opts) {
                var self = $.inplaceeditform;
                self.opts = $.extend(self.opts, opts || {});
                self.inplaceeditfields = this;

                this.each(function () {
                    if (self.opts.disableClick) {
                        $(this).click(function (ev) {
                            if (self.enabled) {
                                ev.preventDefault();
                            }
                        });
                    }

                    $(this).bind(self.opts.eventInplaceEdit, function () {
                        if ($(this).data("ajaxTime")) {
                            return false;
                        }
                        if (!self.enabled) {
                            return false;
                        }
                        $(this).data("ajaxTime", true);
                        var data = self.methods.getDataToRequest($(this).find("span.config"));
                        var extraConfig = $(this).find(".config").data("extraConfig");
                        if (extraConfig) {
                            data = extraConfig(data);
                        }
                        var can_auto_save = parseInt($(this).find("span.config span.can_auto_save").html());
                        data += "&__widget_height=" + $(this).innerHeight() + "px" + "&__widget_width=" + $(this).innerWidth() + "px";
                        var that = this;
                        $.ajax(
                            {
                                data: data,
                                url: self.opts.getFieldUrl,
                                type: "GET",
                                async: true,
                                dataType: 'json',
                                error: self.methods.bind(self.methods.treatmentStatusError, {"context": $(this)}),
                                success: function (response) {
                                    if (!response) {
                                        alert("The server is down");
                                    } else if (response.errors) {
                                        alert(response.errors);
                                    } else {
                                        var tags = $(self.methods.removeStartSpaces(response.field_render));
                                        $(tags).insertAfter($(that));
                                        $(that).hide();
                                        var head = $("head")[0];
                                        try {
                                            var medias = $(self.methods.removeStartSpaces(response.field_media_render));
                                            $.map(medias, function (media) {
                                                self.methods.loadjscssfile(media);
                                            });
                                        } catch (err) {
                                        }
                                        var links_parents = $(that).next().parents("a");
                                        if (links_parents.length > 0) {
                                            $.map(links_parents, function (link, i) {
                                                link = $(link);
                                                var href = link.attr("href");
                                                link.attr("hrefinplaceedit", href);
                                                link.addClass("linkInplaceEdit");
                                                link.removeAttr("href");
                                            });
                                        }
                                        var applyButton = $(that).next().find(".apply");
                                        var cancelButton = $(that).next().find(".cancel");
                                        var applyFileButton = $(that).next().find(".applyFile");
                                        if (cancelButton.size()) {
                                            cancelButton.click(self.methods.inplaceCancel);
                                        }
                                        if (applyButton.size()) {
                                            applyButton.click(self.methods.inplaceApply);
                                            $(that).next(self.formSelector).submit(self.methods.bind(self.methods.inplaceApply, applyButton));
                                        }
                                        if (applyFileButton.size()) {
                                            applyFileButton.click(self.methods.inplaceApplyUpload);
                                            $(that).next(self.formSelector).submit(self.methods.bind(self.methods.inplaceApply, applyFileButton));
                                        }
                                        $(that).next(self.formSelector).find("input, select").focus();
                                        if (self.opts.autoSave && can_auto_save) {
                                            applyButton.hide();
                                            cancelButton.hide();
                                            applyFileButton.hide();
                                            var value = $(that).next(self.formSelector).find("input, select").val();
                                            var autoSave = function () {
                                                var newValue = $(this).val();
                                                if (newValue !== value) {
                                                    $(that).next(self.formSelector).find(".apply").click();
                                                } else {
                                                    $(that).next(self.formSelector).find(".cancel").click();
                                                }
                                            };
                                            $(that).next(self.formSelector).find("input, select").blur(autoSave);
                                            $(that).next(self.formSelector).find("select").change(autoSave);
                                        }
                                    }
                                    $(that).data("ajaxTime", false);
                                }
                            }
                        );
                    });
                });

                window.onbeforeunload = function (event) {
                    var msg = self.opts.unsavedChanges;
                    if ($(self.formSelector).size()) {
                        if (event) {
                            // For IE and Firefox prior to version 4
                            event.returnValue = msg;
                        }
                        // For Safari and Firefox version 4 and later
                        return msg;
                    }
                };

                // https://docs.djangoproject.com/en/1.3/ref/contrib/csrf/#ajax
                $(document).ajaxSend(function (event, xhr, settings) {
                    function getCookie(name) {
                        var cookieValue = null;
                        var i;
                        if (document.cookie && document.cookie !== '') {
                            var cookies = document.cookie.split(';');
                            for (i = 0; i < cookies.length; i += 1) {
                                var cookie = $.trim(cookies[i]);
                                // Does this cookie string begin with the name we want?
                                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                    break;
                                }
                            }
                        }
                        return cookieValue;
                    }

                    function sameOrigin(url) {
                        // url could be relative or scheme relative or absolute
                        var host = document.location.host; // host + port
                        var protocol = document.location.protocol;
                        var sr_origin = '//' + host;
                        var origin = protocol + sr_origin;
                        // Allow absolute or scheme relative URLs to same origin
                        return (url === origin || url.slice(0, origin.length + 1) === origin + '/') ||
                            (url === sr_origin || url.slice(0, sr_origin.length + 1) === sr_origin + '/') ||
                            // or any other URL that isn't scheme relative or absolute i.e relative.
                            !(/^(\/\/|http:|https:).*/.test(url));
                    }

                    function safeMethod(settings) {
                        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) || settings.url.indexOf("send_csrfToken") > -1;
                    }

                    if (!safeMethod(settings) && sameOrigin(settings.url)) {
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    }
                });

                return {
                    enable: function () {
                        self.enabled = true;
                        self.inplaceeditfields.each(function () {
                            $(this).addClass("enable");
                        });
                    },
                    disable: function () {
                        self.enabled = false;
                        self.inplaceeditfields.each(function () {
                            $(this).removeClass("enable");
                        });
                    }
                };
            },

            treatmentStatusError: function (response) {
                if (response.status === 0) {
                    alert("The server is down");
                } else if (response.status === 403) {
                    alert("Permission denied, please check that you are login");
                } else {
                    alert(response.statusText);
                }
                this.context.next(".cancel").click();
                this.context.data("ajaxTime", false);
            },

            revertlinkInplaceEdit: function (links_parents) {
                $.map(links_parents, function (link, i) {
                    link = $(link);
                    var href = link.attr("hrefinplaceedit");
                    link.attr("href", href);
                    link.removeClass("linkInplaceEdit");
                    link.removeAttr("hrefinplaceedit");
                });
            },

            inplaceCancel: function () {
                var self = $.inplaceeditform;
                self.methods.revertlinkInplaceEdit($(this).parents("a.linkInplaceEdit"));
                $(this).parent().prev().fadeIn();
                var cancelFinish = $(this).data("cancelFinish");
                if (cancelFinish) {
                    cancelFinish();
                }
                $(this).parent().remove();
                return false;
            },

            replaceAll: function (txt, replace, with_this) {
                return txt.replace(new RegExp(replace, "g"), with_this);
            },

            inplaceApplySuccess: function (response) {
                var self = $.inplaceeditform;
                if (typeof response === "string") {
                    if ($.browser && $.browser.msie) { // This does not exists in jQuery 1.9
                        response = self.methods.replaceAll(response, "'\\\\\"", "'");
                        response = self.methods.replaceAll(response, "\"'", "'");
                    }
                    try {
                        response = JSON.parse(response);
                    } catch (errno) {
                        response = eval("( " + response + " )");
                    }
                }
                self.methods.revertlinkInplaceEdit($(this.form).parents("a.linkInplaceEdit"));
                var that = this.context;
                var form = this.form;
                var inplaceedit_conf = this.inplaceedit_conf;
                if (!response) {
                    alert("The server is down");
                } else if (response.errors) {
                    form.animate({opacity: 1});
                    form.prepend("<ul class='errors'><li>" + response.errors + "</li></ul>");
                } else {
                    that.parent().fadeOut();
                    that.fadeIn();
                    form.removeClass("inplaceeditformsaving");
                    var inplace_span = inplaceedit_conf.parents(".inplaceedit");
                    var config = inplace_span.find("span.config").html();
                    inplace_span.html(response.value + "<span class='config' style='display:none;'>" + config + "</span>");
                    inplace_span.show();
                    self.methods.inplaceApplySuccessShowMessage(inplace_span, response);
                    var applyFinish = that.data("applyFinish");
                    if (applyFinish) {
                        applyFinish(that);
                    }
                    that.parent().remove();
                }
            },

            inplaceApplySuccessShowMessage: function(inplace_span) {
                var self = $.inplaceeditform;
                if (self.opts.successText) {
                    var success_message = $("<ul class='success'><li>" + self.opts.successText + "</li></ul>");
                    inplace_span.prepend(success_message);
                    setTimeout(function () {
                        success_message.fadeOut(function () {
                            $(this).remove();
                        });
                    }, 2000);
                }
            },

            bind: function (func, that) {
                return function () {
                    return func.apply(that, arguments);
                };
            },

            getCSFRToken: function () {
                return csrf_token;
            },

            inplaceApply: function () {
                var self = $.inplaceeditform;
                var form = $(this).parents(self.formSelector);
                form.animate({opacity: 0.1});
                form.find("ul.errors").fadeOut(function () {
                    $(this).remove();
                });
                var inplaceedit_conf = form.prev().find("span.config");
                var data = self.methods.getDataToRequest(inplaceedit_conf);
                var field_id = form.find("span.field_id").html();
                var getValue = $(this).data("getValue"); // A hook
                var value;
                if (getValue) {
                    value = getValue(form, field_id);
                } else {
                    value = form.find("#" + field_id).val();
                }
                data += "&value=" + encodeURIComponent($.toJSON(value));
                var csrfmiddlewaretoken = self.methods.getCSFRToken();
                if (csrfmiddlewaretoken) {
                    data += "&csrfmiddlewaretoken=" + csrfmiddlewaretoken;
                }
                $.ajax(
                    {
                        data: data,
                        url: self.opts.saveURL,
                        type: "POST",
                        async: true,
                        dataType: 'text',
                        error: self.methods.bind(self.methods.treatmentStatusError, {"context": $(this)}),
                        success: self.methods.bind(self.methods.inplaceApplySuccess, {
                            "context": $(this),
                            "form": form,
                            "inplaceedit_conf": inplaceedit_conf
                        })
                    }
                );
                return false;
            },

            inplaceApplyUpload: function () {
                var self = $.inplaceeditform;
                var form = $(this).parents(self.formSelector);
                form.animate({opacity: 0.1});
                form.find("ul.errors").fadeOut(function () {
                    $(this).remove();
                });
                var inplaceedit_conf = form.prev().find("span.config");
                var data = self.methods.getDataToRequestUpload(inplaceedit_conf);
                var csrfmiddlewaretoken = self.methods.getCSFRToken();
                if (csrfmiddlewaretoken) {
                    data.csrfmiddlewaretoken = csrfmiddlewaretoken;
                }
                var field_id = form.find("span.field_id").html();
                var getValue = $(this).data("getValue"); // A hook
                var value;
                if (getValue) {
                    value = getValue(form, field_id);
                } else {
                    value = form.find("#" + field_id).val();
                }
                data.value = encodeURIComponent($.toJSON(value));

                form.ajaxSubmit(
                    {
                        url: self.opts.saveURL,
                        data: data,
                        async: true,
                        type: "POST",
                        method: "POST",
                        dataType: "application/json",
                        error: self.methods.bind(self.methods.treatmentStatusError, {"context": $(this)}),
                        success: self.methods.bind(self.methods.inplaceApplySuccess, {
                            "context": $(this),
                            "form": form,
                            "inplaceedit_conf": inplaceedit_conf
                        })
                    }
                );
                return false;
            },

            getDataToRequest: function (inplaceedit_conf) {
                var dataToRequest = "";
                var settings = inplaceedit_conf.find("span");
                $.map(settings, function (setting, i) {
                    setting = $(setting);
                    var data = "&";
                    if (i === 0) {
                        data = "";
                    }
                    var key = setting.attr("class");
                    var value = setting.html();
                    data = data + key + "=" + value;
                    dataToRequest += data;
                });
                var fontSize = inplaceedit_conf.parent().css("font-size");
                if (fontSize) {
                    dataToRequest += "&font_size=" + fontSize;
                }
                return dataToRequest;
            },

            getDataToRequestUpload: function (inplaceedit_conf) {
                var dataToRequest = {};
                var settings = inplaceedit_conf.find("span");
                $.map(settings, function (setting, i) {
                    setting = $(setting);
                    var key = setting.attr("class");
                    var value = setting.html();
                    dataToRequest[key] = value;
                });
                var fontSize = inplaceedit_conf.parent().css("font-size");
                if (fontSize) {
                    dataToRequest.font_size = fontSize;
                }
                return dataToRequest;
            },

            removeStartSpaces: function (html) {
                // Remove the espaces and \n to the begin of the field_render
                return html.replace(/^( |\n)*/g, "");
            },

            loadjscssfile: function (media) {
                var self = $.inplaceeditform;
                var fileref;
                if (media.tagName === "SCRIPT") { //if filename is a external JavaScript file
                    fileref = document.createElement('script');
                    fileref.setAttribute("type", "text/javascript");
                    if (media.src !== null && media.src !== "") {
                        fileref.setAttribute("src", media.src);
                    } else {
                        self.methods.appendChild(fileref, media.innerHTML);
                    }
                } else if (media.tagName === "LINK" && media.rel === "stylesheet") { //if filename is an external CSS file
                    var type = media.type || "text/css";
                    var rel = "stylesheet";
                    var href = media.href;
                    fileref = document.createElement("link");
                    fileref.setAttribute("rel", rel);
                    fileref.setAttribute("type", type);
                    fileref.setAttribute("href", media.href);
                }

                if (typeof fileref !== "undefined") {
                    document.getElementsByTagName("head")[0].appendChild(fileref);
                }
            },

            appendChild: function (node, text) {
                if (null === node.canHaveChildren || node.canHaveChildren) {
                    node.appendChild(document.createTextNode(text));
                } else {
                    node.text = text;
                }
            }
        }
    );
})(jQuery);
