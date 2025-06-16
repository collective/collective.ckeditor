// plonelink/plonelink.js
import PloneLinkUI from './plonelinkui.js';
import { Plugin } from 'ckeditor5';

export default class PloneLink extends Plugin {
    static get requires() {
        return [ PloneLinkUI ];
    }
}

