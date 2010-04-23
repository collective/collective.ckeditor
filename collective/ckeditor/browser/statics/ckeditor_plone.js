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

launchCKInstances = function() {
    jQuery('.ckeditor_plone').each(function(){
        ckid = jQuery(this).attr('id');
        cke_config_url = jQuery('.cke_config_url', jQuery(this).parent()).val();
        /* Here starts the local js overload of settings by a field widget */
        /* for now it only works with at rich widget : basehref width and height are the only attributes */
        /* TODO improve it for any possible widget settings with jQuery.each('',jQuery(this).parent()) ... */
        if (jQuery('.cke_iswidget', jQuery(this).parent()).length) {
            cke_width = jQuery('.cke_width', jQuery(this).parent()).val();
            cke_height = jQuery('.cke_height', jQuery(this).parent()).val();
            cke_baseHref = jQuery('.cke_baseHref', jQuery(this).parent()).val();
            CKEDITOR.replace( ckid,
              {
                customConfig : cke_config_url,
                width : cke_width,
                height : cke_height,
                baseHref : cke_baseHref
              });
            }
        else  {
            CKEDITOR.replace( ckid,
              {
                customConfig : cke_config_url
              });
            }
    })    
}

jQuery(document).ready(launchCKInstances);

