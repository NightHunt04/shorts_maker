import os
import ffmpeg

def format_timestamp_ass(seconds):
    millisec = int((seconds % 1) * 100)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:01d}:{minutes:02d}:{seconds:02d}.{millisec:02d}"

def return_subtitle_style_hex(font_size, font_color, background_color, italic, bold, subtitles_position, font_family):
    print('font color:', font_color)
    print('background color:', background_color)
    ass_color_codes = {
        # Transparent Colors
        "transparent-0": "&HFF000000",  
        "transparent-1": "&H80000000",  
        "transparent-2": "&H60000000",  
        "transparent-3": "&H40000000",  
        "transparent-4": "&H20000000",  
        "transparent-5": "&H00000000",  

        # Yellows & Oranges (Swapped Red ↔ Blue)
        "yellow-0": "&H0000FFFF",  # Bright Yellow
        "yellow-1": "&H0000D7FF",  # Gold
        "yellow-2": "&H0000A5FF",  # Orange-Yellow
        "yellow-3": "&H008BECFF",  # Light Goldenrod Yellow
        "orange-0": "&H0000A5FF",  # Orange
        "orange-1": "&H00008CFF",  # Dark Orange
        "orange-2": "&H000051E6",  # Deep Orange

        # Blues (Swapped Red ↔ Blue)
        "blue-0": "&H00FF0000",  # Pure Blue
        "blue-1": "&H00FF901E",  # Dodger Blue
        "blue-2": "&H00FFCD00",  # Medium Blue
        "blue-3": "&H00EBCE87",  # Sky Blue
        "blue-4": "&H00ED9564",  # Royal Blue
        "blue-5": "&H00E16941",  # Deep Blue

        # Greens (Unchanged, as Green is in the middle)
        "green-0": "&H0000FF00",  # Pure Green
        "green-1": "&H0032CD32",  # Lime Green
        "green-2": "&H00008B00",  # Dark Green
        "green-3": "&H007CFC00",  # Lawn Green
        "green-4": "&H0000FA9A",  # Medium Spring Green
        "green-5": "&H0056A902",  # Olive Green

        # Reds & Pinks (Swapped Red ↔ Blue)
        "red-0": "&H00FF0000",  # Pure Red
        "red-1": "&H00DC143C",  # Crimson
        "red-2": "&H008B0000",  # Dark Red
        "red-3": "&H00FF4500",  # Orange Red
        "red-4": "&H008515C7",  # Medium Violet Red
        "pink-0": "&H00B469FF",  # Hot Pink
        "pink-1": "&H00CBC0FF",  # Light Pink
        "pink-2": "&H009370DB",  # Pale Violet Red

        # Purples & Violets (Swapped Red ↔ Blue)
        "purple-0": "&H00800080",  # Pure Purple
        "purple-1": "&H00D30094",  # Dark Violet
        "purple-2": "&H00E22B8A",  # Blue Violet
        "purple-3": "&H00CC007A",  # Deep Purple

        # Browns (Swapped Red ↔ Blue)
        "brown-0": "&H0013458B",  # Saddle Brown
        "brown-1": "&H002A2AA5",  # Brown
        "brown-2": "&H001E69D2",  # Chocolate

        # Greys & Blacks
        "grey-0": "&H00D3D3D3",  # Light Grey
        "grey-1": "&H00808080",  # Grey
        "grey-2": "&H00404040",  # Dark Grey
        "black": "&H00000000",  # Black

        # Whites (Unchanged)
        "white": "&H00FFFFFF",  # Pure White
        "offwhite": "&H00FAF0E6",  # Linen
    }

    is_bold = 0
    is_italic = 0
    subtitle_position_num = 2
    if subtitles_position.lower().strip() == 'center':
        subtitle_position_num = 5
    if bold:
        is_bold = 1
    if italic:
        is_italic = 1

    fonts_available = ('Playfair Display', 'Tahoma', 'Times New Roman', 'Verdana', 'Arial', 'Courier New', 'Noto Sans', 'Bebas Neue')
    if font_family not in fonts_available:
        font_family = 'Tahoma'

    style = f'Style: sub_style,{font_family},{font_size},{ass_color_codes[font_color.strip().lower()]},&H70000000,{ass_color_codes[background_color.strip().lower()]},&H00000000,{is_bold},{is_italic},0,0,100,100,0,0,3,2,0,{subtitle_position_num},10,10,50,1\n\n'
    return style

highlight_ass_colors = {
    "black": r"\c&H000000&",
    "white": r"\c&HFFFFFF&",
    "red": r"\c&H0000FF&",
    "green": r"\c&H00FF00&",
    "blue": r"\c&HFF0000&",
    "yellow": r"\c&H00FFFF&",
    "cyan": r"\c&HFFFF00&",
    "magenta": r"\c&HFF00FF&",
    "gray": r"\c&H808080&",
    "light_gray": r"\c&HCCCCCC&",
    "dark_gray": r"\c&H404040&",
    "orange": r"\c&H00A5FF&",
    "pink": r"\c&HFF80FF&",
    "purple": r"\c&H800080&",
    "brown": r"\c&H2A2AA5&",
    "lime": r"\c&H00FF80&",
    "gold": r"\c&H00D7FF&",
    "navy": r"\c&H800000&",
    "teal": r"\c&H808000&",
    "olive": r"\c&H008080&",
    "maroon": r"\c&H000080&",
    "violet": r"\c&HEE82EE&",
    "indigo": r"\c&H82004B&",
    "turquoise": r"\c&HADDDDD&",
    "beige": r"\c&HDCF5F5&",
    "sky_blue": r"\c&HFFA07A&",
    "coral": r"\c&H507FFF&",
    "transparent": r"\c&H00000000&"
}

