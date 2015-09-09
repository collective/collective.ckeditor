*** Settings ***

Library  collective.ckeditor.tests.keyword.TestKeywords

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/saucelabs.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  plone.app.robotframework.keywords.Debugging

Test Setup  Open SauceLabs test browser
Test Teardown  Run keywords  Report test status  Close all browsers

*** Test cases ***

Scenario: As an editor, I am using CKEditor
    Given a logged-in editor
    and a document
    When I edit the document
    Then CKEditor is used for the text field


*** Keywords *****************************************************************

# --- GIVEN ------------------------------------------------------------------

a logged-in editor
  Enable autologin as  Editor  Contributor

a document
  Create content  type=Document  id=document-to-edit  text=<p id="p1">paragraph1</p><p id="p2">paragraph2</p><p>paragraph3</p><p>paragraph4</p>

# --- WHEN -------------------------------------------------------------------
    
I edit the document
  Go to  ${PLONE_URL}/document-to-edit/edit

# --- THEN -------------------------------------------------------------------


CKEditor is used for the text field
  Page should contain element  css=#archetypes-fieldname-text #cke_text #cke_1_contents iframe

