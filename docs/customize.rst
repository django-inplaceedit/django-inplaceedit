.. _customize:

==============================
Customizing django-inplaceedit
==============================

django-inplaceedit is generic, customizable and extensible.

Permission Adaptor API
======================

By default you can inline edit a field if you are authenticated with a superuser. But it's customizable:


Overwriting the default permission adaptor
-------------------------------------------

This package have two inplementations:

 * `SuperUserPermEditInline <https://github.com/Yaco-Sistemas/django-inplaceedit/blob/master/inplaceeditform/perms.py/>`_ (by default): Only you can edit if you are super user
 * `AdminDjangoPermEditInline <https://github.com/Yaco-Sistemas/django-inplaceedit/blob/master/inplaceeditform/perms.py/>`_: Yo can edit the content if you have a permission edit for that model. If you want enabled this, write in your settings:

 ::

   ADAPTOR_INPLACEEDIT_EDIT = 'inplaceeditform.perms.AdminDjangoPermEditInline'



You can create a specify adaptor. MyAdaptorEditInline is a class with a single class method, this method receives a adaptor field

::

 # in your settings

 ADAPTOR_INPLACEEDIT_EDIT = 'app_name.perms.MyAdaptorEditInline'


 # in app_name.perms

 class MyAdaptorEditInline(object):

     @classmethod
     def can_edit(cls, adaptor_field):
        return True # All user can edit

Example
-------

::

 class MyAdaptorEditInline(object):

     @classmethod
     def can_edit(cls, adaptor_field):
         user = adaptor_field.request.user
         obj = adaptor_field.obj
         can_edit = False
         if user.is_anonymous():
             pass
         elif user.is_superuser:
             can_edit = True
         else:
            can_edit = has_permission(obj, user, 'edit')
         return can_edit



Creating an adaptor
===================

You can create an adaptor to work with django-inplaceedit, the behavior is fully customizable. To default inplaceedit has 17 `adaptors <https://github.com/Yaco-Sistemas/django-inplaceedit/blob/master/inplaceeditform/fields.py/>`_ (AdaptorTextField, AdaptorTextAreaField, AdaptorChoicesField, AdaptorBooleanField, AdaptorDateTimeField, AdaptorForeingKeyField, AdaptorManyToManyField, AdaptorImageField etc). These use the api, overwriting some methods for them.

You can see four examples in `django-inplaceedit-extra-fields project <https://github.com/goinnn/django-inplaceedit-extra-fields/blob/master/inplaceeditform_extra_fields/fields.py/>`_

First step
----------

In your settings:

::

    ADAPTOR_INPLACEEDIT = {'myadaptor': 'app_name.fields.MyAdaptor'}

In app_name.fields.MyAdaptor:

::

    class MyAdaptor(BaseAdaptorField):

        @property
        def name(self):
            return 'myadaptor'


You can overwrite a default adaptor. To overwrite a adaptor add in your settings something like this:

::

 ADAPTOR_INPLACEEDIT = {'text': 'app_name.fields.MyAdaptorText'}

For this case you overwrite the AdaptorText with MyAdaptorText.


Python API
----------

 * loads_to_post: It returns the value of the request (normally request.POST)
 * classes: Classes of tag cover. By default "inplaceedit" and "myadaptorinplaceedit"
 * get_config: Preprocessed of the configuration. By default, it does nothing.
 * get_form_class: It returns the form class.
 * get_form: It returns a instace of form class.
 * get_field: It returns a field of instance of form class.
 * render_value: It returns the render of the value. If you write {% inplace_edit "obj.name|filter1" %} it returns something like this {{ obj.name|filter1 }}.
 * render_value_edit: It returns the render value if you can edit. It returns by default the same of "render_value", but if the value is None call to empty_value
 * empty_value: It returns an empty value for this adaptor. By default, 'Dobleclick to edit'.
 * render_field: It returns the render of form, with a field.
 * render_media_field: It returns the media (scripts and css) of the field.
 * render_config: It returns the render of config.
 * can_edit: It returns a boolean that indicate if this user can edit inline this content or not.
 * get_value_editor: It returns a clean value to be saved in DB.
 * save: Save the value in DB.
 * get_auto_height: Returned if the field rendered with auto height
 * get_auto_width: Returned if the field rendered with auto width
 * treatment_height: Special treatment to widget's height.
 * treatment_width: Special treatment to widget's width.

::

    If you want to use own options in your adaptor, you can do it. These options will be in self.config in the adaptor.
    {% inplace_edit "obj.field_name" my_opt1="value1", my_opt2="value2" %}


JavaScript API
--------------

You can change the javascript behaviour by adding or overriding methods from the original implementation by adding the special file jquery.inplaceeditform.hooks.js to your project.
$.inplaceeditform.extend takes an object with the new or replacement methods.

::

    $.inplaceeditform.extend(
        {
            inplaceApplySuccessShowMessage: function(inplace_span) {
                var self = $.inplaceeditform;
                if (self.opts.successText) {
                    var modal = $('#inplaceedit-modal');
                    var body = modal.find('div.modal-body p');
                    body.html(self.opts.successText);

                    setTimeout(function () {
                        modal.fadeOut(function () {
                            $(this).remove();
                        });
                    }, 2000);
                }
                modal.show();
            }
        }
    );


Additionally there are four hooks,

 * getValue: if the value is componing for various widgets, you can set the function getValue, to these DOM elements. Something like this:

    ::

        <script type="text/javascript">
            (function($){
                $(document).ready(function () {
                    function myGetValue(form, field_id) {
                        return ""Something"";
                    }
                    $(".applyMyAdaptor").data("getValue", myGetValue);
            });
            })(jQuery);
        </script>

 * applyFinish: if you need/want to do some action after the value be saved. Something like this:

    ::

        <script type="text/javascript">
            (function($){
                $(document).ready(function () {
                    function myApplyFinish(applyButton) {
                        return ""Something"";
                    }
                    $(".applyMyAdaptor").data("applyFinish", myApplyFinish);
            });
            })(jQuery);
        </script>

 * cancelFinish: if you need/want to do some action after the cancel the edit. Something like this:

    ::

        <script type="text/javascript">
            (function($){
                $(document).ready(function () {
                    function myCancelFinish(cancelButton) {
                        return ""Something"";
                    }
                    $(".cancelMyAdaptor").data("cancelFinish", myCancelFinish);
            });
            })(jQuery);
        </script>

  * extraConfig: if you need/want add something to the config in the ajax request to print the field

    ::

        <script type="text/javascript">
            (function($){
                $(document).ready(function () {
                    function myExtraConfig(data) {
                        return data + ""Something"";
                    }
                    $(".configMyAdaptor").data("extraConfig", myExtraConfig);
            });
            })(jQuery);
        </script>

For example the adaptor datetime use these hooks.

