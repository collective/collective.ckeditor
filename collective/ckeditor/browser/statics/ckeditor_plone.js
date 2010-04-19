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
        ck_basehref = jQuery('.ck_basehref', jQuery(this).parent()).val();
        CKEDITOR.replace( ckid,
          {
            customConfig : ck_basehref + '/ckeditor_plone_config.js'
          });

    })    
}

jQuery(document).ready(launchCKInstances);

