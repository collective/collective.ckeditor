*** Settings ***

Library  collective.ckeditor.tests.keyword.TestKeywords

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/saucelabs.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  plone.app.robotframework.keywords.Debugging

Test Setup  Open SauceLabs test browser
Test Teardown  Run keywords  Report test status  Close all browsers

*** Variables ***

${SELENIUM_IMPLICIT_WAIT}  2

*** Test cases ***

Scenario: Uses image2 editor
    Given a logged-in editor
    and a document
    When I edit the document
    Then CKEditor uses image2 editor
    Click element  css=.cke_dialog_ui_button_cancel
    Cancel edit

*** Keywords *****************************************************************

# --- GIVEN ------------------------------------------------------------------

a logged-in editor
  Enable autologin as  Editor  Contributor

a document
  Create content  type=Document  id=document-to-edit  title=Document to edit  text=<p id="p1">paragraph1</p><p id="p2">paragraph2</p><p>paragraph3</p><p>paragraph4</p>
  Go to  ${PLONE_URL}/document-to-edit
  Page Should Contain  paragraph1
  Page Should Contain  paragraph4
  Page Should Contain Element  css=#p1
  Page Should Not Contain Element  css=#p1 strong

# --- WHEN -------------------------------------------------------------------
    
I edit the document
  Go to  ${PLONE_URL}/document-to-edit/edit

# --- THEN -------------------------------------------------------------------

CKEditor uses image2 editor
  Page Should Not Contain Element  css=.cke_editor_text_dialog .cke_dialog_title
  Page Should Contain Element  css=span.cke_button__image_icon 
  Click Element  css=span.cke_button__image_icon
  Wait Until Element Is Visible  css=.cke_editor_text_dialog .cke_dialog_title
  Page Should Contain Element  css=.cke_editor_text_dialog .cke_dialog_title
  Element should contain  css=.cke_editor_text_dialog .cke_dialog_title  Image Properties
  Element should contain  css=.cke_editor_text_dialog  Captioned image

Cancel edit
  Unselect frame
  Click element  name=form.button.cancel
