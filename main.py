PSD_PATH = r"" # 入力するPSDファイルパス
OUTPUT_DIR = r"" # 出力するディレクトリ
EXPORT_HIDDEN = True  # 非表示のレイヤーを出力するか

from psd_tools import PSDImage
from pathlib import Path
import os

def sanitize_filename(name):
    if not name:
        return "layer"
    invalid_chars = r'<>:"/\\|?*'
    for c in invalid_chars:
        name = name.replace(c, "_")
    return name.strip()

def unique_path(path):
    counter = 1
    new_path = path
    while new_path.exists():
        new_path = path.with_stem(f"{path.stem}_{counter}")
        counter += 1
    return new_path

def export_layer(layer, base_path):
    layer_name = sanitize_filename(layer.name)

    print(f"処理中: {layer_name} | group={layer.is_group()}")

    if not EXPORT_HIDDEN and not layer.is_visible():
        return

    if layer.is_group():
        group_path = base_path / layer_name
        group_path.mkdir(parents=True, exist_ok=True)

        for child in layer:
            export_layer(child, group_path)

    else:
        try:
            image = layer.composite()
        except Exception as e:
            print("composite失敗:", e)
            return

        if image:
            file_path = unique_path(base_path / f"{layer_name}.png")
            try:
                image.save(file_path)
                print("保存:", file_path)
            except Exception as e:
                print("保存失敗:", e)

def psd_to_png_layers():
    print("PSD存在確認:", os.path.exists(PSD_PATH))

    psd = PSDImage.open(PSD_PATH)

    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)

    print("出力先:", output_path.resolve())

    for layer in psd:
        export_layer(layer, output_path)

    print("完了")

if __name__ == "__main__":
    psd_to_png_layers()
