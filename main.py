from argparse import ArgumentParser
import re
from pathlib import Path
from urllib.parse import urljoin

from requests.sessions import Session
from tqdm import tqdm


BASE_URL = 'http://tsinghua.xuetangx.com/'


def key_to_url(key):
    return 'http://tsinghua.xuetangx.com/courses/course-v1:' + key[9:key.find(
        '+type')] + '/xblock/' + key + '/handler/transcript/translation/zh'


def get_list(data):
    return re.findall(r'href="(/courses.*?)"', data)[6:]


def parser_subtitle_url(data):
    key = re.search(r'(block-v1:TsinghuaX\+.*?\+type@video\+block@.*?)\&', data).group(1)
    return key_to_url(key)


def main(args):
    directory = Path(args.directory)
    directory.mkdir(exist_ok=True, parents=True)

    session = Session()
    session.headers.update({
        'Cookie': args.cookie,
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    })
    response = session.get(args.target)
    if response.status_code != 200:
        print('[ERROR] Get basic url failed!')
        return
    data = response.text
    video_list = list(map(lambda x: urljoin(BASE_URL, x), get_list(data)))
    for url in tqdm(video_list):
        data = session.get(url).text
        title = re.search('<title>(.*?)</title>', data, re.DOTALL).group(1).split('|')[0].strip()
        try:
            subtitle_url = parser_subtitle_url(data)
        except AttributeError:
            # it means it's not a video
            continue
        try:
            subtitle = session.get(subtitle_url).json()['text']
            open(directory.joinpath(f'{title}.txt'), 'w').write('\n'.join(subtitle))
        except:
            # Generally speaking, it means a video without subtitle
            print(f'[INFO] ignore url {url}')


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('-t', '--target', type=str, help="Any url of this course's mooc")
    parser.add_argument('-c', '--cookie', type=str, required=True,
                        help="Cookie for user (Obviously the author is too lazy to finish login)")
    parser.add_argument('-d', '--directory', type=str, default='result', help='Output directory to save subtitles')
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_arguments())
