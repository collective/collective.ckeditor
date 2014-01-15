(function() {
    var showMessage = function showMessage(editor, text, effect) {
        var editorbody = $(".cke_top", editor.container.$);
        var message = $(".cke_msg", editorbody);
        message.remove();
        if (effect === 'keep') {
            var body = text + '<span class="cke_discrete">Click to close message.</span>';
        }
        else {
            var body = text;
        }
        editorbody.prepend('<div class="cke_msg">' + body + '</div>');
        var message = $(".cke_msg", editorbody);
        if (effect == 'in') {
            message.fadeIn(400).delay(400);
        }
        else if (effect === 'keep') {
            message.show();
            message.click(function() {
                $(this).remove();
            });
        }
        else {
            message.show().delay(800).fadeOut(800);
        };
    };
    var saveCmd = {
        modes : { wysiwyg:1, source:1 },
        exec : function( editor ) {
        if (!editor.checkDirty()) {
            return;
        }
        showMessage(editor, 'Saving content...', 'in');
        editor.updateElement();
        var url = $('base').attr('href') + '/cke-save';
        var name = editor.element.$.name;
        var data = {
            fieldname: name,
            text: editor.getData()
        };
        var settings = {
            url: url,
            type: 'POST',
            data: data,
            success: function(data){
                editor.resetDirty();
                showMessage(editor, 'Content saved.');
            },
            error: function(xhr, status, error){
                showMessage(editor, 'Error : content not saved.', 'keep');
            }
        };
        $.ajax(settings);
        }
    };
    var pluginName = 'ajaxsave';
    CKEDITOR.plugins.add( pluginName, {
        icons: 'ajaxsave',
        requires : [ 'dialog' ],
        init : function( editor ) {
            var command = editor.addCommand( pluginName, saveCmd );
            command.modes = { wysiwyg : !!( editor.element.$.form ) };
            editor.ui.addButton( 'AjaxSave', {
                label: "Save",
                command: pluginName,
                className: 'cke_button_save'
                });
            editor.element.getDocument().appendStyleSheet(
                CKEDITOR.getUrl('../++resource++cke_ajaxsave/message.css')); }
        }
    );
})();