def add_subtitles(
        segments, 
        input_video, 
        output_path, 
        video_uuid, 
        words_per_subtitle = 3, 
        font_size = 19, 
        font_color = 'white', 
        background_color = 'transparent-0', 
        font_highlight_color = 'yellow-1', 
        italic = False, 
        bold = False, 
        font_highlight_size = 24, 
        subtitles_position = 'center', 
        kinetic_subtitles = False,
        font_family = 'Tahoma'
    ):
    subtitles = []
    buffer = []

    for segment in segments['segments']:
        for ind, word_info in enumerate(segment['words']):
            buffer.append(word_info)

            if len(buffer) == words_per_subtitle:
                for i in range(len(buffer)):
                    text = ''
                    start = buffer[i]['start']
                    end = buffer[i]['end']

                    if i == len(buffer) - 1:
                        if ind + 1 < len(segment['words']):
                            end = segment['words'][ind + 1]['start']
                    else:
                        end = buffer[i + 1]['start']

                    for j, word_info__ in enumerate(buffer):
                        if j == i:
                            if kinetic_subtitles:
                                # text += f"{{\\fs{text_highlight_font_size}\\c&H00FFFF&}}{word_info__['word']}{{\\r}}"
                                # text += f"{{\\fs{font_highlight_size}{highlight_ass_colors.get(font_highlight_color, r'\c&HFFFFFF&')}}}{word_info__['word']}{{\\r}}"
                                color_code = highlight_ass_colors.get(font_highlight_color, r'\c&HFFFFFF&')
                                text += f"{{\\fs{font_highlight_size}{color_code}}}{word_info__['word']}{{\\r}}"
                            else:
                                text += word_info__['word']
                        else:
                            text += word_info__['word']

                    subtitles.append({
                        'start': format_timestamp_ass(start),
                        'end': format_timestamp_ass(end),
                        'text': text
                    })
                
                buffer = []

    for i in range(len(buffer)):
        text = ''
        start = buffer[i]['start']
        end = buffer[i]['end']

        if i == len(buffer) - 1:
            if ind + 1 < len(segment['words']):
                end = segment['words'][ind + 1]['start']
        else:
            end = buffer[i + 1]['start']

        for j, word_info__ in enumerate(buffer):
            if j == i:
                if kinetic_subtitles:
                    # text += f"{{\\fs{font_highlight_size}{highlight_ass_colors.get(font_highlight_color, r'\c&HFFFFFF&')}}}{word_info__['word']}{{\\r}}"
                    color_code = highlight_ass_colors.get(font_highlight_color, r'\c&HFFFFFF&')
                    text += f"{{\\fs{font_highlight_size}{color_code}}}{word_info__['word']}{{\\r}}"
                else:
                    text += word_info__['word']
            else:
                text += word_info__['word']

        subtitles.append({
            'start': format_timestamp_ass(start),
            'end': format_timestamp_ass(end),
            'text': text
        })
    
    buffer = []

    # write .ass file for subtitles
    with open(f'{video_uuid}_subtitles.ass', 'w', encoding='utf-8') as f:
        f.write("[Script Info]\n")
        f.write("; Script generated by script\n")
        f.write("ScriptType: v4.00+\n")

        f.write("[V4+ Styles]\n")
        f.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
        f.write("Style: Default,Arial,20,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1\n")
        f.write("Style: ybi_center,Tahoma,19,&HFFFFFF&,&H70000000,&HFF000000,&H00000000,1,0,0,0,100,100,0,0,3,2,0,5,10,10,20,1\n")
        f.write("Style: ybi_center_blackbg,Tahoma,19,&HFFFFFF&,&H70000000,&HFF000000,&H00000000,1,0,0,0,100,100,0,0,3,2,0,2,10,10,50,1\n\n")
        f.write(return_subtitle_style_hex(
            font_size, 
            font_color, 
            background_color, 
            italic, 
            bold, 
            subtitles_position,
            font_family
        ))

        f.write("[Events]\n")
        f.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")

        for i, subtitle in enumerate(subtitles, start=1):
            f.write(f"Dialogue: 0,{subtitle['start']},{subtitle['end']},sub_style,,0,0,0,,{subtitle['text']}\n")

    # merge the subtitles onto the video
    try:
        if not os.path.exists(f'{video_uuid}_subtitles.ass'):
            raise FileNotFoundError(f"ASS file not found: {video_uuid}_subtitles.ass")

        fonts_dir = 'fonts/'
        (
            ffmpeg
            .input(input_video)
            .output(
                output_path, 
                vf=f"ass={video_uuid}_subtitles.ass:fontsdir={fonts_dir}",
                vcodec='libx264',
                acodec='aac'
            )
            .run(overwrite_output=True)
        )
        print(f"Output video created at: {output_path}")

        os.remove(f'{video_uuid}_subtitles.ass')
    except Exception as e:
        print(e)