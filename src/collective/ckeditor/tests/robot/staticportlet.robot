*** Settings ***

Library  collective.ckeditor.tests.keyword.TestKeywords

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  plone.app.robotframework.keywords.Debugging

Test Setup  Open test browser and set window size
Test Teardown  Run keywords  Close all browsers

*** Variables ***

${SELENIUM_IMPLICIT_WAIT}  1
${WAIT_MORE}  3
${PORTLET_HEADER}  My static portlet

*** Test cases ***

Scenario: As a site administrator, I am using CKEditor in static portlet
    Given a logged-in site administrator
    When I add a static portlet
    Then CKEditor is used for the text field
    Cancel add

Scenario: As a site administrator, I can save static portlet
    Given a logged-in site administrator
    When I add a static portlet
    and modify its fields
    Then I can save the portlet

*** Keywords *****************************************************************

# --- GIVEN ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Editor  Contributor  Site Administrator

# --- WHEN -------------------------------------------------------------------

I add a static portlet
  Go to  ${PLONE_URL}/@@topbar-manage-portlets/plone.rightcolumn
  Select From List By Value  css=select.add-portlet  /++contextportlets++plone.rightcolumn/+/plone.portlet.static.Static

modify its fields
  Input text  name=form.widgets.header  ${PORTLET_HEADER}
  Select Frame  css=iframe.cke_wysiwyg_frame
  Press keys  css=#content p  Roosevelt
  Page should contain  Roosevelt
  Set focus to element  name=form.widgets.footer
  Page should not contain  There were some errors

# --- THEN -------------------------------------------------------------------

CKEditor is used for the text field
  Wait until page contains element  css=#cke_1_contents
  Page should contain element  css=#formfield-form-widgets-text #cke_1_contents iframe

I can save the portlet
  Unselect frame
  Execute javascript  document.querySelector('.pattern-modal-buttons').scrollIntoView(true);
  Backport Wait For Then Click element  css=.pattern-modal-buttons [name="form.buttons.add"]
  Page Should Contain Link  ${PORTLET_HEADER}

Cancel add
  Unselect frame
  Execute javascript  document.querySelector('.pattern-modal-buttons').scrollIntoView(true);
  Backport Wait For Then Click element  css=.pattern-modal-buttons [name="form.buttons.cancel_add"]

Open test browser and set window size
  Open test browser
  Set window size  2000  1200

Backport Wait For Element
    [Documentation]  Can contain css=, jquery=, or any other element selector.
    ...              Element must match exactly one time.
    [Arguments]  ${element}
    Wait Until Page Contains Element  ${element}
    Set Focus To Element  ${element}
    Wait Until Element Is Visible  ${element}
    Sleep  0.1
    ${count} =  Get Element Count  ${element}
    Should Be Equal as Numbers  ${count}  1

Backport Wait For Then Click Element
    [Documentation]  Can contain css=, jquery=, or any other element selector.
    ...              Element must match exactly one time.
    [Arguments]  ${element}
    Backport Wait For Element  ${element}
    Click Element  ${element}
