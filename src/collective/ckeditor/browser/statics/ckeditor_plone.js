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
            // takeover textarea focus for ckeditor
            widget_config.startupFocus = (this == document.activeElement)
            /* Here starts the local js overload of settings by a field widget */
            if (jQuery('.cke_iswidget', jQuery(this).parent()).length) {
                // overridden boolean settings need to be converted to boolean again
                var booleanWidgetSettings = ['allowedContent'];
                settings = jQuery('.widget_settings input', jQuery(this).parent());
                settings.each(function () {
                    setting = jQuery(this);
                    var name = setting.attr('class');
                    var value = setting.val();
                    if (jQuery.inArray(name, booleanWidgetSettings) != -1) {
                        value = value == 'true'
                    }
                    widget_config[name] = value;
                });
                /* Destroy instance if it exists because an existing instance can not be managed twice */
                if (typeof CKEDITOR.instances != 'undefined') {
                    var instance = CKEDITOR.instances[ckid];
                        if (instance) { instance.destroy(true); }
	            };
            }
            CKEDITOR.replace( ckid, widget_config);
	    };
    });
};

jQuery(document).ready(launchCKInstances);

(function() {

CKEDITOR.on( 'dialogDefinition', function( ev ) {
    // Take the dialog name and its definition from the event
    // data.
    var dialogName = ev.data.name;
    var dialogDefinition = ev.data.definition;

    if (!ev.editor._getObjectInfoUrl) {
        ev.editor._getObjectInfoUrl = function(current_uid) {
            return CKEDITOR_PLONE_PORTALPATH + '/show_object_info/' + current_uid
        }
    }

    var showObjectInfo = function showObjectInfo(domElement, urlTextElement, protocol, current_uid) {
            function format(msg) {
                return '<p>Actual URL:</p><p>'+msg+'</p>';
            }

            domElement.setHtml(format('Loading...'));
            if (protocol == 'resolveuid/' && current_uid) {
                $.ajax({
                    url: ev.editor._getObjectInfoUrl(current_uid),
                    dataType: 'json',
                    method: 'GET',
                    success: function (data, textStatus, jqXHR) {
                        var resolved_url = data.url,
                            resolved_title = data.title;
                        domElement.setHtml(format(resolved_url));
                        if (urlTextElement && (urlTextElement.getValue() == '' || !urlTextElement.dirty)) {
                            urlTextElement.setValue(resolved_title);
                            urlTextElement.dirty = false;
                        }
                    },
                    error: function (jqXHR, textStatus) {
                        domElement.setHtml(format('Could not be resolved.'));
                    }
                });
            } else {
                domElement.setHtml('<p></p>');
            }
    };

    // Check if the definition is from the dialog we're
    // interested on (the "Link" dialog).
    if ( dialogName == 'link' ) {
        // Get a reference to the "Link Info" tab.
        var infoTab = dialogDefinition.getContents( 'info' );
        var protocol = infoTab.get('protocol');

        // Introduce custom protocol
        protocol['items'].push(['resolveuid/', 'resolveuid/']);

        // Add element to show the resolved uid
        var urlOptions = infoTab.get('urlOptions');
        urlOptions.children.push( {
            id: 'actual',
            type : 'html',
            setup: function( data ) {
                var domElement = this.getElement();
                // Since we can't hook into the plugin's url parsing, we have to do it here.
                if (data.url && !data.url.protocol && data.url.url.indexOf('resolveuid/') == 0) {
                    showObjectInfo(domElement, null, 'resolveuid/', data.url.url.split('resolveuid/')[1]);
                } else {
                    domElement.setHtml('<p></p>');
                }
            },
            html : ''
        });

        // Additional selectable protocols (might be extended by other plugins)
        ev.editor.plugins.link.additionalProtocols = [
            'resolveuid/'
        ];

        // Extended function `onKeyUp` to automatically check for our any custom protocol and set fields accordingly.
        var url = infoTab.get('url');
        var default_onKeyUp = url.onKeyUp;
        url.onKeyUp = CKEDITOR.tools.override(default_onKeyUp, function(org) {
            return function() {
                org.apply(this);
                this.allowOnChange = false;
                // Start of updating protocol
                var protocolField = this.getDialog().getContentElement('info', 'protocol'),
                    protocolValue = protocolField.getValue(),
                    urlField = this.getDialog().getContentElement('info', 'url'),
                    urlValue = urlField.getValue(),
                    linkTextField = this.getDialog().getContentElement('info', 'linkDisplayText'),
                    actualField = this.getDialog().getContentElement('info', 'actual'),
                    actualElement = actualField.getElement(),
                    additionalProtocol;

                for (var i=0;i<ev.editor.plugins.link.additionalProtocols.length;i++) {
                    additionalProtocol = ev.editor.plugins.link.additionalProtocols[i];

                    if (urlValue.indexOf(additionalProtocol) == 0) {
                        protocolField.setValue(additionalProtocol);
                        protocolValue = protocolField.getValue();
                        urlField.setValue(urlValue.substr(additionalProtocol.length));
                        urlValue = urlField.getValue();
                    }
                }
                if (protocolValue == 'resolveuid/') { // Update url as well
                    showObjectInfo(actualElement, linkTextField, protocolValue, urlValue);
                }
                this.allowOnChange = true;
            }
        });

        // Mark field, if it has not been populated by object's data.
        var linkTextField = infoTab.get('linkDisplayText');
        linkTextField.onKeyUp = function(ev) {
            this.dirty = true;
        };
        linkTextField.setup = CKEDITOR.tools.override(linkTextField.setup, function(org) {
            return function (data) {
                org.apply(this, [data]);
                if (this.getValue()) {
                    this.dirty = true;
                }
            }
        });

        // Setup url field correctly if its a `resolveuid` link.
        var defaultUrlSetup = url.setup;
        url.setup = CKEDITOR.tools.override(defaultUrlSetup, function(org) {
            return function (data) {
                var additionalProtocol;
                org.apply(this, [data]);
                this.allowOnChange = false;

                for (var i=0;i<ev.editor.plugins.link.additionalProtocols.length;i++) {
                    additionalProtocol = ev.editor.plugins.link.additionalProtocols[i];
                    if (data.url && data.url.url.indexOf(additionalProtocol) == 0) {
                        this.getDialog().getContentElement('info', 'url').setValue(data.url.url.split(additionalProtocol)[1]);
                    }
                }
                this.allowOnChange = true;
            }
        });

        // Setup protocol field correctly if its a `resolveuid` link.
        var protocolField = infoTab.get('protocol');
        var defaultProtocolSetup = protocolField.setup;
        protocolField.setup = CKEDITOR.tools.override(defaultProtocolSetup, function(org) {
            return function (data) {
                var additionalProtocol;
                org.apply(this, [data]);
                for (var i=0;i<ev.editor.plugins.link.additionalProtocols.length;i++) {
                    additionalProtocol = ev.editor.plugins.link.additionalProtocols[i];
                    if (data.url && data.url.url.indexOf(additionalProtocol) == 0) {
                        this.getDialog().getContentElement('info', 'protocol').setValue(additionalProtocol);
                    }
                }
            }
        });
        protocolField.onChange = function (ev) {
            var protocolField = this.getDialog().getContentElement('info', 'protocol');
            var urlField = this.getDialog().getContentElement('info', 'url');
            if (ev.data.value == 'resolveuid/') {
                urlField.disable();
            } else {
                urlField.enable();
            }
            if (protocolField.previousValue == 'resolveuid/' && ev.data.value != 'resolveuid/' || protocolField.previousValue != 'resolveuid/' && ev.data.value == 'resolveuid/') {
                this.allowOnChange = false;
                urlField.setValue('');
                this.allowOnChange = true;
            }
            protocolField.previousValue = ev.data.value;
        }
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
