"""
Backrooms Navigation System - Fandom JP
Database Update Orchestrator

Fandom JP の一覧HTMLから、データベース・検索用Level Listまでを
一括更新する。

[1] 全更新
    一覧HTMLを再取得
    ↓
    一覧HTML解析
    ↓
    ページ分類
    ↓
    翻訳一覧解析
    ↓
    翻訳記事分類
    ↓
    Master Database統合
    ↓
    Level List生成

[2] HTMLを再取得せずDBだけ再構築
    現在の index_html/ を使用
    ↓
    一覧HTML解析
    ↓
    ページ分類
    ↓
    翻訳一覧解析
    ↓
    翻訳記事分類
    ↓
    Master Database統合
    ↓
    Level List生成

[0] 終了

実行:
    python modules/update_database.py
"""

import os
import sys
import time
import traceback


# =============================================================================
# 基本パス (modules/ の親ディレクトリ = プロジェクトルートを取得)
# =============================================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODULES_DIR = os.path.join(
    BASE_DIR,
    "modules"
)

INDEX_HTML_DIR = os.path.join(
    BASE_DIR,
    "index_html"
)

PARSED_INDEX_DIR = os.path.join(
    BASE_DIR,
    "parsed_index"
)

LEVEL_LIST_DIR = os.path.join(
    BASE_DIR,
    "level_lists"
)


# =============================================================================
# modules を import path に追加
# =============================================================================

if MODULES_DIR not in sys.path:

    sys.path.insert(
        0,
        MODULES_DIR
    )


# =============================================================================
# モジュール読み込み
# =============================================================================

try:

    import index_collector
    import index_parser
    import classify_pages
    import translation_parser
    import translation_classifier
    import merge_databases
    import level_list_generator

except Exception as e:

    print()
    print("=" * 80)
    print(
        "【エラー】モジュールの読み込みに失敗しました。"
    )
    print("=" * 80)

    print()
    print(
        f"エラー種類: {type(e).__name__}"
    )

    print(
        f"エラー内容: {e}"
    )

    print()
    traceback.print_exc()

    raise e


# =============================================================================
# ファイル確認
# =============================================================================

def file_exists(path):
    """
    ファイルが存在するか確認する。
    """

    return os.path.isfile(
        path
    )


def directory_exists(path):
    """
    フォルダが存在するか確認する。
    """

    return os.path.isdir(
        path
    )


# =============================================================================
# index_html確認
# =============================================================================

def check_index_html():
    """
    DB再構築モードで必要な一覧HTMLが存在するか確認する。
    """

    required_files = [
        "hierarchy.html",
        "translation.html",
        "normal_eta.html",
        "anomalous.html",
        "sublevel.html",
    ]

    missing = []

    if not directory_exists(
        INDEX_HTML_DIR
    ):

        missing = required_files

    else:

        for file_name in required_files:

            file_path = os.path.join(
                INDEX_HTML_DIR,
                file_name
            )

            if not file_exists(
                file_path
            ):

                missing.append(
                    file_name
                )

    if not missing:

        return True

    print()
    print("=" * 80)

    print(
        "【エラー】必要な一覧HTMLがありません。"
    )

    print("=" * 80)

    print()

    print(
        "確認対象フォルダ:"
    )

    print(
        f"  {INDEX_HTML_DIR}"
    )

    print()

    print(
        "不足しているファイル:"
    )

    for file_name in missing:

        print(
            f"  - {file_name}"
        )

    print()

    print(
        "[1] 全更新を選択すると一覧HTMLを取得できます。"
    )

    return False


# =============================================================================
# DB状態表示
# =============================================================================

def show_database_status():
    """
    parsed_index内の主要ファイルを表示する。
    """

    print()
    print(
        "【生成済みDB】"
    )

    print()

    files = [
        "all_links.csv",
        "pages_database.csv",
        "pages_database_classified.csv",
        "translation_database.csv",
        "translation_database_classified.csv",
        "pages_master.csv",
    ]

    found = False

    for file_name in files:

        file_path = os.path.join(
            PARSED_INDEX_DIR,
            file_name
        )

        if os.path.isfile(
            file_path
        ):

            found = True

            try:

                size = os.path.getsize(
                    file_path
                )

                print(
                    f"  ✓ {file_name} "
                    f"({size:,} bytes)"
                )

            except OSError:

                print(
                    f"  ✓ {file_name}"
                )

    if not found:

        print(
            "  生成済みDBはありません。"
        )


