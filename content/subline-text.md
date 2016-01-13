title: Setup Sublime Text3
Date: 2015-10-12 00:16:00
Modified: 2015-10-12 00:16:00
Category: development
Slug: sublime-text-3
Summary: Sublime Text3 メモ

# Sublime Text 3

- [Sublime Text 3](http://www.sublimetext.com/3)
- [Package Control](https://packagecontrol.io/installation)
- [SublimeLinter](https://packagecontrol.io/packages/SublimeLinter)
- [ConvertToUTF8](https://packagecontrol.io/packages/ConvertToUTF8)
- [JsFormat](https://packagecontrol.io/packages/JsFormat)
- [SublimeLinter-contrib-eslint_d](https://packagecontrol.io/packages/SublimeLinter-contrib-eslint_d)
- [Theme Soda](https://packagecontrol.io/packages/Theme%20-%20Soda)
- [Tomorrow Color Schemes](https://packagecontrol.io/packages/Tomorrow%20Color%20Schemes)

## Preferences.sublime-settings

**⌘,** で設定ファイルが開くので以下を入れとく

```
{
    "color_scheme": "Packages/User/SublimeLinter/Tomorrow-Night-Eighties (SL).tmTheme",
    "default_encoding": "UTF-8",
    "fallback_encoding": "UTF-8",
    "font_face": "Ricty Diminished",
    "font_size": 16,
    "highlight_line": true,
    "ignored_packages":
    [
        "Vintage"
    ],
    "show_encoding": true,
    "translate_tabs_to_spaces": true,
    "trim_trailing_white_space_on_save": true,
    "theme": "Soda Dark 3.sublime-theme",
    "soda_classic_tabs": true,
    "soda_folder_icons": true
}
```