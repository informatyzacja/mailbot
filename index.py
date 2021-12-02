from src import mails_to_json, utils


def convert_mails(txt_filename: str, json_filename: str):
    """Converts mails from txt file to json file"""
    mails_to_json.convert_file_to_json(
        f"data/{txt_filename}", f"data/{json_filename}")
    print("Mails converted!")
    utils.log(f"{utils.current_time()} Mails converted")


if __name__ == "__main__":
    config = utils.load_config()
    convert_mails(config['mails_txt_file'], config['mails_json_file'])
