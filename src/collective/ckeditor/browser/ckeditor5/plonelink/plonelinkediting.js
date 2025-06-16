// plonelink/plonelinkediting.js

import { Plugin } from 'ckeditor5';



var createPloneLinkElement = function(uid, writer) {
    var linkElement = writer.createAttributeElement( 'a', { uid }, { priority: 5 } );
    writer.setCustomProperty( 'plonelink', true, linkElement );
    return linkElement;
}

export default class PloneLinkEditing extends Plugin {
    init() {
        // console.log( 'PloneLinkEditing#init() got called' );
	// var editor = this.editor;
	// editor.model.schema.extend('$text', { allowAttributes: 'linkPloneUid'});
	// editor.conversion.for( 'dataDowncast' )
	    // .attributeToElement( { model: 'linkPloneUid', view: createPloneLinkElement } );
        // console.log( 'PloneLinkEditing#init() done' );
    }
}

