from flask import Blueprint, render_template
from chuck_pyutils import core as utils
import paramiko
import asyncio
from pyppeteer import launch
from witnessme.utils import patch_pyppeteer, start_event_loop
# from witnessme.console.witnessme import screenshot
import argparse
from witnessme.commands import ScreenShot
from time import sleep
async def run_screenshot():
    # parser = argparse.ArgumentParser()
    # args = parser.parse_args()
    browser = await launch(
        headless=False,
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False
    )
    page = await browser.newPage()
    url = "https://example.com"
    await page.goto(url)
    await page.screenshot({'path': 'example1.png'})
    await page.waitForSelector('input[name=username]', timeout=60000)
    await page.type('input[name=username]', '')
    await page.type('input[name=password]', '')
    await page.click('button[type=submit]')
    sleep(2)
    await page.goto(f"{url}")
    await page.waitForSelector('', timeout=60000)
    sleep(5)
    await page.screenshot({'path': 'example.png'})
    # await browser.close()
    # args.target
    # screenshot(args)


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
            stdin, stdout, stderr = client.exec_command(
                "sudo service {} status".format(s)
            )
            temp_dict = {"name": x, "service": s, "log": [line for line in stdout]}
            result.append(temp_dict)
        stdin, stdout, stderr = client.exec_command(
            "sudo df -h"
        )
        temp_dict = {"name": x, "service": "Disk Usage", "log": [line for line in stdout]}
        result.append(temp_dict)
        stdin, stdout, stderr = client.exec_command(
            "sudo du -x -h /var/lib/elasticsearch | sort -h | tail -1"
        )
        temp_dict = {"name": x, "service": "Elastic Usage", "log": [line for line in stdout]}
        result.append(temp_dict)
        stdin, stdout, stderr = client.exec_command(
            "sudo du -x -h /var/lib/docker/containers | sort -h | tail -1"
        )
        temp_dict = {"name": x, "service": "Docker Usage", "log": [line for line in stdout]}
        result.append(temp_dict)
        stdin, stdout, stderr = client.exec_command(
            "sudo docker ps"
        )
        temp_dict = {"name": x, "service": "Docker Processes", "log": [line for line in stdout]}
        result.append(temp_dict)
        client.close()
    return result


core = Blueprint("core", __name__)


@core.route("/")
async def index():
    """
    Renders index page.
    :return:
    :rtype:
    """
    # await run_screenshot()
    return render_template("index.html", services=get_data())
