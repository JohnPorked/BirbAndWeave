# Birb and Weave

This is the Godot project for **Birb and Weave**, configured to publish as one self-contained HTML file through GitHub Pages.

## Controls

- Move: arrow keys
- Aim: move the mouse
- Fire: left mouse button
- Dash: hold a movement direction and press Shift

## Publish it on GitHub Pages

1. Extract the ZIP. Keep its folders in place; `project.godot` should be at the top level.
2. Copy the extracted contents into the top level of your GitHub repository.
3. Commit and push the files to `main` or `master`. For a different branch name, change the branch list in `.github/workflows/deploy.yml`.
4. In the repository on GitHub, open **Settings → Pages** and set **Build and deployment → Source** to **GitHub Actions**.
5. Open the **Actions** tab. The “Build and publish Birb and Weave” workflow exports the project with Godot 4.4.1, bundles the engine, game data, and code into a single `index.html`, and publishes that page. When deployment completes, use the URL shown in the workflow details.

The published site is a single HTML file. Godot’s normal Web export has separate files for its runtime and game data; the workflow embeds those into the page automatically. The standalone HTML is large because it includes the WebAssembly engine. Godot Web requires a modern browser with WebAssembly and WebGL 2 support; use Chrome, Edge, or Firefox.

## Open the project in Godot

Open `project.godot` in Godot 4.4.1 or newer. The project uses the GL Compatibility renderer for WebGL support. The exported standalone HTML is created by the GitHub Actions workflow after the project is pushed.

## Windows build

The supplied `windows.zip` was Godot editor cache data, not a finished Windows game. To make a Windows build, open the project in Godot, install its matching export templates, and export with the **Windows Desktop** preset. Keep the generated `.exe`, its `_Data` folder, and companion files together; zip the whole output folder before sharing it.
