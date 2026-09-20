"""
Backrooms Navigation System - Fandom JP

Backrooms Fandom JP のローカルデータベースを
閲覧・検索・ナビゲーションするための統合システム。
"""

import os
import sys

# =============================================================================
# カレントディレクトリの強制固定
# (ショートカット等から起動された場合でも、作業場所をexeの場所に固定する)
# =============================================================================

if getattr(sys, "frozen", False):
    os.chdir(os.path.dirname(sys.executable))


from pathlib import Path


# =============================================================================
# モジュール
# =============================================================================

# HTMLダウンローダー
from modules.downloader import main as run_downloader

# 画像抽出・ダウンローダー
from modules.image_downloader import download_images

# HTML本文・情報データ抽出
from modules.extractor import extract_levels

# Levelネットワーク抽出
from modules.network import process_backrooms_data

# Levelルート検索
from modules.navigator import run_navigation

# ローカルデータベース
from modules.database import (
    browse_database,
    find_level_candidates,
    get_level_info,
    print_level_info,
)

# Levelブラウザー
from modules.browser import browse_level

# Master Database 更新モジュール
from modules.update_database import main as run_update_database


# =============================================================================
# 基本設定
# =============================================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
)


# =============================================================================
# 共通
# =============================================================================

def pause():
    """
    Enterキーが押されるまで待機する。
    """

    input(
        "\nEnterキーでメニューに戻ります..."
    )


# =============================================================================
# メインメニュー
# =============================================================================

def show_menu():
    """
    メインメニューを表示する。
    """

    print()
    print("=" * 80)

    print(
        "        Backrooms Navigation System - Fandom JP"
    )

    print("=" * 80)

    print()

    print(
        "[1] Levelを検索"
    )

    print(
        "[2] Level情報を見る"
    )

    print(
        "[3] ルートを検索"
    )

    print(
        "[4] ローカルデータベースを見る"
    )

    print(
        "[5] Fandom JPからHTMLをダウンロード"
    )

    print(
        "[6] 画像をダウンロード"
    )

    print(
        "[7] 情報データベースを更新 (ローカルHTML抽出)"
    )

    print(
        "[8] ネットワークを更新"
    )

    print(
        "[9] Master Database を更新"
    )

    print()

    print(
        "[0] 終了"
    )

    print()


# =============================================================================
# Level検索
# =============================================================================

def level_search():
    """
    Level Browserを起動する。
    """

    browse_level()


# =============================================================================
# Level情報
# =============================================================================

def level_info():
    """
    Master Database / ローカルデータから
    Level情報を検索・表示する。
    """

    print()
    print("=" * 80)

    print(
        "        Backrooms Fandom JP - Level Information"
    )

    print("=" * 80)

    while True:

        print()

        query = input(
            "▶ Level・ページ名を入力 "
            "(空欄で終了) : "
        ).strip()

        if not query:

            print()
            print(
                "Level情報を終了します。"
            )

            return

        # ---------------------------------------------------------------------
        # 候補検索
        # ---------------------------------------------------------------------

        candidates = (
            find_level_candidates(
                query
            )
        )

        if not candidates:

            print()
            print(
                f"❌ ページが見つかりません: {query}"
            )

            continue

        # ---------------------------------------------------------------------
        # Master DB候補
        # ---------------------------------------------------------------------

        if (
            candidates
            and isinstance(
                candidates[0],
                dict
            )
        ):

            if len(candidates) == 1:

                selected_page = (
                    candidates[0]
                )

            else:

                print()
                print(
                    "候補が複数あります。"
                )

                visible_count = min(
                    len(candidates),
                    30
                )

                for index, page in enumerate(
                    candidates[
                        :visible_count
                    ],
                    1
                ):

                    print(
                        f"  [{index}] "
                        f"{page['title']} "
                        f"[{page.get('language') or '-'}] "
                        f"[{page.get('category') or '-'}]"
                    )

                if len(candidates) > 30:

                    print(
                        f"  ... 他 "
                        f"{len(candidates) - 30} 件"
                    )

                selected_page = None

                while True:

                    choice = input(
                        "番号を入力してください"
                        "（Enterでキャンセル）: "
                    ).strip()

                    if not choice:

                        break

                    if not choice.isdigit():

                        print(
                            "数字を入力してください。"
                        )

                        continue

                    index = (
                        int(choice) - 1
                    )

                    if (
                        0
                        <= index
                        < visible_count
                    ):

                        selected_page = (
                            candidates[index]
                        )

                        break

                    print(
                        "範囲外の番号です。"
                    )

                if selected_page is None:

                    continue

            level_id = (
                selected_page["title"]
            )

        # ---------------------------------------------------------------------
        # Legacy候補
        # ---------------------------------------------------------------------

        else:

            if len(candidates) == 1:

                level_id = (
                    candidates[0]
                )

            else:

                print()
                print(
                    "候補が複数あります。"
                )

                visible_count = min(
                    len(candidates),
                    30
                )

                for index, candidate in enumerate(
                    candidates[:visible_count],
                    1
                ):

                    print(
                        f"  [{index}] "
                        f"{candidate}"
                    )

                if len(candidates) > 30:

                    print(
                        f"  ... 他 "
                        f"{len(candidates) - 30} 件"
                    )

                level_id = None

                while True:

                    choice = input(
                        "番号を入力してください"
                        "（Enterでキャンセル）: "
                    ).strip()

                    if not choice:

                        break

                    if not choice.isdigit():

                        print(
                            "数字を入力してください。"
                        )

                        continue

                    index = (
                        int(choice) - 1
                    )

                    if (
                        0
                        <= index
                        < visible_count
                    ):

                        level_id = (
                            candidates[index]
                        )

                        break

                    print(
                        "範囲外の番号です。"
                    )

                if level_id is None:

                    continue

        # ---------------------------------------------------------------------
        # 情報取得
        # ---------------------------------------------------------------------

        info = get_level_info(
            level_id
        )

        print_level_info
