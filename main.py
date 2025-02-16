import click
import uuid
import os
from utils.download_youtube_video import download_youtube_video
from utils.load_youtube_transcript import load_youtube_transcript
from utils.format_youtube_transcript import format_youtube_transcript
from utils.select_clips import select_clips
from utils.trim_selected_clips import trim_selected_clips
from utils.auto_detect_humans import auto_detect_humans
from utils.ratio_change_without_ad import resize_frame
from utils.curve_mask import curve_mask
from utils.make_audio_file import make_audio_file   
from utils.add_without_broll import add_without_broll
from utils.add_with_stock_broll import add_with_stock_broll
from utils.add_with_ai_broll import add_with_ai_broll

@click.command()
@click.option('-u', '--url', default=None, show_default=True, help='URL of the YouTube video')
@click.option('-sl', '--shorts_length', default=60, show_default=True, help='Length of shorts in seconds')
@click.option('-ns', '--number_of_shorts', default=1, show_default=True, help='Number of shorts to make out of video')
@click.option('-adc', '--auto_detection_crop', is_flag=True, help='Whether to auto detect humans in the trimmed shorts (default: False)')
@click.option('-gbc', '--gaussian_blur_bg_crop', is_flag=True, help='Whether to make video with original video blurred and enlarged in the background & the original video placed on the top of it (default: False)')
@click.option('-cc', '--cinematic_crop', is_flag=True, help='Whether to make a cinematic crop of the video (default: False)')
@click.option('-ccbg', '--cinematic_crop_background', default='black', show_default=True, help='Background color of the cinematic crop')
@click.option('-t', '--threads', default=4, show_default=True, help='Number of threads to be used')
@click.option('-sbrl', '--add_stock_broll', is_flag=True, help='Whether to add stock b-roll in the video (default: False)')
@click.option('-aibrl', '--add_ai_broll', is_flag=True, help='Whether to add AI generated b-roll in the video (default: False)')
@click.option('-nbrl', '--no_broll', is_flag=True, help='Whether to not add b-roll in the video (default: False)')
@click.option('-wps', '--words_per_subtitle', default=3, show_default=True, help='Words per subtitle')
@click.option('-ct', '--custom_timestamps', default=None, show_default=True, help='Custom timestamps to cut the video in your own given timestamps. The format for this is: \n"start_time->end_time;" (for single clip)\n"start_time->end_time;start_time->end_time" (for multiple clips)\nExample: "20->70;123->180" (time must be in seconds)')
@click.option('-sp', '--subtitles_position', default='center', show_default=True, help='Position of subtitles in the video [center, bottom]')
@click.option('-ff', '--font_family', default='Tahoma', show_default=True, help='Font family of subtitles in the video')
@click.option('-fs', '--font_size', default=19, show_default=True, help='Font size of subtitles in the video')
@click.option('-fhs', '--font_highlight_size', default=24, show_default=True, help='Font size of text highlight in the video')
@click.option('-bgc', '--background_color', default='transparent-0', show_default=True, help='Color of subtitles background')
@click.option('-fc', '--font_color', default='white', show_default=True, help='Color of font')
@click.option('-fhc', '--font_highlight_color', default='yellow-1', show_default=True, help='Color of font highlight')
@click.option('-i', '--italic', is_flag=True, help='Whether to make the subtitles italic (default: False)')
@click.option('-b', '--bold', is_flag=True, help='Whether to make the subtitles bold (default: False)')
@click.option('-ks', '--kinetic_subtitles', is_flag=True, help='Whether to add kinetic subtitles in the video (default: False)')
@click.option('-bgm', '--background_music', default=None, show_default=True, help="Background music")
@click.option('-bgmv', '--background_music_volume', default=0.4, show_default=True, help="Volume of the background music")
@click.option('--show_fonts', is_flag=True, help="Shows all available fonts")
@click.option('--show_bgms', is_flag=True, help="Shows all available background music")
def cli(
        url, 
        shorts_length, 
        number_of_shorts, 
        custom_timestamps,
        auto_detection_crop, 
        gaussian_blur_bg_crop,
        cinematic_crop,
        cinematic_crop_background,
        threads, 
        add_stock_broll, 
        add_ai_broll, 
        no_broll, 
        words_per_subtitle, 
        subtitles_position,
        kinetic_subtitles,
        italic,
        bold,
        font_size,
        font_highlight_size,
        font_color,
        background_color,
        font_highlight_color,
        font_family,
        show_fonts,
        background_music,
        show_bgms,
        background_music_volume
    ):
    if show_fonts:
        fonts_available = ('Playfair Display', 'Tahoma', 'Times New Roman', 'Verdana', 'Arial', 'Courier New', 'Noto Sans', 'Bebas Neue')
        click.echo(f'Available fonts: {", ".join(fonts_available)}')
        return

    if show_bgms:
        bgm = (
            'music/Into-timelapse.mp3',
            'music/Echo-Sax-End.mp3',
            'music/piano-0.mp3',
            'music/piano-1.mp3',
            'music/adventure-intro.mp3',
            'music/uplifting-fairy-tale.mp3',
            'music/soul-voyager-epic-cinematic.mp3',
            'music/astroscape-motivation.mp3',
            'music/adventure-music-prime-facts.mp3',
        )
        click.echo('Available background music:')
        for ind, m in enumerate(bgm):
            click.echo(f'{ind}: {m}')
        click.echo('')
        click.echo('Check the available background music in folder:')
        click.echo(os.path.abspath('music/'))
        return

    video_uuid = str(uuid.uuid4())
    
    # downloading the youtube video
    video_status = download_youtube_video(url, video_uuid)
    click.echo(video_status)

    transcript = None
    transcript_status = None

    if custom_timestamps:
        # trim the selected clips
        trimmed_status = trim_selected_clips(
            transcript, 
            video_uuid, 
            f"media/downloads/{video_uuid}.mp4", 
            threads, 
            custom_timestamps, 
            shorts_length
        )
        click.echo(trimmed_status)
    else:
        # loading the transcript of video
        transcript, transcript_status = load_youtube_transcript(url, shorts_length)
        click.echo(transcript_status)

        # formatting the transcript
        formatted_transcript, transcript_format_status = format_youtube_transcript(transcript, shorts_length)
        click.echo(transcript_format_status)

        # selecting the clips
        selected_clips, clips_selection_status = select_clips(
            formatted_transcript, 
            shorts_length, 
            number_of_shorts
        )
        click.echo(clips_selection_status)

        # trim the selected clips
        trim_status = trim_selected_clips(
            selected_clips, 
            video_uuid, 
            f"media/downloads/{video_uuid}.mp4", 
            threads, 
            custom_timestamps, 
            shorts_length
        )
        click.echo(trim_status)
    
    if auto_detection_crop:
        # auto detect humans in the trimmed shorts
        auto_detect_humans_status = auto_detect_humans(video_uuid, threads)
        click.echo(auto_detect_humans_status)
    elif cinematic_crop:
        # make a cinematic crop of the video
        curve_mask_status = curve_mask(video_uuid, threads, cinematic_crop_background)
        click.echo(curve_mask_status)
    elif gaussian_blur_bg_crop:
        # add gaussian blur in bg
        resize_frame_status = resize_frame(video_uuid, threads)
        click.echo(resize_frame_status)

    # make audio file
    make_audio_file_status = make_audio_file(video_uuid)
    click.echo(make_audio_file_status)

    if add_stock_broll:
        add_with_stock_broll_status = add_with_stock_broll(
            video_uuid = video_uuid, 
            THREADS_TO_BE_USED = threads, 
            words_per_subtitle = words_per_subtitle, 
            kinetic_subtitles = kinetic_subtitles,
            font_size = font_size, 
            font_color = font_color, 
            background_color = background_color, 
            font_highlight_color = font_highlight_color, 
            italic = italic, 
            bold = bold, 
            font_highlight_size = font_highlight_size, 
            subtitles_position = subtitles_position.lower().strip(),
            font_family = font_family,
            background_music = background_music,
            background_music_volume = background_music_volume
        )
        click.echo(add_with_stock_broll_status)
    if add_ai_broll:
        add_with_ai_broll_status = add_with_ai_broll(
            video_uuid = video_uuid, 
            THREADS_TO_BE_USED = threads, 
            words_per_subtitle = words_per_subtitle, 
            kinetic_subtitles = kinetic_subtitles,
            font_size = font_size, 
            font_color = font_color, 
            background_color = background_color, 
            font_highlight_color = font_highlight_color, 
            italic = italic, 
            bold = bold, 
            font_highlight_size = font_highlight_size, 
            subtitles_position = subtitles_position.lower().strip(),
            font_family = font_family,
            background_music = background_music,
            background_music_volume = background_music_volume
        )
        click.echo(add_with_ai_broll_status)
    if no_broll:
        add_without_broll_status = add_without_broll(
            video_uuid = video_uuid, 
            THREADS_TO_BE_USED = threads, 
            words_per_subtitle = words_per_subtitle, 
            kinetic_subtitles = kinetic_subtitles,
            font_size = font_size, 
            font_color = font_color, 
            background_color = background_color, 
            font_highlight_color = font_highlight_color, 
            italic = italic, 
            bold = bold, 
            font_highlight_size = font_highlight_size, 
            subtitles_position = subtitles_position.lower().strip(),
            font_family = font_family,
            background_music = background_music,
            background_music_volume = background_music_volume
        )
        click.echo(add_without_broll_status)

if __name__ == '__main__':
    cli()