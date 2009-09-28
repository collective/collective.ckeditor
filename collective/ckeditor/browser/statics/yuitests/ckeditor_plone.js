// yui tests for ckeditor_plone.js

var oTestCase = new YAHOO.tool.TestCase({ 
     
        name: "TestCase ckeditor_plone",          
         
        setUp : function () { 
        }, 
     
        tearDown : function () { 

        }, 
 
        testCKeditorPloneGlobalConfig: function () { 
            // test Content Area Css
            ContentAreaCss = CKEDITOR.instances.text.config.contentsCss;
            YAHOO.util.Assert.areEqual(portal_url + '/base.css', ContentAreaCss, "Content Area Css should be '" + portal_url + "/base.css'"); 
        },
           
        testCKeditorPloneInstanceConfig: function () { 
            // test File Browser Url
            filebrowserBrowseUrl = CKEDITOR.instances.text.config.filebrowserBrowseUrl;
            YAHOO.util.Assert.areEqual(portal_url + "/@@plone_finder", filebrowserBrowseUrl, "File Browser Url should be '" + portal_url + "/@@plone_finder'"); 
        }          
    }); 
    

// Add the tests
YAHOO.tool.TestRunner.add(oTestCase);

// Important : launch the test after all DOM elements are loaded
jQuery(window).load( function(){
    //launch the test logger instance for displaying tests results
    var oLogger = new YAHOO.tool.TestLogger();  
    //run all tests
    YAHOO.tool.TestRunner.run();
    });
   