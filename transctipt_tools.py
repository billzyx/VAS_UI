def load_cha_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        return process_lines(lines[8:-1])


def load_txt_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        return process_lines(lines)


def process_lines(lines):
    speaker_list = []
    text_list = []
    audio_list = []
    for idx, line in enumerate(lines):
        split_list = line.split('\t')
        speaker = split_list[0]
        if '' in split_list[1]:
            split_text_list = split_list[1].split('')
            text = split_text_list[0]
            audio = split_text_list[1].replace('', '')
        else:
            text = split_list[1]
            audio = None
        # print(speaker, text, audio)
        speaker_list.append(speaker)
        text_list.append(text)
        audio_list.append(audio)
    return speaker_list, text_list, audio_list

