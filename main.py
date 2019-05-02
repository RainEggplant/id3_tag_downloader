# -*- coding:utf-8 -*-

import argparse
import os
import re
import urllib.request
from datetime import datetime
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from PIL import Image
from ncm_api import CloudApi


def extract_file_name_id_pairs(directory):
    list_path = os.path.join(directory, 'url_list.txt')
    if (not os.path.exists(list_path)):
        print('No "url_list.txt" under working directory! Aborted.')
        raise FileNotFoundError()

    re_file_name = re.compile(r'(?<=/)\w+\.\w+(?=\?&suffix)')
    re_id = re.compile(r'(?<=id=)\d+$')
    pairs = []
    with open(list_path, 'r') as f:
        for line in f:
            pairs.append((re_file_name.search(line).group(0),
                          re_id.search(line).group(0)))
    return pairs


def download_id3_tag(file_name_id_pairs, directory):
    log_path = os.path.join(directory, 'id3_tag_downloader.log')
    api = CloudApi()
    img_list = []
    counter = 0
    length = len(file_name_id_pairs)
    # write log
    with open(log_path, 'a', encoding='utf-8') as f:
        for pair in file_name_id_pairs:
            counter += 1
            print(
                'Processing [{0:<5} / {1:<5}] {2}:'.format(counter, length, pair[0]))
            old_file_path = os.path.join(directory, pair[0])

            if (os.path.exists(old_file_path)):
                song_info = api.get_song(pair[1])
                song_file_root = format_string(song_info['name'])
                song_file_extension = pair[0].replace(
                    os.path.splitext(pair[0])[0], '')
                f.write('%s, %s\n' %
                        (pair[1], song_file_root+song_file_extension))

                # Modify ID3 tag
                audio = EasyID3(old_file_path)
                audio['title'] = song_info['name']
                audio['artist'] = ' & '.join(
                    [artist['name'] for artist in song_info['artists']])
                audio['album'] = song_info['album']['name']
                audio['date'] = datetime.fromtimestamp(
                    (song_info['album']['publishTime'] / 1000)).strftime('%Y-%m-%d')
                audio['tracknumber'] = str(song_info['no'])
                audio['discnumber'] = str(song_info['disc'])
                audio.save()

                # Download and resize cover
                cover_url = song_info['album']['blurPicUrl']
                if cover_url is None:
                    cover_url = song_info['album']['picUrl']
                cover_file_name = '{}.jpg'.format(
                    song_info['album']['picId'] or song_info['album']['pic'])
                cover_file_path = os.path.join(directory, cover_file_name)
                if img_list.count(cover_file_name) == 0:
                    if (not os.path.exists(cover_file_path)) or os.path.getsize(cover_file_path) == 0:
                        urllib.request.urlretrieve(cover_url, cover_file_path)
                        img_list.append(cover_file_name)
                resize_img(cover_file_path)

                # Add cover
                audio = ID3(old_file_path)
                with open(cover_file_path, 'rb') as cover:
                    audio['APIC'] = APIC(
                        encoding=3,
                        mime='image/jpeg',
                        type=3,
                        data=cover.read()
                    )
                audio.save()

                # Rename
                index = 1
                song_file_path = os.path.join(
                    directory, song_file_root + song_file_extension)
                # Deal with duplicate file name
                while os.path.exists(song_file_path):
                    print('  Warning! File name already exists. Renaming.')
                    index += 1
                    song_file_path = os.path.join(
                        directory, song_file_root + '_{}'.format(index) + song_file_extension)

                os.rename(old_file_path, song_file_path)
                print('  Done! New name: {}'.format(song_file_root +
                                                    ('' if index == 1 else'_{}'.format(index)) + song_file_extension))

            else:
                print('  Error! File not found.')

    for img in img_list:
        os.remove(os.path.join(directory, img))


def resize_img(file_path, max_size=(640, 640), quality=90):
    try:
        img = Image.open(file_path)
    except IOError:
        print('Can\'t open image:', file_path)
        return

    if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
        img.thumbnail(max_size, Image.ANTIALIAS)
        if img.format == 'PNG':
            img = img.convert('RGB')
        img.save(file_path, quality=quality)


def format_string(string):
    """
    Replace illegal characters by ' '
    """
    return re.sub(r'[\\/:*?"<>|\t]', ' ', string)


def main():
    parser = argparse.ArgumentParser(
        description='''Add ID3 tags to mp3 file from netease cloud music according to music ID.
        NOTE: You will need to use it in combination with moresound.tk .''')
    parser.add_argument('-d', '--directory', dest='directory', required=True,
                        help='the directory of the audio files and "url_list.txt"')
    args = parser.parse_args()
    print('Start processing: ', end='')
    pairs = extract_file_name_id_pairs(args.directory)
    print('{0:<5} item(s) found.'.format(len(pairs)))
    download_id3_tag(pairs, args.directory)
    print('\nAll jobs finished!')


if __name__ == '__main__':
    main()
