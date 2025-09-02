[Setup]
AppName=GoogleSuiteOpener
AppVersion=1.0
DefaultDirName={autopf}\GoogleSuiteOpener
DefaultGroupName=GoogleSuiteOpener
OutputBaseFilename=GoogleSuiteOpenerInstaller
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest

[Files]
Source: "googlesuiteopener.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "rclone.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\GoogleSuiteOpener"; Filename: "{app}\googlesuiteopener.exe"

[Registry]
; Context menu entry (installed only if user selects addcontext)
Root: HKCU; Subkey: "Software\Classes\*\shell\GoogleSuiteOpener"; ValueType: string; ValueData: "Open with GoogleSuiteOpener"; Flags: uninsdeletekey; Check: AddContext
Root: HKCU; Subkey: "Software\Classes\*\shell\GoogleSuiteOpener\command"; ValueType: string; ValueData: """{app}\googlesuiteopener.exe"" ""%1"""; Flags: uninsdeletevalue; Check: AddContext

; PATH update (installed only if user selects addpath)
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{app};{olddata}"; Flags: preservestringtype; Check: AddPath

[Tasks]
Name: "addcontext"; Description: "Add right-click context menu entry"; GroupDescription: "Options:"; Flags: checkedonce
Name: "addpath"; Description: "Add GoogleSuiteOpener to PATH (requires logoff/reboot)"; GroupDescription: "Options:"; Flags: unchecked

[Code]
function AddContext: Boolean;
begin
  Result := WizardIsTaskSelected('addcontext');
end;

function AddPath: Boolean;
begin
  Result := WizardIsTaskSelected('addpath');
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if (CurStep = ssPostInstall) and AddPath then
  begin
    MsgBox('Reminder: You enabled PATH integration. A log off or reboot is required for Windows to recognize the change.',
      mbInformation, MB_OK);
  end;
end;
