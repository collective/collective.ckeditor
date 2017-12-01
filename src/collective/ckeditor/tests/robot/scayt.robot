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

Scenario: As an editor, CKEditor displays uncorrect spelling
    Given a logged-in editor
    and a document
    When I edit the document
    Then CKEditor shows uncorrect spelling
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

CKEditor shows uncorrect spelling
  Wait Until Page Contains Element  css=iframe.cke_wysiwyg_frame  2s
  Select Frame  css=iframe.cke_wysiwyg_frame
  Wait Until Page Contains Element  css=#p1 .scayt-misspell-word  10s

Cancel edit
  Unselect frame
  Click element  name=form.button.cancel
