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

${SELENIUM_IMPLICIT_WAIT}  1
${WAIT_MORE}  5

*** Test cases ***

Scenario: As an editor, I am using CKEditor
    Given a logged-in editor
    and a document
    When I edit the document
    Then CKEditor is used for the text field
    Cancel edit

Scenario: Does not display uncorrect spelling
    Given a logged-in editor
    and a document
    When I edit the document
    Then CKEditor does not show uncorrect spelling
    Cancel edit

Scenario: Uses default image editor
    Given a logged-in editor
    and a document
    When I edit the document
    Then CKEditor uses default image editor
    Click element  css=.cke_dialog_ui_button_cancel
    Cancel edit

Scenario: Use bold button
    Given a logged-in editor
    and a document
    When I edit the document
    and select some text
    and click the bold button
    and save the document
    Then the selected text is bold

Scenario: Use italic button
    Given a logged-in editor
    and a document
    When I edit the document
    and select some text
    and click the italic button
    and save the document
    Then the selected text is italic

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

select some text
  Select Frame  css=iframe.cke_wysiwyg_frame
  Page Should Contain Element  css=#p1
  Mouse Select  css=#p1  20  2
  Unselect Frame

click the bold button
  Set Selenium implicit wait  ${WAIT_MORE}
  Page Should contain Element  css=span.cke_button__bold_icon 
  Click Element  css=span.cke_button__bold_icon 
  Select Frame  css=iframe.cke_wysiwyg_frame
  Page Should Contain Element  css=#p1 strong
  Set Selenium implicit wait  ${SELENIUM_IMPLICIT_WAIT}

click the italic button
  Set Selenium implicit wait  ${WAIT_MORE}
  Page Should contain Element  css=span.cke_button__italic_icon 
  Click Element  css=span.cke_button__italic_icon 
  Select Frame  css=iframe.cke_wysiwyg_frame
  Page Should Contain Element  css=#p1 em
  Set Selenium implicit wait  ${SELENIUM_IMPLICIT_WAIT}

save the document
  Unselect Frame
  Sleep  ${WAIT_MORE}  Wait for the modification of the content
  Click Button  Save

# --- THEN -------------------------------------------------------------------

CKEditor is used for the text field
  Page should contain element  css=#archetypes-fieldname-text #cke_text #cke_1_contents iframe

the selected text is bold
  Page Should Contain Element  css=#p1 strong

the selected text is italic
  Page Should Contain Element  css=#p1 em

CKEditor does not show uncorrect spelling
  Select Frame  css=iframe.cke_wysiwyg_frame
  Sleep  1s  # to give time to scayt
  Page Should Not Contain Element  css=#p1 .scayt-misspell-word
    
CKEditor uses default image editor
  Page Should Not Contain Element  css=.cke_editor_text_dialog .cke_dialog_title
  Page Should Contain Element  css=span.cke_button__image_icon 
  Click Element  css=span.cke_button__image_icon
  Wait Until Element Is Visible  css=.cke_editor_text_dialog .cke_dialog_title
  Page Should Contain Element  css=.cke_editor_text_dialog .cke_dialog_title
  Element should contain  css=.cke_editor_text_dialog .cke_dialog_title  Image Properties
  Element should contain  css=.cke_editor_text_dialog  Preview

Cancel edit
  Unselect frame
  Click element  name=form.button.cancel
