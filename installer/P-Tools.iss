#define AppVersion "1.0.0"

[Setup]
AppId={{8B7A4B4D-3AAE-4E05-9D28-7A8E1A2F7B0B}
AppName=P-Tools
AppVersion={#AppVersion}
AppPublisher=P-Tools
DefaultDirName={autopf}\P-Tools
DefaultGroupName=P-Tools
UninstallDisplayIcon={app}\P-Tools.exe
OutputDir=..\dist
OutputBaseFilename=P-Tools-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
LicenseFile=..\LICENSE

[Files]
Source: "..\dist\P-Tools.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\P-Tools"; Filename: "{app}\P-Tools.exe"
Name: "{autodesktop}\P-Tools"; Filename: "{app}\P-Tools.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\P-Tools.exe"; Description: "Launch P-Tools"; Flags: nowait postinstall skipifsilent
