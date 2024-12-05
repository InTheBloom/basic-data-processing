# Basic Data Processing
基本的なプログラムの文法を学習したばかりの学習者に向けた練習問題とそのジャッジプログラム群です。
問題データを`/resources`に用意して、`/`で`builder.py`を実行すると`/docs/`にhtmlが出力されます。

## 特徴
- `/resources`を書き換えることでhtmlを生成することができます。テンプレートを変更すれば、問題はそのままにhtmlを変えることができます。
- 完全一致ジャッジをデフォルトでサポート。より複雑なジャッジも`judge.js`を用意することで対応できます。
- すべて静的ファイルとして生成されます。

## 使用方法
2024-12-06版
スクリプトの起動はカレントワーキングディレクトリを起点とします。以後、`/`は実行したディレクトリを指します。

### 用語の定義
- 成果物: 最終的に作られるファイルおよびディレクトリの集合です。
- 通常テンプレート: 成果物の中のhtmlのビルドに利用できるテンプレートです。jinja2を用いて処理されます。
- モジュールテンプレート: 通常テンプレート内で利用できるファイルです。C言語の`#include`とほぼ同じで、単に埋め込むことのみができます。

### 各ディレクトリの役割
- `/resources/root`: 成果物のディレクトリ構造を作るための起点です。
- `/resources/templates/`: 通常テンプレートの読み込み起点です。
- `/resources/templates/modules`: 「モジュール」テンプレートの読み込み起点です。
- `/docs/`: 成果物が出力されます。

### 使い方
1. `/resources/root`以下に作成したディレクトリ構造、配置したいファイルを作成します。
2. 成果物に動的にビルドされるhtmlを含めたい場合、`index.html`を生成したいディレクトリに`config.json`を作成します。`config.json`の構造については後の章を参照してください。
3. `/`で`builder.py`を起動すると、`/docs`に成果物が生成されます。

### 動的にビルドされるhtmlの仕様
一つの`config.json`ファイルが一つの`index.html`に対応します。
`config.json`は次の要求を満たす必要があります。

- すべての`config.json`で共通
| `fileType` | `"problem"|"meta"` |
| `templateFileName` | `str` |
| `title`| `str` |

- `fileType`が`problem`
| `problemTitle` | `str` |
| `problemId` | `str`(uuidなどを想定。衝突判定はしていないです。) |
| `problemStatement` | `str` |
| `inputDescription` | `str` |
| `inputFilePath` | `str` |
| `outputDescription` | `str` |
| `outputFilePath` | `str` |
| `moreInformation` | `str` |
| `judgeFilePath` | `str` |
| `examples` | `list`(listの中身のバリデーションをしてません。現状`{"input": str, "output": str, "description": str}`で運用しています。) |

- `fileType`が`meta`
| なし |

必須属性以外はユーザが自由に定義可能です。
これらの情報を次の形でパックした辞書`context`をjinja2のテンプレート構築時に使用します。

`other`、`problem`、`meta`、`here`、`baseURL`、`module`のフィールドを持つ。
| `here` | `config.json`のある`/resources/root`からの相対ファイルパス |
| `baseURL` | 末尾のセパレータを含まないデプロイ先のディレクトリルート(https://aaa/bbbなど。`builder.py`で定義されています。) |
| `other` | `context[other][(パス(ファイル名含む))]` = `{path: (パス(ファイル名含む)), value: (バイナリオブジェクト)}` |
| `problem` | `context[problem][(パス)]` = `(config.jsonで定義したオブジェクト) + {path: (パス)}` |
| `meta` | `context[meta][(パス)]` = `(config.fsonで定義したオブジェクト) + {path: (パス)}` |
| `module` | `context[module][(モジュールルートからの相対パス)]` = `モジュール文字列` |

ユーザは、`resources/templates`の通常テンプレートのなかで`context`変数を使用することができます。
例えば、`problemTitle`を取得するとき、`{{ problem[here][problemTitle] }}`とします。

# License
MIT
