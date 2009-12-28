browser_height = jQuery(window).height();
browser_width = jQuery(window).width();

CKEDITOR.editorConfig = function( config )
{
    config.contentsCss = portal_url + '/base.css';
    config.filebrowserWindowWidth = parseInt(jQuery(window).width()*80/100);
    config.filebrowserWindowHeight = parseInt(jQuery(window).height()*95/100);
};
