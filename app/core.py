from flask import Blueprint, render_template
from chuck_pyutils import core as utils
import paramiko


def get_data():
    client = paramiko.SSHClient()
    client.get_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    result = []
    config = utils.read_config(utils.get_file_path(__file__, "services.ini"))
    for x in config.sections():
        client.connect(
            config[x]["HOSTNAME"],
            username=config[x]["USERNAME"],
            key_filename=config[x]["KEY_FILE_PATH"],
        )
        for s in config[x]["SERVICES"].split(","):
            stdin, stdout, stderr = client.exec_command(f"sudo service {s} status")
            temp_dict = {"name": x, "service": s, "log": list(stdout)}
            result.append(temp_dict)
        client.close()
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

