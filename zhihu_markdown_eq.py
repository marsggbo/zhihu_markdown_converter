#coding=utf-8
import requests
import argparse

parser = argparse.ArgumentParser(description="Zhihu_markdown_eq_converter")
parser.add_argument("--file", help="your md file path", default="rl.md")
args = parser.parse_args()


with open(args.file, 'r', encoding='utf-8') as f:
    data = f.readlines()

data_str = ''.join(data)

# $$..$$

data_str = data_str.replace("$$", "====")


# $..$
def parse_data(data_str, renderer=0):
    index = 0
    length = len(data_str)
    modifications = {}
    count = 0
    while index < length:
        char = data_str[index]
        if char == '$' and data_str[index-1]!='\\':
            start_index = index+1
            index += 1
            while data_str[index]!='$':
                index += 1
            end_index = index
            equation = data_str[start_index:end_index].replace('\n','')
            equation = requests.utils.quote(r"{}".format(equation))
            href = f"https://www.zhihu.com/equation?tex={equation}"
            if renderer==0:
                img = f'''<img src="{href}" eeimg="1">'''
            else:
                img = f'''<p align="center"><img src="{href}" eeimg="1"></p>'''
            modifications[count] = {'start_index':start_index, 'end_index':end_index, 'img':img}
            count += 1
            index += 1
        else:
            index += 1

    sorted(modifications.items(), key=lambda x:x[1]['start_index'], reverse=True)
    new_data_str = ''
    prev_index = 0
    for _, key in enumerate(modifications):
        start_index = modifications[key]['start_index']
        end_index = modifications[key]['end_index']
        img = modifications[key]['img']
        new_data_str = new_data_str + data_str[prev_index:start_index-1] + img
        prev_index = end_index + 1
    return new_data_str

data_str = parse_data(data_str,0)
data_str = data_str.replace('====','$')
data_str = parse_data(data_str,1)

with open('zhihu_'+args.file, 'w', encoding='utf') as f:
    f.write(data_str)
