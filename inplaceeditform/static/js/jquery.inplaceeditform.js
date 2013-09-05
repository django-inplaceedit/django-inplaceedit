(function ($) {
    "use strict";
    var attr_old = $.fn.attr;
    $.fn.attr = function () {
        var a, aLength, attributes,  map;
        if (this[0] && arguments.length === 0) {
            map = {};
            attributes = this[0].attributes;
            aLength = attributes.length;
            for (a = 0; a < aLength; a = a + 1) {
                map[attributes[a].name.toLowerCase()] = attributes[a].value;
            }
            return map;
        }
        return attr_old.apply(this, arguments);
    };
    $.fn.redraw = function () {
        return this.hide(0, function () {
            $(this).show();
        });
    };
    $.fn.inplaceeditform = function (method) {
        var methods = $.inplaceeditform.methods;

        // method calling logic
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        }
        if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        }
        $.error('Method ' + method + ' does not exist on jQuery.inplaceeditform');
    };

    $.inplaceeditform = {
        opts: {
            "getFieldUrl": "/inplaceeditform/get_field/",
            "saveURL": "/inplaceeditform/save/",
            "successText": "Successfully saved",
            "eventInplaceEdit": "dblclick",
            "disableClick": true,
            "autoSave": false,
            "unsavedChanges": "You have unsaved changes!",
            "enableClass": "enable"
        },
        formSelector: "form.inplaceeditform",
        enabled: false,
        inplaceeditfields: null,
        methods: {},

        extend: function (newMethods) {
            this.methods = $.extend(this.methods, newMethods);
        }
    };

    $.inplaceeditform.extend({
        init: function (opts) {
            var self = $.inplaceeditform;
            self.isMsIE = $.browser && $.browser.msie;
            self.opts = $.extend(self.opts, opts || {});
            self.inplaceeditfields = this;
            // Hack to event onbeforeunload in IE
            if (self.isMsIE) {
                if ($(document).on !== undefined) {
                    $(document).on("click", "a", function () {
                        window.couldCatch = true;
                        window.newLocation = $(this).attr("href");
                    });
                } else {
                    $("a").live("click", function () {
                        window.couldCatch = true;
                        window.newLocation = $(this).attr("href");
                    });
                }
            }
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
                    if (!self.enabled || !$(this).hasClass(self.opts.enableClass)) {
                        return false;
                    }
                    $(this).data("ajaxTime", true);
                    var data = self.methods.getDataToRequest($(this).find("inplaceeditform"));
                    var extraConfig = $(this).find("inplaceeditform").data("extraConfig");
                    if (extraConfig) {
                        data = extraConfig(data);
                    }
                    var can_auto_save = parseInt($(this).find("inplaceeditform").attr("can_auto_save"));
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
                                        var medias_preferred = medias.filter("[delay=delay]");
                                        var medias_regular = medias.not("[delay=delay]");
                                        $.map(medias_preferred, function (media, i) {
                                            if (i === 0) {
                                                self.methods.loadjscssfile(media);
                                            } else {
                                                setTimeout(function () {
                                                    self.methods.loadjscssfile(media);
                                                }, 500);
                                            }
                                        });
                                        if (medias_preferred.length === 0) {
                                            $.map(medias_regular, function (media) {
                                                self.methods.loadjscssfile(media);
                                            });
                                        } else {
                                            setTimeout(function () {
                                                $.map(medias_regular, function (media) {
                                                    self.methods.loadjscssfile(media);
                                                });
                                            }, 500);
                                        }
                                    } catch (err) {
                                    }
                                    var links_parents = $(that).next().parents("a");
                                    if (links_parents.length > 0) {
                                        $.map(links_parents, function (link) {
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
                                    $(that).next(self.formSelector).find("input, select, textarea").focus();
                                    if (self.opts.autoSave && can_auto_save) {
                                        applyButton.hide();
                                        cancelButton.hide();
                                        applyFileButton.hide();
                                        var value = $(that).next(self.formSelector).find("input, select, textarea").val();
                                        var autoSave = function () {
                                            var newValue = $(this).val();
                                            if (newValue !== value) {
                                                $(that).next(self.formSelector).find(".apply").click();
                                            } else {
                                                $(that).next(self.formSelector).find(".cancel").click();
                                            }
                                        };
                                        $(that).next(self.formSelector).find("input, select, textarea").blur(autoSave);
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
                var msg = undefined;
                if ($(self.formSelector).size()) {
                    if (!self.isMsIE || (window.couldCatch && !(window.newLocation.indexOf("javascript:") === 0))) {
                        msg = self.opts.unsavedChanges;
                        if (event) {
                            // For IE and Firefox prior to version 4
                            event.returnValue = msg;
                        }
                    }
                }
                window.couldCatch = false;
                window.newLocation = null;
                return msg;
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
                        $(this).addClass(self.opts.enableClass);
                    });
                },
                disable: function () {
                    self.enabled = false;
                    self.inplaceeditfields.each(function () {
                        $(this).removeClass(self.opts.enableClass);
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
            $.map(links_parents, function (link) {
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
                if (self.isMsIE) {
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
                var config = inplace_span.find("inplaceeditform").attr();
                var config_html = "<inplaceeditform";
                var attr;
                for (attr in config) {
                    config_html += ' ' + attr + '="' + config[attr] + '"';
                }
                config_html += "></inplaceeditform>";
                inplace_span.html(response.value + config_html);
                inplace_span.css("display", "");
                self.methods.inplaceApplySuccessShowMessage(inplace_span, response);
                var applyFinish = that.data("applyFinish");
                if (applyFinish) {
                    applyFinish(that);
                }
                that.parent().remove();
            }
        },

        inplaceApplySuccessShowMessage: function (inplace_span) {
            var self = $.inplaceeditform;
            if (self.opts.successText) {
                var success_message = $("<ul class='success'><li>" + self.opts.successText + "</li></ul>");
                inplace_span.prepend(success_message);
                inplace_span.removeClass(self.opts.enableClass);
                setTimeout(function () {
                    success_message.fadeOut(function () {
                        $(this).remove();
                        inplace_span.redraw();
                        inplace_span.addClass(self.opts.enableClass);
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
            var inplaceedit_conf = form.prev().find("inplaceeditform");
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
            var inplaceedit_conf = form.prev().find("inplaceeditform");
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
            if (self.isMsIE) {
                data.msie = true;
            }
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
            var settings = inplaceedit_conf.attr();
            $.map(settings, function (value, key) {
                var data = "";
                if (dataToRequest !== "") {
                    data = "&";
                }
                data += key + "=" + value;
                dataToRequest += data;
            });
            var fontSize = inplaceedit_conf.parent().css("font-size");
            if (fontSize) {
                dataToRequest += "&font_size=" + fontSize;
            }
            return dataToRequest;
        },

        getDataToRequestUpload: function (inplaceedit_conf) {
            var dataToRequest = inplaceedit_conf.attr();
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
    });
})(jQuery);