# =============================================================================
# ステップ実行
# =============================================================================

def run_step(
    number,
    name,
    function
):
    """
    1つの処理を実行する。

    Returns
    -------
    bool
        成功ならTrue、失敗ならFalse
    """

    print()
    print("=" * 80)

    print(
        f"[{number}] {name}"
    )

    print("=" * 80)

    start_time = time.time()

    try:

        result = function()

        elapsed = (
            time.time()
            - start_time
        )

        if result is False:

            print()
            print(
                f"【FAILED】[{number}] {name}"
            )

            print(
                f"処理時間: {elapsed:.1f} 秒"
            )

            return False

        print()
        print(
            f"【SUCCESS】[{number}] {name}"
        )

        print(
            f"処理時間: {elapsed:.1f} 秒"
        )

        print(
            "=" * 80
        )

        return True

    except Exception as e:

        elapsed = (
            time.time()
            - start_time
        )

        print()
        print("=" * 80)

        print(
            f"【FAILED】[{number}] {name}"
        )

        print(
            f"処理時間: {elapsed:.1f} 秒"
        )

        print("=" * 80)

        print()

        print(
            f"エラー種類: {type(e).__name__}"
        )

        print(
            f"エラー内容: {e}"
        )

        print()
        traceback.print_exc()

        return False


# =============================================================================
# メニュー
# =============================================================================

def show_menu():
    """
    更新方法選択メニューを表示する。
    """

    print()
    print("=" * 80)

    print(
        " Backrooms Navigation System - Fandom JP"
    )

    print(
        " Database Update"
    )

    print("=" * 80)

    print()

    print(
        "更新方法を選択してください。"
    )

    print()

    print(
        "[1] 全更新"
    )

    print(
        "    一覧HTMLを再取得"
    )

    print(
        "    → DB再構築"
    )

    print(
        "    → Level List生成"
    )

    print()

    print(
        "[2] HTMLを再取得せずDBだけ再構築"
    )

    print(
        "    現在のindex_html/を使用"
    )

    print(
        "    → DB再構築"
    )

    print(
        "    → Level List生成"
    )

    print()

    print(
        "[0] 終了"
    )

    print()

    print("=" * 80)


# =============================================================================
# モード入力
# =============================================================================

def get_mode():
    """
    ユーザーから更新モードを取得する。

    Returns
    -------
    str
        "1", "2", "0"
    """

    while True:

        try:

            choice = input(
                "▶選択: "
            ).strip()

        except (
            EOFError,
            KeyboardInterrupt
        ):

            print()
            print(
                "終了します。"
            )

            return "0"

        if choice in {
            "0",
            "1",
            "2",
        }:

            return choice

        print()
        print(
            "【エラー】"
            "1 / 2 / 0 のいずれかを入力してください。"
        )

        print()


# =============================================================================
# ステップリスト
# =============================================================================

def build_steps(mode):
    """
    更新モードに応じて実行ステップを作る。
    """

    steps = []

    if mode == "1":

        steps.append(
            (
                "1/7",
                "Fandom JP 一覧HTML取得",
                index_collector.main,
            )
        )

        start_number = 2
        total_number = 7

    else:

        start_number = 1
        total_number = 6

    steps.append(
        (
            f"{start_number}/{total_number}",
            "一覧HTML解析・ページDB作成",
            index_parser.main,
        )
    )

    steps.append(
        (
            f"{start_number + 1}/{total_number}",
            "ページ分類",
            classify_pages.main,
        )
    )

    steps.append(
        (
            f"{start_number + 2}/{total_number}",
            "翻訳一覧HTML解析",
            translation_parser.main,
        )
    )

    steps.append(
        (
            f"{start_number + 3}/{total_number}",
            "翻訳記事分類",
            translation_classifier.main,
        )
    )

    steps.append(
        (
            f"{start_number + 4}/{total_number}",
            "Master Database統合",
            merge_databases.main,
        )
    )

    steps.append(
        (
            f"{start_number + 5}/{total_number}",
            "言語別Level List生成",
            level_list_generator.main,
        )
    )

    return steps


