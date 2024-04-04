# Description
A productivity-enhancing tool that combines a straightforward Pomodoro timer with a Firefox extension designed to block distracting websites during focused work sessions.

# Load the FireFox extension
- Open Firefox and navigate to about:debugging#/runtime/this-firefox.
- Click on "Load Temporary Add-on".
- Select any file in your extension's directory (e.g., manifest.json).

# Build
### windows
```bash
pyinstaller --onefile --noconsole --icon=assets/pomodoro.ico pomodor.py
```
### linux
- **Create the binary**:
```bash
pyinstaller --onefile --noconsole --icon=assets/pomodoro.ico pomodor.py
```
make it executable:
```bash
chmod +x dist/pomodoro
```
run it:
```bash
./pomodoro
```
---

- **Convert the binary to an AppImage**: 
```rust
MyApp.AppDir/ 
	├── AppRun # ->  rename your_binary to AppRun
	├── myapp.desktop 
	└── myapp.png
```
```bash
mkdir Pomodoro.AppDir
cp dist/pomodoro Pomodoro.AppDir/AppRun
cp assets/pomodoro.png Pomodoro.AppDir/
```
- **Create myapp.desktop**: `myapp.desktop` should contain:
 ```ini
[Desktop Entry]
Name=Pomodoro
Exec=AppRun
Icon=pomodoro
Type=Application
Categories=Utility;
```

- **Download AppImageTool**: Download the `appimagetool` from the [AppImage GitHub releases page](https://github.com/AppImage/AppImageKit/releases) and make it executable:
```bash
chmod +x appimagetool-x86_64.AppImage
```
- **Create the AppImage**: Use the `appimagetool` to convert the AppDir into an AppImage:
```bash
./appimagetool-x86_64.AppImage Pomodoro.AppDir
```
