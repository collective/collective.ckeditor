/* Standard CKeditor tips for non compatible browsers
   Must be i18nized */


if ( typeof console != 'undefined' )
	console.log();


if ( window.CKEDITOR )
{
	(function()
	{
		var showCompatibilityMsg = function()
		{
			var env = CKEDITOR.env;

			var html = '<p><strong>Your browser is not compatible with CKEditor.</strong>';

			var browsers =
			{
				gecko : 'Firefox 2.0',
				ie : 'Internet Explorer 6.0',
				opera : 'Opera 9.5',
				webkit : 'Safari 3.0'
			};

			var alsoBrowsers = '';

			for ( var key in env )
			{
				if ( browsers[ key ] )
				{
					if ( env[key] )
						html += ' CKEditor is compatible with ' + browsers[ key ] + ' or higher.';
					else
						alsoBrowsers += browsers[ key ] + '+, ';
				}
			}

			alsoBrowsers = alsoBrowsers.replace( /\+,([^,]+), $/, '+ and $1' );

			html += ' It is also compatible with ' + alsoBrowsers + '.';

			html += '</p><p>With non compatible browsers, you should still be able to see and edit the contents (HTML) in a plain text field.</p>';

			document.getElementById( 'alerts' ).innerHTML = html;
		};

		var onload = function()
		{
			// Show a friendly compatibility message as soon as the page is loaded,
			// for those browsers that are not compatible with CKEditor.
			if ( !CKEDITOR.env.isCompatible )
				showCompatibilityMsg();
		};

		// Register the onload listener.
		if ( window.addEventListener )
			window.addEventListener( 'load', onload, false );
		else if ( window.attachEvent )
			window.attachEvent( 'onload', onload );
	})();
}


/* End Standard CKeditor tips for non compatible browsers  */

/* Plone specific ckeditor launcher using jQuery */

launchCKInstances = function (ids_to_launch) {
    jQuery('.ckeditor_plone').each(function(){
        ckid = jQuery(this).attr('id');
        ids_to_launch = ids_to_launch || [];
	/* we can specify an array of ids for wich CKeditor has to be launched */
	/* if no ids is provided or if the current id is in the array of given ids, we proceed */
        if ((typeof(ids_to_launch[0]) == 'undefined') || (jQuery.inArray(ckid, ids_to_launch) >= 0)) { 
        cke_config_url = jQuery('.cke_config_url', jQuery(this).parent()).val();
        var widget_config = {};
        widget_config.customConfig = cke_config_url;
        /* Here starts the local js overload of settings by a field widget */
        if (jQuery('.cke_iswidget', jQuery(this).parent()).length) {
            settings = jQuery('.widget_settings input', jQuery(this).parent());
            settings.each(function () {
                setting = jQuery(this);
                widget_config[setting.attr('class')] = setting.val();
            });
	    /* Destroy instance if it exists because an existing instance can not be managed twice */
	    if (typeof CKEDITOR.instances != 'undefined') {
	        var instance = CKEDITOR.instances[ckid];
                if (instance) { instance.destroy(true); }
	    };
        }
        CKEDITOR.replace( ckid, widget_config);
	};
    })
}

jQuery(document).ready(launchCKInstances);

(function() {

    var format = function format(msg) {
        return '<p>Actual URL</p><p>'+msg+'</p>';
    };

    var showActualUrl = function showActualUrl(domElement, url) {
        if (url.indexOf('resolveuid') !== -1) {
            domElement.setHtml(format('Loading...'));
            var current_uid = url.split('resolveuid/')[1];
            var new_url = CKEDITOR_PLONE_PORTALPATH + '/convert_uid_to_url/' + current_uid;
            var settings = {
                url: new_url,
                type: 'GET',
                success: function(data, textStatus, jqXHR){
                    if (jqXHR.status == 200) {
                        domElement.setHtml(format(data));
                    } else {
                        domElement.setHtml(format('Could not be resolved.'));
                    }
                },
                error: function(jqXHR, textStatus){
                    domElement.setHtml(format('Could not be resolved.'));
                }
            };
            $.ajax(settings);
            return;
        }
        domElement.setHtml('<p></p>');
    };

CKEDITOR.on( 'dialogDefinition', function( ev ) {
    // Take the dialog name and its definition from the event
    // data.
    var dialogName = ev.data.name;
    var dialogDefinition = ev.data.definition;

    // Check if the definition is from the dialog we're
    // interested on (the "Link" dialog).
    if ( dialogName == 'link' ) {
        // Get a reference to the "Link Info" tab.
        var infoTab = dialogDefinition.getContents( 'info' );

        var urlOptions = infoTab.get('urlOptions');
        urlOptions.children.push( {
            id: 'actual',
            type : 'html',
            setup: function( data ) {
                var domElement = this.getElement();
                if ( data.url ) {
                    showActualUrl(domElement, data.url.url);
                } else {
                    domElement.setHtml('<p></p>');
                }
            },
            html : ''
        });

        var url = infoTab.get('url');
        default_onKeyUp = url.onKeyUp;
        url.onKeyUp = function() {
            var actual = this.getDialog().getContentElement('info', 'actual');
            var domElement = actual.getElement();
            var url = this.getValue();
            showActualUrl(domElement, url);
            default_onKeyUp.apply(this);
        };
    }

   // Check if the definition is from the dialog we're
   // interested on (the "Table" dialog).
   if ( dialogName == 'table' )
   {
       // Get a reference to the "Table Info" tab.
       var infoTab = dialogDefinition.getContents( 'info' );
 
       // Set default width
       txtWidth = infoTab.get( 'txtWidth' );
       defaultTableWidth = ev.editor.config.defaultTableWidth;
       txtWidth['default'] = defaultTableWidth;
   }

});

})();
