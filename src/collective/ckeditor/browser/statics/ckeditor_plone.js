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
        editor = CKEDITOR.replace( ckid, widget_config);
        update_element = function() {
            this.updateElement();
            var event = new Event('change');
            this.element.$.dispatchEvent(event);
        };
        editor.on('blur', update_element);
        editor.on('change', update_element);
        editor.on('input', update_element);
        // hide text format select
        jQuery(editor.element.$).parents('form').find('div.fieldTextFormat').hide() 
        };
    })
}

jQuery(document).ready(launchCKInstances);
// needed for text field in a modal dialog
// among others, portlet manager
jQuery(document).on('after-render.plone-modal.patterns', launchCKInstances);

(function() {

    var format = function format(msg) {
        var ploneLang = editor.lang.plone;
        return '<p>'+ploneLang.actual_url+'</p><p>'+msg+'</p>';
    };

    var showActualUrl = function showActualUrl(domElement, url) {
        var ploneLang = editor.lang.plone;
        if (url.indexOf('resolveuid') !== -1) {
            domElement.setHtml(format(ploneLang.loading));
            var current_uid = url.split('resolveuid/')[1];
            var new_url = CKEDITOR_PLONE_PORTALPATH + '/convert_uid_to_url/' + current_uid;
            var settings = {
                url: new_url,
                type: 'GET',
                success: function(data, textStatus, jqXHR){
                    if (jqXHR.status == 200) {
                        domElement.setHtml(format(data));
                    } else {
                        domElement.setHtml(format(ploneLang.could_not_be_resolved));
                    }
                },
                error: function(jqXHR, textStatus){
                    domElement.setHtml(format(ploneLang.could_not_be_resolved));
                }
            };
            $.ajax(settings);
            return;
        }
        domElement.setHtml('<p></p>');
    };

CKEDITOR.plugins.add('plone', {name: 'plone', path: 'plone'});
CKEDITOR.plugins.setLang('plone', 'en', {
    invalid_ruid_protocol: 'When using internal link that contains "resolveuid", the value of the "Protocol" field needs to be "<other>".',
    actual_url: 'Actual URL',
    loading: 'Loading...',
    could_not_be_resolved: 'Could not be resolved.',
});
CKEDITOR.plugins.setLang('plone', 'fr', {
    invalid_ruid_protocol: 'Quand vous utilisez un lien interne qui contient "resolveuid", la valeur du champs "Protocole" doit être "<autre>".',
    actual_url: 'URL finale',
    loading: 'En cours...',
    could_not_be_resolved: "Ne peut être déterminée.",
});
CKEDITOR.plugins.setLang('plone', 'nl', {
    invalid_ruid_protocol: 'Als je een interne link met "resolveuid" erin gebruikt, moet het "Protocol" veld "<ander>" zijn.',
    actual_url: 'Feitelijke URL',
    loading: 'Laden...',
    could_not_be_resolved: "Kan niet berekend worden.",
});


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

        var default_validate = url.validate;
        url.validate = function() {
            var ploneLang = editor.lang.plone;
            if ( this.getValue().includes('resolveuid') ) {
                var dialog = this.getDialog();
                var protocol = dialog.getValueOf('info', 'protocol');
                console.log("protocol: " + protocol);
                if ( protocol != '') {
                    alert( ploneLang.invalid_ruid_protocol );
                    return false;
                }
            }
            return default_validate.apply(this);
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
