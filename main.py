PSD_PATH = "Input.psd" # インプットするPSDファイルのパス
OUTPUT_DIR = "output" # アウトプットするディレクトリ 
EXPORT_HIDDEN = True # 非表示レイヤーを書き出す

from psd_tools import PSDImage
from pathlib import Path

def sanitize_filename(name):
    invalid_chars = r'<>:"/\\|?*'
    for c in invalid_chars:
        name = name.replace(c, "_")
    return name.strip()

def export_layer(layer, base_path):
    if layer.is_group():
        if not layer.is_visible():
            return

        layer_name = sanitize_filename(layer.name)
        group_path = base_path / layer_name
        group_path.mkdir(parents=True, exist_ok=True)

        for child in layer:
            export_layer(child, group_path)

    else:
        if not EXPORT_HIDDEN and not layer.is_visible():
            return

        layer_name = sanitize_filename(layer.name)

        image = layer.composite()
        if image:
            file_path = base_path / f"{layer_name}.png"
            image.save(file_path)

def psd_to_png_layers():
    psd = PSDImage.open(PSD_PATH)
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)

    for layer in psd:
        export_layer(layer, output_path)

if __name__ == "__main__":
    psd_to_png_layers()
