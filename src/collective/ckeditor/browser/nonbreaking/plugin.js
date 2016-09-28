(function() {
    var pluginName = 'nonbreaking';
    var insertNbspaceCmd = {
        exec: function( editor ) {
            editor.insertHtml( '&nbsp;' );
        }
    };
    var insertNbhyphenCmd = {
        exec: function( editor ) {
            console.log('nbhy');
            editor.insertHtml( '&#8209;' );
        }
    };
    CKEDITOR.plugins.add( pluginName, {
        icons: 'nbspace,nbhyphen',
        init : function( editor ) {
            editor.addCommand( 'insertNbspace', insertNbspaceCmd);
            editor.addCommand( 'insertNbhyphen', insertNbhyphenCmd);
            editor.ui.addButton( 'NbSpace', {
                label: "Non-breaking space (CTRL + ALT + space)",
                command: 'insertNbspace',
                className: 'cke_button_nbsp'
            });
            editor.ui.addButton( 'NbHyphen', {
                label: "Non-breaking hyphen (CTRL + ALT + hyphen)",
                command: 'insertNbhyphen',
                className: 'cke_button_nbhy'
            });
            editor.setKeystroke( CKEDITOR.ALT + CKEDITOR.CTRL + 32 /* space */, 'insertNbspace' );
            editor.setKeystroke( CKEDITOR.ALT + CKEDITOR.CTRL + 173 /* hyphen */, 'insertNbhyphen' );
        },
     });
})();
