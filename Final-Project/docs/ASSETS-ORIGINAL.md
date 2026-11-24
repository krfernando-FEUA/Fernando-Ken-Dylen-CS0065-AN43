# Visual asset provenance

Retrieved and verified on **25 October 2026**. All files are local and work offline.

## Character illustrations

The character artwork belongs to **Sanrio**. LoopGuard is an unofficial educational prototype, with fictional shops, exchange rates, crafting recipes and mechanics. It is not an official Sanrio game or product. Public availability of these source files is not an assertion of an open-content redistribution license.

The following transparent PNG illustrations come from Sanrio's official Japanese character pages. Their transparent bounds were cropped and each image was centered on a 512 × 512 transparent canvas without changing the illustration's colors. For Hello Kitty, the separate apple and milk props were excluded by selecting the connected mascot silhouette.

| Local file | Official character page | Original image |
| --- | --- | --- |
| `assets/hello-kitty.png` | [Hello Kitty](https://www.sanrio.co.jp/characters/hellokitty/) | [Source PNG](https://www.sanrio.co.jp/wp-content/uploads/2022/06/mv-hellokitty.png) |
| `assets/my-melody.png` | [My Melody](https://www.sanrio.co.jp/characters/mymelody/) | [Source PNG](https://www.sanrio.co.jp/wp-content/uploads/2022/06/list-mymelody.png) |
| `assets/kuromi.png` | [Kuromi](https://www.sanrio.co.jp/characters/kuromi/) | [Source PNG](https://www.sanrio.co.jp/wp-content/uploads/2022/06/list-kuromi.png) |
| `assets/cinnamoroll.png` | [Cinnamoroll](https://www.sanrio.co.jp/characters/cinnamon/) | [Source PNG](https://www.sanrio.co.jp/wp-content/uploads/2022/06/mv-cinnamon.png) |
| `assets/pompompurin.png` | [Pompompurin](https://www.sanrio.co.jp/characters/pompompurin/) | [Source PNG](https://www.sanrio.co.jp/wp-content/uploads/2022/06/list-pompompurin.png) |
| `assets/keroppi.png` | [Keroppi](https://www.sanrio.co.jp/characters/keroppi/) | [Source PNG](https://www.sanrio.co.jp/wp-content/uploads/2022/06/mv-keroppi.png) |
| `assets/little-twin-stars.png` | [Little Twin Stars](https://www.sanrio.co.jp/characters/kikilala/) | [Source PNG](https://www.sanrio.co.jp/wp-content/uploads/2022/06/mv-kikilala.png) |

The six matching character-name `.svg` files are official compact navigation portraits, retained as optional alternatives for small avatars. They were discovered on Sanrio's [Character Goodies page](https://www.sanrio.com/pages/character-goodies) and downloaded unchanged from its Shopify CDN:

- [My Melody SVG](https://cdn.shopify.com/s/files/1/0416/8083/0620/files/Navigation_ICON_11062020_MyMelody.svg?v=1604696827)
- [Kuromi SVG](https://cdn.shopify.com/s/files/1/0416/8083/0620/files/Navigation_ICON_11062020_Kuromi.svg?v=1604696827)
- [Cinnamoroll SVG](https://cdn.shopify.com/s/files/1/0416/8083/0620/files/Navigation_ICON_11062020_Cinnamoroll.svg?v=1604696827)
- [Pompompurin SVG](https://cdn.shopify.com/s/files/1/0416/8083/0620/files/Navigation_ICON_11062020_Pompompurin.svg?v=1614311071)
- [Keroppi SVG](https://cdn.shopify.com/s/files/1/0416/8083/0620/files/Navigation_ICON_11062020_Keroppi.svg?v=1604696827)
- [Little Twin Stars SVG](https://cdn.shopify.com/s/files/1/0416/8083/0620/files/Navigation_ICON_11062020_LittleTwinStars.svg?v=1604696827)

## Original item icons

These simple 64 × 64 SVG illustrations were authored specifically for the prototype. They are original decorative item representations, not official Sanrio game assets. Each includes a descriptive SVG title and has no scripts or external references.

| File | Representation |
| --- | --- |
| `assets/coin.svg` | A gold friendship coin with a heart embossing |
| `assets/ribbon.svg` | A rose-colored bow and ribbon tails |
| `assets/gift-box.svg` | A lavender gift box with a pink ribbon |
| `assets/stamp.svg` | A perforated mint friendship stamp |
| `assets/star-charm.svg` | A lilac and gold star charm with a hanging ring |
| `assets/pudding.svg` | A caramel pudding on a cream saucer |
| `assets/coffee-bean.svg` | A warm brown coffee bean with a cream center seam |
| `assets/latte.svg` | A pale blue latte cup with a heart in its foam and a gold star |

`assets/manifest.json` provides machine-readable filenames, dimensions, descriptions and source URLs. The seven PNGs were checked for correct dimensions and alpha transparency. All fourteen SVGs were XML-parsed and checked for script tags and external asset references. A contact sheet was visually inspected for complete silhouettes, clean transparent edges, and consistent padding.


## Offline typeface

**Nunito** is bundled in `assets/nunito-latin-variable.woff2` (39 KB). This is the Latin subset, normal style, with a variable weight range of 200–1000. The weight range and CDN URL were verified using the [official Google Fonts stylesheet](https://fonts.googleapis.com/css2?family=Nunito:wght@200..1000&display=swap). The [original WOFF2 file](https://fonts.gstatic.com/s/nunito/v32/XRXV3I6Li01BKofINeaB.woff2) is unchanged. `assets/nunito.css` provides the local `@font-face` declaration; the font needs no external requests at runtime.

Copyright 2014 The Nunito Project Authors. The font is distributed under **SIL Open Font License 1.1**, included in full as `assets/Nunito-OFL.txt`, downloaded from [the official Google Fonts repository](https://github.com/google/fonts/blob/main/ofl/nunito/OFL.txt). Include this license when redistributing the font. Characters outside the included Latin subset use the application's system-font fallback.

`FontFace.load()` was also checked in an isolated Chromium browser: the bundled WOFF2 decoded successfully and reported the 200–1000 variable weight range.
