(function ($) {
    $.fn.inplaceeditform = function (opts, callback) {
        var defaults = {
            "getFieldUrl": "/inplaceeditform/get_field/",
            "saveURL": "/inplaceeditform/save/",
            "successText": "Successfully saved",
            "eventInplaceEdit": "dblclick",
            "disableClick": true
        };
        var enabled = true;
        opts = $.extend(defaults, opts || {});
        this.each(function () {
            if (opts.disableClick) {
                $(this).click(function () {
                    if (!enabled) {
                        return true;
                    }
                    return false;
                });
            }
            $(this).bind("mouseenter", function () {
                if (!enabled) {
                    return false;
                }
                $(this).addClass("edit_over");
            });

            $(this).bind("mouseleave", function () {
                $(this).removeClass("edit_over");
            });

            $(this).bind(opts.eventInplaceEdit, function () {
                if (!enabled) {
                    return false;
                }
                $(this).data("inplace_enabled");
                var data = getDataToRequest($(this).find("span.config"));
                data += "&__widget_height=" + $(this).innerHeight() + "px" + "&__widget_width=" + $(this).innerWidth() + "px";
                var that = $(this);
                $.ajax({
                    data: data,
                    url: opts.getFieldUrl,
                    type: "GET",
                    async: true,
                    dataType: 'json',
                    error: bind(treatmentStatusError, {"context": $(this)}),
                    success: function (response) {
                        if (!response) {
                            alert("The server is down");
                        } else if (response.errors) {
                            alert(response.errors);
                        } else {
                            that.hide();
                            that.addClass("inplaceHide");
                            var tags = $(response.field_render);
                            $(response.field_render).insertAfter(that);

                            var head = $("head")[0];
                            try {
                                var medias = $(response.field_media_render);
                                $.map(medias, function (media) {
                                    loadjscssfile(media);
                                });
                            } catch (err) {
                            }
                            var links_parents = that.next().parents("a");
                            if (links_parents.length > 0) {
                                $.map(links_parents, function (link, i) {
                                    link = $(link);
                                    var href = link.attr("href");
                                    link.attr("hrefinplaceedit", href);
                                    link.addClass("linkInplaceEdit");
                                    link.removeAttr("href");
                                });
                            }
                            var applyButton = that.next().find(".apply");
                            var cancelButton = that.next().find(".cancel");
                            var applyFileButton = that.next().find(".applyFile");
                            if (cancelButton) {
                                cancelButton.click(inplaceCancel);
                            }
                            if (applyButton) {
                                applyButton.click(inplaceApply);
                                that.next("form.inplaceeditform").submit(bind(inplaceApply, applyButton));
                            }
                            if (applyFileButton) {
                                applyFileButton.click(inplaceApplyUpload);
                                that.next("form.inplaceeditform").submit(bind(inplaceApply, applyFileButton));
                            }


                        }
                    }
                });
            });
            function treatmentStatusError(response) {
                if (response.status === 0) {
                    alert("The server is down");
                } else if (response.status === 403) {
                    alert("Permission denied, please check that you are login");
                } else {
                    alert(response.statusText);
                }
                this.context.next(".cancel").click();
            }

            function revertlinkInplaceEdit(links_parents) {
                $.map(links_parents, function (link, i) {
                    link = $(link);
                    var href = link.attr("hrefinplaceedit");
                    link.attr("href", href);
                    link.removeClass("linkInplaceEdit");
                    link.removeAttr("hrefinplaceedit");
                });
            }

            function inplaceCancel() {
                revertlinkInplaceEdit($(this).parents("a.linkInplaceEdit"));
                $(this).parent().prev().fadeIn();
                $(this).parent().prev().removeClass("inplaceHide");
                var cancelFinish = $(this).data("cancelFinish");
                if (cancelFinish) {
                    cancelFinish();
                }
                $(this).parent().remove();
                return false;
            }

            function replaceAll(txt, replace, with_this) {
                return txt.replace(new RegExp(replace, "g"), with_this);
            }

            function inplaceApplySuccess(response) {
                if (typeof response === "string") {
                    if ($.browser.msie) {
                        response = replaceAll(response, "'\\\\\"", "'");
                        response = replaceAll(response, "\"'", "'");
                    }
                    try {
                        response = JSON.parse(response);
                    } catch (errno) {
                        response = eval("( " + response + " )");
                    }
                }
                revertlinkInplaceEdit($(this.form).parents("a.linkInplaceEdit"));
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
                    var success_message = $("<ul class='success'><li>" + opts.successText + "</li></ul>");
                    if (opts.successText) {
                        inplace_span.prepend(success_message);
                        setTimeout(function () {
                            success_message.fadeOut(function () {
                                $(this).remove();
                            });
                        }, 2000);
                    }
                    inplace_span.show();
                    inplace_span.removeClass("inplaceHide");
                    var applyFinish = $(that).data("applyFinish");
                    if (applyFinish) {
                        applyFinish(that);
                    }
                    that.parent().remove();
                }
            }

            function bind(func, that) {
                return function () {
                    return func.apply(that, arguments);
                };
            }
            function getCSFRToken() {
                return csrf_token;
            }
            function inplaceApply() {
                var form = $(this).parents("form.inplaceeditform");
                form.animate({opacity: 0.1});
                form.find("ul.errors").fadeOut(function () {$(this).remove(); });
                var inplaceedit_conf = form.prev().find("span.config");
                var data = getDataToRequest(inplaceedit_conf);
                var field_id = form.find("span.field_id").html();
                var getValue = $(this).data("getValue"); // A hook
                var value;
                if (getValue) {
                    value = getValue(form, field_id);
                } else {
                    value = form.find("#" + field_id).val();
                }
                data += "&value=" + encodeURIComponent($.toJSON(value));
                var csrfmiddlewaretoken = getCSFRToken();
                if (csrfmiddlewaretoken) {
                    data += "&csrfmiddlewaretoken=" + csrfmiddlewaretoken;
                }
                $.ajax({
                    data: data,
                    url:  opts.saveURL,
                    type: "POST",
                    async: true,
                    dataType: 'text',
                    error: bind(treatmentStatusError, {"context": $(this)}),
                    success: bind(inplaceApplySuccess, {"context": $(this),
                                                        "form": form,
                                                        "inplaceedit_conf": inplaceedit_conf})
                });
                return false;
            }

            function inplaceApplyUpload() {
                var form = $(this).parents("form.inplaceeditform");
                form.animate({opacity: 0.1});
                form.find("ul.errors").fadeOut(function () {$(this).remove(); });
                var inplaceedit_conf = form.prev().find("span.config");
                var data = getDataToRequestUpload(inplaceedit_conf);
                var csrfmiddlewaretoken = getCSFRToken();
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
                var that = $(this);

                form.ajaxSubmit({
                    url: opts.saveURL,
                    data: data,
                    async: true,
                    type: "POST",
                    dataType: "application/json",
                    error: bind(treatmentStatusError, {"context": $(this)}),
                    success: bind(inplaceApplySuccess, {"context": $(this),
                                                        "form": form,
                                                        "inplaceedit_conf": inplaceedit_conf})
                });
                return false;
            }

            function getDataToRequest(inplaceedit_conf) {
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
            }

            function getDataToRequestUpload(inplaceedit_conf) {
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
            }

            function loadjscssfile(media) {
                var fileref;
                if (media.tagName === "SCRIPT") { //if filename is a external JavaScript file
                    fileref = document.createElement('script');
                    fileref.setAttribute("type", "text/javascript");
                    if (media.src !== null && media.src !== "") {
                        fileref.setAttribute("src", media.src);
                    } else {
                        appendChild(fileref, media.innerHTML);
                    }
                } else if (media.tagName === "LINK" && media.type === "text/css") { //if filename is an external CSS file
                    fileref = document.createElement("link");
                    fileref.setAttribute("rel", "stylesheet");
                    fileref.setAttribute("type", "text/css");
                    fileref.setAttribute("href", media.href);
                }

                if (typeof fileref !== "undefined") {
                    document.getElementsByTagName("head")[0].appendChild(fileref);
                }
            }
            function appendChild(node, text) {
                if (null === node.canHaveChildren || node.canHaveChildren) {
                    node.appendChild(document.createTextNode(text));
                } else {
                    node.text = text;
                }
            }
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


        });
        return {
            enable: function () {
                enabled = true;
            },
            disable: function () {
                enabled = false;
            }
        };
    };
})(jQuery);
