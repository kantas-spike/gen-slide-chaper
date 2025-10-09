# gen-slide-chaper

.blendファイルの指定チャンネルから各ストリップの開始時間をチャプター情報として出力する

引数で指定する、スライドのチャプター番号とタイトルの対応を記載されたJSONファイルは、
[別ツール(marp2titles)](https://github.com/kantas-spike/my-marp-utils)により作成する。

## インストール

本リポジトリをチェックアウトしたディレクトリに移動後、以下を実行する。

```shell
uv tool install .
```

## 使い方

```shell
$ gen-slide-chapter --help
usage: gen-slide-chapter [-h] [--channel CHANNEL] [-t TITLES.json] -o OUTPUT_FILE [--force] BLEND_FILE

.blendファイルの指定チャンネルから各ストリップの開始時間をチャプター情報として出力する

positional arguments:
  BLEND_FILE            チャプター情報を取得する.blendファイル

options:
  -h, --help            show this help message and exit
  --channel CHANNEL     スライド画像が配置されているチャンネル番号. デフォルト: 3
  -t TITLES.json, --titles TITLES.json
                        チャプター番号とタイトルの対応を記載されたJSONファイル
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        チャプター情報の出力先ファイル
  --force               出力先ファイルが存在する場合に上書きする
```

## 更新履歴

### v0.1.0

- 初回リリース
