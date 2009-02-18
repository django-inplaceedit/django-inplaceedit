
var $j = jQuery.noConflict();

function inplaceeditform_ready(form_prefix, field_name, obj_id, content_type_id, form, filters){

    $j('#view_'+form_prefix+'-'+field_name+'').bind("mouseenter",function(){
      $j(this).addClass("chunk_over");
    }).bind("mouseleave",function(){
      $j(this).removeClass("chunk_over");
    });

    $j('#view_'+form_prefix+'-'+field_name+'').dblclick(function (){
        $j('span#view_'+form_prefix+'-'+field_name+'_save').fadeOut();
        document.getElementById('view_'+form_prefix+'-'+field_name+'').style.display = 'none';
        document.getElementById('tools_'+form_prefix+'-'+field_name+'').style.display = 'block';
        var tools_error = document.getElementById('tools_'+form_prefix+'-'+field_name+'_error');
        var child_nodes = tools_error.childNodes;
        for (i=0; i<child_nodes.length; i++)
        {
            tools_error.removeChild(child_nodes[i]);
        }
    });

    $j('#tools_'+form_prefix+'-'+field_name+'_cancel_id').click(function (){
        $j('span#view_'+form_prefix+'-'+field_name+'_save').fadeOut();
        document.getElementById('tools_'+form_prefix+'-'+field_name+'').style.display = 'none';
        document.getElementById('view_'+form_prefix+'-'+field_name+'').style.display = 'block';
    });

    $j('#tools_'+form_prefix+'-'+field_name+'_apply_id').click(function (){


        var value_input = $j('#id_'+form_prefix+'-'+field_name+'');

        var value_input = $j('#id_'+form_prefix+'-'+field_name+'')[0];
        var value;

        if (value_input.multiple)
        {
            var options_selected = $j('#id_'+form_prefix+'-'+field_name+' option:selected');
            value = [];
            for( i =0; i< options_selected.length; i++)
            {
                value[i] = options_selected[i].value;
            }
        }
        else{
            value = value_input.value;
        }
        var form_query = '';
        if (form)
        {
            form_query = '&form='+form;
        }
//         filters[filters.length]='|safe';
        x = filters;
        var data = 'id='+obj_id+'&field='+field_name+'&value='+escape($j.toJSON(value))+'&content_type_id='+content_type_id+form_query+'&'+'filters='+$j.toJSON(filters);
        $j.ajax({
        data: data,
        url: "/inplaceeditform/",
        type: "POST",
        async:true,
        success: function(response){

            response = eval("("+ response +")");
            if (response.errors)
            {
                var tools_error = $j('#tools_'+form_prefix+'-'+field_name+'_error')[0];
                var child_nodes = tools_error.childNodes;
                for (i=0; i<child_nodes.length; i++)
                {
                    tools_error.removeChild(child_nodes[i]);
                }
                var ul = document.createElement('ul');
                ul.className = "errors";
                $j('#tools_'+form_prefix+'-'+field_name+'_error')[0].appendChild(ul);
                for (var error in response)
                {
                    if (error != 'errors')
                    {
                        var li = document.createElement('li');
                        if ("'+field_name+'" == error)
                            li.innerHTML = response[error];
                        else
                            li.innerHTML = error+ ": " +response[error];
                        ul.appendChild(li);
                    }
                }
            }
            else
            {
                $j('#tools_'+form_prefix+'-'+field_name+'')[0].style.display = 'none';
                $j('#view_'+form_prefix+'-'+field_name+'')[0].style.display = 'block';
                $j('#view_'+form_prefix+'-'+field_name+'_id')[0].innerHTML = response.value;
                $j('div#view_'+form_prefix+'-'+field_name+'_save').fadeIn();
                window.setTimeout("$j('div#view_"+form_prefix+"-"+field_name+"_save').fadeOut()", 2000);
            }
        }
    });
  });
}
