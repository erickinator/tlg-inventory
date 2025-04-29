[Setup]
AppName=TLG Inventory Tool
AppVersion=1.0.0
AppPublisher=The Marketing Systems Collective
DefaultDirName={pf}\TLG Inventory
DefaultGroupName=TLG Inventory
AllowNoIcons=yes
OutputDir=dist
OutputBaseFilename=TLG_Installer
SetupIconFile=dist\tlg.ico
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\TLG_Inventory.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\config.json"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "dist\logo.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\readme.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\readme.html"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\version.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\tlg.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\TLG Inventory Tool"; Filename: "{app}\TLG_Inventory.exe"; IconFilename: "{app}\tlg.ico"
Name: "{commondesktop}\TLG Inventory Tool"; Filename: "{app}\TLG_Inventory.exe"; Tasks: desktopicon; IconFilename: "{app}\tlg.ico"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"; Flags: checkedonce

[Run]
Filename: "{app}\TLG_Inventory.exe"; Description: "Launch TLG Inventory Tool"; Flags: nowait postinstall skipifsilent
Filename: "{app}\readme.html"; Description: "View Getting Started Guide"; Flags: shellexec postinstall skipifsilent
