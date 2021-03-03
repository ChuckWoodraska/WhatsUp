from flask import Blueprint, render_template
from chuck_pyutils import core as utils
import paramiko
import json
import operator as ops

def read_service_file():
    with open('services.json') as f:
        data = json.load(f)
    # print(data)
    return data

def get_data():
    # client = paramiko.SSHClient()
    # client.get_host_keys()
    # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    result = []
    config = read_service_file()
    # print(config)
    for x in config:
        print(x)
    #     client.connect(
    #         config["hostname"],
    #         username=config[["username"],
    #         key_filename=config["key_file_path"],
    #     )
        for s in x["services"]:
    #         stdin, stdout, stderr = client.exec_command(
    #             "{} service {} status".format(sudo_var, s)
    #         )
            print(s)
            sudo_var = ""
            if s["sudo"]:
                sudo_var = "sudo "
            print("{}{}".format(sudo_var, s['command']))
            log = [line for line in stdout]
    #         temp_dict = {"name": x, "service": s, "log": [line for line in stdout]}
    #         result.append(temp_dict)
    #     client.close()
    # for x in ["service1", "service2"]:
    #     temp_dict = {"name": x,
    #                     "commands": {}}
    #     for s in ["command1", "command2"]:
    #         temp_dict["commands"] = {"name": s, "result": ""}
    #     result.append(temp_dict)
    print(result)
    return result


core = Blueprint("core", __name__)


@core.route("/")
def index():
    """
    Renders index page.
    :return:
    :rtype:
    """
    return render_template("index.html", services=get_data())

if __name__ == '__main__':
    get_data()

