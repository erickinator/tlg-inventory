; Script generated for The Light Garden Inventory Tool

[Setup]
AppName=The Light Garden Inventory Tool
AppVersion=1.0.4
DefaultDirName={pf}\The Light Garden Inventory Tool
DefaultGroupName=The Light Garden Inventory Tool
OutputDir=dist
OutputBaseFilename=TLG_Installer
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
DisableWelcomePage=no

[Files]
Source: "dist\TLG_Inventory.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\logo.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\config.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\readme.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\readme.html"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\version.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\tlg.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\TLG Inventory Tool"; Filename: "{app}\TLG_Inventory.exe"; IconFilename: "{app}\tlg.ico"
Name: "{commondesktop}\TLG Inventory Tool"; Filename: "{app}\TLG_Inventory.exe"; IconFilename: "{app}\tlg.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\TLG_Inventory.exe"; Description: "Launch the Inventory Tool"; Flags: nowait postinstall skipifsilent

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"
