// plonelink/plonelinkui.js

import { ButtonView, Plugin, LinkUI, LinkFormView } from 'ckeditor5';

export default class PloneLinkUI extends LinkUI {
    static get pluginName() {
	    return 'PloneLinkUI';
    }

    _createFormView() {
	var view = super._createFormView();
	view.urlInputView.label = 'Plone Link';
	view.children.first.label = 'Plone Link';
	view.children.last.children.add(this._createBrowseButton(view), 1);
	this.editor.on('plone_set_url', (evt, data) => {
	    view.urlInputView.fieldView.value = data.url;
	    view.fire('submit');
	    this._showUI();
	});
	return view;
    }

    _createBrowseButton(locale) {
	    const t = locale.t;
	    const saveButton = new ButtonView( locale );

	    saveButton.set( {
		    label: t( 'Browse server' ),
		    tooltip: false,
		    withText: true,
		    type: 'submit',
		    class: 'ck-button-action ck-button-bold'
	    } );
	    var plone_dom_id = this.editor.config.get('plone_dom_id');
	    var filebrowserBrowserUrl = this.editor.config.get('filebrowserBrowserUrl') + '&CKEditorFuncNum=' + plone_dom_id;
	    saveButton.on('execute', () => {
	        window.open(
		    filebrowserBrowserUrl,
		    null,
		    'location=no,menubar=no,toolbar=no,dependent=yes,minimizable=no,modal=yes,alwaysRaised=yes,resizable=yes,scrollbars=yes'
		);
	    });
	    return saveButton;
    }

}

