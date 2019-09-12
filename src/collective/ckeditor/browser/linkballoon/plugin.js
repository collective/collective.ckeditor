( function() {
    'use strict';

    CKEDITOR.plugins.add( 'linkballoon', {
        requires: 'balloontoolbar,link',

        init: function( editor ) {
            editor.balloonToolbars.create( {
                buttons: 'Link,Unlink',
                cssSelector: 'a'
            } );
        }
    } );
} )();
