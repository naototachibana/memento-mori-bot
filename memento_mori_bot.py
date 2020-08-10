import requests
import json
import time
import os
import yaml

def calc_year_progress():
    now = datetime.now()
    start = date(now.year, 1, 1)
    end = date(now.year, 12, 31)
    today = date.today()
    elapsed_days = int((today-start).days)+1
    num_days_1year = int((end-start).days)+1
    progress = 100*elapsed_days/num_days_1year
    return progress

def calc_remaining_life():
    now = datetime.now()
    start = datetime(1996, 1, 1, 0, 0, 0, 0)
    goal = datetime(1996+80, 1, 1, 0, 0, 0, 0)
    remaining = goal - now
    progress_ratio = (1-(remaining/(goal-start)))*100
    return remaining, progress_ratio

def post_slack(post_url, name, text):
    requests.post(
        post_url,
        data=json.dumps(
            {"text": text,
             "username": name,
             "icon_emoji": ":python:"}))

def write_log(text):
    path_w = "log.md"
    if not os.path.isfile(path_w):
        with open(path_w, mode='w') as f:
            f.write(text)
    else:
        with open(path_w, mode='a') as f:
            f.write(text)
            
def read_yaml_file_as_dict(filepath):
    with open(filepath) as file:
        dict_from_yaml = yaml.load(file, Loader=yaml.FullLoader)


if __name__ == '__main__':
    slack_keys = read_yaml_file_as_dict('./slack-keys.yaml')
    url_daily_bots = slack_keys['api_post_url']
    
    now = datetime.now(timezone(timedelta(hours=9)))

    post_slack(post_url = url_daily_bots, name = "memento_mori_bot",text = str_text)

    str_today = str(now)
    str_year_progress = ("{year} 年は {progress:.1f} % 終了しました.\n".format(year  = now.year,
                                                                            progress=calc_year_progress()))
    remaining, progress_ratio = calc_remaining_life()
    str_remaining_life = ("1996 年生まれの寿命を 80 歳とするなら, 貴方の余命は {remaining} 日です.\n"
                            "貴方の人生の {progress_ratio:.4f} % が終了しました.".format(remaining=remaining.days,
                                                                                     progress_ratio=progress_ratio))
    str_text = str_today +'\n'+ str_year_progress + "\n" +str_remaining_life
    post_slack(post_url = url_daily_bots,
               name = "memento_mori_bot",
               text = str_text)
    str_text = "initialize"
    print(str_text)
    while True:
        now = datetime.now(timezone(timedelta(hours=9)))
        if (now.strftime('%H') == "07"):
            str_today = str(now)
            str_year_progress = ("{year} 年は {progress:.1f} % 終了しました.\n".format(year  = now.year,
                                                                                    progress=calc_year_progress()))
            remaining, progress_ratio = calc_remaining_life()
            str_remaining_life = ("1996 年生まれの寿命を 80 歳とするなら, 貴方の余命は {remaining} 日です.\n"
                                    "貴方の人生の {progress_ratio:.4f} % が終了しました.".format(remaining=remaining.days,
                                                                                             progress_ratio=progress_ratio))
            str_text = str_today +'\n'+ str_year_progress + "\n" +str_remaining_life
            post_slack(post_url = url_daily_bots,
                       name = "memento_mori_bot",
                       text = str_text)
            write_log(str_text)
            waiting_time = 24*60*60
            time.sleep(waiting_time)
        else:
            waiting_time = 60*60
            write_log(str(now))
            time.sleep(waiting_time)