# =============================================================================
# 選択内容表示
# =============================================================================

def show_selected_mode(mode):
    """
    選択した更新モードを表示する。
    """

    print()
    print("=" * 80)

    if mode == "1":

        print(
            "選択: [1] 全更新"
        )

        print(
            "一覧HTMLを再取得してからDBを再構築します。"
        )

    elif mode == "2":

        print(
            "選択: [2] HTMLを再取得せずDBだけ再構築"
        )

        print(
            "現在のindex_html/を使用します。"
        )

    print("=" * 80)


# =============================================================================
# 更新実行
# =============================================================================

def execute_update(mode):
    """
    選択されたモードで更新処理を実行する。
    """

    # -------------------------------------------------------------------------
    # [2] HTML確認
    # -------------------------------------------------------------------------

    if mode == "2":

        if not check_index_html():

            return False

    # -------------------------------------------------------------------------
    # ステップ作成
    # -------------------------------------------------------------------------

    steps = build_steps(
        mode
    )

    # -------------------------------------------------------------------------
    # 総処理時間
    # -------------------------------------------------------------------------

    overall_start = time.time()

    completed = 0

    # -------------------------------------------------------------------------
    # 順番に実行
    # -------------------------------------------------------------------------

    for number, name, function in steps:

        success = run_step(
            number,
            name,
            function
        )

        if not success:

            print()
            print("=" * 80)

            print(
                "データベース更新を中断しました。"
            )

            print("=" * 80)

            print()

            print(
                f"完了済み: "
                f"{completed}/{len(steps)} ステップ"
            )

            print()

            show_database_status()

            return False

        completed += 1

    # -------------------------------------------------------------------------
    # 完了
    # -------------------------------------------------------------------------

    elapsed = (
        time.time()
        - overall_start
    )

    print()
    print()
    print("=" * 80)

    print(
        " ★ データベース更新完了 ★"
    )

    print("=" * 80)

    print()

    print(
        f"全ステップ完了: "
        f"{completed}/{len(steps)}"
    )

    print(
        f"総処理時間: "
        f"{elapsed:.1f} 秒"
    )

    print()

    print(
        "更新された主なデータ:"
    )

    if mode == "1":

        print(
            "  index_html/"
        )

    print(
        "  parsed_index/all_links.csv"
    )

    print(
        "  parsed_index/pages_database.csv"
    )

    print(
        "  parsed_index/pages_database_classified.csv"
    )

    print(
        "  parsed_index/translation_database.csv"
    )

    print(
        "  parsed_index/translation_database_classified.csv"
    )

    print(
        "  parsed_index/pages_master.csv"
    )

    print(
        "  level_lists/"
    )

    print()

    show_database_status()

    print()

    print("=" * 80)

    return True


# =============================================================================
# メイン
# =============================================================================

def main():

    print()
    print("=" * 80)

    print(
        "Backrooms Navigation System - Fandom JP"
    )

    print(
        "Database Update"
    )

    print("=" * 80)

    print()

    print(
        f"実行フォルダ: "
        f"{BASE_DIR}"
    )

    show_menu()

    mode = get_mode()

    if mode == "0":

        print()
        print(
            "終了します。"
        )

        return True

    show_selected_mode(
        mode
    )

    success = execute_update(
        mode
    )

    return success


# エイリアス（親プログラムからの分かりやすい呼び出し用）
update_database = main


# =============================================================================
# 実行
# =============================================================================

if __name__ == "__main__":

    try:

        success = main()
        if not success:
            sys.exit(1)

    except KeyboardInterrupt:

        print()
        print(
            "Ctrl+Cが押されたため、"
            "更新処理を終了します。"
        )

        sys.exit(130)

    except Exception as e:

        print()
        print("=" * 80)

        print(
            "【致命的エラー】"
        )

        print("=" * 80)

        print()

        print(
            f"エラー種類: {type(e).__name__}"
        )

        print(
            f"エラー内容: {e}"
        )

        print()
        traceback.print_exc()

        sys.exit(1)
