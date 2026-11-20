"""Rebuild the Chinese-v0.2 Unity bundle from the published patch and TextAsset/."""

import argparse
import hashlib
from pathlib import Path
from struct import pack, unpack_from

import UnityPy

BASE_SHA256 = "30b4e5d171a1446bdff6b17d27cc6bcf251ea4324e28e7e4c740a6b171c5c2bb"

# Serialized font ID and first atlas array offset.
# These locations apply only to the exact bundle identified by BASE_SHA256.
DYNAMIC_FONTS = {
    "sharedassets1.assets": ((57, 10000), (58, 22832), (59, 18340)),
    "sharedassets14.assets": ((283, 13356),),
    "sharedassets25.assets": ((267, 13436),),
    "sharedassets28.assets": ((304, 5748), (305, 12460)),
    "resources.assets": (
        (120, 4004), (121, 3492), (122, 2948), (123, 3620),
        (124, 3684), (127, 4800), (132, 2596),
    ),
}


def update_fonts(files):
    for file_name, fonts in DYNAMIC_FONTS.items():
        asset = files[file_name]
        for font_id, atlas_offset in fonts:
            font = asset.objects[font_id]
            data = font.get_raw_data()
            count, file_id, texture_id, index, flags = unpack_from("<iiqii", data, atlas_offset)
            if (count, file_id, index, flags) != (1, 0, 0, 0):
                raise ValueError(f"Unexpected atlas layout: {file_name}:{font_id}")

            texture = asset.objects[texture_id].parse_as_object()
            if not texture.m_Name.endswith((" SDF Atlas", " SDF - Fallback Atlas")):
                raise ValueError(f"Unexpected atlas texture: {texture.m_Name}")
            if not texture.m_IsReadable:
                texture.m_IsReadable = True
                texture.save()

            # The first byte after m_AtlasTextureIndex is m_IsMultiAtlasTexturesEnabled.
            flags_offset = atlas_offset + 20
            font.set_raw_data(data[:flags_offset] + b"\x01" + data[flags_offset + 1:])

    # Register the embedded dynamic Xiaolai fallback in TMP Settings. This also
    # serves scene text elements that still use a static, non-CJK primary font.
    settings = files["resources.assets"].objects[131]
    data = settings.get_raw_data()
    fallback_offset = 152
    if data[fallback_offset:fallback_offset + 8] != pack("<ii", 0, 1):
        raise ValueError("Unexpected TMP Settings fallback table")
    settings.set_raw_data(
        data[:fallback_offset] + pack("<iiq", 1, 0, 127) + data[fallback_offset + 4:]
    )


def update_text(objects, text_dir):
    translations = {p.stem: p for p in text_dir.glob("*.txt")}
    if not translations:
        raise ValueError(f"No translations in {text_dir}")

    updated = set()
    for obj in objects:
        if obj.type.name != "TextAsset":
            continue
        text = obj.parse_as_object()
        path = translations.get(text.m_Name)
        if path is None:
            continue
        if text.m_Name in updated:
            raise ValueError(f"Multiple Unity TextAssets named {text.m_Name}")
        translation = path.read_bytes()
        text.m_Script = translation.decode("utf-8")
        text.save()
        updated.add(text.m_Name)

    missing = translations.keys() - updated
    if missing:
        raise ValueError("No matching Unity TextAsset for " + ", ".join(sorted(missing)))
    return len(updated)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="data.unity3d extracted from Chinese-v0.2")
    parser.add_argument("output", type=Path, help="path for the rebuilt bundle")
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output already exists")
    with args.source.open("rb") as source:
        if hashlib.file_digest(source, "sha256").hexdigest() != BASE_SHA256:
            parser.error("source does not match the published Chinese-v0.2 bundle")

    env = UnityPy.load(str(args.source))
    objects = env.objects
    files = {obj.assets_file.name: obj.assets_file for obj in objects}
    update_fonts(files)
    count = update_text(objects, Path(__file__).resolve().parents[1] / "TextAsset")
    bundle = next(iter(env.files.values()))
    data = bundle.save(packer="lz4")
    with args.output.open("xb") as output:
        output.write(data)
    print(f"Wrote {args.output} with {count} TextAssets and updated font settings.")


if __name__ == "__main__":
    main()
