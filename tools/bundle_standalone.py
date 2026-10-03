#!/usr/bin/env python3
"""Bundle a Godot 4 single-threaded web export into one self-contained HTML page."""

from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path


def as_js_chunks(data: bytes, chunk_size: int = 65536) -> str:
    encoded = base64.b64encode(data).decode("ascii")
    chunks = [encoded[i : i + chunk_size] for i in range(0, len(encoded), chunk_size)]
    return "[\n" + ",\n".join(json.dumps(chunk) for chunk in chunks) + "\n].join('')"


def only_match(directory: Path, pattern: str) -> Path:
    matches = sorted(directory.glob(pattern))
    if len(matches) != 1:
        raise SystemExit(f"Expected one {pattern} in {directory}, found {len(matches)}")
    return matches[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("export_dir", type=Path)
    parser.add_argument("output_html", type=Path)
    args = parser.parse_args()

    export_dir = args.export_dir
    pck = only_match(export_dir, "*.pck")
    wasm = only_match(export_dir, "*.wasm")
    loader = export_dir / f"{pck.stem}.js"
    if not loader.is_file():
        raise SystemExit(f"Missing Godot web loader: {loader}")

    loader_js = loader.read_text(encoding="utf-8").replace("</script", "<\\/script")
    wasm_chunks = as_js_chunks(wasm.read_bytes())
    pck_chunks = as_js_chunks(pck.read_bytes())

    page = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
  <meta name="theme-color" content="#182218">
  <title>Birb and Weave</title>
  <style>
    html, body { width: 100%; height: 100%; margin: 0; overflow: hidden; background: #182218; }
    body { display: flex; align-items: center; justify-content: center; }
    canvas { display: block; width: 100%; height: 100%; outline: none; }
    #status { position: fixed; inset: 0; display: grid; place-items: center; color: #fff;
      background: #182218; font: 16px system-ui, sans-serif; text-align: center; }
    #status.error { color: #ffd5d5; padding: 24px; }
  </style>
</head>
<body>
  <div id="status">Loading Birb and Weave…</div>
  <canvas id="canvas" tabindex="0"></canvas>
  <script>
@ENGINE_LOADER@
  </script>
  <script>
    const statusBox = document.getElementById('status');
    const wasmBase64 = @WASM_BASE64@;
    const pckBase64 = @PCK_BASE64@;
    function decodeBase64(text) {
      const binary = atob(text);
      const bytes = new Uint8Array(binary.length);
      for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
      return bytes;
    }
    const wasmUrl = URL.createObjectURL(new Blob([decodeBase64(wasmBase64)], { type: 'application/wasm' }));
    const pckBytes = decodeBase64(pckBase64);
    const engine = new Engine();
    engine.init(wasmUrl)
      .then(() => engine.preloadFile(pckBytes.buffer, 'index.pck'))
      .then(() => engine.start({
        args: ['--main-pack', 'index.pck'],
        canvas: document.getElementById('canvas'),
        canvasResizePolicy: 2
      }))
      .then(() => { statusBox.remove(); document.getElementById('canvas').focus(); })
      .catch((error) => {
        statusBox.classList.add('error');
        statusBox.textContent = 'The game could not start. Try opening it in a recent version of Chrome, Edge, or Firefox. ' + error;
        console.error(error);
      });
  </script>
</body>
</html>
'''
    page = page.replace("@ENGINE_LOADER@", loader_js)
    page = page.replace("@WASM_BASE64@", wasm_chunks)
    page = page.replace("@PCK_BASE64@", pck_chunks)

    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    args.output_html.write_text(page, encoding="utf-8")
    print(f"Created {args.output_html} ({args.output_html.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
