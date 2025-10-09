import argparse
import datetime
import json
import logging
import os
import sys

import bpy

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def timedelta2str(delta: datetime.timedelta):
    hours, remaining_secs = divmod(int(delta.total_seconds()), 60 * 60)
    mins, remaining_secs = divmod(remaining_secs, 60)
    secs = int(remaining_secs)
    # 1時間以上なら
    if hours > 0:
        return f"{hours:02}:{mins:02}:{secs:02}"
    else:
        return f"{mins:02}:{secs:02}"


def get_titles_info(titles_json):
    json_path = os.path.abspath(titles_json)
    if not os.path.isfile(json_path):
        logging.warning(
            f"指定されたjsonファイルが存在しないため無視します: {titles_json}"
        )
        return {}
    with open(json_path, "rb") as f:
        return json.load(f)


def save_chapter_info(timecode_list, titles_info, output, force):
    output_path = os.path.abspath(output)

    if os.path.exists(output_path):
        if force:
            logger.warning(
                f"出力先ファイルが既に存在するため上書きします.:{output_path}"
            )
        else:
            logger.error(
                f"出力先ファイルが既に存在するため処理を中止します.:{output_path}"
            )
            raise FileExistsError(
                f"出力先ファイルが既に存在するため処理を中止します.:{output_path}"
            )

    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        logger.warning(
            f"出力先ファイルのディレクトリが存在しないため作成します.: {output_dir}"
        )
        os.makedirs(output_dir)

    with open(output_path, "w") as f:
        DEFAULT_TITLE = "不明"
        for i, timecode in enumerate(timecode_list):
            chap_no = str(i + 1)
            title = titles_info.get(chap_no, f"{chap_no}_{DEFAULT_TITLE}")
            f.write(f"{timecode} {title}\n")


def get_timecode_list(blend_path, channel_no):
    # プロジェクトファイルを開く
    blend_full_path = os.path.abspath(blend_path)
    bpy.ops.wm.open_mainfile(filepath=blend_full_path)

    # 対象strip一覧を取得
    se = bpy.context.scene.sequence_editor
    start_frame_list = []
    for strip in se.strips:
        if strip.channel == channel_no:
            start_frame_list.append(strip.frame_final_start)
    # フレームの開始時間
    start_time_list = [
        timedelta2str(bpy.utils.time_from_frame(frame))
        for frame in sorted(start_frame_list)
    ]
    return start_time_list


def parse_args(script_args):
    parser = argparse.ArgumentParser(
        prog="gen-slide-chapter",
        description=".blendファイルの指定チャンネルから各ストリップの開始時間をチャプター情報として出力する",
    )
    parser.add_argument(
        "blend_file",
        metavar="BLEND_FILE",
        help="チャプター情報を取得する.blendファイル",
    )
    DEFAULT_IMAGE_CHANNEL = 3
    parser.add_argument(
        "--channel",
        metavar="CHANNEL",
        type=int,
        default=DEFAULT_IMAGE_CHANNEL,
        help=f"スライド画像が配置されているチャンネル番号. デフォルト: {DEFAULT_IMAGE_CHANNEL}",
    )
    parser.add_argument(
        "-t",
        "--titles",
        metavar="TITLES.json",
        help="チャプター番号とタイトルの対応を記載されたJSONファイル",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="OUTPUT_FILE",
        help="チャプター情報の出力先ファイル",
        required=True,
    )
    parser.add_argument(
        "--force", action="store_true", help="出力先ファイルが存在する場合に上書きする"
    )
    return parser.parse_args(script_args)


def main():
    try:
        # -- 以降の引数を取得
        script_args = sys.argv[sys.argv.index("--") + 1 :]
        logger.debug(f"script_args: {script_args}")
        args = parse_args(script_args)
        logger.info(f"args: {args}")

        titles_info = {}
        if args.titles:
            titles_info = get_titles_info(args.titles)

        timecode_list = get_timecode_list(args.blend_file, args.channel)
        logger.info(f"start_frame_list: {timecode_list}")

        save_chapter_info(timecode_list, titles_info, args.output, args.force)
    except FileExistsError:
        return 1


if __name__ == "__main__":
    sys.exit(main())
