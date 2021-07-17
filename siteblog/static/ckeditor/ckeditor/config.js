/**
 * @license Copyright (c) 2003-2020, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
    config['placeholder'] = 'О чем Вы хотите написать?';
    config.width = '100%';
    config.autoGrow_minHeight = 200;
    config.autoGrow_maxHeight = 400;
    autoGrow_bottomSpace: 50,
    config.autoGrow_onStartup = true;
};
